// Test script to check if frontend can reach backend
async function testBackendConnection() {
  try {
    const response = await fetch('http://localhost:8000/');
    const data = await response.json();
    console.log('Connection successful:', data);
    return true;
  } catch (error) {
    console.error('Connection failed:', error);
    return false;
  }
}

// Test the signup endpoint specifically
async function testSignupEndpoint() {
  try {
    const response = await fetch('http://localhost:8000/api/auth/signup', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email: 'testuser2@example.com',
        name: 'Test User 2',
        password: 'securepassword123'
      })
    });
    
    if (response.ok) {
      const data = await response.json();
      console.log('Signup successful:', data);
    } else {
      const errorData = await response.json().catch(() => ({}));
      console.log('Signup response:', response.status, errorData);
    }
  } catch (error) {
    console.error('Signup request failed:', error);
  }
}

console.log('Testing backend connection...');
testBackendConnection().then(success => {
  if (success) {
    console.log('Testing signup endpoint...');
    testSignupEndpoint();
  }
});