import os
from rembg import remove, new_session
from PIL import Image
import io
import logging

logger = logging.getLogger(__name__)

class ImageProcessor:
    """
    Handles background removal processing using rembg
    """
    
    # Size thresholds in pixels (width * height)
    SMALL_IMAGE_THRESHOLD = 1000 * 1000  # 1MP
    LARGE_IMAGE_THRESHOLD = 2000 * 2000  # 4MP
    
    def __init__(self):
        # Initialize rembg session with u2net model
        self.session = new_session("u2net")
    
    def _get_image_size(self, image_data):
        """Get image dimensions"""
        img = Image.open(io.BytesIO(image_data))
        return img.size
    
    def _resize_image(self, image_data, max_size):
        """Resize image while maintaining aspect ratio"""
        img = Image.open(io.BytesIO(image_data))
        ratio = (max_size / float(max(img.size))) ** 0.5
        new_size = tuple(int(dim * ratio) for dim in img.size)
        resized = img.resize(new_size, Image.Resampling.LANCZOS)
        
        buffer = io.BytesIO()
        resized.save(buffer, format='PNG')
        return buffer.getvalue()
    
    def _get_alpha_params(self, image_size):
        """Get optimized alpha matting parameters based on image size"""
        width, height = image_size
        total_pixels = width * height
        
        if total_pixels <= self.SMALL_IMAGE_THRESHOLD:
            return {
                'alpha_matting_foreground_threshold': 240,
                'alpha_matting_background_threshold': 10,
                'alpha_matting_erode_size': 10
            }
        else:
            return {
                'alpha_matting_foreground_threshold': 250,  # More aggressive
                'alpha_matting_background_threshold': 5,    # More conservative
                'alpha_matting_erode_size': 5              # Smaller erosion
            }
    
    def process_image(self, image_data, use_alpha=False):
        """
        Removes background from the provided image
        
        Args:
            image_data: Image data in bytes
            use_alpha: Whether to use alpha matting for higher quality edges
            
        Returns:
            bytes: Processed image data
        """
        try:
            # Get image dimensions
            image_size = self._get_image_size(image_data)
            total_pixels = image_size[0] * image_size[1]
            
            logger.info(f"Processing image of size {image_size[0]}x{image_size[1]}")
            
            # Resize large images when using alpha matting
            if use_alpha and total_pixels > self.LARGE_IMAGE_THRESHOLD:
                logger.info("Large image detected, resizing for alpha matting")
                image_data = self._resize_image(image_data, 
                    int((self.LARGE_IMAGE_THRESHOLD) ** 0.5))
                image_size = self._get_image_size(image_data)
            
            # Base parameters
            params = {
                'session': self.session,
                'alpha_matting': use_alpha,
                'post_process_mask': True  # Enable post-processing for better quality
            }
            
            # Add optimized alpha matting parameters if enabled
            if use_alpha:
                params.update(self._get_alpha_params(image_size))
            
            # Process the image
            output = remove(image_data, **params)
            
            # Convert to PNG format
            output_img = Image.open(io.BytesIO(output))
            output_buffer = io.BytesIO()
            output_img.save(output_buffer, format='PNG')
            
            return output_buffer.getvalue()
            
        except Exception as e:
            raise Exception(f"Error processing image: {str(e)}")
