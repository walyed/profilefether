"""
Instagram Profile Picture Proxy — Railway Deployment
Fetches Instagram profile pictures using this server's IP.
"""
import os
import requests
from bs4 import BeautifulSoup
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

API_SECRET = os.environ.get("PROXY_SECRET", "instacontest-proxy-2026")


def fetch_profile_pic(username: str) -> dict:
    url = f"https://www.instagram.com/{username}/"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        resp = requests.get(url, headers=headers, timeout=15)
    except Exception as e:
        return {"error": str(e), "image": None, "status": 0, "loginWall": False}

    login_wall = "/accounts/login" in resp.text

    if resp.status_code != 200:
        return {
            "error": f"HTTP {resp.status_code}",
            "image": None,
            "status": resp.status_code,
            "loginWall": login_wall,
        }

    soup = BeautifulSoup(resp.text, "html.parser")
    og = soup.find("meta", property="og:image")

    if og and og.get("content"):
        img_url = og["content"]
        if "/rsrc.php/" in img_url or "static.cdninstagram.com" in img_url:
            return {
                "error": "Got Instagram logo, not real profile pic",
                "image": None,
                "status": resp.status_code,
                "htmlLen": len(resp.text),
                "loginWall": login_wall,
            }
        return {
            "error": None,
            "image": img_url,
            "status": resp.status_code,
            "loginWall": login_wall,
        }

    return {
        "error": "No og:image found",
        "image": None,
        "status": resp.status_code,
        "htmlLen": len(resp.text),
        "loginWall": login_wall,
    }


@app.route("/api/instagram", methods=["GET"])
def instagram_endpoint():
    secret = request.headers.get("x-proxy-secret", "")
    if secret != API_SECRET:
        return jsonify({"error": "Unauthorized"}), 401

    username = request.args.get("username", "").strip().lstrip("@")
    if not username or len(username) > 30:
        return jsonify({"error": "Invalid username"}), 400

    result = fetch_profile_pic(username)
    return jsonify(result)


@app.route("/health", methods=["GET"])
def health():
    # Also show the server's IP so we can check if it's datacenter
    try:
        ip = requests.get("https://api.ipify.org", timeout=5).text
    except Exception:
        ip = "unknown"
    return jsonify({"status": "ok", "serverIp": ip})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    app.run(host="0.0.0.0", port=port)
