from PIL import Image
import io

class ImageValidator:
    """
    Handles image validation and preprocessing
    """
    
    @staticmethod
    def validate_image(file_stream):
        """
        Validates and preprocesses the uploaded image
        
        Args:
            file_stream: The uploaded file stream
            
        Returns:
            tuple: (is_valid, message, processed_image)
        """
        try:
            # Try to open the image to verify it's valid
            image = Image.open(file_stream)
            
            # Convert to RGB if necessary
            if image.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[-1])
                image = background
            elif image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Convert to bytes for processing
            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            img_byte_arr.seek(0)
            
            return True, "Image is valid", img_byte_arr
            
        except Exception as e:
            return False, f"Invalid image: {str(e)}", None
