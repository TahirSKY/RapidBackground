import os
from flask import Flask, request, render_template, send_file
from services.validator import ImageValidator
from services.image_processor import ImageProcessor
import io

app = Flask(__name__)
image_processor = ImageProcessor()

# Configure max content length (16MB)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

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
        if 'image' not in request.files:
            return 'No image uploaded', 400
            
        file = request.files['image']
        if not file.filename:
            return 'No image selected', 400

        # Validate and preprocess the image
        is_valid, message, processed_image = ImageValidator.validate_image(file)
        if not is_valid:
            return message, 400

        # Process the image with rembg
        result = image_processor.process_image(processed_image.getvalue())
        
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
