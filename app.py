import os
import io
import logging
import psutil
from flask import Flask, request, render_template, send_file
from services.validator import ImageValidator
from services.image_processor import ImageProcessor

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
image_processor = ImageProcessor()

# Configure max content length (16MB)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

def get_memory_usage():
    """Get current memory usage of the process"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # Convert to MB

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process_image():
    """
    Process the uploaded image
    
    Returns:
        Processed image as attachment or error message
    """
    try:
        # Log initial memory usage
        initial_memory = get_memory_usage()
        logger.info(f"Starting image processing. Memory usage: {initial_memory:.2f}MB")
        
        # Get alpha matting parameter
        use_alpha = request.args.get('alpha', '0') == '1'
        logger.info(f"Alpha matting enabled: {use_alpha}")
        
        if 'image' not in request.files:
            logger.warning("No image file in request")
            return 'No image uploaded', 400
            
        file = request.files['image']
        if not file.filename:
            logger.warning("Empty filename in request")
            return 'No image selected', 400

        # Validate and preprocess the image
        is_valid, message, processed_image = ImageValidator.validate_image(file)
        if not is_valid:
            logger.warning(f"Image validation failed: {message}")
            return message, 400

        # Process the image with rembg
        logger.info("Starting background removal")
        result = image_processor.process_image(processed_image.getvalue(), use_alpha=use_alpha)
        
        # Log memory usage after processing
        final_memory = get_memory_usage()
        logger.info(f"Processing complete. Final memory usage: {final_memory:.2f}MB (Change: {final_memory - initial_memory:.2f}MB)")
        
        # Return the processed image
        return send_file(
            io.BytesIO(result),
            mimetype='image/png',
            as_attachment=True,
            download_name='processed.png'
        )

    except Exception as e:
        app.logger.error(f"Error processing image: {str(e)}")
        return str(e), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
