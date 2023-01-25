import pandas as pd
import random
from scipy.spatial import distance

# read the data
df = pd.read_csv('lingo_data.csv')

# select a random sample of 30 rows
random_rows = random.sample(range(len(df)), 30)
df_sample = df.iloc[random_rows]

threshold = 0.5
n_closest_users = 6

# initialize the group number
group_number = 0

while len(df_sample) > 0:
    # select a random row as the starting point
    starting_row = random.randint(0, len(df_sample) - 1)
    starting_user = int(df_sample.iloc[starting_row]['Unnamed: 0'])
    closest_users = [(starting_user, float('inf'))]
    df_sample.loc[df_sample['Unnamed: 0'] == starting_user, 'group'] = group_number + 1
    if len(df_sample) > 0:
        while len(closest_users) < n_closest_users and len(df_sample) > 0:
            min_diff = float('inf')
            closest_user = None
            for i, row in df_sample.iterrows():
                user1 = df_sample.loc[df_sample['Unnamed: 0'] == starting_user][df_sample.columns.difference(['Unnamed: 0', 'group'])].values.flatten()
                if \
                        df_sample.loc[df_sample['Unnamed: 0'] == starting_user][
                            df_sample.columns.difference(['Unnamed: 0', 'group'])].values.shape[
                            0] > 0:
                    diff = distance.euclidean(user1, df_sample.loc[df_sample['Unnamed: 0'] == starting_user][
                        df_sample.columns.difference(['Unnamed: 0', 'group'])].values.flatten())
                    if diff < min_diff:
                        min_diff = diff
                        closest_user = int(row['Unnamed: 0'])
            if min_diff <= threshold:
                closest_users.append((closest_user, min_diff))
                df_sample = df_sample[df_sample['Unnamed: 0'] != closest_user]
                df_sample.loc[df_sample['Unnamed: 0'] == closest_user, 'group'] = group_number + 1
            else:
                break
    group_number += 1
    # print the group number and the ids of the closest users
    print("Group number:", group_number)
    print("User ids:", [user[0] for user in closest_users])
