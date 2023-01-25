import pymysql
import numpy as np

DATABASE_NAME = 'itc_hackaton'
# USER = 'root'
# PASSWORD = 'root1!2@'
# HOST = 'localhost'
USER = 'm1ow7xhhjf2u87ondhja'
PASSWORD = 'pscale_pw_kI2oJ1yIUdgQQHMK4ovdB6UARJB4cf8UAmWwJliuuJp'
HOST = 'eu-central.connect.psdb.cloud'
MAX_USERS = 6
LANGUAGE = 'english'


def create_connection():
    con = pymysql.connect(host=HOST,
                          user=USER,
                          password=PASSWORD,
                          database=DATABASE_NAME,
                          autocommit=True,
                          ssl={'ssl': {'ca': '/etc/ssl/certs/ca-certificates.crt'}})
    return con


def sql_query(query, con):
    """
    "sql_connection" receives a string with sql query and returns it result using pymysql module.
    """
    with con.cursor() as cursor:
        cursor.execute(query)
        result = cursor.fetchall()
    return result


def get_user_ratings(user_id, con):
    con = create_connection()
    user_ratings_query = f'''SELECT interests_id,rating FROM Users_Interests where user_id = {user_id};'''
    ratings = np.array(sql_query(user_ratings_query, con))[:, 1]
    # rank_dict = {0: 0, 1: .2, 2: 0.4, 3: 0.6, 4: 0.8, 5: 1}
    # ratings = np.vectorize(rank_dict.get)(ratings)
    return ratings


def get_available_chats(max_users, language, con):
    chat_rooms = {}
    for num in range(1, max_users):
        Chat_rooms_id_query = f'''SELECT id FROM Chat_Rooms where active_users = {num} and where language = {language};'''
        Chat_rooms_id = sql_query(Chat_rooms_id_query, con)
        chat_rooms[num] = Chat_rooms_id
    return chat_rooms


def get_chat_vectors(chat_rooms, user_nuber, con):
    chat_list = chat_rooms[user_nuber]
    Chat_vectors_query = f'''SELECT feature_vector FROM Chat_Rooms where id in {tuple(chat_list)};'''
    Chat_rooms_vectors = sql_query(Chat_vectors_query, con)
    return Chat_rooms_vectors


def calc_chat_vector(chat_id, con):
    # get all users id
    Chat_users_query = f'''SELECT user_id FROM User_chat where chat_id = {chat_id} AND leave_timestamp IS NULL;'''
    Chat_users = sql_query(Chat_users_query, con)

    # get users ratings
    ratings = np.array([])
    for Chat_user in Chat_users:
        rating = get_user_ratings(Chat_user, con)
        ratings = np.concatenate([ratings, rating], axis=1)

    # calc vector
    rating_vector = ratings.mean(axis=1)
    return rating_vector


def update_chat_vector(chat_id, rating_vector, con):
    update_chat_vector_query = f'UPDATE Chat_rooms SET feature_vector = {rating_vector} WHERE chat_id = {chat_id};'
    sql_query(update_chat_vector_query, con)


def main():
    # user_id = 578
    # language = 'spenish'
    # chat_id = 384
    con = create_connection()
    get_user_ratings(user_id, con)
    chat_rooms = get_available_chats(MAX_USERS, LANGUAGE, con)
    # user_nuber = 1
    chat_vectors = get_chat_vectors(chat_rooms, user_nuber, con)
    update_chat_vector(chat_id, con)


if __name__ == '__main__':
    main()
