import pandas as pd
from scipy.spatial import distance

conn = mysql.connector.connect(
    host="hostname",
    user="username",
    password="password",
    database="database name"
)


users = pd.read_sql_query("SELECT * FROM Users", conn)
interests = pd.read_sql_query("SELECT * FROM Interests", conn)
users_interests = pd.read_sql_query("SELECT * FROM Users_Interests", conn)

users_interests = users_interests.merge(users, on='user_id')
users_interests = users_interests.merge(interests, on='interests_id')

# pivot the dataframe to get the ratings in a vector format
users_vectors = users_interests.pivot(index='user_id', columns='name', values='rating')

# fill the missing values with 0
users_vectors = users_vectors.fillna(0)

# sort the columns by name
users_vectors = users_vectors.sort_index(axis=1)

min_diff = float('inf')
closest_users = (0, 0)

for i in range(len(users_vectors)):
    for j in range(i+1, len(users_vectors)):
        user1 = users_vectors.iloc[i].values
        user2 = users_vectors.iloc[j].values
        diff = distance.euclidean(user1, user2)
        if diff < min_diff:
            min_diff = diff
            closest_users = (i+1, j+1)

# specify the threshold
threshold = 0.5

if min_diff <= threshold:
    print(f"The closest users are user {closest_users[0]} and user {closest_users[1]} with a difference of {min_diff}")
else:
    print("No two users have a difference below the threshold")
