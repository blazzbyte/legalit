import requests

# Define the base URL of the FastAPI application
BASE_URL = "http://localhost:8000/api"  # Update with the actual URL of your FastAPI application

def test_chat_endpoint():
    # Define a sample chat message data
    chat_data = {
        "messages": [
            {"role": "user", "content": "Hello, how are you?"}
        ]
    }
    
    # Make a POST request to the chat endpoint
    response = requests.post(f"{BASE_URL}/chat", json=chat_data)
    
    # Print the response status code and content
    print("Response Status Code:", response.status_code)
    print("Response Content:", response.text)

if __name__=="__main__":
    # Test the chat endpoint
    test_chat_endpoint()