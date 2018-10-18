import math
from itertools import combinations
import numpy as np
from random import randint

def simulation(n,p,nd,nh):
    #making dict in schema:
    #{day1: {hotel1: [people who visited hotel1], hotel2: [people who visited hotel], ...},
    #day2: {hotel1: [people who visited hotel1], hotel2: [people who visited hotel], ... },
    #...
    #daynd {...}}
    dict = {}
    for day in range(nd):
        day_dict = {}

        for person in range(n):
            goToHotel = np.random.choice([1,0], p=[p,1-p])
            if goToHotel==1:
                hotel = randint(0, nh)
                if hotel in day_dict:
                    day_dict[hotel].append(person)
                else:
                    day_dict[hotel] = []
                    day_dict[hotel].append(person)

        dict[day] = day_dict
    return dict

def make_combination(dict):
    #making people combinations dictionary
    #{day1: {hotel1: [every pair of people who visited hotel1], hotel2: [every pair of people who visited hotel], ...},
    #day2: {hotel1: [every pair of people who visited hotel1], hotel2: [every pair of people who visited hotel], ... },
    #...
    #day_nd {...}}

    pairs_dict ={}
    for d in dict: #for each day
        single_day_dict={}

        for h in dict[d]: #for each hotel
            combin = list(combinations(dict[d][h],2))
            if len(combin)>0:
                single_day_dict[h] = combin
        pairs_dict[d] = single_day_dict

    return pairs_dict

def calculate_meetings(pairs_dict):
    #returns dictionary of meetinge amount
    #{(pair): amountOfMeetings

    pair_meets_dict={}
    for x in pairs_dict: #for each day
        for y in pairs_dict[x]: #for each hotel
            pairs_list = pairs_dict[x][y]
            for z in pairs_list:
                if z in pair_meets_dict:
                    pair_meets_dict[z] += 1
                else:
                    pair_meets_dict[z]=1

    return pair_meets_dict

def calculate_suspected_pairs(pair_meets_dict):
    amount_of_sus_pairs = 0
    amount_of_suspected_people_and_days = 0

    for i in pair_meets_dict:
        if pair_meets_dict[i]>1:
            amount_of_sus_pairs+=1
            x=pair_meets_dict[i]
            amount_of_suspected_people_and_days+=math.factorial(x)/(2*(math.factorial(x-2)))

    return amount_of_sus_pairs, amount_of_suspected_people_and_days

def calculate_people(pair_meets_dict):
    suspected_people = [];
    for i in pair_meets_dict:
        if pair_meets_dict[i]>1:
            if i[0] not in suspected_people:
                suspected_people.append(i[0])
            if i[1] not in suspected_people:
                suspected_people.append(i[1])
    amount_of_sus_people = len(suspected_people)

    return amount_of_sus_people

def make_histogram(dict):
    hist={}
    for i in dict:
        if dict[i] in hist:
            hist[dict[i]]+=1
        else:
            hist[dict[i]] = 1

    x=[]
    y=[]
    for i in hist:
        x.append(i)
        y.append(hist[i])

    return x, y

def calculate(n, p, nd, nh):
    dict = simulation(n, p, nd, nh)
    pairs_dict = make_combination(dict)
    pair_meets_dict = calculate_meetings(pairs_dict)
    amount_of_sus_pairs, amount_of_suspected_people_and_days = calculate_suspected_pairs(pair_meets_dict)
    amount_of_sus_people = calculate_people(pair_meets_dict)
    x, y = make_histogram(pair_meets_dict)
    return amount_of_sus_pairs, amount_of_suspected_people_and_days, amount_of_sus_people, x, y

#def average_histogram()
#return x, y


def make_statistics(n, p, nd, nh, amount_of_simulation):
    amount_of_sus_pairs = 0
    amount_of_suspected_people_and_days = 0
    amount_of_sus_people = 0

    for i in range(amount_of_simulation):
        amount_of_sus_pairs_tmp, amount_of_suspected_people_and_days_tmp, amount_of_sus_people_tmp, x_tmp, y_tmp =  calculate(n, p, nd, nh)
        amount_of_sus_pairs += amount_of_sus_pairs_tmp
        amount_of_suspected_people_and_days += amount_of_suspected_people_and_days_tmp
        amount_of_sus_people  += amount_of_sus_people_tmp

    amount_of_sus_pairs = amount_of_sus_pairs / amount_of_simulation
    amount_of_suspected_people_and_days = amount_of_suspected_people_and_days / amount_of_simulation
    amount_of_sus_people = amount_of_sus_people / amount_of_simulation

    return amount_of_sus_pairs, amount_of_suspected_people_and_days, amount_of_sus_people

def main():
    n = 10000
    p = 0.1
    nd = 100
    nh = 100
    amount_of_simulation = 1

    amount_of_sus_pairs, amount_of_suspected_people_and_days, amount_of_sus_people= make_statistics(n, p, nd, nh, amount_of_simulation)
    print("Liczba podejrzanych par osób: ", int(round(amount_of_sus_pairs,0)))
    print("Liczba podejrzanych par osób i dni: ", int(round(amount_of_suspected_people_and_days,0)))
    print("Liczba podejrzanych osób: ", int(round(amount_of_sus_people,0)))

if __name__ == "__main__":
    main()