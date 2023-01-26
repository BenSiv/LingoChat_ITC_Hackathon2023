"""
inference server
"""

import sys
sys.path.insert(0, "../src/")

# moduls
from model import *
from db_queries import *
from flask import Flask
from flask import request
import pandas as pd
import numpy as np

def main():

    THRESHOLD = 1.7
    app = Flask(__name__)

    @app.route("/get_chat_id")
    def get_id():
        print("start")
        con = create_connection()

        feature_inputs = request.args.to_dict()
        print(feature_inputs)
        # example:
        # feature_inputs = {"user_id" : 823, "language" : "english", "max_users" : 6}
        max_users = int(feature_inputs["max_users"])
        user_id = int(feature_inputs["user_id"])
        print(user_id,max_users)

        user_vector = get_user_vector(user_id, con)
        print(user_vector)
        available_chats = get_available_chats(max_users, feature_inputs["language"], con)
        for user_number, chat_rooms in available_chats.items():
            current_chat_vectors = get_chat_vectors(chat_rooms, con)
            if len(current_chat_vectors) == 0:
                continue
            distances = np.array(distance_vectorized(current_chat_vectors, user_vector))
            print(distances)
            if len(distances) == 0:
                continue
            min_dist = distances.min()
            argmin_dist = distances.argmin()
            if min_dist < THRESHOLD:
                return str(chat_rooms[argmin_dist])
        return "0"

    @app.route("/update_vector")
    def update_vec():
        print("start")
        con = create_connection()

        inputs = request.args.to_dict()
        # example:
        # inputs = {"chat_id" : 450}
        chat_id = int(inputs["chat_id"])
        print(inputs)
        rating_vector = calc_chat_vector(chat_id, con)
        update_chat_vector(chat_id, rating_vector, con)
        return "done"

    app.run(host='0.0.0.0', port=8080)


if __name__ == "__main__":
    main()