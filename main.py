import datetime
import os
import time
import csv
import mysql.connector
import shutil
from datetime import datetime

conn=mysql.connector.connect(host="localhost", user="root", password="Calendar1989.", database="curs")
cursor=conn.cursor(buffered=True)


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
        self.text=[]
        with open(self.Path,'r') as file:
            reader=csv.reader(file)
            next(reader)
            for row in reader:
                self.text.append(row)
            return self.text    
          
    def scrie_fisier(self,outputPath):
        with open(outputPath,"w",newline='') as file:
            writer=csv.writer(file)
            writer.writerows(self.lines)


import datetime


def main():
    while True:
        fisiereVechi = []
        fisiere = os.listdir("proiect/Intrari")
        if len(fisiereVechi) == len(fisiere):
            print("Nu avem fisiere noi.")
        else:
            for fisierNou in fisiere:
                if not fisierNou in fisiereVechi:
                    type=fisierNou.split(".")[1]
                    if(type=="txt"):
                        fisiertxt=FisierTxt('proiect/Intrari/'+fisierNou)
                        text=fisiertxt.citeste_fisier()
                        for line in text:
                            element=line.split(",")
                            IdPersoana=element[0]
                            Data=element[1]
                            Sens=element[2]
                            NumePoarta=fisierNou.split(".")[0]
                            cursor.execute(f"INSERT INTO ACCESS VALUES('{IdPersoana}','{Data}','{Sens}','{NumePoarta}');")
                            conn.commit()

                    if(type=="csv"):
                        fisiercsv=FisierCsv('proiect/Intrari/'+fisierNou)
                        text=fisiercsv.citeste_fisier()
                        for element in text:
                            IdPersoana=element[0]
                            Data=element[1]
                            Sens=element[2]
                            NumePoarta=fisierNou.split(".")[0]
                            cursor.execute(f"INSERT INTO ACCESS VALUES('{IdPersoana}','{Data}','{Sens}','{NumePoarta}');")
                            conn.commit()
                source = 'proiect/Intrari/'+fisierNou 
                backup = 'proiect/Backup_intrari/'  
                data=datetime.datetime.now().date()
                nume_fisier=f"{fisierNou}_{data}"
                destination=os.path.join(backup,nume_fisier)
                shutil.move(source, destination)       
        fisiereVechi = fisiere
        time.sleep(5)

# main()
     




