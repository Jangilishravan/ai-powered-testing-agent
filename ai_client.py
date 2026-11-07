
import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env
load_dotenv()

# Read API key securely
api_key = os.getenv("OPENAI_API_KEY")

if not api_key or api_key == "your_actual_secret_key_here":
    raise ValueError("OpenAI API key is missing. Check your .env file.")

# Create OpenAI client
client = OpenAI(api_key=api_key)

# Select the model
MODEL = os.getenv("OPENAI_MODEL", "gpt-6-luna")


def ask_ai(prompt):

    response = client.responses.create(
        model=MODEL,
        input=prompt
    )

    return response.output_text


if __name__ == "__main__":

    print("\n========== AI CONNECTION TEST ==========")

    result = ask_ai(
        "Explain in one sentence why API testing is important."
    )

    print("\nAI Response:", result)
    print("\nAI CONNECTION SUCCESSFUL!")
