from rembg import remove, new_session
from PIL import Image
import io

class ImageProcessor:
    """
    Handles background removal processing using rembg
    """
    
    def __init__(self):
        # Initialize rembg session with u2net model
        self.session = new_session("u2net")
        
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
            # Process the image with rembg
            params = {
                'session': self.session,
                'alpha_matting': use_alpha
            }
            
            # Add alpha matting parameters only if enabled
            if use_alpha:
                params.update({
                    'alpha_matting_foreground_threshold': 240,
                    'alpha_matting_background_threshold': 10,
                    'alpha_matting_erode_size': 10
                })
            
            output = remove(image_data, **params)
            
            # Convert to PNG format
            output_img = Image.open(io.BytesIO(output))
            output_buffer = io.BytesIO()
            output_img.save(output_buffer, format='PNG')
            
            return output_buffer.getvalue()
            
        except Exception as e:
            raise Exception(f"Error processing image: {str(e)}")
