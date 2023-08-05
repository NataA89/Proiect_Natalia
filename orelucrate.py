from datetime import datetime
import mysql.connector
from mail import send_mail
import time



def calculeaza_ore_lucrate():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Calendar1989.",
        database="curs"
    )
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM access
    """)
    date_acces = cursor.fetchall()

    cursor.execute("""
        SELECT ID, IdManager, MailManager
        FROM users
    """)
    users_data = cursor.fetchall()

    angajati_detalii = {}

    for inregistrare in date_acces:
        id_angajat = inregistrare[0]
        data_ora = inregistrare[1]
        directie = inregistrare[2].strip().replace(';', '')  
        timestamp = datetime.strptime(data_ora, '%Y-%m-%dT%H:%M:%S.%fZ')

        if id_angajat not in angajati_detalii:
            angajati_detalii[id_angajat] = {'intrare': None, 'iesire': None, 'ore_lucrate': 0}  
            
        if directie == 'in':
            angajati_detalii[id_angajat]['intrare'] = timestamp
            
        elif directie == 'out':
            angajati_detalii[id_angajat]['iesire'] = timestamp

        # Calculăm durata lucrată pentru fiecare angajat și o adăugăm în dicționarul angajati_detalii
        if angajati_detalii[id_angajat]['intrare'] and angajati_detalii[id_angajat]['iesire']:
            durata_lucrata = (angajati_detalii[id_angajat]['iesire'] - angajati_detalii[id_angajat]['intrare']).total_seconds() / 3600
            angajati_detalii[id_angajat]['ore_lucrate'] += durata_lucrata

    # Asociem datele din tabelul "users" pe baza coloanei comune "ID"
    for inregistrare in users_data:
        id_angajat = inregistrare[0]
        id_manager = inregistrare[1]
        mail_manager = inregistrare[2]

        if id_angajat in angajati_detalii:

            angajati_detalii[id_angajat]['IdManager'] = id_manager
            angajati_detalii[id_angajat]['MailManager'] = mail_manager

    cursor.close()
    conn.close()

    # Angajați cu mai puțin de 8 ore lucrate
    angajati_ore = {}
    for id_angajat, detalii in angajati_detalii.items():
        if 'MailManager' in detalii and detalii['ore_lucrate'] < 8:
            angajati_ore[id_angajat] = {'ore_lucrate': detalii['ore_lucrate'], 'MailManager': detalii['MailManager']}

    return angajati_ore

def main():
    flag = 0
    while True:
        oraCurenta = datetime.now().time()
        ora = oraCurenta.hour
        if ora >= 20:
            if flag == 0:
                angajati_ore = calculeaza_ore_lucrate()

                # Trimitem e-mail-uri către angajații cu mai puțin de 8 ore lucrate
                for id_angajat, detalii in angajati_ore.items():
                    ore_lucrate = detalii['ore_lucrate']
                    mail_manager = detalii['MailManager']
                    if ore_lucrate < 8:
                        mesaj = f"Angajatul cu ID-ul {id_angajat} a lucrat astăzi doar {ore_lucrate:.2f} ore."
                        send_mail(mail_manager, "Raport ore lucrate", mesaj)

                flag += 1
        else:
            flag = 0
        time.sleep(5)
        
if __name__ == "__main__":
    main()