import React, { useState } from 'react';
import './App.css';

function App() {
  const [responseMessage, setResponseMessage] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const testRegisterUser = async () => {
    try {
      const response = await fetch('/api/register/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: 'testuser',
          password: 'testpassword',
          email: 'testuser@example.com',
        }),
      });

      if (!response.ok) {
        throw new Error(`Error: ${response.status} - ${response.statusText}`);
      }

      const data = await response.json();
      setResponseMessage(`Success: ${data.message}`);
    } catch (error) {
      setErrorMessage(`Failed: ${error.message}`);
    }
  };

  return (
    <div className="App">
      <h1>Welcome to MealForge</h1>
      <button onClick={testRegisterUser}>Test Register User</button>
      {responseMessage && <p style={{ color: 'green' }}>{responseMessage}</p>}
      {errorMessage && <p style={{ color: 'red' }}>{errorMessage}</p>}
    </div>
  );
}

export default App;