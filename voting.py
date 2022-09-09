from cmath import isnan
from pickle import FALSE
import pandas as pd
from collections import defaultdict
import sys

# read file - enter your CSV file name below
df = pd.read_csv(r'YOUR FILE HERE.csv')

# votes will be the main dictionary for data manipulation
votes = {}
# leaderboard will store the end of season adjusted points
leaderboard = {}
# perroundadj will store the per round adjusted scores to deteremine man of the match
perroundadj = {}
# dictionary of all non-voters per team per round
nonvoters = {}

# read excel of non voters per round
dfnovote = pd.read_excel('nonvoters.xlsx', sheet_name='Sheet1')

# set the team and penalty worked on
setTeam = "Ressies"
penalty = 0


# penalty function for non voters
def nonVoterPenalty(voter, round, team):
    # The penalty for not voting on a specific gameweek
    for a in range(len(dfnovote)):

        for i in dfnovote.loc[a]:
            if dfnovote.loc[a][0] == round and dfnovote.loc[a][1] == team:
                if i == voter:
                    return True


# input a string that states something like "30 votes for john" and returns 30, john
def converter(stringin):
    indexstart = stringin.find('r')
    votecount = stringin[:indexstart-9]
    player = stringin[indexstart+2:len(stringin)]
    return votecount, player


# search df and convert to dict, this reformats the data from the template team app export
def search():
    rndNum = 0
    for i in range(len(df)):

        if not isnan(df.loc[i]["Round Number"]):
            rndNum = int(df.loc[i]["Round Number"])
            votes[rndNum] = {}
            # total points for the round
            votes[rndNum]["Total Points"] = 0
            # players actual scores
            votes[rndNum]["Players Actual"] = {}
            # players adjusted scores
            votes[rndNum]["Players Adjusted"] = {}

        if isinstance(df.loc[i]["Votes Leaderboard"], str):
            votecount, player = converter(df.loc[i]["Votes Leaderboard"])
            votes[rndNum]["Total Points"] += int(votecount)
            votes[rndNum]["Players Actual"][player] = int(votecount)


# create actual scores based on total points per round
def createActuals():
    for i in votes:
        for j in votes[i]["Players Actual"]:
            # j is the name of eachplayer
            # i is round
            if nonVoterPenalty(j, i, setTeam):
                if votes[i]["Players Actual"][j] > penalty:
                    (votes[i]["Players Actual"][j]) -= penalty

            adjpoints = (votes[i]["Players Actual"][j]) / \
                (votes[i]["Total Points"])*100
            # set adjusted points
            votes[i]["Players Adjusted"][j] = adjpoints

            if j in leaderboard:
                leaderboard[j] += (adjpoints)
            else:
                leaderboard[j] = (adjpoints)


# action functions
search()
createActuals()

# extract the adjusted per round scores
for i in votes:
    perroundadj[i] = votes[i]["Players Adjusted"]

# sort the leaderboard
leaderboard = dict(
    sorted(leaderboard.items(), reverse=True, key=lambda item: item[1]))


# sort per round adjusted
for i in perroundadj:
    perroundadj[i] = dict(
        sorted(perroundadj[i].items(), reverse=True, key=lambda item: item[1]))


# export dicts to csv
def exportperroundtocsv():
    with open('perroundres0.csv', 'w') as f:
        for key in perroundadj.keys():
            f.write("%s, %s\n" % (key, perroundadj[key]))


def exportleadertocsv():
    with open('leaderboardrres0.csv', 'w') as f:
        for key in leaderboard.keys():
            f.write("%s, %s\n" % (key, leaderboard[key]))


exportleadertocsv()
exportperroundtocsv()
