from team import *
import sys
from brasileirao import find_team_indx

team_file = sys.argv[1]
games_file = sys.argv[2]
Nsims = int(sys.argv[3])
Nsims *= 20
teams = []

# Read in the teams and their attributes
with open(team_file) as tfile:
    for line in tfile:
        name = line.split()[0]
        elo = int(line.split()[1])
        #pts = int(line.split()[2])
        #matches = int(line.split()[3])
        #wins = int(line.split()[4])
        #losses = int(line.split()[6])
        #gp = int(line.split()[7])
        #gc = int(line.split()[8])

        teams.append(Team(name=name, elo_home=elo, elo_away=elo))

results = []
goal_avg = 0.0
ng=0

with open(games_file) as gfile:
    for line in gfile:
        if len(line.split()) == 3:
            # game is to be played
            i1 = find_team_indx(teams, line.split()[0])
            i2 = find_team_indx(teams, line.split()[2])

            if (i1 is not None) and (i2 is not None):
                home_wins=0
                home_defeats = 0
                home_draws = 0

                score_sums = 0

                for i in range(0,Nsims):
                    if goal_avg > 0:
                        score = teams[i1].play(teams[i2], update='no', goal_avg=goal_avg)
                    else:
                        score = teams[i1].play(teams[i2], update='no')

                    score_sums += (score[0] - score[1])
                    if score[0] > score[1]:
                        home_wins +=1

                    elif score[0] < score[1]:
                        home_defeats +=1

                    else:
                        home_draws +=1

                home_wins = 100 * float(home_wins)/Nsims
                home_defeats = 100 * float(home_defeats)/Nsims
                home_draws = 100 * float(home_draws)/Nsims


                avg_score_diff = np.round(float(score_sums)/Nsims)

                results.append( teams[i1].name + " x " +  teams[i2].name + ': goal diff:' + str(avg_score_diff))
                results.append(str(int(0.5+home_wins))+ ':' + str(int(0.5+ home_draws)) + ':' \
                               + str(int(home_defeats+0.5)))



            elif i1 is None:
                print 'could not find team ', line.split()[0]
            elif i2 is  None:
                print 'could not find team ', line.split()[2]

        elif len(line.split()) == 5:
            # match has already been played
            i1 = find_team_indx(teams, line.split()[0])
            i2 = find_team_indx(teams, line.split()[4])



            score = np.zeros(2, dtype=int)
            score[0] = int(line.split()[1])
            score[1] = int(line.split()[3])

            # online computation of goals average
            ng += 1
            dg = np.sum(score) - goal_avg
            goal_avg += dg/ng

            if (i1 is not None) and (i2 is not None):

                teams[i1].update_stats(score, 'home')
                teams[i1].update_elo(teams[i2].elo_away[-1], score, 'home')

                teams[i2].update_stats(score, 'away')
                teams[i2].update_elo(teams[i1].elo_home[-2], score, 'away')

                #print teams[i1].name, score[0], 'x ', score[1], teams[i2].name

            elif i1 is None:
                print 'could not find team ', line.split()[0]
            elif i2 is None:
                print 'could not find team ', line.split()[2]

print "==================="
print "tabela Antes rodada"
print "==================="
tt = sorted(teams,reverse=True)

print 'pos name pts eloh eloa sg, gp'
for i in range(0, len(tt)):

    print '%2d'%(i+1), tt[i].name, tt[i].pts, '%4.0f'%tt[i].elo_home[-1], '%4.0f'%tt[i].elo_away[-1], \
        tt[i].gp - tt[i].gc, tt[i].gp


print "\n resultados\n"
for line in results:
    print line


print "goals average = ", goal_avg



def online_variance(data):
    '''
    Online algorithm for computation of variance. Found on wikipaedia
    :param data:
    :return: variance
    '''
    n = 0
    mean = 0.0
    M2 = 0.0

    for x in data:
        n = n + 1
        delta = x - mean
        mean = mean + delta/n
        M2 = M2 + delta*(x - mean)

    if n < 2:
        return float('nan');
    else:
        return M2 / (n - 1)