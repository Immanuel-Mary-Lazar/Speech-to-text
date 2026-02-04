"""
Speech-to-Text Streamlit Application

This application provides a web interface for converting audio files to text
using FunASR-ONNX. It supports various audio formats and automatically converts
unsupported formats using FFmpeg. The ONNX version provides a lightweight
alternative to PyTorch-based models with significantly reduced dependencies.
"""

import os
import shutil
import tempfile
from pathlib import Path
from typing import Optional, Tuple

import ffmpeg
import streamlit as st
from funasr import AutoModel

# FFmpeg will be checked lazily when AudioConverter is used
# This prevents blocking the app startup and health checks


# Supported audio formats by FunASR
FUNASR_SUPPORTED_FORMATS = {".wav", ".mp3", ".flac", ".m4a", ".ogg"}

# All common audio/video formats that can be converted
ACCEPTED_FORMATS = {
    ".wav", ".mp3", ".flac", ".m4a", ".ogg", ".wma", ".aac",
    ".mp4", ".avi", ".mkv", ".mov", ".wmv", ".webm", ".3gp"
}


@st.cache_resource
def load_funasr_model() -> AutoModel:
    """
    Load the lightweight FunASR ONNX model with caching to avoid reloading.
    
    Note: This model (iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-onnx)
    is primarily designed for Chinese language. For other languages, different model 
    configurations may be needed.
    
    The ONNX version significantly reduces dependency size compared to PyTorch models.

    Returns:
        AutoModel: The loaded FunASR ONNX model
    """
    try:
        with st.spinner("Loading speech recognition model... This may take a moment."):
            model = AutoModel(
                model="iic/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-onnx",
                vad_model="iic/speech_fsmn_vad_zh-cn-16k-common-onnx",
                punc_model="iic/punc_ct-transformer_zh-cn-common-vocab272727-onnx",
            )
        return model
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        st.stop()


class AudioConverter:
    """Handles audio format conversion using FFmpeg."""

    @staticmethod
    def is_ffmpeg_available() -> bool:
        """
        Check if FFmpeg is available in the system.

        Returns:
            bool: True if FFmpeg is installed and available, False otherwise
        """
        return shutil.which("ffmpeg") is not None

    @staticmethod
    def convert_to_wav(input_path: str, output_path: str) -> bool:
        """
        Convert an audio file to WAV format using FFmpeg.

        Args:
            input_path: Path to the input audio file
            output_path: Path where the converted WAV file will be saved

        Returns:
            bool: True if conversion was successful, False otherwise
        """
        # Check if FFmpeg is available
        if not AudioConverter.is_ffmpeg_available():
            st.error(
                "❌ **FFmpeg is not installed or not found in PATH.**\n\n"
                "FFmpeg is required to convert video files and unsupported audio formats.\n\n"
                "**Installation Instructions:**\n"
                "- **Ubuntu/Debian:** `sudo apt update && sudo apt install ffmpeg`\n"
                "- **macOS:** `brew install ffmpeg`\n"
                "- **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to PATH\n\n"
                "After installing FFmpeg, restart the application."
            )
            return False

        try:
            (
                ffmpeg
                .input(input_path)
                .output(output_path, acodec='pcm_s16le', ac=1, ar='16000')
                .overwrite_output()
                .run(capture_stdout=True, capture_stderr=True, quiet=True)
            )
            return True
        except ffmpeg.Error as e:
            st.error(f"FFmpeg conversion error: {e.stderr.decode()}")
            return False
        except Exception as e:
            st.error(f"Unexpected error during conversion: {str(e)}")
            return False


class SpeechToTextModel:
    """Manages the FunASR speech-to-text model."""

    def __init__(self):
        """Initialize the FunASR model."""
        self.model: Optional[AutoModel] = None

    def get_model(self) -> AutoModel:
        """
        Get the loaded model, initializing it if necessary.

        Returns:
            AutoModel: The FunASR model instance
        """
        if self.model is None:
            self.model = load_funasr_model()
        return self.model

    def transcribe(self, audio_path: str) -> Optional[str]:
        """
        Transcribe an audio file to text.

        Args:
            audio_path: Path to the audio file

        Returns:
            Optional[str]: The transcribed text, or None if transcription failed
        """
        try:
            model = self.get_model()
            result = model.generate(input=audio_path)
            
            if result and len(result) > 0:
                # Extract text from the result
                if isinstance(result[0], dict) and 'text' in result[0]:
                    return result[0]['text']
                elif isinstance(result[0], str):
                    return result[0]
                else:
                    return str(result[0])
            return None
        except Exception as e:
            st.error(f"Error during transcription: {str(e)}")
            return None


def process_audio_file(
    uploaded_file,
    speech_model: SpeechToTextModel,
    converter: AudioConverter
) -> Optional[str]:
    """
    Process an uploaded audio file and return its transcription.

    Args:
        uploaded_file: The uploaded file object from Streamlit
        speech_model: The SpeechToTextModel instance
        converter: The AudioConverter instance

    Returns:
        Optional[str]: The transcribed text, or None if processing failed
    """
    # Get file extension
    file_extension = Path(uploaded_file.name).suffix.lower()
    
    # Create temporary directory for processing
    with tempfile.TemporaryDirectory() as temp_dir:
        # Save uploaded file
        input_path = os.path.join(temp_dir, uploaded_file.name)
        with open(input_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Check if format is supported by FunASR
        if file_extension in FUNASR_SUPPORTED_FORMATS:
            transcription_path = input_path
        else:
            # Convert to WAV format
            st.info(f"Converting {file_extension} to WAV format...")
            output_path = os.path.join(temp_dir, "converted.wav")
            
            if not converter.convert_to_wav(input_path, output_path):
                return None
            
            transcription_path = output_path
            st.success("Conversion successful!")
        
        # Perform transcription
        with st.spinner("Transcribing audio..."):
            transcription = speech_model.transcribe(transcription_path)
        
        return transcription


def main():
    """Main function to run the Streamlit application."""
    # Page configuration
    st.set_page_config(
        page_title="Speech to Text",
        page_icon="🎤",
        layout="centered"
    )
    
    # Title and description
    st.title("🎤 Speech to Text Converter")
    st.markdown(
        """
        Upload an audio file and convert it to text using AI-powered speech recognition.
        Supports various audio and video formats.
        """
    )
    
    # Initialize models and converter
    speech_model = SpeechToTextModel()
    converter = AudioConverter()
    
    # File uploader
    st.subheader("Upload Audio File")
    uploaded_file = st.file_uploader(
        "Choose an audio or video file",
        type=[fmt.lstrip('.') for fmt in ACCEPTED_FORMATS],
        help="Supported formats: " + ", ".join(sorted(ACCEPTED_FORMATS))
    )
    
    # Process uploaded file
    if uploaded_file is not None:
        # Display file info
        st.write(f"**Filename:** {uploaded_file.name}")
        st.write(f"**File size:** {uploaded_file.size / 1024:.2f} KB")
        
        # Add a process button
        if st.button("🎯 Transcribe Audio", type="primary"):
            transcription = process_audio_file(uploaded_file, speech_model, converter)
            
            if transcription:
                # Display results
                st.success("✅ Transcription completed!")
                
                st.subheader("Transcription Result")
                st.text_area(
                    "Transcribed Text",
                    value=transcription,
                    height=200,
                    key="transcription_output"
                )
                
                # Copy button functionality
                st.markdown("### 📋 Copy to Clipboard")
                st.code(transcription, language=None)
                st.info("💡 Click on the code block above to copy the text to your clipboard.")
                
            else:
                st.error("❌ Transcription failed. Please try a different file.")
    
    # Sidebar with information
    with st.sidebar:
        st.header("ℹ️ Information")
        st.markdown(
            """
            ### Supported Formats
            **Natively Supported:**
            - WAV, MP3, FLAC, M4A, OGG
            
            **Converted via FFmpeg:**
            - WMA, AAC, MP4, AVI, MKV, MOV, WMV, WebM, 3GP
            
            ### Features
            - 🎵 Multiple format support
            - 🔄 Automatic format conversion
            - 📝 Copy transcription to clipboard
            - 🚀 Fast AI-powered recognition
            
            ### Language Support
            - 🇨🇳 Primarily supports Chinese language
            - For other languages, model configuration may need adjustment
            
            ### Tips
            - Use high-quality audio for best results
            - Clear speech improves accuracy
            - Avoid background noise when possible
            """
        )


if __name__ == "__main__":
    main()

