import numpy as np
import Variables as v
from Variables import Person
from Variables import Place

infected_count = 0
dead_count = 0
recovered_count = 0

dead_people = list()
infected_people = list()
population = list()

for i in range(v.population_size):
    person = Person()
    population.append(person)
    v.places[0].people.append(person)


# Interpersonal distance is not taken in account yet in this simulation

population[0].state = 1 # Infect a person
for day in range(v.sim_duration_days):
    # At the beginning of each day
    for person in population: # For every person
        person.current_hangout_duration = np.random.randint(v.min_hangout_duration, v.max_hangout_duration) # Change his hangout duration for that day
        if person.state == 4: # If he was infected the day before
            person.state = 1 # Make him infected today
            person.days_ill += 1 # Add a day to his day_ill count
        elif person.state == 1: # If the person was already infected
            person.days_ill += 1 # Add a day to his day_ill count

    for hour in range(v.sim_day_duration): # For every hour in a day
        # MOVE THE POPULATION
        for person in population:
            # If the person isn't receovered
            if person.state != 2 and person.state != 3:
                # If the person has been out the max time possible
                if person.time_away >= person.current_hangout_duration:
                    if person.current_position != 0:
                        person.move(0) # Move the person home
                else:
                    if person.current_position != 0:
                        if np.random.rand() < 0.5:
                            newPosition = np.random.choice(v.places[1:]).index # Select a new position (home excluded)
                            person.move(newPosition)
                    else:
                        newPosition = np.random.choice(v.places[1:]).index # Select a new position (home excluded)
                        person.move(newPosition)
                    person.time_away += 1 # Increase the hours the person has been out

        # INFECT THE POPULATION
        for place in v.places[1:]: # For every place (home excluded)
            for person in place.people: # For every person currently in that place
                if person.state == 1: # If someone is infected
                    ppl = list()
                    for i in range(0,5): # 5 times
                        if person in place.matrix[i]: # If the person sits in the cell we are checking
                            inx = place.matrix[i].index(person) # Save his index
                            # If he's not on a side
                            if inx > 0:
                                ppl.append(place.matrix[i][inx-1])
                            if inx < 4:
                                ppl.append(place.matrix[i][inx+1])
                            if i > 0:
                                ppl.append(place.matrix[i-1][inx])
                            if i < 4:
                                ppl.append(place.matrix[i+1][inx])

                    for to_infect in ppl:
                        if type(to_infect) != int:
                            if to_infect.state != 1 and to_infect.state != 4:
                                prob = 0
                                if person.wears_mask:
                                    prob = v.infect_probability_mask
                                else:
                                    prob = v.infect_probability

                                if np.random.rand() < prob:
                                    to_infect.state = 4
                                    infected_count += 1

    # KILL THE INFECTED PART OF THE POPULATION
    for person in population:
        if person.state == 1 or person.state == 4:
            if np.random.rand() < v.death_probability:
                person.state = 3
                person.move(0)
                dead_count += 1

    # At the end of each day
    for person in population:
        # If the person reached the max days ill
        if person.days_ill >= person.max_days_ill:
            person.state = 2 # Recover the person
            person.move(0) # Move the person home forever (he wouldn't interact with anyone anyway)
            recovered_count += 1
