# AI-Powered Essay to Video Generator

This application automatically generates narrated videos from a single topic using artificial intelligence. It creates an essay, converts it to speech, and generates relevant images that are synchronized with the narration.

## Features

- **Multi-Language Support**: Supports multiple languages including:
  - English
  - Italian
  - Spanish
  - French
  - German

- **AI-Powered Content Generation**:
  - Essay generation using GPT-4 or GPT-3.5
  - Image generation using DALL-E 2 or DALL-E 3
  - Smart image-text synchronization

- **Customizable Output**:
  - Choose essay length (30 seconds, 1 minute, or 4 minutes)
  - Select number of images (1-10)
  - Control AI model selection for both text and images

## Installation

1. Clone this repository:
```bash
git clone [your-repository-url]
cd [repository-name]
```

2. Create and activate a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install required packages:
```bash
pip install -r requirements.txt
```

4. Set up your OpenAI API key:
   - Create a `.env` file in the project root directory
   - Add your OpenAI API key to the `.env` file:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```
   - You can get an API key from [OpenAI's website](https://platform.openai.com/api-keys)

## Usage

1. Run the application:
```bash
python app.py
```

2. Follow the interactive prompts:
   - Enter your essay topic
   - Choose number of images (1-10)
   - Select language
   - Choose AI models:
     - Text model (0: GPT-4, 1: GPT-3.5)
     - Image model (0: DALL-E 2, 1: DALL-E 3)
   - Select essay length:
     - 0: 30 seconds
     - 1: 1 minute
     - 2: 4 minutes

3. The application will:
   - Generate an essay about your topic
   - Convert the essay to speech
   - Create AI-generated images
   - Produce a video with synchronized narration and images

## How It Works

1. **Essay Generation**:
   - Uses OpenAI's GPT models to create a coherent essay about your topic
   - Automatically adjusts length based on your selection

2. **Speech Synthesis**:
   - Converts the essay to natural-sounding speech using gTTS
   - Supports multiple languages with appropriate accents

3. **Image Generation**:
   - Analyzes the essay to identify key visual moments
   - Uses DALL-E to create relevant images
   - Each image corresponds to specific portions of the essay

4. **Video Creation**:
   - Synchronizes images with their corresponding narrative sections
   - Images transition based on their position in the essay
   - Creates a seamless audio-visual experience

## Output

The application generates:
- An MP3 file containing the narrated essay
- PNG files for each generated image
- A final MP4 video combining narration and images

Files are saved in the same directory as the script:
- `speech.mp3`: Audio narration
- `image_0.png`, `image_1.png`, etc.: Generated images
- `output_video.mp4`: Final video

## Requirements

- Python 3.7 or higher
- Internet connection for API access
- OpenAI API key with access to:
  - GPT-4/3.5
  - DALL-E 2/3

## Dependencies

- `openai`: For AI text and image generation
- `pillow`: For image processing
- `moviepy`: For video creation
- `gtts`: For text-to-speech conversion
- `nltk`: For text processing

## Limitations

- Requires an active OpenAI API key
- API usage may incur costs
- Video generation time depends on:
  - Essay length
  - Number of images
  - Selected AI models

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
