# TrimFlow - Video Silence Cutter 📹✂️

TrimFlow is a web and GUI application designed to automatically trim silence from video files, making your video content concise and engaging. The app utilizes the `auto-editor` command-line tool to perform silence detection and removal.

## Features 🌟

- **Web Interface**: Upload videos, set parameters, and download the processed outputs through a simple web interface.
- **Desktop GUI**: Use the desktop GUI version for local processing.
- **Customizable Settings**: Set silence threshold and margin for precise editing.

## Installation 📥

1. Clone this repository:
    ```bash
    git clone https://github.com/yourusername/TrimFlow.git
    cd TrimFlow
    ```

2. Install Python dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Ensure `auto-editor` and its dependencies (like `ffmpeg`) are installed and accessible in your system's PATH. Installation instructions for `auto-editor` can be found [here](https://github.com/WyattBlue/auto-editor).

## Running the Web App 🌐

1. Start the server:
    ```bash
    python app.py
    ```
2. Access the web app by navigating to [http://localhost:5000](http://localhost:5000) in your browser.

## Using the Desktop GUI 🖥️

1. Run the script:
    ```bash
    python auto_editor_gui.py
    ```
2. Follow the on-screen instructions to select your input file, set threshold and margin, and start processing.

## Usage Instructions 📝

- **Web Interface**:
  1. Select the video file to process.
  2. Set the silence threshold and margin.
  3. Click "Start Cutting Silence" and wait for the download link.
  
- **Desktop GUI**:
  1. Select the video file.
  2. Set the silence threshold and margin.
  3. Set the output file name and location.
  4. Click "Start Cutting Silence" to process.

## Building Standalone Executable 🔧

To build a standalone executable version using PyInstaller:

1. Install PyInstaller:
    ```bash
    pip install pyinstaller
    ```

2. Build the executable:
    ```bash
    pyinstaller --onefile --windowed auto_editor_gui.py
    ```

The executable will be found in the `dist` directory.

## License 📄

MIT License

## Credits and Acknowledgments 🙌

This project utilizes the `auto-editor` by Wyatt Blue. More about `auto-editor` can be found [here](https://github.com/WyattBlue/auto-editor).

Enjoy using TrimFlow! 🎉
