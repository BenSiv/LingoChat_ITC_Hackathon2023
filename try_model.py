import pandas as pd
import numpy as np
from scipy.spatial import distance

pd.options.mode.chained_assignment = None

def calculate_distance(user1, user2):
    return distance.euclidean(user1, user2)


<<<<<<< HEAD
def best_topic(index_list, df):
    index_df = df.loc[index_list]
    index_df = index_df.drop(columns=['Age', 'Gender_mapped', 'Unnamed: 0'])
    sums = index_df.sum()
    max_col = sums.idxmax()
    return max_col


def new_user_potential_group(row_sample, dict_group, df, threshold, n_closest_users):
    dict_for_users = dict()
    df_new = df.drop(row_sample.index)

    for group, value in dict_group.items():
        if len(value[0]) < n_closest_users:
            index_df = df.loc[value[0]]
            min_diff = float('inf')
            for i, row in index_df.iterrows():
                new_user = row_sample[df_new.columns.difference(['Unnamed: 0', 'group'])].values.flatten()
                old_user = row[df.columns.difference(['Unnamed: 0', 'group'])].values
                diff = calculate_distance(new_user, old_user)
                if diff < threshold:
                    if diff < min_diff:
                        min_diff = diff
                        dict_for_users.update({group: min_diff})

    return dict_for_users


def min_distance_or_new_group(new_dict_dist, existing_group, index_new_user):
    if new_dict_dist:
        min_key = min(new_dict_dist, key=lambda x: new_dict_dist[x])
        existing_group[min_key][0].append(index_new_user[0])
    else:
        if len(existing_group) > 0:
            existing_group[max(existing_group.keys()) + 1] = [[index_new_user[0]]]
        else:
            existing_group[1] = [[index_new_user[0]]]
    return existing_group


def group_without_topic(dict_value, df):
    for value in dict_value.values():
        topic = best_topic(value[0], df)
        if len(value) == 1:
            value.append(topic)
        if len(value) > 1:
            value[1] = topic
    return dict_value


def get_vectors_groups(dict_value, df):
    list_vector = list()
    for value in dict_value.values():
        df_value = df.loc[value[0]]
        list_vector = list()
        for i, row in df_value.iterrows():
            list_vector.append(row[df.columns.difference(['Unnamed: 0', 'group'])].values)
        mean_vector = np.mean(list_vector, axis=0)
        list_vector.append(mean_vector)
        return list_vector
=======
def find_closest_users(df, n_closest_users, threshold, group_number):
    """
    Find the n closest users to the starting user in the given dataframe
    :param df: dataframe to search for closest users in
    :param n_closest_users: number of closest users to find
    :param threshold: maximum allowed distance between users
    :param group_number: the number of the group
    :return: group_number, closest_users list, new df
    """

    starting_row = random.randint(0, len(df) - 1)
    starting_user = int(df.iloc[starting_row]['Unnamed: 0'])
    closest_users = [(starting_user, float('inf'))]

    counter = 0
    if len(df) > 1:
        while len(closest_users) < n_closest_users and len(df) > 1:
            min_diff = float('inf')
            closest_user = None
            for i, row in df[df['Unnamed: 0'] != starting_user].iterrows():
                user1 = df.loc[df['Unnamed: 0'] == starting_user][df.columns.difference(['Unnamed: 0', 'group'])].values.flatten()
                user2 = row[df.columns.difference(['Unnamed: 0', 'group'])].values
                diff = calculate_distance(user1, user2)
                if diff < min_diff:
                    min_diff = diff
                    closest_user = int(row['Unnamed: 0'])

            if min_diff <= threshold:
                df = df[df['Unnamed: 0'] != closest_user]
                closest_users.append((closest_user, min_diff))
            else:
                break

            counter += 1

            if len(closest_users) == 1 and counter > 6:
                break

        df = df[df['Unnamed: 0'] != starting_user]

    group_number += 1

    return group_number, closest_users, df
>>>>>>> 084861d3899df883cf5d5ec2dbd3a16fccb97cf2


if __name__ == '__main__':
    df = pd.read_csv('lingo_data.csv')
<<<<<<< HEAD
    df_sample = df.sample(n=20)

    THRESHOLD = 1.7
    n_closest_users = 6
    dict_group = dict()

    for num in range(20):
        row_sample = df.sample()
        if len(dict_group) > 0:
            distance_within_threshold = new_user_potential_group(row_sample, dict_group, df, THRESHOLD, n_closest_users)
        else:
            distance_within_threshold = None
        dict_group = min_distance_or_new_group(distance_within_threshold, dict_group, row_sample.index)
        dict_group = group_without_topic(dict_group, df)
        print(dict_group)

    print(dict_group)
    print(get_vectors_groups(dict_group, df))


=======
    # select a random sample of 30 rows
    df_sample = df.sample(40)

    THRESHOLD = 2
    n_closest_users = 6

    group_number = 0

    while len(df_sample) > 1:
        group_number, closest_users, df_sample = find_closest_users(df_sample, n_closest_users, THRESHOLD, group_number)

        print(closest_users)

        print("Group number:", group_number)
        print("User ids:", [user[0] for user in closest_users])


>>>>>>> 084861d3899df883cf5d5ec2dbd3a16fccb97cf2
