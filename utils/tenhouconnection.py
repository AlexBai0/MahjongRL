import socket
from urllib.parse import quote
import re
import numpy as np
from time import sleep
import random
import tensorflow as tf
from threading import Thread
import _thread


def convert(t136):
    return int(t136/4)

class Connection:

    def __init__(self,
                 model,
                 host='133.242.10.78',
                 port = 10080,
                 userid = 'NoName'
                 ):
        self.host = host
        self.port = port
        self.user = userid
        self.ingame = True
        self.wake_thread = None
        self.model = model
        self.sess = tf.Session()
        self.sess.run(tf.global_variables_initializer())

    def connect(self):
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.socket.connect((self.host,self.port))
        print('Connected')

    def play(self):
        # Join table
        self.halt()
        self.send('<JOIN t="0,1" />')
        self.searchingTable = True
        print('Looking for game')
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
                    seat = re.search('oya="(.+?)"',m).group(1)
                    # game_id = re.search('log="(.+?)"',m).group(1)
                    # link = 'http://tenhou.net/0/?log='+game_id+'&tw='+seat
                    seat = int(seat)
                    self.ingame = True
                    print('IN TABLE')

                if 'LN' in m:
                    self.send('<PXR V="1" />')

        # if self.searchingTable:
        #     print('No game found')

        while self.ingame:
            self.halt()
            message = self.receive()
            for m in message:
                if '<INIT' in m:
                    # dealer = int(re.search('dealer="(.+?)"',m).group(1))
                    hand = re.search('hai="(.+?)"',m).group(1)
                    hand = [int(t) for t in hand.split(',')]
                    self.hand136 = hand
                    hand = self.handconvert(hand)   # Input parameters
                    self.hand34 = hand
                    print('Hand:',hand)
                if '<T' in m:
                    if 't="16"' in m or 't="48"' in m:  # win
                        self.halt()
                        self.send('<N type="7" />')
                        print('win')
                    if 't="64"' in m:   # game is draw
                        self.halt()
                        self.send('<N type="9" />')
                        print('draw')
                    else:
                        tile = int(re.match(r'^<[tefgEFGTUVWD]+\d*',m).group()[2:])
                        self.draw(tile)
                    self.discarding = self.discard()  # TODO
                    # self.discarding = self.discard()
                    self.halt()
                    self.send('<D p="{}"/>'.format(self.discarding))
                    print('Discard: ',self.discarding)
                if '<AGARI' in m or '<RYUUKYOKU' in m:
                    self.halt()
                    self.send('<NEXTREADY />')
                win_suggestions = [
                    't="8"', 't="9"', 't="10"', 't="11"', 't="12"', 't="13"', 't="15"'
                ]
                if any(i in m for i in win_suggestions):
                    self.halt()
                    self.send('<N type="6" />')
                    print('Win!')
                if '<PROF' in m:
                    self.ingame = False
                call_suggestions=[
                    't="1"','t="2"','t="3"','t="4"','t="5"','t="7"'
                ]
                if any(i in m for i in call_suggestions):
                    self.halt()
                    self.send('<N />')
                    print('Ignore')
        self.end()



    def wake(self):
        def ping():
            while self.ingame:
                self.send('<Z />')
                for i in range(30):
                    if self.ingame:
                        sleep(0.5)
        self.wake_thread = Thread(target=ping)
        self.wake_thread.start()

    def authencate(self):
        self.send('<HELO name="{}" tid="f0" sx="M" />'.format(quote(self.user)))
        messages = self.receive()
        auth_message = messages[0]
        print(auth_message)
        if not auth_message:
            return False

        # we reconnected to the game
        if '<GO' in auth_message:
            self.reconnected_messages = messages
            return True
        auth_string= re.search('auth="(.+?)"',auth_message).group(1)

        print(auth_string)
        if not auth_string:
            return False

        auth_token = self.generate_auth_token(auth_string)
        print(auth_token)

        self.send('<AUTH val="{}"/>'.format(auth_token))
        self.send('<PXR V="1" />')

        # sometimes tenhou send an empty tag after authentication (in tournament mode)
        # and bot thinks that he was not auth
        # to prevent it lets wait a little bit
        # and lets read a group of tags
        continue_reading = True
        counter = 0
        authenticated = False
        while continue_reading:
            messages = self.receive()
            for message in messages:
                if '<LN' in message:
                    authenticated = True
                    continue_reading = False

            counter += 1
            # to avoid infinity loop
            if counter > 10:
                continue_reading = False

        if authenticated:
            self.wake()

            return True
        else:
            return False


    def generate_auth_token(self, auth_string):
        translation_table = [63006, 9570, 49216, 45888, 9822, 23121, 59830, 51114, 54831, 4189, 580, 5203, 42174, 59972,
                             55457, 59009, 59347, 64456, 8673, 52710, 49975, 2006, 62677, 3463, 17754, 5357]

        parts = auth_string.split('-')
        if len(parts) != 2:
            return False

        first_part = parts[0]
        second_part = parts[1]
        if len(first_part) != 8 or len(second_part) != 8:
            return False

        table_index = int('2' + first_part[2:8]) % (12 - int(first_part[7:8])) * 2

        a = translation_table[table_index] ^ int(second_part[0:4], 16)
        b = translation_table[table_index + 1] ^ int(second_part[4:8], 16)

        postfix = format(a, '2x') + format(b, '2x')

        result = first_part + '-' + postfix

        return result

    def end(self):
        self.ingame=False
        self.connected = False
        self.send('<BYE />')
        print('End game')

    def decision(self):
        para = self.hand34.reshape(1,34)
        actions = self.sess.run(self.model.q_nn,feed_dict={self.model.state:para})
        return np.argmax(actions)

    def discard(self):
        dis34 = self.decision()
        todis = [dis34*4+j for j in range(4)]
        dis = random.choice(self.hand136)
        for t in self.hand136:
            if any(t == to for to in todis):
                dis = t
        self.hand34[int(dis/4)] -= 1
        self.hand136.remove(dis)
        return dis

    def draw(self,tile):
        self.hand136.append(tile)
        self.hand34[convert(tile)]+=1

    def handconvert(self,hand):
        hand = [convert(t) for t in hand]
        hand_new = np.zeros(34)
        for i in hand:
            hand_new[i] += 1
        return hand_new

    def send(self,m):
        m += '\0'
        self.socket.sendall(m.encode())
        print('SEND: ',m)

    def receive(self):
        m = self.socket.recv(2048).decode('utf-8')
        m = m.split('\x00')[0:-1]
        for mes in m:
            if mes:
                print('Receive: ',mes)
        return m

    def halt(self):
        sleep(random.randint(1,3))