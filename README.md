# Fastapi-QueueHandler-QueueListener
This repository implements QueueHandler and QueueListener for Python's logging module, enabling non-blocking, asynchronous logging. It allows log messages to be sent to a queue and processed in a separate thread, improving application performance. Supports various handlers, including SMTP, and is easily configurable for flexible logging setups.

## Features

- Asynchronous context management for application lifespan.
- Integration with a logging system that uses a queue to handle log messages.
- A test endpoint to demonstrate logging functionality.

## Requirements

- Python 3.7 or higher
- FastAPI
- Uvicorn
- Any additional dependencies required for your logging setup

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/fastapi-logging-example.git
   cd fastapi-logging-example ```

2. Create a virtual environment (optional but recommended):
    ```bash
        python -m venv venv
        source venv/bin/activate  # On Windows use `venv\Scripts\activate` ```

3. Install the required packages:
``` bash
    pip install fastapi uvicorn
```

4. Install any additional dependencies for your logging setup (e.g., if you use logger_setup).
Usage
To run the FastAPI application, use the following command:
```bash
    uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

Parameters:
main: The name of the Python file without the .py extension (replace with your actual filename if different).
app: The FastAPI application instance defined in your code.
--host 0.0.0.0: Makes the server accessible from any IP address.
--port 8000: The port on which the server will run.
--reload: Enables auto-reload for development purposes.
Testing the Endpoint
Once the server is running, you can test the /test endpoint by navigating to:
```text
    http://localhost:8000/test 
```

This endpoint will log a critical message and return the duration of the request processing in JSON format:

```Json
    {
        "duration": 0.123  // Example response showing duration in seconds
    }
```

Stopping the Application
To stop the server, you can press CTRL + C in your terminal.
