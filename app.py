from flask import Flask, g, request, jsonify, b, session, redirect, url_for, abort
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import timedelta
import os

app = Flask(__name__)
app.secret_key = "supersecretkey123"
app.permanent_session_lifetime = timedelta(minutes=30)

database = "database.db"

# تنظیمات آپلود 
folder = "static/avatars"
a = {"png", "jpg", "jpeg", "gif"}
os.makedirs(folder, exist_ok=True)
app.config["folder"] = folder

def file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in a 

# اتصال دیتابیس 
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

#  مسیر اصلی 
@app.route("/")
def index():
    if "username" in session:
        return f"سلام {session['username']}! <a href='/logout'>خروج</a>"
    return "فلسک ران میشه. <a href='/login'>ورود</a> | <a href='/register'>ثبت‌نام</a>"

#  ثبت‌نام 
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

    return b("register.html")

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

    return b("login.html")

#  خروج 
@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("user_id", None)
    return redirect(url_for("index"))
      # مسیر کاربران
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

    # نام یا عنوان شغلی
    name = request.args.get("name")
    if name:
        query += " AND (u.username LIKE ? OR u.job_title  LIKE ?)"
        params.extend([f"%{name}%", f"%{name}%"])

    #  مهارت
    skill = request.args.get("skill")
    if skill:
        query += " AND s.skill LIKE ?"
        params.append(f"%{skill}%")

    #  لوکیشن
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
def freelancer(id):
    db = get_db()

    # اطلاعات کاربر و مهارت‌ها
    user = db.execute("""
        SELECT u.*, GROUP_CONCAT(s.skill, ', ') AS skills
        FROM users u
        LEFT JOIN skills s ON u.id = s.user_id
        WHERE u.id = ?
        GROUP BY u.id
    """, (id,)).fetchone()
    if user is None:
        return "کاربر پیدا نشد", 404
    # نمونه‌کارها
    portfolios = db.execute("SELECT * FROM portfolios WHERE user_id = ?", (id,)).fetchall()

    # نظرات فریلنسر
    reviews = db.execute("""
        SELECT r.*, u.username AS employer_name
        FROM reviews r
        JOIN users u ON r.employer_id = u.id
        WHERE r.freelancer_id=?
    """, (id,)).fetchall()

    return b("profile.html", user=user, portfolios=portfolios, reviews=reviews)
# پروفایل خود کاربر 
@app.route("/profile")
def my_profile():
    if "user_id" not in session:
        return redirect(url_for("login"))

    db = get_db()
    user_id = session["user_id"]

    user = db.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    skills = db.execute("SELECT skill FROM skills WHERE user_id=?", (user_id,)).fetchall()

    return b("my_profile.html", user=user, skills=[s["skill"] for s in skills])

#  ویرایش پروفایل 
@app.route("/profile/edit", methods=["GET", "POST"])
def edit_profile():
    if "user_id" not in session:
        return redirect(url_for("login"))

    db = get_db()
    user_id = session["user_id"]

    if request.method == "POST":
        bio = request.form.get("bio", "")
        rate = request.form.get("rate", "")
        job_title= request.form.get("job_title", "")
        location = request.form.get("location", "")
        skills = request.form.get("skills", "")

        avatar_path = None
        if "avatar" in request.files:
            file = request.files["avatar"]
            if file and file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file.save(filepath)
                avatar_path = filename

        if avatar_path:
            db.execute("UPDATE users SET bio=?, rate=?, job_title=?, location=?, avatar=? WHERE id=?",
                       (bio, rate, job_title, location, avatar_path, user_id))
        else:
            db.execute("UPDATE users SET bio=?, rate=?, job_title=?, location=? WHERE id=?",
                       (bio, rate, job_title, location, user_id))

        # بروزرسانی مهارت‌ها
        db.execute("DELETE FROM skills WHERE user_id=?", (user_id,))
        for skill in skills.split(","):
            skill = skill.strip()
            if skill:
                db.execute("INSERT INTO skills (user_id, skill) VALUES (?, ?)", (user_id, skill))

        db.commit()
        return redirect(url_for("my_profile"))

    # فرم با اطلاعات
    user = db.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    skills = db.execute("SELECT skill FROM skills WHERE user_id=?", (user_id,)).fetchall()
    skills_str = ", ".join([s["skill"] for s in skills])

    return b("edit_profile.html", user=user, skills=skills_str)

#  افزودن نظر برای فریلنسر 
@app.route("/freelancers/<int:freelancer_id>/reviews", methods=["GET", "POST"])
def freelancer_reviews(freelancer_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    db = get_db()
    employer_id = session["user_id"]

    if request.method == "POST":
        rating = request.form.get("rating")
        comment = request.form.get("comment", "")

        # بررسی اینکه کارفرما قبلاً نظر داده باشد
        existing = db.execute(
            "SELECT * FROM reviews WHERE freelancer_id=? AND employer_id=?",
            (freelancer_id, employer_id)
        ).fetchone()

        if existing:
            return"نظر شما قبلا درمورد این فریلنسر ثبت شده است!", 400

        db.execute(
            "INSERT INTO reviews (freelancer_id, employer_id, rating, comment) VALUES (?, ?, ?, ?)",
            (freelancer_id, employer_id, rating, comment)
        )
        db.commit()
        return redirect(url_for("freelancer_reviews", freelancer_id=freelancer_id))

    # نمایش همه نظرات برای فریلنسر
    reviews = db.execute("""
        SELECT r.*, u.username AS employer_name
        FROM reviews r
        JOIN users u ON r.employer_id = u.id
        WHERE r.freelancer_id=?
    """, (freelancer_id,)).fetchall()
    return b("reviews.html", reviews=reviews, freelancer_id=freelancer_id)

    # علاقه ها
  favorites = {}
  c = "secret"
  def require_auth(f):
    def wrapper(*args, **kwargs):
        c = request.headers.get("Authorization")
        if not c or c != f"Bearer {c}":
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route("/favorites/<username>", methods=["GET"])
@require_auth
def favorites(username):
    favorite = users_favorite.get(username, [])
    return jsonify({"favorites": favorite})

@app.route("/favorites/<username>", methods=["POST"])
@require_auth
def add_favorite(username):
    data = request.json
    if not data or "item" not in data:
        return jsonify({"error": "Missing 'item' in request"}), 400

    item = data["item"]
    favorites(username, [])
    
    if item in favorites[username]:
        return jsonify({"message": "Item already in favorites"}), 409
    
    favorites[username].append(item)
    return jsonify({"message": "Added successfully", "favorites": favorites[username]}), 201

@app.route("/favorites/<username>", methods=["DELETE"])
@require_auth
def rfavorite(username):
    data = request.json
    if not data or "item" not in data:
        return jsonify({"error": "Missing 'item' in request"}), 400

    item = data["item"]
    if username not in favorites or item not in favorites[username]:
        return jsonify({"message": "Item not found"}), 404
    
     favorites[username].remove(item)
    return jsonify({"message": "Removed successfully", "favorites": favorites[username]}), 200



if name == "__main__":
    app.run(debug=True)