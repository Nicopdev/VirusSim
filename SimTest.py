import numpy as np
import Variables as v
from Variables import Person

# Create the population
population = [Person(i) for i in range(v.population_size)] # There is a population of population_size (currently set to 100) people (see Person on the Variables file to access the class)

recovered_count = 0
dead_count = 0
good_count = v.population_size
infected_count = 0

population[0].state = 1 # Infect the first person

def move():
	# Move the population
    for person in population: # For every person in the Population
        if person.state != 2 and person.state != 3: # If the current person is not: dead (3) or recovered (2)
            if person.current_hangout_duration <= person.time_away: # If max hangout time is reached
                person.goHome() # Move the person to home
            else: # If there is still hangout time
                if person.current_position == 0: # If the person is still at home
                    if np.random.rand() < 0.5: # 50% of the time
                        person.time_away += 1
                        person.move(np.random.choice(v.places[1:]).index) # Move the person to somewhere else (indexes from 1 to max)
                else: # If the person was not at home
                    if np.random.rand() < 0.5: # 50% of the time
                        person.time_away += 1
                        person.move(np.random.choice(v.places[1:]).index) # Move the person to somewhere else (indexes from 1 to max)
def infect():
    global infected_count
    for place in v.places[1:]: # For every place (home excluded)
        for person in place.people: # For every person inside that place
            if person.state == 1: # If the person is infected
                # We need to find out where in the matrix this person is:
                to_infect = list() # Create a list to store the people that can be infected
                for i in range(0, v.room_dimensions): # The matrixes are currently 5x5
                    if person in place.matrix[i]: # If the person is inside the line i of the matrix
                    	inx = place.matrix[i].index(person) # Get his index in the line of the matrix

                        if inx > 0: # If the infected person is not on the left side of the matrix
                            to_infect.append(place.matrix[i][inx-1]) # Save the person on the left (if there is any)
                        if inx < 4: # If the infected person is not on the right side of the matrix
                            to_infect.append(place.matrix[i][inx+1]) # Save the person on the right (if there is any)
                      	if i > 0: # If the infected person is not on the first line of the matrix
                            to_infect.append(place.matrix[i-1][inx]) # Save the person on top (if there is any)
                        if i < 4: # If the infected person is not on the last line of the matrix
                            to_infect.append(place.matrix[i+1][inx]) # Save the person on bottom (if there is any)

                for person_to_infect in to_infect: # For every person that we save inside our to_infect list
                    if type(person_to_infect) != int: # If there is a person in that position (otherwise we have a integer: 0)
                    	if person_to_infect.state != 1 and person_to_infect.state != 4 and person_to_infect.state != 2 and person_to_infect.state != 3: # If the person is not already infected, dead or recovered
                            inf_prob = 0
                            if person.wears_mask: # If the infected person is wearing a mask
                            	inf_prob = v.infect_probability_mask # The probability to infect someone else is 0.2
                            else:
                                inf_prob = v.infect_probability # Here it's 0.85

                            if np.random.rand() < inf_prob: # Randomically choose to infect or not dependingo on the probability
                                person_to_infect.state = 4 # Infect that person
                                infected_count += 1 # Increase the number of infected people


def hour():
    move()
    infect()
    print("INFECTED COUNT")
    print(infected_count - dead_count - recovered_count)

def kill():
    global dead_count
    for person in population:
        if person.state == 1 or person.state == 4:
            if np.random.rand() < v.death_probability:
                person.state = 3
                person.goHome()
                dead_count += 1

def recover():
    global recovered_count
    for person in population:
        if person.state == 1:
            if person.max_days_ill == person.days_ill:
                person.state = 2
                person.goHome()
                recovered_count += 1

def day():
  	# BEGINNING OF THE DAY
    for person in population: # For every person in our population
        person.current_hangout_duration = np.random.randint(v.min_hangout_duration, v.max_hangout_duration) # Change his hangout duration value (how much time he can stay out before going back home)
        person.time_away = 0 # Reset how much time the person spent outside
        if person.state == 4 or person.state == 1:
            person.days_ill += 1

        if person.state == 4: # If someone yesterday was infected
            person.state = 1 # Today he will be able to infect other people

    for i in range(v.sim_day_duration): # (sim_day_duration is currently set to 16)
        hour()
        print("Hour inx: " + str(i))
        print("home")
        print v.places[0].people
        for place in v.places[1:]:
            print(place.name)
            print(place.matrix[0])
            print(place.matrix[1])
            print(place.matrix[2])
            print(place.matrix[3])
            print(place.matrix[4])
        print("\n\n")

    for person in population:
        person.goHome()

	# END OF THE DAY
    # TODO : we must move to home every person that gets killed or that recovers
    kill() # First kill 3% of the infected people
    recover() # Then recover whoever has reached their max days

population[0].state = 1
population[0].max_days_ill = v.sim_duration_days
for d in range(v.sim_duration_days):
    day()

print("home")
print(v.places[0].people)

for place in v.places[1:]:
    print(place.name)
    print(place.matrix[0])
    print(place.matrix[1])
    print(place.matrix[2])
    print(place.matrix[3])
    print(place.matrix[4])

print(infected_count - dead_count - recovered_count)
print(dead_count)
print(recovered_count)
print(v.population_size - infected_count)

#for person in population:
#    print(person.state)
