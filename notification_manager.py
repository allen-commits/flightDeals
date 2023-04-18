import smtplib
import os


class NotificationManager:
    def __init__(self):
        self.MY_GMAIL_EMAIL = os.environ['MY_GMAIL_EMAIL']
        self.MY_GMAIL_EMAIL_PASSWORD = os.environ['MY_GMAIL_EMAIL_PASSWORD']

    def send_email(self, api_price,
                   api_dep_city_name,
                   api_dep_iata_code,
                   api_arr_city_name,
                   api_arr_iata_code,
                   api_outbound_date,
                   api_inbound_date):
        """this sends an email to my dummy email, alerting me of a new deal"""
        with  smtplib.SMTP("smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=self.MY_GMAIL_EMAIL, password=self.MY_GMAIL_EMAIL_PASSWORD)
            connection.sendmail(from_addr=self.MY_GMAIL_EMAIL,
                                to_addrs="SAMPLE@gmail.com",
                                msg=f"Subject:Major deal alert!!\n\n Low price alert! Only {api_price} "
                                    f"to fly from {api_dep_city_name}-{api_dep_iata_code} to {api_arr_city_name}-"
                                    f"{api_arr_iata_code}, from {api_outbound_date} to {api_inbound_date}")
