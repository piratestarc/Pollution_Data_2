import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

class Email():
    def __init__(self, vehicle_data, thing):
        my_email = "piratestarc@gmail.com"
        password = "uzyk stkn zxsj sdnm"
        to_email = "aliaskiyotaka@gmail.com"

        # Creating the email content
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"{thing} Expiring Notification"
        msg["From"] = my_email
        msg["To"] = to_email

        # Start the HTML message with table header
        html = """
        <html>
        <body>
            <p>Hello,</p>
            <p>Here are the vehicle details expiring tomorrow:</p>
            <table border="1" cellpadding="5" cellspacing="0">
                <tr>
                    <th>Vehicle Number</th>
                    <th>Owner Name</th>
                    <th>Registered Name</th>
                    <th>Phone Number</th>
                    <th>Vehicle</th>
                    <th>Vehicle Model</th>
                    
                </tr>
        """

        # Using a for loop to generate table rows from vehicle_data
        for vehicle in vehicle_data:
            html += f"""
                <tr>
                    <td>{vehicle.customer.vehicle_number}</td>
                    <td>{vehicle.customer.current_owner}</td>
                    <td>{vehicle.customer.register_owner}</td>
                    <td>{vehicle.customer.phone_number}</td>
                    <td>{vehicle.customer.vehicle_type}</td>
                    <td>{vehicle.customer.vehicle_model}</td>
                </tr>
            """

        # End the HTML message
        html += """
            </table>
            <p>Best regards,<br>Your Company</p>
        </body>
        </html>
        """

        # Attach HTML content to the message
        part = MIMEText(html, "html")
        msg.attach(part)

        # Sending the email
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(from_addr=my_email, to_addrs=to_email, msg=msg.as_string())
            print("Message sent")

# Example data to pass into the function

# Assuming form is an object that has the required vehicle information
# You can call the class like this:

