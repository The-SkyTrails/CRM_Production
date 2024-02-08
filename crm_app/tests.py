import requests

# Define your API key and other parameters
api_key = "key_IqTwUC2O8n"
number = "+919973884727"
url = "https://public.doubletick.io/whatsapp/message/template"

# Define the message payload
payload = {
    "api_key": api_key,
    "number": number,
    "template": {"type": "text", "text": "Your message goes here"},
}

# Send the POST request to the API
response = requests.post(url, json=payload)

# Check the response status
if response.status_code == 200:
    print("Message sent successfully!")
    print(response.json())  # Optional: Print response JSON
else:
    print("Failed to send message:", response.text)
