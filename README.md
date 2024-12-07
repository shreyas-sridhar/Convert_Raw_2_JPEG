## Overview
This application converts raw image files into JPEG format using Flask. It provides a simple web interface for uploading, processing, and downloading images.

## Features
- **Upload RAW Images**: Supports multiple formats including `.nef`, `.cr2`, `.arw`, and more.
- **Convert to JPEG**: Processes images efficiently using multiprocessing.
- **Download Converted Files**: Easily download your converted JPEG images.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/raw-image-converter.git
   cd raw-image-converter
   ```

2. Install the required packages:
   ```bash
   pip install Flask rawpy imageio
   ```

3. Ensure you have `ffmpeg` installed for image processing.

## Usage
1. Start the application:
   ```bash
   python app.py
   ```

2. Open your browser and go to `http://localhost:5000`.

3. Upload your raw images using the provided form.

4. Click the process button to convert them to JPEG.

5. Download your processed JPEG files from the links provided.

## Directory Structure
```
/raw-image-converter
│
├── app.py                # Main application file
├── uploads/              # Directory for uploaded raw images
├── outputs/              # Directory for converted JPEG images
└── templates/            # HTML templates for rendering pages
```

## Contributing
Feel free to fork the repository and submit pull requests with improvements or features.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
