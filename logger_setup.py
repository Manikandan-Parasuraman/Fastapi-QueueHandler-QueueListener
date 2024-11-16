import logging
import queue
from logging.handlers import SMTPHandler, QueueHandler, QueueListener

# SMTP configuration for sending emails
SMTP_HOST = 'smtp.gmail.com'                # SMTP server address for Gmail
SMTP_PORT = 587                             # Port for TLS/STARTTLS
USERNAME = 'Manikandan'                     # Username for SMTP authentication (should be full email)
PASSWORD = ''                               # Password or App password for authentication (leave empty for security)
FROM_ADDR = ''                              # Sender's email address (should be a valid email)
TO_ADDRS = ['tech.cod.mk13@gmail.com']      # List of recipient email addresses
SUBJECT = 'Critical Error in Application!'  # Subject line for emails

# Create a logger object for this module
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.CRITICAL)  # Set logging level to CRITICAL

# Define the log format
log_formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')

# Create an SMTPHandler for sending emails with log messages
smtp_handler = SMTPHandler(
    mailhost=(SMTP_HOST, SMTP_PORT),           # Tuple of host and port for the SMTP server
    fromaddr=FROM_ADDR,                        # Sender's email address
    toaddrs=TO_ADDRS,                          # List of recipient addresses
    subject='Critical Error in Application!',  # Subject line for emails
    credentials=(FROM_ADDR, PASSWORD),         # Credentials for SMTP authentication
    secure=()                                  # Secure connection parameters (empty tuple means no additional parameters)
)

# Assign the formatter to the SMTP handler to format log messages
smtp_handler.formatter = log_formatter

# Uncomment the following line to add the SMTP handler directly to the logger
# LOGGER.addHandler(smtp_handler)

# Create a Queue object to hold log messages temporarily before processing them
log_queue = queue.Queue()

# Create a QueueHandler that sends log records to the queue instead of directly to the handler
queue_handler = QueueHandler(log_queue)
LOGGER.addHandler(queue_handler)  # Add the QueueHandler to the logger

# Start the listener - creates a thread that listens for log messages in the queue and processes them using the SMTP handler
LISTENER = QueueListener(log_queue, smtp_handler)