import os
import logging
import torch
from TTS.api import TTS

logger = logging.getLogger(__name__)

# Global variable to store the TTS model
tts_model = None

def load_tts_model():
    """
    Load the XTTS-v2 text-to-speech model.
    """
    global tts_model
    
    if tts_model is None:
        logger.info("Loading XTTS-v2 model...")
        try:
            # Initialize the TTS model
            tts_model = TTS(model_name="coqui/xtts-v2", progress_bar=False)
            logger.info("TTS model loaded successfully")
        except Exception as e:
            logger.error(f"Error loading TTS model: {str(e)}")
            raise Exception(f"Failed to load XTTS-v2 model: {str(e)}")

def generate_audio(text, output_path, voice_type="default"):
    """
    Generate audio narration from text using XTTS-v2 model.
    
    Args:
        text (str): Text to convert to speech
        output_path (str): Path to save the generated audio file
        voice_type (str): Type of voice to use ('default', 'male', 'female')
        
    Returns:
        str: Path to the generated audio file
    """
    # Load model if not already loaded
    load_tts_model()
    
    logger.info(f"Generating audio narration with voice type: {voice_type}...")
    
    try:
        # Set speaker based on voice type
        if voice_type == "male":
            speaker = "male"
        elif voice_type == "female":
            speaker = "female"
        else:
            speaker = "default"  # Default voice
        
        # Generate speech
        tts_model.tts_to_file(
            text=text,
            file_path=output_path,
            speaker=speaker,
            language="en"
        )
        
        logger.info(f"Audio generated successfully and saved to {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Error generating audio: {str(e)}")
        raise Exception(f"Failed to generate audio: {str(e)}")