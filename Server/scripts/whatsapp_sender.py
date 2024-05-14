from twilio.rest import Client

def send_whatsapp_message(account_sid: str, auth_token: str, from_whatsapp_number: str, to_whatsapp_number: str, message: str):
    client = Client(account_sid, auth_token)
    try:
        message = client.messages.create(
            body=message,
            from_=f'whatsapp:{from_whatsapp_number}',
            to=f'whatsapp:{to_whatsapp_number}'
        )
        print(f'Mensaje enviado con SID: {message.sid}')
    except Exception as e:
        print(f'Error al enviar el mensaje: {e}')
        raise e
