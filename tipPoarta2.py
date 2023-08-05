from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Calendar1989.",
    database="curs"
)

cursor = conn.cursor()

def inserare_date_in_baza(data, sens, id_persoana, id_poarta):
    try:
        query = "INSERT INTO access (Data, Sens, IdPersoana, IdPoarta) VALUES (%s, %s, %s, %s)"
        values = (data, sens, id_persoana, id_poarta)

        cursor.execute(query, values)
        conn.commit()

        return True

    except mysql.connector.Error as error:
        print("Eroare la inserarea datelor:", error)
        return False

@app.route('/salvare_date', methods=['POST'])
def salvare_date():
    try:
        data = request.json['Data']
        sens = request.json['Sens']
        id_persoana = request.json['IdPersoana']
        id_poarta = request.json['IdPoarta']

        if inserare_date_in_baza(data, sens, id_persoana, id_poarta):
            return jsonify({"message": "Date salvate cu succes!"}), 201
        else:
            return jsonify({"error": "Eroare!"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)