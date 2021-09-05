from datetime import datetime
from datetime import timedelta

class DateTimeHandler:
    def DateTimeMinusOneMinute(self, pdate_yyyymmdd_hhmm):
        mydt = datetime.strptime(pdate_yyyymmdd_hhmm, "%Y%m%d %H:%M")
        a = timedelta(minutes = 1)
        new_time = mydt - a
        return new_time.strftime("%Y%m%d %H:%M")
    def DateTimeMinusOneDay(self, pdate_yyyymmdd_hhmm):
        mydt = datetime.strptime(pdate_yyyymmdd_hhmm, "%Y%m%d %H:%M")
        a = timedelta(days = 1)
        new_time = mydt - a
        return new_time.strftime("%Y%m%d %H:%M")

class Player:
    def __init__(self):
        self.UserName = ""
    def PlayerAsCsvLine(self):
        return self.UserName

class PlayerList:
    def __init__(self):
        self.Players = []
    def LoadFromFile(self, infile):
        self.Players.clear()
        file1 = open(infile, 'r')
        Lines = file1.readlines()
        file1.close()
        for line in Lines:
            s = line.replace("\n","")
            item = Player()
            a = s.split(",")
            item.UserName = a[0]
            self.Players.append(item)
            del item
    def SaveToFile(self, outfile):
        file2 = open(outfile, 'w')
        for p in self.Players:
            file2.write(p.PlayerAsCsvLine() + "\n")
        file2.close()



class Game:
    def __init__(self):
        self.GameID = ""
        self.GameURL = ""
        self.WhitePlayerName = ""
        self.BlackPlayerName = ""
        self.started_yyyymmdd_hhmm = "19000101 00:00"
        self.ended_yyyymmdd_hhmm = "99991231 23:59"
        self.GameResult = 0 # 1 = White wins, -1 = Black wins, 0 = Draw
        self.GameResultValid = False # False if this game is for whatever reason not eligible for rating processing
    def GameAsCsvLine(self):
        s = (self.GameID + "," + self.GameURL + "," +
                       self.WhitePlayerName + "," + self.BlackPlayerName + "," +
                       self.started_yyyymmdd_hhmm + "," + self.ended_yyyymmdd_hhmm + ","
                       + str(self.GameResult))
        if self.GameResultValid == True:
            s = s + ",yes"
        else:
            s = s + ",no"
        
        return s
class GameList:
    def __init__(self):
        self.Games = []
    def LoadFromFile(self, infile):
        self.Games.clear()
        file1 = open(infile, 'r')
        Lines = file1.readlines()
        file1.close()
        for line in Lines:
            s = line.replace("\n","")
            item = Game()
            a = s.split(",")
            item.GameID = a[0]
            item.GameURL = a[1]
            item.WhitePlayerName = a[2]
            item.BlackPlayerName = a[3]
            item.started_yyyymmdd_hhmm = a[4]
            item.ended_yyyymmdd_hhmm = a[5]
            item.GameResult = int(a[6])
            
            if a[7].upper() == "YES" or a[7].upper() == "TRUE":
                item.GameResultValid = True
            else:
                item.GameResultValid = False

            self.Games.append(item)
            del item
    def SaveToFile(self, outfile):
        file2 = open(outfile, 'w')
        for g in self.Games:
            file2.write(g.GameAsCsvLine() + "\n")
        file2.close()
    def OrderByDate(self):
        self.Games.sort(key=lambda x: (x.ended_yyyymmdd_hhmm, x.started_yyyymmdd_hhmm))
class RatingRecord:
    def __init__(self):
        self.PlayerName = ""
        self.Rating = 1200
        self.validfrom_yyyymmdd_hhmm = "19000101 00:00"
        self.validtill_yyyymmdd_hhmm = "99991231 23:59"
    def RatingRecordAsCsvLine(self):
        return (self.PlayerName + "," + str(self.Rating) + "," +
                self.validfrom_yyyymmdd_hhmm + "," + self.validtill_yyyymmdd_hhmm)
class RatingRecordList:
    def __init__(self):
        self.RatingRecords = []
    def ModifyRating(self, pPlayerName, pRating, pdate_yyyymmdd_hhmm):
        for r in self.RatingRecords:
            if (r.PlayerName == pPlayerName and r.validfrom_yyyymmdd_hhmm <= pdate_yyyymmdd_hhmm
                    and r.validtill_yyyymmdd_hhmm >= pdate_yyyymmdd_hhmm):
                a = DateTimeHandler()
                r.validtill_yyyymmdd_hhmm = a.DateTimeMinusOneMinute(pdate_yyyymmdd_hhmm)
                del a
        item = RatingRecord()
        item.PlayerName = pPlayerName
        item.Rating = pRating
        item.validfrom_yyyymmdd_hhmm = pdate_yyyymmdd_hhmm
        self.RatingRecords.append(item)
        del item
    def SaveToFile(self, outfile):
        file2 = open(outfile, 'w')
        for r in self.RatingRecords:
            file2.write(r.RatingRecordAsCsvLine() + "\n")
        file2.close()
    def OrderByPlayerDate(self):
        self.RatingRecords.sort(key=lambda x: (x.PlayerName, x.validfrom_yyyymmdd_hhmm))

class RatingImpactItem:
    def __init__(self):
        self.RatingDifferenceFrom = 0
        self.RatingDifferenceTill = 0
        self.HigherRatedWin = 0
        self.HigherRatedDraw = 0
        self.HigherRatedLoss = 0
        self.LowerRatedWin = 0
        self.LowerRatedDraw = 0
        self.LowerRatedLoss = 0
    def RatingImpactItemAsCsvLine(self):
        s = (str(self.RatingDifferenceFrom) + "," + str(self.RatingDifferenceTill) + "," +
             str(self.HigherRatedWin) + "," + str(self.HigherRatedDraw) + "," +
             str(self.HigherRatedLoss) + "," + str(self.LowerRatedWin) + "," +
             str(self.LowerRatedDraw) + "," + str(self.LowerRatedLoss))
        return s

class RatingImpactTable:
    def __init__(self):
        self.RatingImpactItems = []
    def LoadFromFile(self, infile):
        self.RatingImpactItems.clear()
        file1 = open(infile, 'r')
        Lines = file1.readlines()
        file1.close()
        for line in Lines:
            s = line.replace("\n","")
            item = RatingImpactItem()
            a = s.split(",")
            item.RatingDifferenceFrom = int(a[0])
            item.RatingDifferenceTill = int(a[1])
            item.HigherRatedWin = int(a[2])
            item.HigherRatedDraw = int(a[3])
            item.HigherRatedLoss = int(a[4])
            item.LowerRatedWin = int(a[5])
            item.LowerRatedDraw = int(a[6])
            item.LowerRatedLoss = int(a[7])
            self.RatingImpactItems.append(item)
            del item
    def SaveToFile(self, outfile):
        file2 = open(outfile, 'w')
        for r in self.RatingImpactItems:
            file2.write(r.RatingImpactItemAsCsvLine() + "\n")
        file2.close()
    def OrderByRatingDifferenceFrom(self):
        self.RatingImpactItems.sort(key=lambda x: x.RatingDifferenceFrom)
class RatingFloor:
    def __init__(self):
        self.InitialRating = 0
    def LoadFromFile(self, infile):
        file1 = open(infile, 'r')
        Lines = file1.readlines()
        file1.close()
        self.InitialRating = int(Lines[0])
    def SaveToFile(self, outfile):
        file2 = open(outfile, 'w')
        file2.write(str(self.InitialRating) + "\n")
        file2.close()
