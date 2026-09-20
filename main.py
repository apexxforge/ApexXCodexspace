from flask import Flask, request, jsonify, Response
import json

app = Flask(__name__)

@app.route('/PING', methods=['POST'])
def ping():
    return jsonify({"status": 0, "message": "PONG"})

@app.route('/GetLoginData', methods=['POST'])
def get_login_data():
    # Game yahan account settings aur server profile maangta hai
    data = {
        "status": 0,
        "config": {
            "announcement_url": "",
            "customer_service_url": ""
        },
        "account_info": {
            "account_id": 17023400447,
            "nickname": "YwxXUWbIVBlV"
        }
    }
    return jsonify(data)

@app.route('/LoginGetSplash', methods=['POST'])
def login_get_splash():
    return jsonify({"status": 0, "splash_url": ""})

@app.route('/GetLoginDesc', methods=['POST'])
def get_login_desc():
    return jsonify({"status": 0, "description": "Active"})

@app.route('/LoginGetAccountInfo', methods=['POST'])
def login_get_account_info():
    return jsonify({
        "status": 0,
        "account_id": 17023400447,
        "nickname": "YwxXUWbIVBlV",
        "region": "IND",
        "gold": 999999,
        "diamond": 999999
    })

@app.route('/LoginGetProfile', methods=['POST'])
def login_get_profile():
    return jsonify({
        "status": 0,
        "profile": {
            "avatar": 102000007,
            "level": 70,
            "likes": 9999
        }
    })

@app.route('/GetPlayerDailyRankingSummary', methods=['POST'])
def daily_ranking():
    return jsonify({"status": 0, "rank": 1})

@app.route('/GetPlayerPersonalshow', methods=['POST'])
def personal_show():
    return jsonify({"status": 0, "items": []})

@app.route('/Get friend', methods=['POST'])
def get_friend():
    return jsonify({"status": 0, "friends": []})

@app.route('/GetPlatformProfile', methods=['POST'])
def platform_profile():
    return jsonify({"status": 0})

@app.route('/GetAccountFreshInfo', methods=['POST'])
def fresh_info():
    return jsonify({"status": 0})

@app.route('/GetPrimeAccountInfo', methods=['POST'])
def prime_info():
    return jsonify({"status": 0, "is_prime": True})

@app.route('/GetWishListItem', methods=['POST'])
def wishlist():
    return jsonify({"status": 0, "items": []})

@app.route('/GetAccountWeapon', methods=['POST'])
def account_weapon():
    return jsonify({"status": 0, "weapons": []})

@app.route('/GetWeaponExpInfo', methods=['POST'])
def weapon_exp():
    return jsonify({"status": 0})

@app.route('/GetFriendRequestList', methods=['POST'])
def friend_requests():
    return jsonify({"status": 0, "requests": []})

# Generic fallback for any missed endpoints in the loop
@app.route('/<path:subpath>', methods=['POST', 'GET'])
def catch_all(subpath):
    return jsonify({"status": 0, "message": f"Handled {subpath}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
    
