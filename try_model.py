import pandas as pd
import numpy as np
from scipy.spatial import distance

pd.options.mode.chained_assignment = None


def calculate_distance(user1, user2):
    return distance.euclidean(user1, user2)

def best_topic(index_list, df):
    index_df = df.loc[index_list]
    index_df = index_df.drop(columns=['Age', 'Gender_mapped', 'Unnamed: 0'])
    means = index_df.mean().values
    highest_ind = np.argmax(means)
    max_col = index_df.columns[highest_ind]
    return max_col


def new_user_potential_group(row_sample, dict_group, df, threshold, n_closest_users):
    dict_for_users = dict()
    df_new = df.drop(row_sample.index)

    for group, value in dict_group.items():
        if len(value[0]) < n_closest_users:
            index_df = df.loc[value[0]]
            min_diff = float('inf')
            new_user = row_sample[df_new.columns.difference(['Unnamed: 0', 'group'])].values.flatten()
            group_vector = get_vectors_groups(index_df, df)
            diff = calculate_distance(new_user, group_vector)
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


def get_vectors_groups(df_value, df):
    #can change df to columns list
    list_vector = list()
    for i, row in df_value.iterrows():
        list_vector.append(row[df.columns.difference(['Unnamed: 0', 'group'])].values)
    mean_vector = np.mean(list_vector, axis=0)
    return mean_vector


if __name__ == '__main__':
    df = pd.read_csv('lingo_data.csv')
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
    for value in dict_group.values():
        #print(value)
        df_value = df.loc[value[0]]
        #print(get_vectors_groups(df_value, df))




