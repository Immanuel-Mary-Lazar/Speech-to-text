# Speech-to-Text Converter 🎤

A professional Streamlit web application for converting audio files to text using FunASR (Fun Automatic Speech Recognition). The application supports multiple audio and video formats with automatic conversion capabilities.

## Features

- 🎵 **Multiple Format Support**: Handles WAV, MP3, FLAC, M4A, OGG, WMA, AAC, MP4, AVI, MKV, MOV, and more
- 🔄 **Automatic Conversion**: Uses FFmpeg to convert unsupported formats automatically
- 📝 **Easy Copy**: Built-in copy-to-clipboard functionality for transcribed text
- 🚀 **Fast Processing**: AI-powered speech recognition with FunASR
- 💎 **Professional UI**: Clean and intuitive Streamlit interface
- ⚡ **Auto-Setup**: Automatically installs FFmpeg if not present (on supported platforms)

## Prerequisites

- Python 3.8 or higher
- FFmpeg (automatically installed on Streamlit Cloud and Linux systems)

### FFmpeg Installation

**The application now includes automatic FFmpeg installation!** 

For **Streamlit Cloud** deployments, FFmpeg is automatically installed via the `packages.txt` file.

For **local Linux systems**, the application will attempt to install FFmpeg automatically on first run.

For **manual installation** (macOS, Windows, or if auto-install fails):

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from [FFmpeg official website](https://ffmpeg.org/download.html) and add to PATH.

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Immanuel-Mary-Lazar/Speech-to-text.git
cd Speech-to-text
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Open your web browser and navigate to the displayed URL (typically `http://localhost:8501`)

3. Upload an audio file using the file uploader

4. Click the "Transcribe Audio" button to start the conversion

5. Copy the transcribed text using the copy button or code block

## Supported Audio Formats

### Natively Supported by FunASR
- WAV
- MP3
- FLAC
- M4A
- OGG

### Supported via FFmpeg Conversion
- WMA
- AAC
- MP4 (video)
- AVI (video)
- MKV (video)
- MOV (video)
- WMV (video)
- WebM (video)
- 3GP (video)

## Architecture

The application is built with a professional, modular architecture:

- **AudioConverter**: Handles format conversion using FFmpeg
- **SpeechToTextModel**: Manages the FunASR model and transcription
- **Process Pipeline**: Automated workflow for file processing and conversion
- **Caching**: Model caching for improved performance

## Code Style

This project follows professional Python coding standards:
- Type hints for better code clarity
- Comprehensive docstrings
- Proper error handling
- Modular class-based design
- PEP 8 compliance

## Troubleshooting

### Model Loading Issues
- First run may take time as models are downloaded
- Ensure stable internet connection for initial setup
- Models are cached for subsequent runs

### FFmpeg Errors
- Verify FFmpeg is installed: `ffmpeg -version`
- Check file is not corrupted
- Ensure sufficient disk space

### Memory Issues
- Large audio files may require more RAM
- Consider splitting long recordings

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Acknowledgments

- [FunASR](https://github.com/alibaba-damo-academy/FunASR) - Speech recognition framework
- [Streamlit](https://streamlit.io/) - Web application framework
- [FFmpeg](https://ffmpeg.org/) - Audio/video processing