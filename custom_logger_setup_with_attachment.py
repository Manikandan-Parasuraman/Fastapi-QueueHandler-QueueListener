import logging
import time
from logging.handlers import SMTPHandler
from email.message import EmailMessage
import smtplib

class SMTPAttachmentHandler(SMTPHandler):
    """
    A custom logging handler that sends log messages via email with optional attachments.

    This handler extends the built-in SMTPHandler to allow for sending email notifications
    when a log record is created. It can include file attachments specified in the log record.

    Attributes:
        credentials (tuple): A tuple containing the username and password for SMTP authentication.
    """

    def __init__(self, mailhost, fromaddr, toaddrs, subject, credentials=None, secure=None):
        """
        Initializes the SMTPAttachmentHandler.

        Args:
            mailhost (tuple): A tuple containing the SMTP server address and port.
            fromaddr (str): The email address from which the email will be sent.
            toaddrs (list): A list of recipient email addresses.
            subject (str): The subject line for the email.
            credentials (tuple, optional): A tuple containing the username and password for SMTP authentication.
            secure (tuple or None, optional): If provided, should contain parameters for a secure connection.
        """
        super().__init__(mailhost, fromaddr, toaddrs, subject, credentials=credentials, secure=secure)
        self.credentials = credentials

    def emit(self, record):
        """
        Sends an email with the log record details and an optional attachment.

        This method is called when a log message is emitted. It creates an email message,
        formats it with the log record details, checks for an attachment in the record,
        and sends the email using the configured SMTP server.

        Args:
            record (LogRecord): The log record containing information about the event being logged.

        Raises:
            Exception: Catches any exception that occurs during email sending and calls handleError.
        """
        try:
            # Create the email message
            msg = EmailMessage()
            msg['Subject'] = self.getSubject(record)
            msg['From'] = self.fromaddr
            msg['To'] = ', '.join(self.toaddrs)
            msg.set_content(self.format(record))

            # Extract attachment name from the file path
            attachment_name = (record.attachment).split('/')[-1]

            # Add attachment if specified
            if hasattr(record, 'attachment'):
                with open(record.attachment, 'rb') as f:
                    file_data = f.read()
                    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=attachment_name)

            # Send the email
            with smtplib.SMTP(self.mailhost) as server:
                if self.secure:
                    server.starttls()  # Upgrade to a secure connection if specified
                if self.credentials:
                    server.login(*self.credentials)  # Log in using provided credentials
                server.send_message(msg)  # Send the constructed email message

        except Exception as exec:
            print(exec)  # Print any exception that occurs during sending
            self.handleError(record)  # Call handleError to manage logging errors

# SMTP Configuration
SMTP_HOST = ''  # SMTP server address for Gmail
SMTP_PORT = 587 # Port for TLS/STARTTLS
USERNAME = ''   # Username for SMTP authentication (should be full email)
PASSWORD = ''   # Password or App password for authentication
FROM_ADDR = ''  # Sender's email address
TO_ADDRS = []   # List of recipient email addresses
SUBJECT = 'Critical Error in Application!'  # Subject line for emails

# Logger Setup
LOGGER = logging.getLogger(__name__)  # Create a logger object for this module
LOGGER.setLevel(logging.CRITICAL)     # Set logging level to CRITICAL

log_formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s | %(message)s')  # Define log format

# Create an instance of the custom SMTP handler
smtp_handler = SMTPAttachmentHandler(
    mailhost=(SMTP_HOST, SMTP_PORT),    # Tuple of host and port for SMTP server
    fromaddr=FROM_ADDR,                 # Sender's address
    toaddrs=TO_ADDRS,                   # List of recipient addresses
    subject=SUBJECT,                    # Subject line for emails
    credentials=(FROM_ADDR, PASSWORD),  # Credentials for SMTP authentication
    secure=()                           # Secure connection parameters (empty tuple means no additional parameters)
)

smtp_handler.formatter = log_formatter   # Assign formatter to handler
LOGGER.addHandler(smtp_handler)          # Add handler to logger

# Example of logging a critical error with an attachment
start = time.time()  # Start timing for performance tracking
LOGGER.critical("A Test", extra={'attachment': 'Fastapi-QueueHandler-QueueListener/app.py'})  # Log a critical message with an attachment path
print(f"Duration = {time.time() - start}")  # Print duration taken to execute logging operation