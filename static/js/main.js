document.addEventListener('DOMContentLoaded', () => {
    const imageInput = document.getElementById('image-input');
    const uploadSection = document.getElementById('upload-section');
    const progressSection = document.getElementById('progress-section');
    const inputPreview = document.getElementById('input-preview');
    const outputPreview = document.getElementById('output-preview');
    const inputImage = document.getElementById('input-image');
    const outputImage = document.getElementById('output-image');
    const downloadLink = document.getElementById('download-link');
    const imageInfo = document.getElementById('image-info');
    const imageDimensions = document.getElementById('image-dimensions');
    const sizeWarning = document.getElementById('size-warning');
    const processingStatus = document.getElementById('processing-status');
    const progressIndicator = document.getElementById('progress-indicator');

    // Constants
    const LARGE_IMAGE_THRESHOLD = 2000 * 2000; // 4MP

    // Preview uploaded image and show size info
    imageInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const img = new Image();
            const reader = new FileReader();
            
            reader.onload = (e) => {
                img.onload = () => {
                    // Show image dimensions
                    const megapixels = (img.width * img.height / 1000000).toFixed(1);
                    imageDimensions.textContent = `${img.width}x${img.height} (${megapixels}MP)`;
                    imageInfo.style.display = 'block';
                    
                    // Show warning for large images
                    if (img.width * img.height > LARGE_IMAGE_THRESHOLD) {
                        sizeWarning.style.display = 'block';
                    } else {
                        sizeWarning.style.display = 'none';
                    }
                };
                
                img.src = e.target.result;
                inputImage.src = e.target.result;
                inputPreview.style.display = 'block';
                outputPreview.style.display = 'none';
            };
            reader.readAsDataURL(file);
        }
    });

    // Update progress bar
    window.updateProgress = (percent) => {
        progressIndicator.style.width = `${percent}%`;
    };

    // Update processing status
    window.updateStatus = (status) => {
        processingStatus.textContent = status;
    };
});

async function processImage() {
    const imageInput = document.getElementById('image-input');
    const progressSection = document.getElementById('progress-section');
    const outputPreview = document.getElementById('output-preview');
    const outputImage = document.getElementById('output-image');
    const downloadLink = document.getElementById('download-link');
    const processingStatus = document.getElementById('processing-status');

    if (!imageInput.files || !imageInput.files[0]) {
        alert('Please select an image first');
        return;
    }

    const formData = new FormData();
    formData.append('image', imageInput.files[0]);

    // Get alpha matting preference
    const useAlpha = document.getElementById('alpha-matting').checked;

    try {
        progressSection.style.display = 'block';
        window.updateProgress(10);
        window.updateStatus('Preparing image for processing...');
        
        const response = await fetch(`/process${useAlpha ? '?alpha=1' : ''}`, {
            method: 'POST',
            body: formData
        });

        window.updateProgress(50);
        window.updateStatus('Removing background...');

        if (!response.ok) {
            const error = await response.text();
            throw new Error(error);
        }

        window.updateProgress(80);
        window.updateStatus('Finalizing image...');

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        
        window.updateProgress(100);
        window.updateStatus('Processing complete!');
        
        outputImage.src = url;
        downloadLink.href = url;
        outputPreview.style.display = 'block';
        
        // Reset progress after a delay
        setTimeout(() => {
            progressSection.style.display = 'none';
            window.updateProgress(0);
        }, 1500);
        
    } catch (error) {
        window.updateStatus('Error: ' + error.message);
        setTimeout(() => {
            progressSection.style.display = 'none';
            window.updateProgress(0);
        }, 3000);
    }
}
