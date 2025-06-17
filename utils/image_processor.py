import os
import logging
from PIL import Image
import torch
from torchvision import transforms

logger = logging.getLogger(__name__)

def process_image(image_path):
    """
    Process the uploaded image to prepare it for the Kosmos-2 model.
    
    Args:
        image_path (str): Path to the uploaded image file
        
    Returns:
        PIL.Image: Processed image ready for the model
    """
    logger.info(f"Processing image: {image_path}")
    
    try:
        # Open the image
        image = Image.open(image_path)
        
        # Resize image to fit model requirements (Kosmos-2 typically uses 224x224)
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])
        
        # Apply transformations
        processed_image = transform(image)
        
        logger.info("Image processed successfully")
        return processed_image
        
    except Exception as e:
        logger.error(f"Error processing image: {str(e)}")
        raise Exception(f"Failed to process image: {str(e)}")