from flask import Flask, g, request, jsonify
import sqlite3

app = Flask(__name__)
DATABASE = "database.db"

# اتصال به دیتابیس
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

# بستن اتصال دیتابیس بعد از هر درخواست
@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()
# صفحه ی اصلی 
@app.route("/")
def index():
    return {"message": "Flask API is running!"}

# route کاربران با فیلتر
@app.route("/users", methods=["GET"])
def get_users():
    db = get_db()
    query = """
        SELECT u.*
        FROM users u
        LEFT JOIN skills s ON u.id = s.user_id
        WHERE 1=1
    """
    params = []

    # فیلتر بر اساس نام
    name = request.args.get("name")
    if name:
        query += " AND (u.username LIKE ? OR u.job_title LIKE ?)"
        params.extend([f"%{name}%", f"%{name}%"])

    # فیلتر بر اساس مهارت ها
    skill = request.args.get("skill")
    if skill:
        query += " AND s.skill LIKE ?"
        params.append(f"%{skill}%")

    # فیلتر بر اساس لوکیشن
    location = request.args.get("locarion")
    if location:
        query += " AND u.location LIKE ?"
        params.append(f"%{location}%")

    query += " GROUP BY u.id"

    rows = db.execute(query, params).fetchall()
    users = [dict(row) for row in rows]

    return jsonify(users)

if name == "__main__":
    app.run(debug=True)