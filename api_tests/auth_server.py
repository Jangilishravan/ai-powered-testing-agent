from flask import Flask, request, jsonify

app = Flask(__name__)

# Demo tokens
TOKENS = {
    "sunny123": "user",
    "admin123": "admin"
}

@app.route("/profile", methods=["GET"])
def profile():

    auth_header = request.headers.get("Authorization")

    if not auth_header:
        return jsonify({"error": "Token missing"}), 401

    if not auth_header.startswith("Bearer "):
        return jsonify({"error": "Invalid authentication format"}), 401

    token = auth_header.split(" ", 1)[1]

    if token not in TOKENS:
        return jsonify({"error": "Invalid token"}), 401

    return jsonify({"message": "Profile accessed successfully"}), 200


@app.route("/admin", methods=["GET"])
def admin():

    auth_header = request.headers.get("Authorization")

    if not auth_header or not auth_header.startswith("Bearer "):
        return jsonify({"error": "Authentication required"}), 401

    token = auth_header.split(" ", 1)[1]

    if token not in TOKENS:
        return jsonify({"error": "Invalid token"}), 401

    if TOKENS[token] != "admin":
        return jsonify({"error": "Admin permission required"}), 403

    return jsonify({"message": "Welcome Admin!"}), 200

@app.route("/login", methods=["POST"])
def login():

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({"error": "Request body is required"}), 400

    username = data.get("username")
    password = data.get("password")

    # Validate data types
    if not isinstance(username, str) or not isinstance(password, str):
        return jsonify({
            "error": "Username and password must be strings"
        }), 400

    # Both fields empty
    if not username.strip() and not password.strip():
        return jsonify({
            "error": "Username and password are required"
        }), 400

    # Missing username
    if not username.strip():
        return jsonify({
            "error": "Username is required"
        }), 400

    # Missing password
    if not password.strip():
        return jsonify({
            "error": "Password is required"
        }), 400

    # Validate username format
    if not username.isalnum():
        return jsonify({
            "error": "Username format is invalid"
        }), 400

    # Username length validation
    if len(username) < 3 or len(username) > 20:
        return jsonify({
            "error": "Username must be between 3 and 20 characters"
        }), 400

    # Password length validation
    if len(password) < 6 or len(password) > 30:
        return jsonify({
            "error": "Password must be between 6 and 30 characters"
        }), 400

    # Check credentials
    if username != "sunny" or password != "sunny123":
        return jsonify({
            "error": "Invalid username or password"
        }), 401

    return jsonify({
        "message": "Login successful"
    }), 200
if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
