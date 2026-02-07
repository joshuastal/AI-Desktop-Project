from http import client
import threading
import time
from xml.parsers.expat import model
from dotenv import load_dotenv
import os
from google import genai
from google.genai import errors


def retry_on_server_error(retries: int = 5, delay: int = 5):
    """Decorator that retries a function when `errors.ServerError` is raised.

    Returns `None` if max retries are exceeded.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            attempt = 0
            while attempt <= retries:
                try:
                    return func(*args, **kwargs)
                except errors.ServerError as e:
                    if attempt == retries:
                        print("Max retries reached. Please try again later.")
                        return None
                    print(f"Server is overloaded: {e}")
                    print(f"Retrying in {delay} seconds... (attempt {attempt+1}/{retries})")
                    time.sleep(delay)
                    attempt += 1
        return wrapper
    return decorator

class GeminiService:
    def __init__(self):
        load_dotenv()
        self.client = None
        self.chat = None

    
    @retry_on_server_error()
    def init_gemini(self):
        print("Initializing Gemini Chat...")

        key = os.getenv("GEMINI_KEY")
        model = os.getenv("GEMINI_MODEL")
        
        if not key or not model:
            print("GEMINI_KEY or GEMINI_MODEL environment variable is not set.")
            return

        try:
            self.client = genai.Client(api_key=key)
            self.chat = self.client.chats.create(model=model, history=[])
            print("Gemini Chat Initialized...")
        except Exception as e:
            print(f"Error initializing Gemini Chat: {e}")

    
    def send_message(self, message):
        if self.chat is None:
            print("Gemini Chat is not initialized.")
            return None

        try:
            response = self.chat.send_message(message)
            return response.text
        except Exception as e:
            return f"Error sending message to Gemini Chat: {e}"

