import numpy as np

# Duration of the illness
min_days_ill = 1
max_days_ill = 3

# Distance without mask
max_distance = 1
infect_probability = 0.85

# Death probability
death_probability = .3

# Probability of people wearing a wearing a mask
prob_wear_mask = 0.8
infect_probability_mask = 0.20
distance_with_mask = 5

population_size = 100
hangout_probability = 0.3

sim_duration_days = 7
sim_day_duration = 16

# Hangout duration
min_hangout_duration = 1
max_hangout_duration = 6

positions = [
    "home", "market", "cinema", "theatre", "bar", "school", "doctor"
]

class Person():
    def __init__(self):
        # STATE
        self.state = 0 # 0 = Good, 1 = Infected, 2 = Recovered, 3 = Dead, 4 = Just infected (can't infect others in that day)
        self.wears_mask = np.random.rand() <= prob_wear_mask # Constant for the whole simulation
        self.max_days_ill = np.random.randint(min_days_ill, max_days_ill+1)

        # DAILY stats
        self.days_ill = 0
        self.current_hangout_duration = 0 # Set at the start of each day
        self.time_away = 0 # In hours, the time spent away from home today

        # HOURLY stats
        self.current_position = 0 # First position is always home

    def move(self, newPosition):

        places[self.current_position].people.remove(self)

        for arr in places[self.current_position].matrix:
            if self in arr:
                arr.remove(self)
                arr.append(0)

        while (not 0 in places[newPosition].matrix[0]) and (not 0 in places[newPosition].matrix[1]) and (not 0 in places[newPosition].matrix[2]) and (not 0 in places[newPosition].matrix[3]) and (not 0 in places[newPosition].matrix[4]):
            newPosition = np.random.choice(places[1:]).index

        self.current_position = newPosition
        places[newPosition].people.append(self)
        first = np.random.randint(0,5)
        second = np.random.randint(0,5)

        while places[newPosition].matrix[first][second] != 0:
            first = np.random.randint(0,5)
            second = np.random.randint(0,5)
        places[newPosition].matrix[first][second] = self

class Place():

    def __init__(self, index):
        self.name = positions[index]
        self.index = index
        self.people = list()
        self.count = len(self.people)
        self.matrix = [[0]*5 for i in range(5)]

places = [
    Place(0),
    Place(1),
    Place(2),
    Place(3),
    Place(4),
    Place(5),
    Place(6)
]
# People can stay home -> infect probability = 0
# When the people are away there is the max infect probability
# Every person randomly decides wether she wants to go outside or not
