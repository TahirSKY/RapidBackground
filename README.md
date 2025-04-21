# RapidBG - Background Removal Tool

A powerful background removal tool built with Flask and rembg. This application provides a simple web interface for removing backgrounds from images with high-quality results.

## Features

- High-quality background removal using rembg
- Support for various image formats
- Simple, clean web interface
- Efficient image processing
- Production-ready configuration

## Local Development

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
- Windows:
```bash
.\venv\Scripts\activate
```
- Unix/MacOS:
```bash
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the development server:
```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Deployment on Render

1. Push your code to a GitHub repository

2. Create a new Web Service on Render:
   - Connect your GitHub repository
   - Select Python environment
   - Set the following:
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `gunicorn app:app`
   - Environment Variables: None required for basic setup

3. Deploy the application

The application will be automatically deployed and available at your Render URL.

## Technical Details

- Flask web framework
- rembg for background removal
- Gunicorn for production server
- Support for various image formats
- Error handling and logging
- Production-ready configuration

## File Size Limits

- Maximum upload size: 16MB
- Supported formats: All common image formats (PNG, JPEG, WebP, etc.)

## License

MIT License
