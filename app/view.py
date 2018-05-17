from app import app
from flask import request, jsonify
import traceback
from .manager import APIHandler

def processFail():
    message = APIAdmin.process("fail").getMessage()
    viewLog("fail")
    return jsonify(message)

@app.route("/keyboard", methods=["GET"])
def yellow_keyboard():
    message, code = APIHandler.process("home")
    return jsonify(message), code


@app.route("/message", methods=["POST"])
def yellow_message():
    try:
        message, code = APIHandler.process("message", request.json)
        return jsonify(message), code
    except:
        traceback.print_exc()
        return processFail(), 400

@app.route("/friend", methods=["POST"])
def yellow_friend_add():
    message, code = APIHandler.process("add", request.json)
    return jsonify(message), code


@app.route("/friend/<key>", methods=["DELETE"])
def yellow_friend_block(key):
    message, code = APIHandler.process("block", key)
    return jsonify(message), code


@app.route("/chat_room/<key>", methods=["DELETE"])
def yellow_exit(key):
    message, code = APIHandler.process("exit", key)
    return jsonify(message), code
