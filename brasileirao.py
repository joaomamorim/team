import sys

from team import *


def find_team_indx(teams, name):
    '''
    Given a list Team objects, returns the index of the objective with obj.name equal
    string 'name'
    :param teams: a list of Team objects
    :param name: a string
    :return: the list index for the object that has obj.name == name
    '''
    indx = None
    for i in range(0, len(teams)):
        if teams[i].name == name:
            indx = i
            break

    return indx


team_file = sys.argv[1]
games_file = sys.argv[2]

teams = []

# Read in the teams and their attributes
with open(team_file) as tfile:
    for line in tfile:
        name = line.split()[0]
        elo = int(line.split()[1])
        #pts = int(line.split()[2])
        #matches = int(line.split()[3])
        #gp = int(line.split()[4])
        #gc = int(line.split()[5])
        teams.append(Team(name=name, elo_home=elo, elo_away=elo))
results = []
with open(games_file) as gfile:
    for line in gfile:
        if len(line.split()) == 3:
            # game is to be played
            i1 = find_team_indx(teams, line.split()[0])
            i2 = find_team_indx(teams, line.split()[2])

            if (i1 is not None) and (i2 is not None):

                score = teams[i1].play(teams[i2])
                results.append( teams[i1].name + " " + str(score[0])  \
                        + ' x ' + str(score[1]) + ' '+ teams[i2].name)

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


print "tabela"
tt = sorted(teams,reverse=True)

print 'pos name pts eloh eloa sg, gp'
for i in range(0, len(tt)):

    print '%2d'%(i+1), tt[i].name, tt[i].pts, '%4.0f'%tt[i].elo_home[-1], '%4.0f'%tt[i].elo_away[-1], \
        tt[i].gp - tt[i].gc, tt[i].gp