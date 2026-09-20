import base64
import json
import os
from flask import Flask, jsonify, request

app = Flask(__name__)


# JWT Token ko decode karne ka function (Without external secret verification for local bypass)
def decode_jwt(auth_header):
  try:
    if not auth_header or not auth_header.startswith('Bearer '):
      return None
    token = auth_header.split(' ')[1]
    parts = token.split('.')
    if len(parts) < 2:
      return None

    # Base64 padding fix
    payload_part = parts[1]
    payload_part += '=' * (-len(payload_part) % 4)
    decoded_bytes = base64.urlsafe_b64decode(payload_part)
    return json.loads(decoded_bytes.decode('utf-8'))
  except Exception as e:
    print(f'JWT Decode Error: {e}')
    return None


@app.route('/PING', methods=['POST'])
def handle_ping():
  return jsonify({'status': 0, 'message': 'pong', 'server_time': 1789569455})


@app.route('/GetLoginData', methods=['POST'])
def handle_get_login_data():
  auth_header = request.headers.get('Authorization')
  jwt_data = decode_jwt(auth_header)
  account_id = (
      jwt_data.get('account_id', 17023400447) if jwt_data else 17023400447
  )
  nickname = jwt_data.get('nickname', 'YwxWUwBiUBlV') if jwt_data else 'Player'
  region = jwt_data.get('noti_region', 'IND') if jwt_data else 'IND'

  return jsonify({
      'account_id': account_id,
      'nickname': nickname,
      'region': region,
      'is_banned': False,
      'gold': 999999,
      'diamond': 999999,
      'level': 80,
      'avatar': 102000007,
  })


@app.route('/LoginGetSplash', methods=['POST'])
def handle_splash():
  return jsonify({
      'status': 0,
      'splash_url': '',
      'announcement': 'Welcome to Custom Bypass Server',
  })


@app.route('/GetLoginDesc', methods=['POST'])
def handle_login_desc():
  return jsonify({'status': 0, 'description': 'OB55 Bypass Active'})


@app.route('/LoginGetAccountInfo', methods=['POST'])
def handle_account_info():
  auth_header = request.headers.get('Authorization')
  jwt_data = decode_jwt(auth_header)
  account_id = (
      jwt_data.get('account_id', 17023400447) if jwt_data else 17023400447
  )
  nickname = jwt_data.get('nickname', 'YwxWUwBiUBlV') if jwt_data else 'Player'

  return jsonify({
      'account_id': account_id,
      'nickname': nickname,
      'exp': 50000,
      'badge_count': 100,
  })


@app.route('/LoginGetProfile', methods=['POST'])
def handle_login_profile():
  return jsonify({
      'status': 0,
      'profile': {'likes': 9999, 'booyah_count': 500, 'region': 'IND'},
  })


@app.route('/GetPlayerDailyRankingSummary', methods=['POST'])
def handle_daily_ranking():
  return jsonify({'status': 0, 'rank': 1, 'score': 99999})


@app.route(
    '/<path:subpath>', methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
)
def catch_all(subpath):
  # Baaki saare bache hue endpoints ke liye generic success response
  print(f'Catch-all hit for endpoint: /{subpath}')
  return jsonify({'status': 0, 'message': 'success', 'data': {}})


if __name__ == '__main__':
  port = int(os.environ.get('PORT', 8080))
  app.run(host='0.0.0.0', port=port)
    
