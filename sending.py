from twilio.rest import Client

PHONE_NUMBER = "+17208216952"
MY_NUMBER = "+919562614075"
api_endpoint = "https://api.openweathermap.org/data/2.5/onecall"
account_sid = "AC37d8fd1a7123a4a11333e4646ab7954f"
auth_token = "861c4bfedfc11e15007dfd22f66db153"


def sending_password(website, email, password):
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
            body=f"\nPassword Details\nWebsite: {website}\nEmail: {email}\nPassword: {password}",
            from_=PHONE_NUMBER,
            to=MY_NUMBER
        )
    print(message.status)
