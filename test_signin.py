import requests
import json

def test_signin():
    url = "http://127.0.0.1:8000/api/auth/signin"

    # User credentials for sign-in - the endpoint expects a dict with email and password as keys
    user_data = {
        "email": "testuser@example.com",
        "password": "securepassword123"
    }

    try:
        response = requests.post(url, json=user_data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")

        if response.status_code == 200:
            print("Sign-in successful!")
        else:
            print(f"Sign-in failed")

    except Exception as e:
        print(f"Error during sign-in test: {e}")

if __name__ == "__main__":
    test_signin()