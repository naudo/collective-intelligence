# A dictionary of movie critics and their ratings of a small
# set of movies
from math import sqrt

critics={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5,
         'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5,
                   'The Night Listener': 3.0},
                        'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5,
                                  'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0,
                                        'You, Me and Dupree': 3.5},
                             'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0,
                                       'Superman Returns': 3.5, 'The Night Listener': 4.0},
                                  'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0,
                                            'The Night Listener': 4.5, 'Superman Returns': 4.0,
                                                  'You, Me and Dupree': 2.5},
                                       'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                                                 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0,
                                                       'You, Me and Dupree': 2.0},
                                            'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0,
                                                      'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
                                                 'Toby': {'Snakes on a Plane':4.5,'You, Me and Dupree':1.0,'Superman Returns':4.0}}

def sim_distance(prefs, person1, person2):
    si = {}

    #Return a dist based Euclidean distance score
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1
    if len(si) == 0: return 0 #They have nothing in common

    sum_of_squares = sum([ pow(prefs[person1][item] - prefs[person2][item],2)
        for item in prefs[person1] if item in prefs[person2]])

    return 1 / ( 1 + sum_of_squares)


def sim_pearson(prefs, p1, p2):
    si={}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1
    n = len(si)

    #Add up the rankings
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])

    sum1Sq = sum([pow(prefs[p1][it],2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it],2) for it in si])
    
    # Sum the products 
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])

    # Calc the Pearson score
    num = pSum - (sum1 * sum2 / n)
    den = sqrt( (sum1Sq - pow(sum1,2) / n) * (sum2Sq - pow(sum2, 2) / n))

    if den == 0: return 0

    r = num / den

    return r

def sim_manhattan(prefs, p1,p2):
    """ Measure the distance between 2 points along axes"""
    total = 0
    p1_prefs = prefs[p1]
    p2_prefs = prefs[p2]

    for m in p1_prefs:
        if m in p2_prefs:
          total += abs(p1_prefs[m] - p2_prefs[m])

    return total

def sim_jaccard(prefs, p1, p2):
    print "Not Implemented"


def get_recommendations(prefs, person, similarity = sim_pearson):
    totals = {}
    simSums = {}

    for other in prefs: 
        #don't compare me to myself
        if other == person: continue
        sim = similarity(prefs, person, other)

        if sim <= 0: continue
        for item in prefs[other]:

            # only the items I haven't seen  yet
            if item not in prefs[person] or prefs[person][item] == 0:
                totals.setdefault(item, 0)
                totals[item]  += prefs[other][item] * sim

                simSums.setdefault(item, 0)
                simSums[item] += sim
    #create a nprmalized list
    rankings = [(total/simSums[item], item) for item, total in totals.items()]
    rankings.sort(reverse=True)

    return rankings

def transform_preferences(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})

            #flip the tiem and person around
            result[item][person]=prefs[person][item]

    return result



# return the best match for person from the pref dictionary
# Number of results and similarity fx are opt params
def top_matches(prefs, person, n=5, similarity=sim_pearson):
    scores = [ (similarity(prefs, person, other), other)
                for other in prefs if other != person]

    scores.sort()
    scores.reverse()
    return scores[0:n]
