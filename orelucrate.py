from datetime import datetime
import mysql.connector
import smtplib, ssl
import pytz
import csv
from function import send_email


# flag=0
# while True:
#     currentTime=datetime.datetime.now().time()
#     if currentTime.hour>=20:
#         if flag==0:
#             ore_lucrate()
#             flag+=1
#     else:
#         flag=0
#     time.sleep(5)

def calculeaza_ore_lucrate():
    # Conectarea la baza de date MySQL
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Calendar1989.",
        database="curs"
    )
    cursor = conn.cursor()

    # Extragem toate inregistrarile din tabelul "access"
    cursor.execute("SELECT * FROM access")
    date_acces = cursor.fetchall()

    angajati_detalii = {}

    for inregistrare in date_acces:
        id_angajat = inregistrare[0]
        timestamp_str = inregistrare[1]
        directie = inregistrare[2].strip().replace(';', '')  # Eliminam caracterele nedorite, cum ar fi '\n' și ';'
        timestamp = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        
        if id_angajat not in angajati_detalii:
            angajati_detalii[id_angajat] = {'intrare': None, 'iesire': None}
            
        if directie == 'in':
            angajati_detalii[id_angajat]['intrare'] = timestamp
            
        elif directie == 'out':
            angajati_detalii[id_angajat]['iesire'] = timestamp

    # Inchidem conexiunea cu baza de date
    cursor.close()
    conn.close()

    # Calculam durata totala lucrată pentru fiecare angajat
    angajati_ore = {}
    for id_angajat, detalii in angajati_detalii.items():
        timp_intrare = detalii['intrare']
        timp_iesire = detalii['iesire']

        if timp_intrare and timp_iesire:
            durata_lucrata = (timp_iesire - timp_intrare).total_seconds() / 3600
            angajati_ore[id_angajat] = durata_lucrata

    return angajati_ore

def main():
    # Calculam durata totala lucrată pentru fiecare angajat
    angajati_ore = calculeaza_ore_lucrate()

    # Afisam doar angajatii cu mai putin de 8 ore lucrate
    for id_angajat, ore_lucrate in angajati_ore.items():
        if ore_lucrate < 8:
            mesaj=f"Angajatul cu ID-ul {id_angajat} a lucrat astazi doar {ore_lucrate:.2f} ore."
            send_email(mesaj)

if __name__ == "__main__":
    main()

