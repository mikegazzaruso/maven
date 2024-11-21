# MAVEN (Multimedia AI Video Engine)

An advanced AI-powered application that generates engaging videos from text using cutting-edge AI technologies. MAVEN creates coherent narratives, generates matching images, and combines them with synthesized speech to produce professional-quality videos.

## Features

- **Multi-Language Support**: Generate videos in multiple languages including English, Italian, Spanish, French, and German
- **AI-Powered Content Generation**:
  - Essay generation using GPT-4 or GPT-3.5
  - Image generation using DALL-E 2 or DALL-E 3
  - Text-to-speech conversion in multiple languages
- **Real-Time Progress Tracking**:
  - Detailed status updates for each generation step
  - Progress bar showing completion percentage
  - Current step indication
- **Customizable Video Settings**:
  - Adjustable video length (30 seconds to 4 minutes)
  - Configurable number of images (1-10)
  - Choice of language models and image generation models
- **Modern UI/UX**:
  - Light/Dark theme support
  - Responsive design
  - Toast notifications for status updates
  - Dynamic progress tracking

## Technology Stack

### Backend
- FastAPI for the REST API
- OpenAI API (GPT-4, GPT-3.5, DALL-E 2/3) for content generation
- MoviePy for video creation
- gTTS for text-to-speech conversion
- Python-dotenv for environment management
- Async/await pattern for efficient processing

### Frontend
- React.js for the user interface
- Material-UI for component design
- React-Toastify for notifications
- Axios for API communication

## Installation

1. Clone the repository
2. Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Install frontend dependencies:
```bash
cd frontend
npm install
```

4. Set up your environment variables:
   - Copy `.env.example` to create a new `.env` file:
   ```bash
   cp .env.example .env
   ```
   - Replace `your-openai-api-key` in the `.env` file with your actual OpenAI API key
   - You can get an API key from [OpenAI's website](https://platform.openai.com/api-keys)

## Usage

1. Start the backend server:
```bash
cd backend
python api.py
```

2. Start the frontend development server:
```bash
cd frontend
npm start
```

3. Access the application at `http://localhost:3000`

## Video Generation Process

1. **Essay Generation**:
   - AI generates a coherent essay based on the input topic
   - Length is adjusted based on the selected video duration

2. **Image Generation**:
   - Essay is divided into segments
   - Each segment is converted into a detailed image prompt
   - DALL-E generates images based on these prompts

3. **Audio Generation**:
   - Essay is converted to speech using gTTS
   - Multiple language support with natural pronunciation

4. **Video Compilation**:
   - Images are sequenced with proper timing
   - Audio is synchronized with the visuals
   - Final video is rendered in MP4 format

## API Endpoints

- `POST /generate`: Start video generation
- `GET /status/{task_id}`: Check generation status
- `GET /video/{task_id}`: Download generated video

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key
- `OUTPUT_DIR`: Directory for generated files (default: "output")

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## TODO

### Planned Features
- **YouTube Integration**:
  - Automatic video upload to YouTube after generation
  - OAuth2 authentication for YouTube API
  - Customizable video metadata (title, description, tags)
  - Privacy settings configuration (public, unlisted, private)
  - Playlist management
  - Upload status tracking and notifications
