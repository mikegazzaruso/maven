import os
from openai import AsyncOpenAI
from PIL import Image
from io import BytesIO
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip, CompositeVideoClip
from gtts import gTTS
import nltk
from nltk.tokenize import sent_tokenize
import os
from dotenv import load_dotenv
import logging
import shutil
import aiohttp
import asyncio

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

class VideoGenerator:
    def __init__(self, task_id: str, tasks: dict):
        self.task_id = task_id
        self.tasks = tasks
        self.client = AsyncOpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.update_status("queued", "Initializing", 0)

        # Download NLTK data if needed
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')

    def update_status(self, status: str, step: str, progress: float, error: str = None):
        self.tasks[self.task_id].update({
            "status": status,
            "current_step": step,
            "progress": progress,
            "error": error
        })
        logger.info(f"Status updated - Status: {status}, Step: {step}, Progress: {progress}%")

    def detect_language(self, lang_input):
        # Language mapping dictionary
        language_map = {
            'it': {'code': 'it', 'name': 'Italian', 'openai': 'Italian'},
            'italiano': {'code': 'it', 'name': 'Italian', 'openai': 'Italian'},
            'en': {'code': 'en', 'name': 'English', 'openai': 'English'},
            'english': {'code': 'en', 'name': 'English', 'openai': 'English'},
            'es': {'code': 'es', 'name': 'Spanish', 'openai': 'Spanish'},
            'español': {'code': 'es', 'name': 'Spanish', 'openai': 'Spanish'},
            'espanol': {'code': 'es', 'name': 'Spanish', 'openai': 'Spanish'},
            'fr': {'code': 'fr', 'name': 'French', 'openai': 'French'},
            'français': {'code': 'fr', 'name': 'French', 'openai': 'French'},
            'francais': {'code': 'fr', 'name': 'French', 'openai': 'French'},
            'de': {'code': 'de', 'name': 'German', 'openai': 'German'},
            'deutsch': {'code': 'de', 'name': 'German', 'openai': 'German'}
        }
        
        return language_map.get(lang_input.lower().strip())

    def get_system_message(self, length_option, language):
        # Define target word counts
        word_counts = {
            0: 75,    # ~30 seconds
            1: 150,   # ~1 minute
            2: 600    # ~4 minutes
        }
        
        word_count = word_counts[length_option]
        duration = word_counts[length_option]/150
        
        return f"""Write a coherent essay in {language} about the provided topic. 
        The essay should be approximately {word_count} words long to achieve a spoken duration of {duration:.1f} minutes.
        Make the essay vivid and descriptive, with clear imagery that can be visualized."""

    async def generate_essay(self, topic, length_option, model_option, language):
        """Generate an essay about the topic using OpenAI's API."""
        try:
            # Detect and validate language
            lang_info = self.detect_language(language)
            
            # Define models
            models = {
                0: "gpt-4",
                1: "gpt-3.5-turbo"
            }
            
            model = models[model_option]
            
            # Get system message based on length option
            system_message = self.get_system_message(length_option, lang_info['openai'])
            
            logger.info(f"Using {model} to generate essay in {lang_info['name']}...")
            
            # Create the chat completion
            response = await self.client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": f"Write about: {topic}"}
                ]
            )
            
            essay = response.choices[0].message.content.strip()
            logger.info("Essay generated successfully")
            return essay
            
        except Exception as e:
            logger.error(f"Error generating essay: {str(e)}")
            raise

    async def generate_image_prompts(self, essay, num_images, language):
        """Generate image prompts from the essay text."""
        try:
            logger.info(f"Generating {num_images} image prompts...")
            
            language_info = self.detect_language(language)
            
            # Split essay into sentences
            sentences = sent_tokenize(essay)
            
            # Create exactly num_images portions by splitting the essay text
            text_portions = []
            total_length = len(essay)
            chunk_size = total_length // num_images
            
            current_pos = 0
            for i in range(num_images):
                if i == num_images - 1:
                    # Last portion gets the remainder
                    portion = essay[current_pos:]
                else:
                    # Find the next sentence boundary after chunk_size characters
                    end_pos = min(current_pos + chunk_size, total_length)
                    while end_pos < total_length and essay[end_pos] not in '.!?':
                        end_pos += 1
                    end_pos = min(end_pos + 1, total_length)
                    
                    portion = essay[current_pos:end_pos]
                    current_pos = end_pos
                
                if portion.strip():
                    text_portions.append(portion.strip())
            
            # Ensure we have exactly num_images portions
            while len(text_portions) < num_images:
                # If we have too few portions, duplicate the last one
                text_portions.append(text_portions[-1])
            
            # Generate image prompts for each portion
            prompts = []
            positions = []
            
            for i, portion in enumerate(text_portions[:num_images]):  # Limit to num_images
                logger.info(f"Generating prompt {i+1}/{num_images}")
                prompt_response = await self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": f"You are a helpful assistant that creates detailed image prompts in {language_info['openai']} based on text descriptions. Create a vivid and specific image prompt that captures the main visual elements of the text."},
                        {"role": "user", "content": portion}
                    ]
                )
                
                prompt = prompt_response.choices[0].message.content.strip()
                prompts.append(prompt)
                positions.append(i / (num_images - 1) if num_images > 1 else 0.5)
            
            logger.info(f"Generated {len(prompts)} image prompts")
            result = list(zip(prompts[:num_images], positions[:num_images]))  # Ensure exactly num_images results
            logger.info(f"Returning {len(result)} prompts with positions")
            return result
            
        except Exception as e:
            logger.error(f"Error generating image prompts: {str(e)}")
            raise

    async def generate_speech(self, text, language, output_dir):
        """Convert text to speech using gTTS."""
        try:
            logger.info("Converting text to speech...")
            
            language_info = self.detect_language(language)
            if not language_info:
                raise ValueError(f"Unsupported language: {language}")
            
            speech_file = os.path.join(output_dir, "speech.mp3")
            
            # Create speech in a separate thread to not block the event loop
            def generate_speech():
                tts = gTTS(text=text, lang=language_info['code'])
                tts.save(speech_file)
            
            # Run the speech generation in a thread pool
            await asyncio.get_event_loop().run_in_executor(None, generate_speech)
            
            logger.info(f"Speech saved to {speech_file}")
            return speech_file
            
        except Exception as e:
            logger.error(f"Error generating speech: {str(e)}")
            raise

    async def generate_image(self, description, index, image_model_option, output_dir):
        logger.info(f"Generating image for prompt: {description}")
        
        models = {
            0: "dall-e-2",
            1: "dall-e-3"
        }
        
        model = models[image_model_option]
        logger.info(f"Using {model} to generate image...")
        
        response = await self.client.images.generate(
            model=model,
            prompt=description,
            n=1,
            size="1024x1024"
        )
        
        image_url = response.data[0].url
        image_path = os.path.join(output_dir, f'image_{index}.png')
        
        async with aiohttp.ClientSession() as session:
            async with session.get(image_url) as resp:
                if resp.status == 200:
                    with open(image_path, 'wb') as f:
                        f.write(await resp.read())
        
        logger.info(f"Saved image to {image_path}")
        return image_path

    def create_video(self, image_paths_with_positions, audio_path, output_path):
        logger.info("Creating video...")
        
        # Load audio and get duration
        audio = AudioFileClip(audio_path)
        total_duration = audio.duration
        
        # Sort images by their position
        image_paths_with_positions.sort(key=lambda x: x[1])
        
        # Create video clips
        clips = []
        for i, (img_path, position) in enumerate(image_paths_with_positions):
            start_time = position * total_duration
            
            # Calculate end time (either next image position or end of audio)
            if i < len(image_paths_with_positions) - 1:
                end_time = image_paths_with_positions[i + 1][1] * total_duration
            else:
                end_time = total_duration
            
            duration = end_time - start_time
            
            # Create image clip with proper duration and timing
            clip = (ImageClip(img_path)
                   .set_duration(duration)
                   .set_start(start_time)
                   .set_position('center'))
            clips.append(clip)
        
        # Create video with all clips
        video = CompositeVideoClip(clips, size=(1024, 1024))
        
        # Set the duration to match the audio
        video = video.set_duration(total_duration)
        
        # Add audio to video
        final_video = video.set_audio(audio)
        
        # Write video file with audio
        final_video.write_videofile(
            output_path,
            fps=24,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )
        
        logger.info(f"Video saved to {output_path}")
        return output_path

    async def generate(self, topic, num_images, language, text_model, image_model, video_length, output_dir):
        """Main generation method that coordinates the entire process."""
        try:
            self.update_status("processing", "Generating essay", 0)
            
            # Generate essay
            essay = await self.generate_essay(topic, video_length, text_model, language)
            self.update_status("processing", "Generating image prompts", 20)
            
            # Generate image prompts
            prompts_with_positions = await self.generate_image_prompts(essay, num_images, language)
            
            # Generate speech
            self.update_status("processing", "Converting text to speech", 40)
            speech_file = await self.generate_speech(essay, language, output_dir)
            
            # Generate images
            self.update_status("processing", "Generating images", 60)
            image_paths_with_positions = []
            total_images = len(prompts_with_positions)
            
            for index, (prompt, position) in enumerate(prompts_with_positions):
                self.update_status("processing", f"Generating image {index + 1} of {total_images}", 
                                 60 + (20 * (index + 1) / total_images))
                image_path = await self.generate_image(prompt, index, image_model, output_dir)
                image_paths_with_positions.append((image_path, position))
            
            # Create video
            self.update_status("processing", "Creating video", 80)
            output_video = os.path.join(output_dir, "output.mp4")
            self.create_video(image_paths_with_positions, speech_file, output_video)
            
            # Move video to final location
            self.update_status("processing", "Finalizing video", 90)
            final_output = os.path.join(output_dir, f"{self.task_id}.mp4")
            shutil.move(output_video, final_output)
            
            self.update_status("completed", "Video generation completed", 100)
            return final_output
            
        except Exception as e:
            self.update_status("failed", "Error occurred", 0, str(e))
            logger.error(f"Error generating video: {str(e)}")
            raise
