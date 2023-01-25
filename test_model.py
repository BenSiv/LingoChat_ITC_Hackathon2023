"""
testing the model with data from the database
"""
import pandas as pd
from try_model import *

def main():
    df = pd.read_csv('lingo_data.csv')
    # select a random sample of 40 rows
    df_sample = df.sample(40)

    THRESHOLD = 2
    n_closest_users = 6

    group_number = 0

    while len(df_sample) > 1:
        group_number, closest_users, df_sample = find_closest_users(df_sample, n_closest_users, THRESHOLD, group_number)

        print(closest_users)

        print("Group number:", group_number)
        print("User ids:", [user[0] for user in closest_users])

if __name__ == '__main__':
    main()
