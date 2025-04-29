
# TTS Tools Collection (Text-to-Speech)

This is a Streamlit-based web application that provides Text-to-Speech conversion tools using OpenAI's TTS API. The application offers two main tools: Speech TTS and Conversation TTS.

## 🗂 Project Structure

```
├── pages/
│   ├── Conversation_TTS.py    # Two-speaker conversation TTS tool
│   └── Speech_TTS.py         # Single-speaker TTS tool
├── streamlit_app.py          # Main application entry point
├── main.py                   # OpenAI API configuration
├── .replit                   # Replit configuration
├── pyproject.toml           # Python project dependencies
└── usage_log.csv            # Usage tracking log file
```

## 📋 Component Descriptions

### Main Components

1. **streamlit_app.py**
   - Main entry point of the application
   - Provides navigation interface
   - Sets up the Streamlit configuration

2. **pages/Speech_TTS.py**
   - Single-speaker TTS conversion
   - Features:
     - Text/file input support
     - Voice selection (Nova, Shimmer, Echo)
     - Speed adjustment
     - Blank seconds addition
     - Single/Multiple MP3 generation
     - Usage logging
     - Cleanup functionality

3. **pages/Conversation_TTS.py**
   - Two-speaker conversation TTS
   - Features:
     - Alternating speaker voices
     - Speed adjustment
     - Blank seconds addition
     - Combined audio output
     - Automatic cleanup

4. **main.py**
   - OpenAI API configuration
   - Environment variable management

## 🔧 Features

### Common Features
- Multiple voice options (Nova, Shimmer, Echo)
- Adjustable playback speed (0.5x - 2.0x)
- Configurable silence duration at the end
- Auto-cleanup of generated files
- Download options for audio files

### Speech TTS Specific
- Single/Multiple MP3 generation
- Text file upload support
- Usage logging and cost estimation
- Batch processing with individual file naming

### Conversation TTS Specific
- Two-speaker dialogue support
- Automatic voice alternation
- Combined audio output
- Simple A/B conversation format

## 📊 Usage Tracking
The application tracks usage in `usage_log.csv`:
- Timestamp
- Filename
- Model used
- Character count
- Estimated cost

## 🔐 Requirements
- OpenAI API key (set in Replit Secrets)
- FFmpeg (included in Replit environment)
- Python packages:
  - streamlit
  - openai
  - pydub
  - pandas
  - python-dotenv

## 🚀 Getting Started
1. Fork this Repl
2. Add your OpenAI API key to Replit Secrets
3. Click the Run button
4. Select your desired TTS tool from the sidebar
5. Input text and configure settings
6. Generate and download your audio files

## 💡 Best Practices
- Clean up files regularly using the cleanup button
- Keep track of usage through the logging system
- Use appropriate file naming conventions
- Download files promptly after generation

## 📝 Note
This application is designed to run on Replit and includes automatic deployment configurations. All audio processing is done in-memory where possible to maintain efficiency and clean operation.
