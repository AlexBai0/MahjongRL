from mahjong.shanten import Shanten
import numpy as np
import os
import re

class MjlogToCsv:
    def __init__(self,mjlog_file):
        self.mjlog_file = mjlog_file
        self.mjlog = open(self.mjlog_file,"r")
        self.log = self.mjlog.read()
        self.shanten = Shanten()

    # Find init tags to mark the start of every game
    def getTagInit(self,log):
        inits = []
        for t in (re.finditer("<INIT",log)):
            inits.append(t.span())
        return inits

    def initRound(self):
        hand = np.zeros((4, 34))
        discards = []

        return hand, discards

    def retrieveHand(self, text):
        hands = np.zeros((4, 34))
        for j in range(4):
            Hand = re.findall('hai' + str(j) + '="(.+?)"', text)
            Hand = [kyoku.split(",") for kyoku in Hand]
            Hand = [[self.haiConverter(int(tile)) for tile in kyoku] for kyoku in Hand]
            for k in range(len(Hand[0])):
                hands[j][int(Hand[0][k])] += 1
        return hands

    # Get tsumos of players from given text
    def retrieveTsumo(self, text):
        tsumos = []
        tsumos.append([self.haiConverter(int(tile[2:])) for tile in re.findall(r'<T\d+', text)])
        tsumos.append([self.haiConverter(int(tile[2:])) for tile in re.findall(r'<U\d+', text)])
        tsumos.append([self.haiConverter(int(tile[2:])) for tile in re.findall(r'<V\d+', text)])
        tsumos.append([self.haiConverter(int(tile[2:])) for tile in re.findall(r'<W\d+', text)])
        return tsumos

    # Get discards of players from given text
    def retrieveDiscards(self, text):
        discards = []
        discards.append([self.haiConverter(int(tile[2:])) for tile in re.findall(r'<D\d+', text)])
        discards.append([self.haiConverter(int(tile[2:])) for tile in re.findall(r'<E\d+', text)])
        discards.append([self.haiConverter(int(tile[2:])) for tile in re.findall(r'<F\d+', text)])
        discards.append([self.haiConverter(int(tile[2:])) for tile in re.findall(r'<G\d+', text)])
        return discards


    # Get text for a round_num round
    def getRoundText(self, text, round_num, inits):
        if (round_num < len(inits) - 1):
            return text[inits[round_num][1]:inits[round_num + 1][0]]
        else:
            return text[inits[round_num][1]:]

    # Writes info in a specific way into csv
    # Shanten | Discards
    def writeToCSV(self, hands, tsumos, discards, csvfile):
        for player in range(4):
            discard = []
            smaller = len(tsumos[player])
            if (len(discards[player]) < len(tsumos[player])):
                smaller = len(discards[player])
            for k in range(smaller):
                hands[player][tsumos[player][k]] += 1
                hands[player][discards[player][k]] -= 1
                discard.append(discards[player][k])
                target = self.shanten.calculate_shanten(hands[player])
                csvfile.write("%d" % target)
                for m in range(len(discard)):
                    csvfile.write(",%s" % (discard[m]))
                csvfile.write("\n")

    #  converts the mjlog into CSV file with specific format under /csvs/
    # Csv file that is less than 10 bytes will be deleted here
    def convertToCSV(self, foldername):
        hand, discards = self.initializeRound()
        filename = "csvs/%s.csv" % (foldername)
        csvfile = open(filename, "w")
        inits = self.getInitTagPos(self.text)

        for i in range(len(inits)):
            discards = []
            text = self.getRoundText(self.text, i, inits)
            if (re.search('<N', text)):
                # print("Naki, Not going to consider")
                continue

            hands = self.retrieveHand(text)
            tsumos = self.retrieveTsumo(text)
            discards = self.retrieveDiscards(text)
            self.writeToCSV(hands, tsumos, discards, csvfile)
        csvfile.flush()
        csvfile.close()
        if (os.stat(filename).st_size < 10):
            os.remove(filename)
            print("Insignificant size, deleted")


    # Converts 136 into 34 tile types
    def haiConverter(self, tile):
        tile = tile / 4
        return int(tile)
