import mysql.connector
from flask import Flask, jsonify, request

conn=mysql.connector.connect(host="localhost", user="root", password="Calendar1989.", database="curs")
cursor=conn.cursor(buffered=True)

app=Flask(__name__)

@app.route('/persoana',methods=['POST'])
def createPersoana():
    data=request.get_json()
    Nume=data['Nume']
    Prenume=data['Prenume']
    Companie=data['Companie']
    IdManager=data['IdManager']
    cursor.execute(f"INSERT INTO USERS VALUES(null,'{Nume}','{Prenume}','{Companie}','{IdManager}')")
    conn.commit()
    # conn.close()
    # cursor.close()
    return "Persoana inserata "+str(cursor.lastrowid)
    

if __name__ == '__main__':
    app.run(debug=True)