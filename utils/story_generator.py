import logging
import torch
from transformers import AutoProcessor, AutoModelForVision2Seq

logger = logging.getLogger(__name__)

# Global variables to store the model and processor
model = None
processor = None

def load_model():
    """
    Load the Kosmos-2 model and processor.
    """
    global model, processor
    
    if model is None or processor is None:
        logger.info("Loading Kosmos-2 model and processor...")
        try:
            # Load the model and processor
            model_name = "microsoft/kosmos-2"
            processor = AutoProcessor.from_pretrained(model_name)
            model = AutoModelForVision2Seq.from_pretrained(model_name)
            
            # Move model to GPU if available
            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            model = model.to(device)
            
            logger.info(f"Model loaded successfully on {device}")
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise Exception(f"Failed to load Kosmos-2 model: {str(e)}")

def generate_story(image_tensor, story_type="story"):
    """
    Generate a story or poem from the processed image using Kosmos-2 model.
    
    Args:
        image_tensor (torch.Tensor): Processed image tensor
        story_type (str): Type of text to generate ('story' or 'poem')
        
    Returns:
        str: Generated story or poem
    """
    # Load model if not already loaded
    load_model()
    
    logger.info(f"Generating {story_type} from image...")
    
    try:
        # Move image tensor to the same device as the model
        device = next(model.parameters()).device
        image_tensor = image_tensor.unsqueeze(0).to(device)  # Add batch dimension
        
        # Prepare prompt based on story type
        if story_type == "poem":
            prompt = "Write a creative poem inspired by this image:"
        else:  # Default to story
            prompt = "Write a creative short story inspired by this image:"
        
        # Prepare inputs for the model
        inputs = processor(text=prompt, images=image_tensor, return_tensors="pt").to(device)
        
        # Generate text
        with torch.no_grad():
            generated_ids = model.generate(
                pixel_values=inputs["pixel_values"],
                input_ids=inputs["input_ids"],
                attention_mask=inputs["attention_mask"],
                max_length=300,
                num_beams=5,
                early_stopping=True
            )
        
        # Decode the generated text
        generated_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]
        
        # Extract the story part (remove the prompt)
        story = generated_text.replace(prompt, "").strip()
        
        logger.info(f"{story_type.capitalize()} generated successfully")
        return story
        
    except Exception as e:
        logger.error(f"Error generating {story_type}: {str(e)}")
        raise Exception(f"Failed to generate {story_type}: {str(e)}")