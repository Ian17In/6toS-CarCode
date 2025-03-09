# -*- coding: utf-8 -*-
"""
Created on Thu Mar  6 11:43:00 2025

@author: IAN
"""

import socket
import json

class dataPack:

    def __init__(self,ip:str,port:int):
        self.udpSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.ESP32ip = ip
        self.port = port
        self.data = {}
        
    def getData(self,start:list,end:list,obstacle:list,path:list):
        self.data = {
            "obstaculos": obstacle,
            "inicio": start,
            "final": end,
            "ruta": path
            }
    def createJson(self):
        self.message = json.dumps(self.data)
        print(self.message)
    
    def sendMessage(self):
        self.udpSocket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.udpSocket.sendto(self.message.encode(),(self.ESP32ip,self.port))
        print(f"Paquete enviado: {self.message}")
        
        
        try:
            self.response, _=self.udpSocket.recvfrom(1024)
            print(f'ESP32 dice... {self.response.decode()}')
        except socket.timeout:
            print("Houston we have a problem")
            
        
    def closeSocket(self):
        self.udpSocket.close()


if __name__ == "__main__":
    ip = "192.168.68.122"
    port = 800
    start = [5, 5]  # Coordenada de inicio
    end = [100, 200]  # Coordenada final
    obstacle = [[10, 20], [30, 40], [50, 60]]  # Obstáculos
    path = [[5, 5], [10, 10], [20, 30], [50, 60], [100, 200]]
    # Prueba enviando coordenadas al ESP32
    
    pack = dataPack(ip, port)
    pack.getData(start, end, obstacle, path)
    pack.createJson()
    pack.sendMessage()
    pack.closeSocket()

