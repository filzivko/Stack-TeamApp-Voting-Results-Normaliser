# Stack-TeamApp-Voting-Results-Normaliser
Convert voting from Stack TeamApp to normalised results in order to accurately award man of the match and end of season best and fairest awards.

# What is Stack TeamApp and what does this script do?
Stack TeamApp is a free app where users can manage their social sport teams, in particular voting for best and fairest each week.
However the app does not take into consideration issues which may skew the voting, such as:
- Varying number of voters per round (votes are added up in total, this means that the end of season leaderboard is skewed in favour of players played well in weeks that had the most voter compliance - typically early in the season)
- Players not voting (since a player shouldn't vote for themselves, not voting at all can mean increasing their tally compared to others)

This script takes the csv (exported from the app) and carries out data manipulation in order to normalise the results per game and factors in penalties for non-voters in order to balance the results.

Two output files are exported in csv. The leaderboard with adjusted scores (end of season best and fairest) and the per round adjusted points (weekley man of the match).

Simply change the name of the csv file to be read on line 8 and run.
