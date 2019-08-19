import socket
from urllib.parse import quote
import re
from time import sleep
import random
class Connection:
    def __init__(self,
                 host='133.242.10.78',
                 port = 10080,
                 userid = 'NoName',
                 ):
        self.host = host
        self.port = port
        self.user = userid

    def connect(self):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.connect((self.host,self.port))

    def play(self):
        # Join table
        self.send('<JOIN t="1" />')
        self.searchingTable = True
        while self.searchingTable:
            self.halt()
            message = self.receive()
            for m in message:
                if 'REJOIN' in m:
                    self.send('<JOIN t="1,r" />')
                if '<GO' in m:
                    self.halt()
                    self.send('<GOK />')
                    self.send('<NEXTREADY />')
                if 'TAIKYOKU' in m:
                    # Entering table
                    self.searchingTable = False
                    seat = re.search('oya="(.+?)',m).group(1)
                    game_id = re.search('log="(.+?)',m).group(1)
                    link = 'http://tenhou.net/0/?log='+game_id+'&tw='+seat
                    seat = int(seat)
                if 'UN' in m:
                    self
                    #TODO
                if 'LN' in m:
                    self.send('<PXR V="1" />')

        # if self.searchingTable:
        #     print('No game found')



    def send(self,m):
        m += '\0'
        self.socket.sendall(m.encode())

    def receive(self):
        m = self.socket.recv(2048).decode('utf-8')
        m = m.split('\x00')[0:-1]
        return m

    def halt(self):
        sleep(random.randint(1,3))