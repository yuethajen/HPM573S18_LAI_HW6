import numpy as np
import scr.StatisticalClasses as Stat


class SimGames:

    def __init__(self, sim_num):

        self.sim_num = sim_num
        self.reward_list = []
        self.reward = 0

    def sim_game(self):

        for a in range(0, self.sim_num):

            B = Game(a, 10, 0.5)
            self.reward_list.append(B.plot())

        return self.reward_list

    def exp_reward(self):

        for a in range(0, self.sim_num):

            B = Game(a, 10, 0.5)
            self.reward += B.repeat()

        self.reward = self.reward/self.sim_num

        return self.reward


class Game:

    def __init__(self, id, repeat_time, head_prop):

        self.id = id
        self.reward = -250
        self.average_reward = 0
        self.plot_reward=[]
        self.repeat_time = repeat_time
        self.head_prop = head_prop
        self.random = np.random
        self.random.seed(id)
        self.loss = 0
        self.prop_list = []

    def simulate(self):

        toss_result=[]

        for i in range(0,20):
            if self.random.sample() < self.head_prop:
                toss_result.append('Head')
            else:
                toss_result.append('Tail')

        for j in range(2,20):
            if (toss_result[j] == 'Head') and (toss_result[j-1] == 'Tail') and (toss_result[j-2] == 'Tail'):
                self.reward += 100

        return self.reward

    def repeat(self):

        for k in range(0, self.repeat_time):
            L = Game(self.id, self.repeat_time, self.head_prop)
            m = L.simulate()
            self.average_reward += m
            self.plot_reward.append(m)
            self.id += 1

        self.average_reward = self.average_reward/self.repeat_time

        return self.average_reward

    def plot(self):

        for k in range(0, self.repeat_time):
            L = Game(self.id, self.repeat_time, self.head_prop)
            m = L.simulate()
            self.plot_reward.append(m)
            self.id += 1

        return self.plot_reward

    def prop(self):

        for k in range(0, self.repeat_time):
            L = Game(self.id, self.repeat_time, self.head_prop)
            m = L.simulate()
            if m < 0:
                self.loss += 1
            self.id += 1

        self.loss = self.loss/self.repeat_time

        return self.loss

    def get_prop_list(self):

        for k in range(0, self.repeat_time):
            L = Game(self.id, self.repeat_time, self.head_prop)
            m = L.simulate()
            if m < 0:
                self.prop_list.append(0)
            else:
                self.prop_list.append(1)
            self.id += 1

        return self.prop_list


class Stat_outcomes:

    def __init__(self, game_id):
        self.game_id = game_id
        self.reward_list = []
        self.sumStat_reward = \
            Stat.SummaryStat('Expected reward', self.get_reward_list())
        self.prop_list = []
        self.sumStat_prop = \
            Stat.SummaryStat('Probability of losing money', self.get_prop_list())

    def get_reward_list(self):

        if self.game_id == 1:
            self.reward_list = Q.plot()

        if self.game_id == 2:
            self.reward_list = S.sim_game()

        return self.reward_list

    def get_CI_reward(self, alpha):

        return self.sumStat_reward.get_t_CI(alpha)

    def get_prop_list(self):

        if self.game_id == 1:
            self.prop_list = Q.get_prop_list()

        return self.prop_list

    def get_CI_prop(self, alpha):

        return self.sumStat_prop.get_t_CI(alpha)

    def get_PI_reward(self, alpha):

        return self.sumStat_reward.get_PI(alpha)

    def get_PI_prop(self, alpha):

        return self.sumStat_prop.get_PI(alpha)


Q = Game(1, 1000, 0.5)
S = SimGames(1000)
R = Stat_outcomes(1)
T = Stat_outcomes(2)

exp_reward_1000 = Q.repeat()
exp_reward_10 = S.exp_reward()
CI_reward_Q = R.get_CI_reward(0.05)
CI_prop_Q = R.get_CI_prop(0.05)

PI_reward_S = T.get_PI_reward(0.05)


print('Casino owner:')
print('The expected reward is', exp_reward_1000)
print('95% CI of expected reward is', CI_reward_Q)
print('Meaning:')
print('If the casino owner repeats the 1000 games many times, 95% of these intervals will cover the true mean of expected rewards.')
print('')
print('The probability of losing money is', Q.prop())
print('95% CI of probability of losing money is', CI_prop_Q)
print('Meaning:')
print('If the casino owner repeats the 1000 game many times, 95% of these intervals will cover the true probability of losing money.')
print('Casino owner plays the game many times, a steady-state simulation is used.')
print(' ')
print(' ')
print('Gambler:')
print('The expected reward is', exp_reward_10)
print('The 95% PI of expected reward is', PI_reward_S)
print('Meaning:')
print('If the gambler plays the game for 10 times next time, the expected reward has 95% chance to fall between these intervals.')
print('')
print('The gambler plays the game only for 10 times (a small sample size), the expected reward has a very large range and')
print('the experimental probability of losing money could be quite different from the theoretical probability (0.6) of losing money.')
print('A transient-state simulation is used.')




