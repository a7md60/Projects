import os
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

class EmailHelper:
    def __init__(self, sendgrid_api_key):
        self.sendgrid_api_key = sendgrid_api_key

    def send_email(self, sender_email, receiver_email, subject, body):
        
        # Initialize SendGrid client
        sg = SendGridAPIClient(self.sendgrid_api_key)

        # Construct email message
        message = Mail(
            from_email=sender_email,
            to_emails=receiver_email,
            subject=subject,
            html_content=body
        )

        try:
            # Send the email
            response = sg.send(message)
            print("Email sent successfully!")
        except Exception as e:
            print("Failed to send email:", e)

    @staticmethod
    def create_html_for_email(messages, message, chat, description):
        # Start the HTML string
        html_content = "<html><body>"
        data_fields = f"""<h3>A user has reported error on a response </h3>
        <h5> Chat id :  {chat.id}</h5>
        <h5> Chat Name :  {chat.topic}</h5>
        <h5> Message id:  {message.id}</h5>
        <h5> Message Text:  {message.text}</h5>
        <h5>Description added by the user : {description} </h5>
        <h5> Here is the brief chat history</h5>
        </br>
        """
        html_content = html_content + data_fields

        sorted_messages = sorted(messages, key=lambda x: x.updated_at)
        # Iterate through each message
        for message in sorted_messages:
            # Format the message content
            message_html = f"<p>{message.updated_at} - {message.sender}: {message.text}</p>"
            # Append the formatted message to the HTML content
            html_content += message_html
        
        # Close the HTML string
        html_content += "</body></html>"
        
        return html_content


# Example usage:
# credentials_path = 'path/to/your/credentials.json'
# sender_email = 'your_email@gmail.com'
# receiver_email = 'recipient_email@gmail.com'
# subject = 'Test Email from Python'
# body = 'This is a test email sent using Python.'

# email_helper = EmailHelper(credentials_path)
# email_helper.send_email(sender_email, receiver_email, subject, body)

# messages = [...] # List of messages
# message = [...] # Message object
# chat = [...] # Chat object
# description = "Error description"
# html_content = email_helper.create_html_for_email(messages, message, chat, description)
