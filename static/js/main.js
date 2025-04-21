document.addEventListener('DOMContentLoaded', () => {
    const imageInput = document.getElementById('image-input');
    const uploadSection = document.getElementById('upload-section');
    const progressSection = document.getElementById('progress-section');
    const inputPreview = document.getElementById('input-preview');
    const outputPreview = document.getElementById('output-preview');
    const inputImage = document.getElementById('input-image');
    const outputImage = document.getElementById('output-image');
    const downloadLink = document.getElementById('download-link');

    // Preview uploaded image
    imageInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                inputImage.src = e.target.result;
                inputPreview.style.display = 'block';
                outputPreview.style.display = 'none';
            };
            reader.readAsDataURL(file);
        }
    });
});

async function processImage() {
    const imageInput = document.getElementById('image-input');
    const progressSection = document.getElementById('progress-section');
    const outputPreview = document.getElementById('output-preview');
    const outputImage = document.getElementById('output-image');
    const downloadLink = document.getElementById('download-link');

    if (!imageInput.files || !imageInput.files[0]) {
        alert('Please select an image first');
        return;
    }

    const formData = new FormData();
    formData.append('image', imageInput.files[0]);

    try {
        progressSection.style.display = 'block';
        
        const response = await fetch('/process', {
            method: 'POST',
            body: formData
        });

        if (!response.ok) {
            const error = await response.text();
            throw new Error(error);
        }

        const blob = await response.blob();
        const url = URL.createObjectURL(blob);
        
        outputImage.src = url;
        downloadLink.href = url;
        outputPreview.style.display = 'block';
        
    } catch (error) {
        alert('Error processing image: ' + error.message);
    } finally {
        progressSection.style.display = 'none';
    }
}
