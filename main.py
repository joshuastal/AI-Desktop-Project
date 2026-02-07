
import webview
import threading
import time
import os
import sys # Import sys
from src.backend.api import API

# Get the directory of the current script
# This is crucial for Pywebview to find the HTML, CSS, and JS files
script_dir = os.path.dirname(os.path.abspath(__file__))
html_file_path = os.path.join(script_dir, 'index.html')


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def main():
    # Use the new helper function to define file paths
    html_file_path = resource_path('src/frontend/index.html') # Adjusted path for the HTML file

    api = API()

    window = webview.create_window(
        'Pywebview HTML/CSS/JS Demo',
        url=f'file://{html_file_path}', # Use the robust path
        min_size=(600, 400),
        js_api=api
    )
    
    api.set_window(window)

    webview.start(debug=False) # Set debug to False for final build

if __name__ == '__main__':
    main()
