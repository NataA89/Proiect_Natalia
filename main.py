import datetime
import os
import time
import csv
import mysql.connector

conn=mysql.connector.connect(host="localhost", user="root", password="Calendar1989.", database="curs")
cursor=conn.cursor(buffered=True)
cursor.execute("SELECT * FROM USERS")
rows=cursor.fetchall()

class User():
    def __init__(self,Nume,Prenume,Companie,IdManager):
        self.Nume=Nume
        self.Prenume=Prenume
        self.Companie=Companie
        self.IdManager=IdManager
    def insert_user(self):
        cursor.execute(f"INSERT INTO USERS VALUES(null,'{self.Nume}','{self.Prenume}','{self.Companie}','{self.IdManager}');")
        conn.commit()

conn.close()
cursor.close()

class Fisier():
    def __init__(self,Path):
        self.Path=Path

    def citeste_fisier(self):
        with open(self.Path, 'r') as file:
            text=file.readlines()
            return text
    
    def scrie_fisier(self,outputPath):
        with open(self.Path, 'r') as file:
            text=file.readline()
            while text:
                text=text.replace('\n','')
                with open(outputPath,'a') as f:
                    f.write(f'{text}\n')
                text=file.readline()

class FisierTxt(Fisier):
    def __init__(self,Path):
        super().__init__(Path)

    def citeste_fisier(self):
        return super().citeste_fisier()
    def scrie_fisier(self, outputPath):
        return super().scrie_fisier(outputPath)

class FisierCsv(Fisier):
    def __init__(self,Path):
        super().__init__(Path)
    
    def citeste_fisier(self):
        self.coloane=0
        self.randuri=0
        self.lines=[]
        with open(self.Path,'r') as file:
            reader=csv.reader(file)
            for line in reader:
                self.lines.append(line)
        
    def scrie_fisier(self,outputPath):
        with open(outputPath,"w",newline='') as file:
            writer=csv.writer(file)
            writer.writerows(self.lines)
 

def main():
    while True:
        fisiereVechi = []
        fisiere = os.listdir("proiect/Intrari")
        if len(fisiereVechi) == len(fisiere):
            print("Nu avem fisiere noi.")
        else:
            for fisierNou in fisiere:
                if not fisierNou in fisiereVechi:
                    print(fisierNou)            
        fisiereVechi = fisiere
        time.sleep(5)


