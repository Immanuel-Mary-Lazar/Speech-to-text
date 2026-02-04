"""
FFmpeg Setup Script

This script checks if FFmpeg is installed and attempts to install it if missing.
It supports multiple platforms including Streamlit Cloud, Ubuntu/Debian, and others.
"""

import os
import platform
import shutil
import subprocess
import sys


def is_ffmpeg_installed() -> bool:
    """
    Check if FFmpeg is installed and available in the system PATH.
    
    Returns:
        bool: True if FFmpeg is available, False otherwise
    """
    return shutil.which("ffmpeg") is not None


def install_ffmpeg_linux() -> bool:
    """
    Attempt to install FFmpeg on Linux systems using apt-get.
    
    Returns:
        bool: True if installation was successful, False otherwise
    """
    try:
        print("Attempting to install FFmpeg using apt-get...")
        
        # Update package list
        subprocess.run(
            ["sudo", "apt-get", "update", "-qq"],
            check=True,
            capture_output=True,
            timeout=300
        )
        
        # Install ffmpeg
        subprocess.run(
            ["sudo", "apt-get", "install", "-y", "-qq", "ffmpeg"],
            check=True,
            capture_output=True,
            timeout=300
        )
        
        print("✅ FFmpeg installed successfully!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install FFmpeg: {e}")
        return False
    except subprocess.TimeoutExpired:
        print("❌ Installation timed out")
        return False
    except FileNotFoundError:
        print("❌ apt-get not found. Please install FFmpeg manually.")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during installation: {e}")
        return False


def check_streamlit_cloud() -> bool:
    """
    Check if running in Streamlit Cloud environment.
    
    Returns:
        bool: True if running in Streamlit Cloud, False otherwise
    """
    # Streamlit Cloud sets specific environment variables
    return (
        os.environ.get("STREAMLIT_SHARING_MODE") is not None or
        os.environ.get("STREAMLIT_SERVER_HEADLESS") == "true"
    )


def setup_ffmpeg() -> bool:
    """
    Main setup function to ensure FFmpeg is available.
    
    Returns:
        bool: True if FFmpeg is available after setup, False otherwise
    """
    print("=" * 60)
    print("FFmpeg Setup Check")
    print("=" * 60)
    
    # Check if FFmpeg is already installed
    if is_ffmpeg_installed():
        print("✅ FFmpeg is already installed and available!")
        try:
            result = subprocess.run(
                ["ffmpeg", "-version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            version_line = result.stdout.split('\n')[0]
            print(f"Version: {version_line}")
        except Exception:
            pass
        print("=" * 60)
        return True
    
    print("⚠️  FFmpeg not found in PATH")
    
    # If running in Streamlit Cloud, packages.txt should handle installation
    if check_streamlit_cloud():
        print("\n📦 Running in Streamlit Cloud environment")
        print("FFmpeg should be installed via packages.txt file")
        print("If this message persists, ensure packages.txt contains 'ffmpeg'")
        print("=" * 60)
        return False
    
    # Attempt installation on Linux systems
    system = platform.system().lower()
    if system == "linux":
        print(f"\n🐧 Detected Linux system: {platform.platform()}")
        
        # Try to install
        if install_ffmpeg_linux():
            # Verify installation
            if is_ffmpeg_installed():
                print("✅ FFmpeg is now available!")
                print("=" * 60)
                return True
            else:
                print("⚠️  Installation completed but FFmpeg still not in PATH")
        
    else:
        print(f"\n⚠️  Unsupported system for auto-installation: {system}")
    
    # If we reach here, FFmpeg is not available
    print("\n" + "=" * 60)
    print("MANUAL INSTALLATION REQUIRED")
    print("=" * 60)
    print("\nPlease install FFmpeg manually:")
    print("\n**Ubuntu/Debian:**")
    print("  sudo apt update && sudo apt install ffmpeg")
    print("\n**macOS:**")
    print("  brew install ffmpeg")
    print("\n**Windows:**")
    print("  Download from https://ffmpeg.org/download.html")
    print("  Add to PATH after installation")
    print("\n**Streamlit Cloud:**")
    print("  Ensure packages.txt file exists with 'ffmpeg' listed")
    print("=" * 60)
    
    return False


if __name__ == "__main__":
    success = setup_ffmpeg()
    sys.exit(0 if success else 1)
