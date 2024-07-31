# Mental Health API

This API provides endpoints for mental health-related functionalities. It is built with FastAPI.

## Features

- Endpoint to manage mental health data
- Integration with curl and Fetch API for easy access

## Requirements

- Python 3.x
- FastAPI
- Uvicorn

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/hridya7602/health_chatbot.git
   cd health_chatbot
2. Install the dependencies:


    pip install -r requirements.txt
3. Run the application:

    uvicorn main:app --reload
## Usage
 Using curl
    You can interact with the API using curl. Here is an example of how to make a GET request to the API:


    curl -X GET "http://127.0.0.1:8000/your-endpoint" -H "accept: application/json"

    To make a POST request with curl:

    curl -X POST "http://127.0.0.1:8000/your-endpoint" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"key\":\"value\"}"
## Using Fetch API
You can also interact with the API using the Fetch API in JavaScript. Here is an example of how to make a GET request:

fetch('http://127.0.0.1:8000/your-endpoint', {
    method: 'GET',
    headers: {
        'Accept': 'application/json'
    }
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
To make a POST request with the Fetch API:


fetch('http://127.0.0.1:8000/your-endpoint', {
    method: 'POST',
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ key: 'value' })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
## Example Endpoints
# GET

Description: Retrieve data from the API.
Example using curl:

curl -X GET "http://127.0.0.1:8000/your-endpoint" -H "accept: application/json"
Example using Fetch API:

fetch('http://127.0.0.1:8000/your-endpoint', {
    method: 'GET',
    headers: {
        'Accept': 'application/json'
    }
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
## POST 

Description: Send data to the API.
Example using curl:

curl -X POST "http://127.0.0.1:8000/your-endpoint" -H "accept: application/json" -H "Content-Type: application/json" -d "{\"key\":\"value\"}"
Example using Fetch API:
javascript
Copy code
fetch('http://127.0.0.1:8000/your-endpoint', {
    method: 'POST',
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({ key: 'value' })
})
.then(response => response.json())
.then(data => console.log(data))
.catch(error => console.error('Error:', error));
