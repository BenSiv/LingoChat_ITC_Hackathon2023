"""
inference server
"""

# moduls
from test_server import greet_sf
from flask import Flask
from flask import request

def main():

    app = Flask(__name__)

    @app.route("/get_chat_id")
    def get_chat_room():
        return greet_fs()

    app.run()


if __name__ == "__main__":
    main()