# Get every round of game from a mjlog file


import os
import re


class Mjlogtran:
    # mjlog_file is the target mjlog file
    # text stand for the text content of target file
    # rounds is the interval of each round text
    mjlog_file = None
    text = None
    rounds = None

    def __init__(self,path):
        self.rounds = []
        self.mjlog_file = open(path,"r")
        self.text = self.mjlog_file.read()
        self.locate_rounds(self.text)

    # Locate the interval of each round with "<INIT" tag
    def locate_rounds(self,text):
        for i in re.finditer("<INIT",text):
            self.rounds.append(i.span())

    # Write the rounds text into separate txt files
    def writeRounds(self,folder):
        for i in range(len(self.rounds)):
            filename = folder+"/%d.txt"%i
            roundfile = open(filename,"w")
            if i < len(self.rounds) -1 :
                roundfile.write(self.text[self.rounds[i][0]:self.rounds[i+1][0]])
            else:
                roundfile.write((self.text[self.rounds[i][0]:]))

    def reset(self):
        self.rounds = None
        self.text = None
        self.mjlog_file = None
'''
Directory format of data
utils|
      |mjlogs                           |converted
      |[player name directory]     |[player name directory]
      |[mjlogs]                          |[game directory]
                                            |[round files]
'''
def main():
        mjlog_directoris = os.fsencode("./mjlogs/")
        for player in os.listdir(mjlog_directoris):
            folder = mjlog_directoris + os.fsencode(player+b"/")
            new_folder = "./converted/"+ player.decode("utf-8")
            print(folder)
            if not os.path.exists(new_folder):
                os.mkdir(new_folder)

            for game in os.listdir(folder):
                folder_name = "./converted/"+player.decode("utf-8")+"/"+game.decode("utf-8")
                if not os.path.exists(folder_name):
                    os.mkdir(folder_name)
                mjlog = Mjlogtran(folder.decode("utf-8")+"/"+game.decode("utf-8"))
                mjlog.writeRounds(folder_name)
                mjlog.reset()
                print("Done "+folder_name)

main()



