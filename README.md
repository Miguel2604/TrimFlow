# Auto-Editor Minimal GUI

This is a minimalist Graphical User Interface (GUI) application built with Python and Tkinter to provide a simple front-end for the `auto-editor` command-line tool. It allows users to select an input video file, set a silence threshold and margin, specify an output MP4 file, and run `auto-editor` to cut silence.

## Prerequisites

Before running this application, you need to have:

1.  **Python 3.6 or higher** installed on your system.
2.  **auto-editor** and its dependencies (like ffmpeg) installed and accessible in your system's PATH. You can find installation instructions for auto-editor [here](https://github.com/WyattBlue/auto-editor).

## How to Run

1.  Save the provided Python code as `auto_editor_gui.py`.
2.  Open a terminal or command prompt in the directory where you saved the file.
3.  Run the script using Python:

    ```bash
    python auto_editor_gui.py
    ```
    or, on some Windows systems:
    ```bash
    py auto_editor_gui.py
    ```

4.  The GUI window should appear.

## How to Use the GUI

1.  **Select Input Video File:** Click the "Select Input File" button and choose the video file you want to process. The selected file path will be displayed.
2.  **Silence Threshold:** Enter the desired silence threshold value in the text field (e.g., "4%" or "-30dB"). A default value is provided.
3.  **Margin:** Enter the desired margin value in the text field (e.g., "0.2sec"). A default value is provided.
4.  **Set Output MP4 File:** Click the "Set Output File" button and choose where to save the output MP4 file. A suggested filename based on the input will be provided.
5.  **Start Cutting Silence:** Click the "Start Cutting Silence" button to begin the process. The status bar at the bottom will update to indicate the progress ("Processing...", "Finished!", or "Error occurred").

## Packaging as a Standalone Executable

To make the application easier for non-technical users to run, you can package it into a standalone executable using PyInstaller.

1.  **Install PyInstaller:** If you don't have it installed, open a terminal and run:
    ```bash
    pip install pyinstaller
    ```
2.  **Package the script:** Navigate to the directory containing `auto_editor_gui.py` in your terminal and run:
    ```bash
    pyinstaller --onefile auto_editor_gui.py
    ```
3.  A `dist` folder will be created in the same directory. Inside this folder, you will find the standalone executable (`auto_editor_gui.exe` on Windows).

**Note:** The packaged executable still requires `auto-editor` and its dependencies to be installed and in the system's PATH on the user's machine.

## Credits

This project uses the `auto-editor` command-line tool created by Wyatt Blue. You can find more information about `auto-editor` and its development at https://github.com/WyattBlue/auto-editor.

