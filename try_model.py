import pandas as pd
import random
from scipy.spatial import distance

pd.options.mode.chained_assignment = None


def select_random_sample(df, n):
    """
    Select a random sample of n rows from the given dataframe
    :param df: dataframe to select the sample from
    :param n: number of rows to select
    :return: dataframe with the selected rows
    """
    random_rows = random.sample(range(len(df)), n)
    df_new_sample = df.iloc[random_rows]
    return df_new_sample


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

    if len(df) > 0:
        while len(closest_users) < n_closest_users and len(df) > 0:
            min_diff = float('inf')
            closest_user = None
            for i, row in df.iterrows():
                user1 = df.loc[df['Unnamed: 0'] == starting_user][
                        df.columns.difference(['Unnamed: 0', 'group'])].values.flatten()
                if \
                        df.loc[df['Unnamed: 0'] == starting_user][
                                df.columns.difference(['Unnamed: 0', 'group'])].values.shape[
                                0] > 0:
                    diff = distance.euclidean(user1, df.loc[df['Unnamed: 0'] == starting_user][
                            df.columns.difference(['Unnamed: 0', 'group'])].values.flatten())
                    if diff < min_diff:
                        min_diff = diff
                        closest_user = int(row['Unnamed: 0'])

            if min_diff <= threshold:
                df = df[df['Unnamed: 0'] != closest_user]
                closest_users.append((closest_user, min_diff))
            else:
                break

    group_number += 1

    return group_number, closest_users, df


if __name__ == '__main__':
    # read the data
    df = pd.read_csv('lingo_data.csv')
    # select a random sample of 30 rows
    df_sample = select_random_sample(df, 30)

    THRESHOLD = 0.5
    n_closest_users = 6

    group_number = 0

    while len(df_sample) > 0:
        group_number, closest_users, df_sample = find_closest_users(df_sample, n_closest_users, THRESHOLD, group_number)

        print("Group number:", group_number)
        print("User ids:", set(user[0] for user in closest_users))


