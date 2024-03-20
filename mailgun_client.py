import requests

def send_simple_message():
	return requests.post(
		"https://api.mailgun.net/v3/sandbox2d283f7ff66e457c89e0ef095c932b6a.mailgun.org/messages",
		auth=("api", "<PRIVATE_API_KEY>"),
		data={"from": "Mailgun Sandbox <postmaster@sandbox2d283f7ff66e457c89e0ef095c932b6a.mailgun.org>",
			"to": "Uzair Qarni <uzair@hellogepeto.com>",
			"subject": "Hello Uzair Qarni",
			"text": "Congratulations Uzair Qarni, you just sent an email with Mailgun! You are truly awesome!"})

# You can see a record of this email in your logs: https://app.mailgun.com/app/logs.

# You can send up to 300 emails/day from this sandbox server.
# Next, you should add your own domain so you can send 10000 emails/month for free.
