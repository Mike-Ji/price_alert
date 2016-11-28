from amazon.api import AmazonAPI
from twilio.rest import TwilioRestClient
import smtplib

amazon_api = AmazonAPI("[your Amazon access key ID]",
                       "[your Amazon secret access key]",
                       "[your Amazon Associate ID (tag)]",
                       "[your region]")
product = amazon_api.lookup(ItemId = '[your Amazon item ID]')
product_title = product.title
price_current = product.price_and_currency[0]
price_expected = 100 # change to your expected price


def message(msg):
    account_sid = "[your Twilio Account SID]"
    auth_token = "[your Twilio Auth Token]"
    client = TwilioRestClient(account_sid, auth_token)
    message = client.messages.create(body=msg,
                                     to="+[your phone number]",
                                     frm="+[your Twilio number]")


def send_email(title, price):
    gmail_user = "[your Gmail username]"
    gmail_pswd = "[ypur Gmail password]"
    From = "[sender email address]"
    To = ["[receiver email address]"]
    Subject = "Amazon Price Drop Alert"
    Text = "The price of the product you choose on Amazon has dropped!"
    
    message = "From: %(From)s\n To: %(To)s\n Subject: %(Subject)s\n"

    try:
        server = smtplib.SMTP("smtp.gmail.com", 465) # port 465 or 587
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pswd)
        server.sendmail(From, To, message)
        server.quit()
        print("successfully sent the mail!")
    except:
        print("failed to send the mail.")


if (price_current <= price_expected):
    message(product_title)
    send_email(product_title, price_current)
