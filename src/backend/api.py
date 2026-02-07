from http import client
import threading
import time
from xml.parsers.expat import model
from dotenv import load_dotenv
import os
from google import genai
from google.genai import errors
from .GeminiService import GeminiService



# Define a simple API class to expose Python functions to JavaScript
class API:
    def __init__(self, window=None): # Changed to allow initialization with None
        # Keep the window reference private so pywebview doesn't try to serialize it
        load_dotenv()
        self._window = window
        self.js_ready = False

        self.gemini_service = GeminiService()
        self.gemini_service.init_gemini() # Initialize Gemini Chat when the API is created
        # access Gemini chat via self.gemini_service.chat and methods like self.gemini_service.chat.send_message() etc.
        
    
    def set_window(self, window):
        # Called by main.py once the window exists
        self._window = window

    # This function is called from JavaScript (e.g., by the button click)
    def say_hello_from_python(self, name):
        print(f"Python received a call from {name}!")
        return f"Hello, {name}! This message is from Python."

    # This function is called from JavaScript to signal that JS is ready
    def init_js_ready(self):
        self.js_ready = True
        print("JavaScript is ready!")
        # Once JS is ready, we can call a JS function from Python
        # We'll do this in a separate thread to avoid blocking the main thread
        threading.Thread(target=self.call_js_after_delay).start()




    # A function to demonstrate calling JavaScript from Python after a delay
    def call_js_after_delay(self):
        # Wait until JS is confirmed ready
        while not self.js_ready:
            time.sleep(0.1) # Small delay to prevent busy-waiting
        
        time.sleep(2) # Simulate some work or a delay
        message_from_python = "Python is now updating the message in JavaScript!"
        print(f"Python is calling JavaScript with: '{message_from_python}'")
        # Call the 'updateMessage' JavaScript function
        # The `evaluate_js` method is used to execute JavaScript code in the webview
        if self._window is None:
            return
        self._window.evaluate_js(f"updateMessage('{message_from_python}')")
