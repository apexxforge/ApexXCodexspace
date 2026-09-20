import base64
import json
import os
from flask import Flask, jsonify, request

app = Flask(__name__)


def decode_jwt(auth_header):
  try:
    if not auth_header or not auth_header.startswith('Bearer '):
      return None
    token = auth_header.split(' ')[1]
    parts = token.split('.')
    if len(parts) < 2:
      return None
    payload_part = parts[1] + '=' * (-len(parts[1]) % 4)
    return json.loads(
        base64.urlsafe_b64decode(payload_part).decode('utf-8')
    )
  except:
    return None


# Generic handler jo game ke har request ko success status 0 ke sath respond karega
def success_response(extra_data=None):
  base = {'error_code': 0, 'status': 0, 'message': 'success'}
  if extra_data:
    base.update(extra_data)
  return jsonify(base)


@app.route(
    '/<path:path>/Ping',
    methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
)
@app.route('/Ping', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def handle_ping_path(path=''):
  return success_response({'msg': 'pong'})


@app.route(
    '/<path:path>/MajorLogin',
    methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
)
@app.route('/MajorLogin', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])
def handle_major_login(path=''):
  auth_header = request.headers.get('Authorization')
  jwt_data = decode_jwt(auth_header)
  acc_id = jwt_data.get('account_id', 17023400447) if jwt_data else 17023400447
  nick = jwt_data.get('nickname', 'Player') if jwt_data else 'Player'

  return success_response({
      'account_id': acc_id,
      'nickname': nick,
      'token': (
          auth_header.split(' ')[1] if auth_header else 'mock_token'
      ),
      'server_time': 1789569455,
  })


@app.route(
    '/<path:path>/GetLoginData',
    methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
)
@app.route(
    '/GetLoginData', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
)
def handle_get_login_data(path=''):
  auth_header = request.headers.get('Authorization')
  jwt_data = decode_jwt(auth_header)
  return success_response({
      'account_id': (
          jwt_data.get('account_id', 17023400447) if jwt_data else 17023400447
      ),
      'nickname': (
          jwt_data.get('nickname', 'YwxWUwBiUBlV') if jwt_data else 'Player'
      ),
      'region': 'IND',
      'is_banned': False,
  })


@app.route(
    '/<path:path>/LoginGetSplash',
    methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
)
@app.route(
    '/LoginGetSplash', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
)
def handle_splash(path=''):
  return success_response({'splash_url': ''})


@app.route(
    '/<path:path>/GetLoginDesc',
    methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
)
@app.route(
    '/GetLoginDesc', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
)
def handle_login_desc(path=''):
  return success_response({'description': 'Bypass Active'})


@app.route(
    '/<path:path>/LoginGetAccountInfo',
    methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
)
@app.route(
    '/LoginGetAccountInfo', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
)
def handle_account_info(path=''):
  return success_response()


@app.route(
    '/<path:path>/LoginGetProfile',
    methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'],
)
@app.route(
    '/LoginGetProfile', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
)
def handle_profile(path=''):
  return success_response()


@app.route(
    '/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
)
def catch_all(subpath):
  return success_response()


if __name__ == '__main__':
  port = int(os.environ.get('PORT', 8080))
  app.run(host='0.0.0.0', port=port)
  
