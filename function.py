import yagmail

def send_email(mesaj):
    smtp_server_domain_name = "smtp.gmail.com"
    sender_mail = "natalia.angiu@gmail.com"
    password = "rueyyhbsjgpezmqi"

    yag = yagmail.SMTP(sender_mail, password)

    subject = "Ore lucrate"
    destinatar = "diaconunatalia@yahoo.com"

    yag.send(
        to=destinatar,
        subject=subject,
        contents=mesaj
    )

    print('Emailul a fost trimis cu succes!')
