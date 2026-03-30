import os
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env file
load_dotenv()

# Configure the API key from environment variable
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable not set. Please add it to your .env file.")

# Create a client with the API key
client = genai.Client(api_key=api_key)

# List available models
print("Available models:")
for model in client.models.list():
    print(f"  - {model.name}")

# Generate content using an available model
print("\nGenerating content...")
response = client.models.generate_content(
    model="models/gemini-2.5-flash",
    contents="Hello!"
)

print(f"\nResponse: {response.text}")