# Chatbot main

import os
from dotenv import load_dotenv
from openai import OpenAI
from openai import RateLimitError, APIError

# Load environment variables from .env file
load_dotenv()

# Get API key from environment variable (more secure)
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("Warning: OPENAI_API_KEY environment variable not set.")
    print("Please create a .env file in the project root with: OPENAI_API_KEY=your_key_here")
    print("Or set it using: set OPENAI_API_KEY=your_key_here (Windows) or export OPENAI_API_KEY=your_key_here (Linux/Mac)")
    api_key = input("Enter your OpenAI API key (or press Enter to exit): ").strip()
    if not api_key:
        exit()

client = OpenAI(api_key=api_key)

print("Chatbot ready! Type 'exit', 'quit', or 'bye' to end the conversation.\n")

while True:
    try:
        user_input = input("Ask: ")

        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Thank you! Bye..")
            break
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": user_input}
            ]
        )

        print("Answer:", response.choices[0].message.content)
        print()  # Empty line for readability
        
    except RateLimitError as e:
        print(f"\n❌ Rate Limit Error: {e}")
        print("\nPossible solutions:")
        print("1. Check your OpenAI account at https://platform.openai.com/account/billing")
        print("2. Verify you have available credits/quota")
        print("3. Ensure your API key matches the account with credits")
        print("4. Add a payment method if required (even for free credits)")
        print("5. Wait a few minutes if you just added credits\n")
        break
        
    except APIError as e:
        error_str = str(e)
        print(f"\n❌ API Error: {e}")
        if "invalid_api_key" in error_str or "Incorrect API key" in error_str:
            print("\n⚠ Invalid API Key Detected!")
            print("The API key in your .env file is incorrect or expired.")
            print("Please:")
            print("1. Get a new API key from: https://platform.openai.com/account/api-keys")
            print("2. Update your .env file with: OPENAI_API_KEY=your_new_key_here")
            print("3. Make sure there are no spaces or quotes around the key\n")
        else:
            print("Please check your API key and account status.\n")
        break
        
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}\n")
        break