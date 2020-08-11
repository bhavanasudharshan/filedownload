from functools import wraps
from http import HTTPStatus

import jwt
from bson import ObjectId
from flask import Flask, jsonify, json
from flask import Response, request

from mongodb_client import get_db

app = Flask(__name__)


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):

        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]

        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token.encode('UTF-8'), 'SECRET', algorithm='HS256')
            print("logged in user is ")
            print(data)
        except Exception as e:
            print(e)
            return jsonify({'message': 'token is invalid'+str(e)})
        return f(*args, **kwargs)

    return decorator


@app.route('/')
def index():
    resp = Response()
    resp.set_data('Welcome to File Download Microservice!')
    return resp


@app.route('/download/<uploadId>', methods=["GET"])
@token_required
def download(uploadId):
    r = Response(mimetype="application/json")
    r.headers["Content-Type"] = "application/json; charset=utf-8"

    token = request.headers['Authorization'].split(' ')[1]
    data = jwt.decode(token.encode('UTF-8'), 'SECRET', algorithm='HS256')

    upload = get_db().uploads.find_one({'_id': ObjectId(uploadId), 'status': 'done', 'users': data['sub']})
    if upload is None:
        response_body = {
            'code': 422,
            'message': "upload not found"
        }
        r.status_code = HTTPStatus.UNPROCESSABLE_ENTITY
        r.response = json.dumps(response_body)
        return
    total_chunks = len(upload['chunks'])
    if 'chunk_number' not in request.values:
        response_body = {
            'status': 'start',
            'total_chunks': total_chunks,
            'chunk_number': 0,
            'chunk':upload['chunks'][0]
        }
        r.response = json.dumps(response_body)
        return r
    elif int(request.values['chunk_number']) >= total_chunks:
        response_body = {
            'status': 'error',
            'message': 'chunk size exceeded'
        }
        r.response = json.dumps(response_body)
        return r
    elif int(request.values['chunk_number']) == total_chunks - 1:
        chunk_number = int(request.values['chunk_number'])
        response_body = {
            'status': 'done',
            'chunk': upload['chunks'][chunk_number]
        }
        r.response = json.dumps(response_body)
        return r
    else:
        chunk_number = int(request.values['chunk_number'])
        response_body = {
            'chunk': upload['chunks'][chunk_number],
            'next_chunk': chunk_number + 1
        }
        r.response = json.dumps(response_body)
        return r


if __name__ == "__main__":
    # app.run(port=8081)
    app.run(host="0.0.0.0")
            # ssl_context=("/etc/ssl/certs/pythonusersapi/cert.pem","/etc/ssl/certs/pythonusersapi/key.pem"),
            # port=8080)
