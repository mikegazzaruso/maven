# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.2] - 2024-01-10

### Added
- Optional OpenAI API key input in UI
- Security key requirement for video generation
- CORS support for multiple origins

### Changed
- Updated application title to "MAVEN"
- Backend accepts connections from multiple origins
- Improved security with API key handling

### Security
- Added security key validation for video generation
- Secure handling of OpenAI API keys
- Environment-based API key fallback

## [0.1.1] - 2024-01-10

### Added
- New branding: Renamed to MAVEN (Multimedia AI Video Engine)
- Added version number display in UI
- Added BETA status indicator
- Added author attribution

### Changed
- Updated documentation to reflect new branding
- Improved UI header with cleaner layout
- Enhanced project description in README

## [0.1.0] - 2024-01-10

### Added
- Initial release of MAVEN (Multimedia AI Video Engine)
- Core video generation functionality:
  - Essay generation using GPT-4 and GPT-3.5
  - Image generation using DALL-E 2 and DALL-E 3
  - Text-to-speech conversion in multiple languages
  - Video compilation with synchronized audio and images
- Multi-language support:
  - English
  - Italian
  - Spanish
  - French
  - German
- Customizable video settings:
  - Adjustable video length (30s, 1min, 4min)
  - Configurable number of images (1-10)
  - Choice between GPT-4/3.5 and DALL-E 2/3
- Modern UI/UX features:
  - Light/Dark theme switch
  - Responsive Material-UI design
  - Toast notifications for status updates
  - Dynamic progress tracking
- Real-time progress monitoring:
  - Detailed status updates for each generation step
  - Progress bar showing completion percentage
  - Current step indication
- Backend API features:
  - FastAPI REST endpoints
  - Asynchronous video generation
  - Task status tracking
  - Secure file handling
- Environment configuration:
  - Environment variables management
  - Example configuration file
  - OpenAI API integration

### Changed
- Improved image prompt generation for better coherence
- Enhanced text splitting logic for natural sentence boundaries
- Optimized video generation process
- Updated file path handling for better organization

### Fixed
- Video generation task now correctly handles the number of images
- Proper handling of async operations with OpenAI API
- Correct video path references in endpoints
- Task status tracking accuracy
