import numpy as np


class Team:
    def __init__(self, name='', elo_home=1500, elo_away=1500, gp=0, gc=0, points=0, matches=0, wins=0, losses=0):
        self.name = name

        #home elo
        self.elo_home = np.array([], dtype=int)
        self.elo_home= np.hstack((self.elo_home,elo_home))
        #away elo
        self.elo_away = np.array([], dtype=int)
        self.elo_away = np.hstack((self.elo_home,elo_away))

        self.gp = gp
        self.gc = gc
        self.pts = points
        self.matches = matches
        self.wins = wins
        self.losses = losses
        self.draws = matches - wins - losses

    def __eq__(self, other):
        sg = self.gp - self.gc
        sgo = other.gp - other.gc

        return self.pts == other.pts and self.wins == other.wins and sg == sgo and self.gp == other.gp

    def __gt__(self, other):
        sg = self.gp - self.gc
        sgo = other.gp - other.gc

        if self.pts > other.pts:
            return True
        elif self.pts == other.pts and self.wins > other.wins:
            return True
        elif self.pts == other.pts and self.wins == other.wins and  sg > sgo:
            return True
        elif self.pts == other.pts and self.wins == other.wins and sg == sgo and self.gp > other.gp:
            return True
        else:
            return False


    def play(self, opponent, goal_avg=2.3, update='y'):

        # obtain match score
        w = self.get_weights(opponent)
        score = np.zeros(2,dtype=int)

        for i in range(0, 2):
            score[i] = int(w[i] * np.random.poisson(goal_avg, 1))

        if update == 'y':
            # update points, gp, gc
            self.update_stats(score, 'home')
            opponent.update_stats(score, 'away')

            # update elos
            self.update_elo(opponent.elo_away[-1], score, 'home')
            opponent.update_elo(self.elo_home[-2], score, 'away')

        return score

    def get_weights(self, opponent):
        """

        :rtype : w, a vector with 2 floats
        """
        w = np.zeros(2)

        y = (self.elo_home[-1] - opponent.elo_away[-1])/400.

        w[0] = 1/(1 + pow(10, -y))
        w[1] = 1 - w[0]

        return w

    def update_stats(self, score, home_or_away):
        if home_or_away == 'home':
            gp = score[0]
            gc = score[1]
        else:
            gp = score[1]
            gc = score[0]

        if gp < gc:
            pts = 0
            self.losses += 1
        elif gp > gc:
            pts = 3
            self.wins += 1
        else:
            pts = 1
            self.draws += 1

        self.gp += gp
        self.gc += gc
        self.pts += pts
        self.matches +=1

    def update_elo(self, opponent_elo, score, home_or_away='home', k=30):

        """

        :rtype : self.elo is updated
        """
        if home_or_away == 'home':
            goal_diff = score[0] - score[1]
        else:
            goal_diff = score[1] - score[0]

        # determine outcome
        if goal_diff > 0:
            # win
            w = 1.0
        elif goal_diff < 0:
            #defeat
            w = 0.0
            goal_diff *= -1
        else:
            #draw
            w = 0.5

        if goal_diff <= 1:
            G = 1.0
        elif goal_diff == 2:
            G = 1.5
        else:
            G = 1.75 + (goal_diff - 3)/8.0

        if (home_or_away == 'home'):
            elo_diff = self.elo_home[-1] - opponent_elo
        else:
            elo_diff = self.elo_away[-1] - opponent_elo

        # expected outcome
        wex = 1/(1 + pow(10, - elo_diff/400.0))

        # elo change is proportional to the difference between the result and its expectation
        if (home_or_away == 'home'):
            self.elo_home = np.hstack((self.elo_home, self.elo_home[-1] + round(k*G*(w-wex))))
        else:
            self.elo_away = np.hstack((self.elo_away, self.elo_away[-1] + round(k*G*(w-wex))))

        def team_printout(self):
            '''
            Function that prints out all info  necessary to print out a table
            :return: a string
            '''
            print self.name, self.elo_home[-1], self.elo_away[-1], self.matches, self.pts, self.wins, self.draws, self.losses, \
                self.gp, self.gc, self.gp - self.gc





















