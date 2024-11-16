from fastapi import FastAPI
from logger_setup import LOGGER, LISTENER
import time
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for the FastAPI application.

    This asynchronous context manager is used to manage the lifespan of the FastAPI app.
    It yields control to the application during its startup phase and ensures that
    resources are cleaned up properly when the application shuts down.

    Args:
        app (FastAPI): The FastAPI application instance.

    Yields:
        None: Control is yielded to the FastAPI application during its lifespan.

    On exit, this context manager stops the logging listener, which processes log messages.
    """
    yield            # Yield control back to the FastAPI app
    LISTENER.stop()  # Stop the logging listener when the app shuts down

# Start the logging listener in a separate thread
LISTENER.start()

# Create an instance of FastAPI with the lifespan context manager
app = FastAPI(lifespan=lifespan)

@app.get('/test')
def test_router():
    """
    Test endpoint for logging and measuring duration.

    This endpoint logs a critical message indicating that the test has been triggered.
    It also measures and returns the duration of the request handling.

    Returns:
        dict: A JSON response containing the duration of the request processing.
              Example: {"duration": 0.123}
    """
    start = time.time()  # Record the start time
    LOGGER.critical("Testing the Python Queue Handler and Queue Listener")  # Log a critical message
    return {"duration": time.time() - start}  # Return the duration of processing