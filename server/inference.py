"""
inference server
"""

# moduls
from try_model import *
from flask import Flask
from flask import request

def main():

    app = Flask(__name__)

    @app.route("/get_chat_id")
    def get_chat_room():
        feature_inputs = request.args.to_dict()
        # example:
        # feature_inputs = {"user_id" : 1, "language" : "english", "max_users" : 6}

        # return greet_fs()

    app.run(host='0.0.0.0', port=8080)


if __name__ == "__main__":
    main()