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


def get_user_age(user_id, con):
    user_age_query = f'''SELECT age FROM Users where id = {user_id};'''
    age = sql_query(user_age_query, con)[0][0]
    return np.array([age])

def get_user_ratings(user_id, con):
    user_ratings_query = f'''SELECT interests_id,rating FROM Users_Interests where user_id = {user_id};'''
    ratings = np.array(sql_query(user_ratings_query, con))[:, 1]
    return ratings

def get_user_vector(user_id, con):
    age = get_user_age(user_id, con)
    age_scaled = age / 100

    ratings = get_user_ratings(user_id, con)
    ratings_scaled = ratings / 5

    return np.concatenate([age_scaled, ratings_scaled])


def get_available_chats(max_users, language, con):
    chat_rooms = {}
    for num in range(1, 6):
        Chat_rooms_id_query = f'''SELECT id FROM Chat_Rooms WHERE active_users={num} AND language='{language}';'''
        Chat_rooms_id = sql_query(Chat_rooms_id_query, con)
        chat_rooms[num] = np.array(Chat_rooms_id, dtype=int).flatten()
    return chat_rooms


def get_chat_vectors(chat_rooms, con):
    if len(chat_rooms) == 0:
        answer = tuple()
    elif len(chat_rooms) == 1:
        Chat_vectors_query = f'''SELECT chat_vector FROM Chat_Rooms where id={chat_rooms[0]};'''
        answer = sql_query(Chat_vectors_query, con)
    else:
        Chat_vectors_query = f'''SELECT chat_vector FROM Chat_Rooms where id in {tuple(chat_rooms)};'''
        answer = sql_query(Chat_vectors_query, con)

    ans_vecs = list()
    for ans in answer:
        if ans[0] is not None:
            vec = (
                ans[0]
                .replace("(", "")
                .replace(")", "")
                .split(", ")
            )
            flt_vec = [float(v) for v in vec]
            ans_vecs.append(flt_vec)

    return np.array(ans_vecs)


def calc_chat_vector(chat_id, con):
    # get all users id
    Chat_users_query = f'''SELECT user_id FROM User_Chat WHERE chat_id = {chat_id} AND leave_timestamp IS NULL;'''
    Chat_users = sql_query(Chat_users_query, con)

    # get users ratings
    user_vectors = list()
    for Chat_user in Chat_users:
        user_vector = get_user_vector(Chat_user[0], con)
        user_vectors.append(user_vector)
    user_vectors = np.array(user_vectors)

    # calc vector
    chat_vector = user_vectors.mean(axis=0)
    return chat_vector


def update_chat_vector(chat_id, chat_vector, con):
    update_chat_vector_query = f'''UPDATE Chat_Rooms SET chat_vector = "{tuple(chat_vector)}" WHERE id = {chat_id};'''
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
