# RAW to JPEG Converter Web App

This web application allows users to upload RAW image files and convert them to JPEG format. It leverages Flask for the backend, multiprocessing for performance, and libraries like `rawpy` and `imageio` for image processing.

---

## Features

- **Batch Processing**: Upload multiple RAW files and convert them simultaneously.
- **Automatic Cleanup**: Clears uploaded files and processed outputs between sessions.
- **Supported Formats**: `.nef`, `.cr2`, `.arw`, `.raw`, `.dng`, `.raf`, `.3fr`, `.dcr`, `.k25`, `.kdc`, `.mrw`, `.pef`, `.srw`, `.x3f`.

---

## Prerequisites

- Python 3.8 or above
- pip (Python package manager)
- Libraries:
  - `flask`
  - `rawpy`
  - `imageio`
  - `werkzeug`

---

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/your-repo-name/raw-to-jpeg-converter.git
    cd raw-to-jpeg-converter
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows, use venv\Scripts\activate
    ```

3. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

---

## Running the Application Locally

1. Run the application:

    ```bash
    python app.py
    ```

2. Open your browser and navigate to:

    ```
    http://127.0.0.1:5000
    ```

---

## Usage

### Uploading Files
1. Drag and drop or select your RAW image files on the homepage.
2. Click **Upload**.

### Processing Files
1. Once uploaded, click **Process Files**.
2. The app will process the files and provide download links for the JPEG outputs.

### Downloading Files
1. Click on the provided download links to get the JPEG files.

---

## Directory Structure

- **`uploads/`**: Stores uploaded RAW files (cleared after processing).
- **`outputs/`**: Stores converted JPEG files (cleared when a new session starts).

---

## Deployment

To deploy the app, use a production-ready server like **Gunicorn** or **uWSGI**, and a reverse proxy like **Nginx**:

1. Install Gunicorn:

    ```bash
    pip install gunicorn
    ```

2. Run the app:

    ```bash
    gunicorn -w 4 -b 0.0.0.0:8000 app:app
    ```

---

## Troubleshooting

- **File Too Large**: Ensure files are under 50MB (modifiable in `app.config['MAX_CONTENT_LENGTH']`).
- **Timeout**: Increase the timeout duration in the `process_images` function.
- **Permission Errors**: Ensure the `uploads/` and `outputs/` directories have the correct permissions.

---

## Contributing

Feel free to submit issues and pull requests! Contributions are welcome to improve functionality or add new features.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/)
- [rawpy](https://rawpy.github.io/)
- [imageio](https://imageio.readthedocs.io/)

---
