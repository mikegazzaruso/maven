from openai import OpenAI
import requests
from PIL import Image
from io import BytesIO
from moviepy import ImageClip, concatenate_videoclips, AudioFileClip, CompositeVideoClip
from gtts import gTTS
import nltk
from nltk.tokenize import sent_tokenize
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client with API key from environment variable
client = OpenAI(
    api_key=os.getenv('OPENAI_API_KEY')
)

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def detect_language(lang_input):
    # Normalize input: convert to lowercase and strip spaces
    lang = lang_input.lower().strip()
    
    # Language mapping dictionary
    language_map = {
        # Italian variations
        'it': {'code': 'it', 'name': 'Italian', 'openai': 'Italian'},
        'italiano': {'code': 'it', 'name': 'Italian', 'openai': 'Italian'},
        # English variations
        'en': {'code': 'en', 'name': 'English', 'openai': 'English'},
        'english': {'code': 'en', 'name': 'English', 'openai': 'English'},
        # Spanish variations
        'es': {'code': 'es', 'name': 'Spanish', 'openai': 'Spanish'},
        'español': {'code': 'es', 'name': 'Spanish', 'openai': 'Spanish'},
        'espanol': {'code': 'es', 'name': 'Spanish', 'openai': 'Spanish'},
        # French variations
        'fr': {'code': 'fr', 'name': 'French', 'openai': 'French'},
        'français': {'code': 'fr', 'name': 'French', 'openai': 'French'},
        'francais': {'code': 'fr', 'name': 'French', 'openai': 'French'},
        # German variations
        'de': {'code': 'de', 'name': 'German', 'openai': 'German'},
        'deutsch': {'code': 'de', 'name': 'German', 'openai': 'German'}
    }
    
    if lang in language_map:
        return language_map[lang]
    else:
        return None

def generate_essay(topic, length_option, model_option, language):
    print("Generating essay from topic...")
    # Define target word counts based on length option
    word_counts = {
        0: 75,    # ~30 seconds when spoken
        1: 150,   # ~1 minute when spoken
        2: 600    # ~4 minutes when spoken
    }
    
    # Define models
    models = {
        0: "gpt-4",
        1: "gpt-3.5-turbo"
    }
    
    word_count = word_counts[length_option]
    model = models[model_option]
    
    combined_prompt = f"""Write a coherent essay in {language['openai']} about the following topic: {topic}. 
    The essay should be approximately {word_count} words long to achieve a spoken duration of {word_counts[length_option]/150:.1f} minutes.
    Make the essay vivid and descriptive, with clear imagery that can be visualized."""
    
    print(f"Using {model} to generate essay in {language['name']}...")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": combined_prompt}
        ]
    )
    essay = response.choices[0].message.content
    print("Essay generated successfully")
    return essay

def generate_image_prompts(essay, num_images, language):
    print("Generating image prompts from essay...")
    
    prompt = f"""I have an essay in {language['name']} and I need to create {num_images} vivid image prompts from it. 
    Analyze the essay and create {num_images} detailed image prompts that capture key visual elements and scenes.
    For each prompt:
    1. First identify a specific portion of text from the essay
    2. Then create a detailed image prompt based on that portion
    
    Format each response as:
    TEXT: <the exact text portion from the essay>
    PROMPT: <the detailed image prompt>
    
    Make sure the text portions are in sequential order as they appear in the essay.
    
    Essay: {essay}"""
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    # Parse the response to get text portions and prompts
    content = response.choices[0].message.content.strip()
    sections = content.split('\n\n')
    
    text_portions = []
    prompts = []
    
    for section in sections:
        if not section.strip():
            continue
        lines = section.strip().split('\n')
        if len(lines) >= 2:
            text_line = lines[0].strip()
            prompt_line = lines[1].strip()
            
            if text_line.startswith('TEXT:'):
                text = text_line[5:].strip()
                if prompt_line.startswith('PROMPT:'):
                    prompt = prompt_line[7:].strip()
                    text_portions.append(text)
                    prompts.append(prompt)
    
    # Calculate relative positions of text portions in the essay
    positions = []
    for text in text_portions:
        pos = essay.find(text)
        if pos != -1:
            positions.append(pos / len(essay))
        else:
            # If exact text not found, estimate position based on order
            positions.append(len(positions) / len(text_portions))
    
    print(f"Generated {len(prompts)} image prompts")
    return list(zip(prompts, positions))

def generate_speech(text, language):
    print(f"Converting essay to speech in {language['name']}...")
    
    # Use gTTS for text-to-speech
    tts = gTTS(text=text, lang=language['code'])
    speech_file = "speech.mp3"
    tts.save(speech_file)
    
    print(f"Speech saved to {speech_file}")
    return speech_file

def generate_image(description, index, image_model_option):
    print(f"Generating image for prompt: {description}")
    
    # Define image models
    models = {
        0: "dall-e-2",
        1: "dall-e-3"
    }
    
    model = models[image_model_option]
    print(f"Using {model} to generate image...")
    
    response = client.images.generate(
        model=model,
        prompt=description,
        n=1,
        size="1024x1024"
    )
    image_url = response.data[0].url
    image_response = requests.get(image_url)
    image = Image.open(BytesIO(image_response.content))
    image_path = f'image_{index}.png'
    image.save(image_path)
    print(f"Saved image to {image_path}")
    return image_path

def create_video(image_paths_with_positions, audio_path, output_path):
    print("Creating video...")
    
    # Load the audio to get its duration
    audio = AudioFileClip(audio_path)
    total_duration = audio.duration
    
    # Sort image paths by their positions
    image_paths_with_positions.sort(key=lambda x: x[1])  # Sort by position
    
    # Create clips with positions based on the essay text
    clips = []
    for i, (img_path, position) in enumerate(image_paths_with_positions):
        # Calculate start and end times based on position in essay
        start_time = position * total_duration
        
        # For end time, use the start of the next image or the end of audio
        if i < len(image_paths_with_positions) - 1:
            end_time = image_paths_with_positions[i + 1][1] * total_duration
        else:
            end_time = total_duration
            
        duration = end_time - start_time
        
        clip = (ImageClip(img_path)
                .with_duration(duration)
                .with_start(start_time))
        clips.append(clip)
    
    # Combine all clips
    video = CompositeVideoClip(clips)
    
    # Add audio
    final_video = video.with_audio(audio)
    
    # Write the final video
    final_video.write_videofile(output_path, fps=24)
    print(f"Video saved to {output_path}")

def main():
    # Get topic
    topic = input("Enter the topic for your essay: ")
    if not topic:
        print("No topic provided. Exiting...")
        return

    # Get number of images
    while True:
        try:
            num_images = int(input("How many images would you like to generate? (1-10): "))
            if 1 <= num_images <= 10:
                break
            print("Please enter a number between 1 and 10")
        except ValueError:
            print("Please enter a valid number")

    # Get language preference
    while True:
        lang_input = input("Select language (e.g., 'it' for Italian, 'en' for English, 'es' for Spanish): ")
        language = detect_language(lang_input)
        if language:
            print(f"Selected language: {language['name']}")
            break
        print("Unsupported language. Please try again with a supported language code.")

    # Get model preferences
    while True:
        try:
            model_option = int(input("Select text model (0 for GPT-4, 1 for GPT-3.5): "))
            if model_option in [0, 1]:
                break
            print("Please enter 0 or 1")
        except ValueError:
            print("Please enter a valid number (0 or 1)")

    while True:
        try:
            image_model_option = int(input("Select image model (0 for DALL-E 2, 1 for DALL-E 3): "))
            if image_model_option in [0, 1]:
                break
            print("Please enter 0 or 1")
        except ValueError:
            print("Please enter a valid number (0 or 1)")

    # Get essay length preference
    while True:
        try:
            length_option = int(input("Select essay length (0 for 30 secs, 1 for 1 min, 2 for 4 mins): "))
            if length_option in [0, 1, 2]:
                break
            print("Please enter 0, 1, or 2")
        except ValueError:
            print("Please enter a valid number (0, 1, or 2)")

    # Generate essay from topic
    essay = generate_essay(topic, length_option, model_option, language)
    print("\nGenerated Essay:")
    print(essay)
    
    # Generate image prompts from the essay
    prompts_with_positions = generate_image_prompts(essay, num_images, language)
    print("\nGenerated Image Prompts:")
    for i, (prompt, position) in enumerate(prompts_with_positions, 1):
        print(f"{i}. {prompt} (Position: {position:.2%} through the essay)")
    
    # Convert essay to speech
    speech_file = generate_speech(essay, language)

    # Generate images for each prompt
    image_paths_with_positions = []
    for index, (prompt, position) in enumerate(prompts_with_positions):
        image_path = generate_image(prompt, index, image_model_option)
        image_paths_with_positions.append((image_path, position))

    # Create a video from the generated images and audio
    output_video = "output_video.mp4"
    create_video(image_paths_with_positions, speech_file, output_video)
    print(f"Video generated successfully: {output_video}")

if __name__ == "__main__":
    main()
