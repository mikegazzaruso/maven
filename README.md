# 🎬 MAVEN (Multimedia AI Video Engine) v0.2.0

Welcome to MAVEN! 🚀 Your go-to AI-powered video creation suite that transforms text into engaging video content. Using cutting-edge AI technologies, MAVEN crafts professional videos by generating coherent narratives, matching visuals, and natural speech synthesis.

## ✨ Features

### 🔍 Web Search Integration (New in v0.2.0)
- 🌐 Real-time web search for up-to-date information
- 🤖 Multi-agent system powered by OpenAI Swarm
- 📊 Intelligent filtering and organization of search results
- 📝 Enhanced content generation with factual, current information
- 🔄 Toggle to enable/disable web search functionality

### 🌍 Multi-Language Support
Generate videos in multiple languages:
- 🇬🇧 English
- 🇮🇹 Italian
- 🇪🇸 Spanish
- 🇫🇷 French
- 🇩🇪 German

### 🤖 AI-Powered Content Generation
- 📝 Essay generation using GPT-4 or GPT-3.5
- 🎨 Image generation using DALL-E 2 or DALL-E 3
- 🗣️ Text-to-speech conversion in multiple languages
- 🎥 Video compilation with synchronized audio and images

### ⚙️ Customizable Video Settings
- ⏱️ Adjustable video length (30s, 1min, 4min)
- 🖼️ Configurable number of images (1-10)
- 🔄 Choice of language models and image generation models

### 💫 Modern UI/UX Features
- 🌓 Light/Dark theme support
- 📱 Responsive Material-UI design
- 🔔 Toast notifications for status updates
- 📊 Dynamic progress tracking

### 📈 Real-Time Progress Monitoring
- 🔄 Detailed status updates for each generation step
- ⏳ Progress bar showing completion percentage
- 🎯 Current step indication

## 🚀 Installation

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

## 🎮 Usage

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

3. Access MAVEN:
   - Local development: `http://localhost:3030`
   - Network access: `http://your-ip:3030`

## 🔐 Security Features

1. **Video Generation Protection**
   - Required security key for video generation

2. **OpenAI API Key Management**
   - Optional API key input in UI
   - Fallback to environment variable if not provided
   - Secure handling of API keys

## 🎥 Video Generation Process

1. **Web Research** 🌐 (New in v0.2.0)
   - Multi-agent system searches the web for up-to-date information
   - Intelligent filtering and organization of search results
   - Enhanced content generation with factual, current information

2. **Essay Generation** 📝
   - AI generates a coherent essay based on your topic and web research
   - Length is adjusted based on your selected video duration

3. **Image Generation** 🎨
   - Essay is divided into meaningful segments
   - Each segment is converted into a detailed image prompt
   - DALL-E generates stunning visuals based on these prompts

4. **Audio Generation** 🔊
   - Essay is converted to natural-sounding speech
   - Multiple language support with native pronunciation

5. **Video Compilation** 🎬
   - Images are sequenced with perfect timing
   - Audio is synchronized with the visuals
   - Final video is rendered in high-quality MP4 format

## 🛠️ API Endpoints

- `POST /generate`: Start video generation
- `GET /status/{task_id}`: Check generation status
- `GET /video/{task_id}`: Download generated video

## ⚙️ Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key
- `OUTPUT_DIR`: Directory for generated files (default: "output")

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📋 TODO

### Planned Features
- **YouTube Integration** 🎥:
  - Automatic video upload to YouTube after generation
  - OAuth2 authentication for YouTube API
  - Customizable video metadata (title, description, tags)
  - Privacy settings configuration (public, unlisted, private)
  - Playlist management
  - Upload status tracking and notifications

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
