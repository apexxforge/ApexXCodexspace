from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify({
        "status": "Online",
        "message": "Bypass Backend is running successfully!"
    })

@app.route('/login', methods=['GET', 'POST'])
def login_bypass():
    # Incoming request se access_token nikalna
    access_token = request.args.get('access_token')
    
    if not access_token:
        return jsonify({
            "status": "Error",
            "message": "Access token is missing!"
        }, 400)

    # Naye domain par request map aur bypass handle karna
    target_server_url = f"https://loginbp.ppmainecoonghj.com/login?access_token={access_token}"
    
    # Yahan aap chahe toh requests.get(target_server_url) karke response bhi forward kar sakte hain
    return jsonify({
        "serverUrl": target_server_url,
        "status": "Success",
        "bypass": True,
        "message": "Request successfully bypassed and config generated."
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    
