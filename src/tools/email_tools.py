import smtplib
from email.mime.text import MIMEText
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from src.config.settings import OPENAI_API_KEY, EMAIL_SENDER, EMAIL_PASSWORD, LLM_MODEL

# class EmailTools:
#     """
#     Tools for email formatting and sending
#     """
#     def __init__(self):
#         """Initialize the EmailTools with an LLM model"""
#         self.llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model=LLM_MODEL)
    
#     @tool
#     def send_email(self, to_email: str, logs: str, server_name: str) -> dict:
#         """
#         Format and send logs to the specified email address.
        
#         Args:
#             to_email: Recipient email address
#             logs: Log content to send
#             server_name: Name of the server the logs are from
            
#         Returns:
#             Dictionary with status and message
#         """
#         # Create email content using LLM
#         prompt = f"""
#         You are a TMA AI assistant responsible for turning system logs into professional email reports. 
#         Below is a log entry from a Docker container:

#         {logs}

#         Please analyze the logs and summarize the number of HTTP status codes (e.g., 200, 404, 304) in the past 1 hour.
#         Format the response as a professional email report. 

#         Note: Please return only the email content without including a subject line.  
#         Use "TMA Agent" as your name in the signature.
#         """

#         # Generate email content
#         content = self.llm.invoke(prompt).content
        
#         # Create and send email
#         msg = MIMEText(content, "plain", "utf-8")
#         msg["Subject"] = f"Docker Logs from server named {server_name}"
#         msg["From"] = EMAIL_SENDER
#         msg["To"] = to_email
        
#         try:
#             with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
#                 server.login(EMAIL_SENDER, EMAIL_PASSWORD)
#                 server.sendmail(EMAIL_SENDER, to_email, msg.as_string())
#             return {"status": "success", "message": "Email sent successfully."}
#         except Exception as e:
#             return {"status": "error", "message": f"Email Error: {e}"}

@tool
def send_email(to_email: str, logs: str, server_name: str) -> dict:
    """Send logs to the specified email address."""
    sender_email = EMAIL_SENDER
    sender_password = EMAIL_PASSWORD
    # --- enhanced ---
    prompt = f"""
    You are an TMA AI assistant responsible for turning system logs into professional email reports. 
    Below is a log entry from a Docker container:

    {logs}

    Please generate a fully email content send all log to {to_email}
    Note: Plese just return the content, not include title Subject, ... and put your name is AI Agent
    """

    prompt = f"""
    You are a TMA AI assistant responsible for turning system logs into professional email reports. 
    Below is a log entry from a Docker container:

    {logs}

    Please analyze the logs and summarize the number of HTTP status codes (e.g., 200, 404, 304) in the past 1 hour.
    Format the response as a professional email report. 

    Note: Please return only the email content without including a subject line.  
    Use "TMA Agent" as your name in the signature.
    """
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model=LLM_MODEL)
    content = llm.invoke(prompt).content
    # --- done ---

    msg = MIMEText(content, "plain", "utf-8")
    msg["Subject"] = f"Docker Logs from server named {server_name}"
    msg["From"] = sender_email
    msg["To"] = to_email
    
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, to_email, msg.as_string())
        return {"status": "success", "message": "Email sent successfully."}
    except Exception as e:
        return {"status": "error", "message": f"Email Error: {e}"}
