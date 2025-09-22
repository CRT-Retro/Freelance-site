from flask import Flask, g, request, jsonify, render_template, session, redirect, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta

app = Flask(__name__)
app.secret_key = "supersecretkey123"  
app.permanent_session_lifetime = timedelta(minutes=30)

DATABASE = "database.db"
# دیتابیس
def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()

# مسیر اصلی 
@app.route("/")
def index():
    if "username" in session:
        return f"ورود {session['username']}! <a href='/logout'>خروج</a>"
    return "فلسک ران میشه. <a href='/login'>ورود</a> | <a href='/register'>ثبت‌نام</a>"

# ثبت‌نام 
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        job_title = request.form.get("job_title", "")
        location = request.form.get("location", "")

        db = get_db()
        existing_user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if existing_user:
            return "کاربر با این نام وجود دارد!"

        hashed_password = generate_password_hash(password)
        db.execute(
            "INSERT INTO users (username, password, job_title, location) VALUES (?, ?, ?, ?)",
            (username, hashed_password, job_title, location)
        )
        db.commit()
        return redirect(url_for("login"))

    return render_template("register.html")

# ورود 
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        db = get_db()
        user = db.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if user and check_password_hash(user["password"], password):
            session.permanent = True
            session["username"] = user["username"]
            session["user_id"] = user["id"]
            return redirect(url_for("index"))
        return "نام کاربری یا رمز عبور اشتباه است!"

    return render_template("login.html")

# خروج
@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("user_id", None)
    return redirect(url_for("index"))

# مسیر کاربران با فیلتر 
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

    # فیلتر نام یا عنوان شغلی
    name = request.args.get("name")
    if name:
        query += " AND (u.username LIKE ? OR u.job_title LIKE ?)"
        params.extend([f"%{name}%", f"%{name}%"])

    # فیلتر مهارت
    skill = request.args.get("skill")
    if skill:
        query += " AND s.skill LIKE ?"
        params.append(f"%{skill}%")

    # فیلتر لوکیشن
    location = request.args.get("location")
    if location:
        query += " AND u.location LIKE ?"
        params.append(f"%{location}%")

    query += " GROUP BY u.id"

    rows = db.execute(query, params).fetchall()
    users = [dict(row) for row in rows]

    return jsonify(users)

# پروفایل فریلنسر 
@app.route("/freelancers/<int:id>")
def freelancer_profile(id):
    db = get_db()

    user = db.execute("""
        SELECT u.*, GROUP_CONCAT(s.skill, ', ') AS skills
        FROM users u
        LEFT JOIN skills s ON u.id = s.user_id
        WHERE u.id = ?
        GROUP BY u.id
    """, (id,)).fetchone()

    if user is None:
        return "کاربر پیدا نشد", 404

    portfolios = db.execute("SELECT * FROM portfolios WHERE user_id = ?", (id,)).fetchall()

    return render_template("profile.html", user=user, portfolios=portfolios)

if name == "__main__":
    app.run(debug=True)