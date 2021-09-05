from datamodelclasses import DateTimeHandler, RatingFloor, RatingRecordList
from datamodelclasses import Player, RatingFloor
from datamodelclasses import PlayerList
from datamodelclasses import Game
from datamodelclasses import GameList, RatingImpactTable, RatingImpactItem

def DetermineNewRatings(poldratingwhite, poldratingblack, pGameResult):
    ratingdifference = 0
    newratingwhite = 0
    newratingblack = 0

    rf = MyRatingFloor.InitialRating
    minratingwhite = poldratingwhite - ((poldratingwhite - rf) // 2)
    minratingblack = poldratingblack - ((poldratingblack - rf) // 2)

    if poldratingwhite >= poldratingblack:
        ratingdifference = poldratingwhite - poldratingblack
    else:
        ratingdifference = poldratingblack - poldratingwhite

    for item in MyRatingImpactTable.RatingImpactItems:
        if item.RatingDifferenceFrom <= ratingdifference and item.RatingDifferenceTill >= ratingdifference:
            myitem = item

    if pGameResult == 1:
        if poldratingwhite >= poldratingblack:
            newratingwhite = poldratingwhite + myitem.HigherRatedWin
            newratingblack = poldratingblack + myitem.LowerRatedLoss
        else:
            newratingwhite = poldratingwhite + myitem.LowerRatedWin
            newratingblack = poldratingblack + myitem.HigherRatedLoss
    elif pGameResult == 0:
        if poldratingwhite >= poldratingblack:
            newratingwhite = poldratingwhite + myitem.HigherRatedDraw
            newratingblack = poldratingblack + myitem.LowerRatedDraw
        else:
            newratingwhite = poldratingwhite + myitem.LowerRatedDraw
            newratingblack = poldratingblack + myitem.HigherRatedDraw
    elif pGameResult == -1:
        if poldratingwhite >= poldratingblack:
            newratingwhite = poldratingwhite + myitem.HigherRatedLoss
            newratingblack = poldratingblack + myitem.LowerRatedWin
        else:
            newratingwhite = poldratingwhite + myitem.LowerRatedLoss
            newratingblack = poldratingblack + myitem.HigherRatedWin

    if newratingwhite < minratingwhite:
        newratingwhite = minratingwhite
    if newratingblack < minratingblack:
        newratingblack = minratingblack

    return (newratingwhite, newratingblack)

def ProcessGame(pWhitePlayerName, pBlackPlayerName, pended_yyyymmdd_hhmm, pGameResult):
    rb = 0
    rw = 0

    for r in MyRatingRecordList.RatingRecords:
        if (r.PlayerName == pWhitePlayerName and r.validfrom_yyyymmdd_hhmm <= pended_yyyymmdd_hhmm
                                             and r.validtill_yyyymmdd_hhmm >= pended_yyyymmdd_hhmm):
            rw = r.Rating
    for r in MyRatingRecordList.RatingRecords:
        if (r.PlayerName == pBlackPlayerName and r.validfrom_yyyymmdd_hhmm <= pended_yyyymmdd_hhmm
                                             and r.validtill_yyyymmdd_hhmm >= pended_yyyymmdd_hhmm):
            rb = r.Rating


    a = DetermineNewRatings(rw, rb, pGameResult)

    if rw != a[0]:
        rw = a[0]
        MyRatingRecordList.ModifyRating(pWhitePlayerName,rw, pended_yyyymmdd_hhmm)
    if rb != a[1]:
        rb = a[1]
        MyRatingRecordList.ModifyRating(pBlackPlayerName,rb, pended_yyyymmdd_hhmm)

MyPlayerList = PlayerList()
MyGameList = GameList()
MyRatingImpactTable = RatingImpactTable()
MyRatingFloor = RatingFloor()

MyPlayerList.LoadFromFile("inputdata/PlayerList.csv")
MyGameList.LoadFromFile("inputdata/GameList.csv")
MyRatingImpactTable.LoadFromFile("inputdata/Ratingimpact.csv")
MyRatingFloor.LoadFromFile("inputdata/RatingFloor.csv")

MyGameList.OrderByDate()
MyRatingImpactTable.OrderByRatingDifferenceFrom()

MyRatingRecordList = RatingRecordList()

a = DateTimeHandler()
begindate = a.DateTimeMinusOneDay(MyGameList.Games[0].ended_yyyymmdd_hhmm)
del a

if begindate[:4] == "9999":
    begindate = "19700101 00:00"

for p in MyPlayerList.Players:
    MyRatingRecordList.ModifyRating(p.UserName, 1200, begindate)

for g in MyGameList.Games:
    if g.GameResultValid == True:
        if g.ended_yyyymmdd_hhmm[:4] != "9999":
            ProcessGame(g.WhitePlayerName, g.BlackPlayerName, g.ended_yyyymmdd_hhmm, g.GameResult)

MyRatingRecordList.OrderByPlayerDate()

MyPlayerList.SaveToFile("outputdata/PlayerList.csv")
MyGameList.SaveToFile("outputdata/GameList.csv")
MyRatingRecordList.SaveToFile("outputdata/RatingRecordList.csv")
MyRatingImpactTable.SaveToFile("outputdata/Ratingimpact.csv")
MyRatingFloor.SaveToFile("outputdata/RatingFloor.csv")
