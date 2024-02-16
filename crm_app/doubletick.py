import requests
import json


def whatsapp_signup_mes(firstname, lastname, email, password, mobile, user_type):
    # Convert sets to lists or strings
    firstname = str(firstname) if firstname else ""
    lastname = str(lastname) if lastname else ""
    email = str(email)
    password = str(password)
    user_type = str(user_type)
    if user_type == "3":
        user_type_name = "Employee"
    elif user_type == "4":
        user_type_name = "Agent"
    elif user_type == "5":
        user_type_name = "OutSource Agent"
    elif user_type == "2":
        user_type_name = "Admin"
    else:
        user_type_name = "None"

    url = "https://public.doubletick.io/whatsapp/message/template"

    payload = {
        "messages": [
            {
                "content": {
                    "language": "en",
                    "templateData": {
                        "header": {
                            "type": "TEXT",
                            "placeholder": "body",
                            "mediaUrl": "kjhgfdxfcj",
                            "filename": "kjhgcnhj",
                        },
                        "body": {
                            "placeholders": [
                                firstname,
                                lastname,
                                user_type_name,
                                email,
                                password,
                            ]
                        },
                    },
                    "templateName": "welcome_sky",
                },
                "from": "+918800517859",
                "to": "+91" + mobile,
            }
        ]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "key_IqTwUC2O8n",
    }

    response = requests.post(url, json=payload, headers=headers)


def product_add_mes(title, country, contact):
    title = str(title) if title else ""
    country = str(country) if country else ""

    url = "https://public.doubletick.io/whatsapp/message/template"

    payload = {
        "messages": [
            {
                "content": {
                    "language": "en",
                    "templateData": {
                        "header": {
                            "type": "TEXT",
                            "placeholder": "body",
                            "mediaUrl": "kjhgfdxfcj",
                            "filename": "kjhgcnhj",
                        },
                        "body": {
                            "placeholders": [
                                title,
                                country,
                            ]
                        },
                    },
                    "templateName": "product_v2",
                },
                "from": "+918800517859",
                "to": "+91" + contact,
            }
        ]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "Authorization": "key_IqTwUC2O8n",
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response)
