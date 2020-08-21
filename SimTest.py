import numpy as np
import Variables as v
from Variables import Person

# ONE DAY SIM

# Create the population
population = [Person(i) for i in range(v.population_size)]

recovered_count = 0
dead_count = 0
good_count = v.population_size
infected_count = 0

population[0].state = 1 # Infect the first person

def hour():
    # Move
    for person in population:
        if person.state != 2 and person.state != 3: # If the current person is not dead or recovered
            if person.current_hangout_duration <= person.time_away: # If hangout time outisde is finished
                person.move(0) # Move the person to home
            else: # If there is still hangout time
                person.time_away += 1
                if np.random.rand() > 0.5: # 50% of the time
                    person.move(np.random.choice(v.places[1:]).index) # Move the person to somewhere else



def day():
    for person in population:
        person.current_hangout_duration = np.random.randint(v.min_hangout_duration, v.max_hangout_duration)
        person.time_away = 0

        if person.state == 4: # If someone yesterday was infected
            person.state = 1 # Today he will be able to infect other people

    for i in range(v.sim_day_duration):
        hour()
        print("Hour inx:", i)
        for place in v.places:
            print(place.name)
            print(place.matrix)
        print("\n\n\n")




day()

for place in v.places:
    print(place.name)
    print(place.matrix)
