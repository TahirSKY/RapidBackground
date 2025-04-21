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
        
    def process_image(self, image_data):
        """
        Removes background from the provided image
        
        Args:
            image_data: Image data in bytes
            
        Returns:
            bytes: Processed image data
        """
        try:
            # Process the image with rembg
            output = remove(
                image_data,
                session=self.session,
                alpha_matting=True,
                alpha_matting_foreground_threshold=240,
                alpha_matting_background_threshold=10,
                alpha_matting_erode_size=10
            )
            
            # Convert to PNG format
            output_img = Image.open(io.BytesIO(output))
            output_buffer = io.BytesIO()
            output_img.save(output_buffer, format='PNG')
            
            return output_buffer.getvalue()
            
        except Exception as e:
            raise Exception(f"Error processing image: {str(e)}")
