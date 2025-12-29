import requests

# CONFIGURATION
BASE_URL = "http://127.0.0.1:8000"
LOGIN_URL = f"{BASE_URL}/api/auth/login/"
INITIATE_URL = f"{BASE_URL}/api/gokwik/initiate/"

# USER CREDENTIALS (CHANGE THESE IF NEEDED)
EMAIL = "swapnilshrivastava794@gmail.com"
PASSWORD = "password"  # Replace with actual password if different. I'm assuming 'password' or similar based on previous context, user might need to edit.
ORDER_ID = 1

def test_auth():
    print(f"1. Attempting Login with {EMAIL}...")
    
    # 1. LOGIN
    try:
        response = requests.post(LOGIN_URL, json={
            "email": EMAIL,
            "password": "password" # <--- Enter valid password here if this fails
        })
        
        if response.status_code != 200:
            print(f"❌ Login Failed: {response.status_code}")
            print(response.text)
            return

        tokens = response.json()
        access_token = tokens.get("access")
        refresh_token = tokens.get("refresh")
        
        print("\n✅ Login Successful!")
        print(f"Access Token (First 20 chars): {access_token[:20]}...")
        print(f"Refresh Token (First 20 chars): {refresh_token[:20]}...")

    except Exception as e:
        print(f"❌ Connection Error: {e}")
        return

    # 2. CALL GOKWIK API
    print(f"\n2. Calling Gokwik API with ACCESS TOKEN...")
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    data = {
        "order_id": ORDER_ID
    }
    
    response = requests.post(INITIATE_URL, headers=headers, json=data)
    
    if response.status_code == 200:
        print("\n✅ Gokwik API Succcess!")
        print("Response:", response.json())
    else:
        print(f"\n❌ Gokwik API Failed: {response.status_code}")
        print("Response:", response.text)

if __name__ == "__main__":
    test_auth()
