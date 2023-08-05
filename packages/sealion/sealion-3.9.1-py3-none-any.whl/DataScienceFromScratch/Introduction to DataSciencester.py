#data given below
users = [
    {"id" : 0, "name" : "Hero"},
    {"id" : 1, "name" : "Dunn"},
    {"id" : 2, "name" : "Sue"},
    {"id" : 3, "name" : "Chi"},
    {"id" : 4, "name" : "Thor"},
    {"id" : 5, "name" : "Clive"},
    {"id" : 6, "name" : "Hicks"},
    {"id" : 7, "name" : "Devin"},
    {"id" : 8, "name" : "Kate"},
    {"id" : 9, "name" : "Klein"}
]

friendship_pairs = [(0, 1), (0, 2), (1, 2), (1, 3), (2,3), (3,4), (4,5), (5,6),(5,7),(6,8),(7,8),(8,9)] #all friendships in the network (friend1, friend2)

#next, let's create a dictionary that stores each friend to their friends
friendships = {user["id"] : [] for user in users}

for friend1, friend2 in friendship_pairs :
    friendships[friend1].append(friend2)
    friendships[friend2].append(friend1) #they both are friends to each other

#how many connections does the average person have in our social network?

def number_of_friends(user) :
    '''user contains their name and "id" in a dict'''
    user_id = user["id"]
    return len(friendships[user_id]) #return number of friendships for that individual given their ID

total_connections = sum([number_of_friends(user) for user in users])

num_users = len(users)
avg_connections = total_connections/num_users

#find the most connected people in a list
num_friends_by_id = [(user["id"], number_of_friends(user)) for user in users]

num_friends_by_id.sort(
    key = lambda id_and_friends : id_and_friends[1], #sort by num_friends,
    reverse = True
)

#each pair in num_friends_by_id is a (user_id, num_friends)

print("Who is the social one : " , num_friends_by_id)

#to find friends of a friend (foaf)

def foaf_ids_bad(user) :
    # find the ids of the friendships[friend] for every friend in friendships[user]
    return [foaf_id for friend_id in friendships[user["id"]] for foaf_id in friendships[friend_id]]

#find mutual friends, friends of your friends that aren't friends with you in the network!

from collections import Counter
def friends_of_friends(user) :
    user_id = user["id"]
    return Counter(
        foaf_id
        for friend_id in friendships[user_id] #for each of my friends,
        for foaf_id in friendships[friend_id] #find their friends
        if foaf_id != user_id  #that aren't me
        and foaf_id not in friendships[user_id] #and my friends
    )

print("Mutual friends of user 3 : " , friends_of_friends(users[3]))

#you get the interests of the network

interests = [
    (0, "Hadoop"), (0, "Big Data"), (0, "HBase"), (0, "Java"),
    (0, "Spark"), (0, "Storm"), (0, "Cassandra"),
    (1, "NoSQL"), (1, "MongoDB"), (1, "Cassandra"), (1, "HBase"),
    (1, "Postgres"), (2, "Python"), (2, "scikit-learn"), (2, "scipy"),
    (2, "numpy"), (2, "statsmodels"), (2, "pandas"), (3, "R"), (3, "Python"),
    (3, "statistics"), (3, "regression"), (3, "probability"),
    (4, "machine learning"), (4, "regression"), (4, "decision trees"),
    (4, "libsvm"), (5, "Python"), (5, "R"), (5, "Java"), (5, "C++"),
    (5, "Haskell"), (5, "programming languages"), (6, "statistics"),
    (6, "probability"), (6, "mathematics"), (6, "theory"),
    (7, "machine learning"), (7, "scikit-learn"), (7, "Mahout"),
    (7, "neural networks"), (8, "neural networks"), (8, "deep learning"),
    (8, "Big Data"), (8, "artificial intelligence"), (9, "Hadoop"),
    (9, "Java"), (9, "MapReduce"), (9, "Big Data")
]

def data_scientists_who_like(target_interest) :
    '''find data scientists who have that interest'''
    return [user_id for user_id, user_interest in interests if user_interest == target_interest]

#get all interests with the user ids
from collections import defaultdict


user_ids_by_interest = defaultdict(list)
interests_by_user_id = defaultdict(list) #(user_id, all interests)

for user_id, interest in interests :
    interests_by_user_id[user_id].append(interest)
    user_ids_by_interest[interest].append(user_id)

print("These are the interests of our users : " , interests_by_user_id)

def most_common_interests_with(user) :
    '''returns the users with similar interest and how many overlapping interests in (user_id, num_overlapping)'''
    return Counter(
        interested_user_id
        for interest in interests_by_user_id[user["id"]] #for each of that user's interests
        for interested_user_id in user_ids_by_interest[interest] #find the other interested users
        if interested_user_id != user["id"] #who aren't that person
    )

print("Most common interests : " , most_common_interests_with(users[1]))

#salary data in (num_salary, num_tenure)
salaries_and_tenures = [(83000,8.7), (88000,8.1),
                        (48000,0.7), (76000,6),
                        (69000,6.5), (76000,7.5),
                        (60000, 2.5), (83000, 10),
                        (48000, 1.9), (63000, 4.2)]


salary_by_tenure = defaultdict(list) # (tenure, salaries)
for salary, tenure in salaries_and_tenures :
    salary_by_tenure[tenure].append(salary)

average_salary_by_tenure = {tenure : sum(salaries)/len(salaries) for tenure, salaries in salary_by_tenure.items()}  #for everything in a list format of salary_by_tenure find the average salary for that tenure

print("This is the average salary by tenure : " , average_salary_by_tenure)

#everyone has a different tenure so this isn't very useful, so bucket them together!

def tenure_bucket(tenure) :
    if tenure < 2 :
        return "less than two"
    elif tenure < 5 :
        return "between two and five"
    else :
        return "more than five"

salary_by_tenure_bucket = defaultdict(list)
for salary, tenure in salaries_and_tenures :
    bucket = tenure_bucket(tenure)
    salary_by_tenure_bucket[bucket].append(salary)

print("Salary_by_tenure_bucket : ", salary_by_tenure_bucket)

#know find the average

average_salary_by_tenure_bucketed = {tenure_bucket : sum(salaries)/len(salaries) for tenure_bucket, salaries in salary_by_tenure_bucket.items()}
print("More correct data science salaries : ", average_salary_by_tenure_bucketed)

'''
#if we find that longer users pay less, and vice versa
def predict_paid_or_unpaid(years_experience) : 
    if years_experience < 3.0 : return "paid"
    elif years_experience < 8.5 : return "unpaid"
    else : return "paid"
    
#but overfitting and this is dumb compared to linear regression
'''

#find which are the most popular interests
words_and_counts = Counter(word
                           for user, interest in interests #for each interest
                           for word in interest.lower().split()) #make it lower case and split on spaces

for word, count in words_and_counts.most_common() :
    if count > 1 :
        #if statement covers up unique broken stuff like "artificial intelligence" -> "artificial" , "intelligence"
        print(word, count)


