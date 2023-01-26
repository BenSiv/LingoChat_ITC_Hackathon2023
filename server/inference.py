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
    def get_chat_id():

        con = create_connection()

        feature_inputs = request.args.to_dict()
        # example:
        # feature_inputs = {"user_id" : 823, "language" : "english", "max_users" : 6}
        user_vector = get_user_vector(feature_inputs["user_id"], con)
        available_chats = get_available_chats(feature_inputs["max_users"], feature_inputs["language"], con)
        for user_number, chat_rooms in available_chats.items():
            current_chat_vectors = get_chat_vectors(chat_rooms, con)
            distances = np.array(distance_vectorized(current_chat_vectors, user_vector))
            min_dist = distances.min()
            argmin_dist = distances.argmin()
            if min_dist < THRESHOLD:
                return chat_rooms[argmin_dist]
        return 0

    @app.route("/update_chat_vector")
    def update_chat_vector():

        con = create_connection()

        inputs = request.args.to_dict()
        # example:
        # inputs = {"chat_id" : 450}
        rating_vector = calc_chat_vector(inputs["chat_id"], con)
        update_chat_vector(inputs["chat_id"], rating_vector, con)


    app.run(host='0.0.0.0', port=8080)


if __name__ == "__main__":
    main()