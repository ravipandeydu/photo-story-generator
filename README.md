# StoryLens - Multi-modal Photo Story Generator

StoryLens is an AI-powered web application that generates creative short stories or poems from uploaded photos and provides audio narration.

## Features

- Upload photos (vacation, birthday, random snapshots)
- AI-generated creative short stories or poems inspired by the image using microsoft/kosmos-2 model
- Audio narration in AI-generated voice using coqui/xtts-v2
- Easy sharing of stories with audio

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/photo-story-generator.git
   cd photo-story-generator
   ```

2. Create and activate a virtual environment (recommended):
   ```
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Run the application:
   ```
   python app.py
   ```

5. Open your web browser and navigate to:
   ```
   http://localhost:5000
   ```

## Models Used

- **Image Understanding and Story Generation**: microsoft/kosmos-2
- **Text-to-Speech**: coqui/xtts-v2

## Project Structure

```
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── static/                # Static files (CSS, JS, uploaded images)
│   ├── css/
│   ├── js/
│   ├── uploads/
│   └── audio/
├── templates/             # HTML templates
│   ├── index.html
│   └── story.html
└── utils/                 # Utility functions
    ├── image_processor.py # Image processing utilities
    ├── story_generator.py # Story generation using Kosmos-2
    └── audio_generator.py # Audio generation using XTTS-v2
```

## License

MIT