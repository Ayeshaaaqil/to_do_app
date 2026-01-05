import requests
import json

# Test the sign-up endpoint
def test_signup():
    url = "http://127.0.0.1:8000/api/auth/signup"
    
    # Sample user data for sign-up
    user_data = {
        "email": "testuser@example.com",
        "name": "Test User",
        "password": "securepassword123"
    }
    
    try:
        response = requests.post(url, json=user_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200:
            print("Sign-up successful!")
        else:
            print(f"Sign-up failed: {response.text}")
            
    except Exception as e:
        print(f"Error during sign-up test: {e}")

if __name__ == "__main__":
    test_signup()