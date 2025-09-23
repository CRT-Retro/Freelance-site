from flask import Flask, g, request, jsonify, session, redirect, url_for, abort, render_template, render_template_string, escape, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey, String, Text
from sqlalchemy.orm import relationship
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import timedelta
import os
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

app = Flask(__name__)
app.secret_key = "supersecretkey123"
app.permanent_session_lifetime = timedelta(minutes=30)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///search_example.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['MAX_CONTENT_LENGTH'] = 1024
csrf = CSRFProtect(app)
db = SQLAlchemy(app)
daitabase = "database.db"


class CommentForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=20)])
    comment = StringField('Comment', validators=[DataRequired(), Length(max=200)])
    submit = SubmitField('Submit')

def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(daitabase)
        g.db.row_factory = sqlite3.Row
    return g.db

@app.teardown_appcontext
def close_db(exception):
    db_conn = g.pop("db", None)
    if db_conn is not None:
        db_conn.close()

#  آپلود 
folder = "static/avatars"
a = {"png", "jpg", "jpeg", "gif"}
os.makedirs(folder, exist_ok=True)
app.config["folder"] = folder
app.config["UPLOAD_FOLDER"] = folder

def file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in a 

# SEO 
@app.route("/")
def index():
    title = "صفحه اصلی - فریلنسرها"
    description = "به پلتفرم ما خوش آمدید! فریلنسرها و مهارت‌های مختلف را جستجو کنید."
    if "username" in session:
        user_msg = f"سلام {session['username']}! <a href='/logout'>خروج</a>"
    else:
        user_msg = "فلسک ران میشه. <a href='/login'>ورود</a> | <a href='/register'>ثبت‌نام</a>"
    return render_template_string("""
        <!doctype html>
        <html>
        <head>
            <title>{{ title }}</title>
            <meta name="description" content="{{ description }}">
        </head>
        <body>
            {{ user_msg|safe }}
        </body>
        </html>
    """, title=title, description=description, user_msg=user_msg)

@app.route('/comment', methods=['GET', 'POST'])
def comment_form():
    form = CommentForm()
    if form.validate_on_submit():
        safe_username = escape(form.username.data)
        safe_comment = escape(form.comment.data)
        flash(f"Received comment from {safe_username}: {safe_comment}")
    elif request.method == 'POST':
        flash("Form validation failed. Please check your inputs.")
    return render_template_string('''
        <!doctype html>
        <title>Secure Form</title>
        <h1>Submit Comment</h1>
        <form method="POST">
            {{ form.hidden_tag() }}
            <p>{{ form.username.label }}<br>{{ form.username(size=20) }}</p>
            <p>{{ form.comment.label }}<br>{{ form.comment(size=50) }}</p>
            <p>{{ form.submit() }}</p>
        </form>
        {% with messages = get_flashed_messages() %}
          {% if messages %}
            <ul>
            {% for msg in messages %}
              <li>{{ msg }}</li>
            {% endfor %}
            </ul>
          {% endif %}
        {% endwith %}
    ''', form=form)   

# ثبت‌نام 
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        job_title = request.form.get("job_title", "")
        location = request.form.get("location", "")
        db_conn = get_db()
        existing_user = db_conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
        if existing_user:
            return "کاربر با این نام وجود دارد!"
        hashed_password = generate_password_hash(password)
        db_conn.execute(
            "INSERT INTO users (username, password, job_title, location) VALUES (?, ?, ?, ?)",
            (username, hashed_password, job_title, location)
        )
        db_conn.commit()
        return redirect(url_for("login"))
    return render_template("register.html")

# ورود 
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db_conn = get_db()
        user = db_conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()
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

# مسیر کاربران 
@app.route("/users", methods=["GET"])
def get_users():
    db_conn = get_db()
    query = """
        SELECT u.*
        FROM users u
        LEFT JOIN skills s ON u.id = s.user_id
        WHERE 1=1
    """
    params = []

    name = request.args.get("name")
    if name:
        query += " AND (u.username LIKE ? OR u.job_title LIKE ?)"
        params.extend([f"%{name}%", f"%{name}%"])

    skill = request.args.get("skill")
    if skill:
        query += " AND s.skill LIKE ?"
        params.append(f"%{skill}%")

    location = request.args.get("location")
    if location:
        query += " AND u.location LIKE ?"
        params.append(f"%{location}%")

    query += " GROUP BY u.id"
    rows = db_conn.execute(query, params).fetchall()
    users = [dict(row) for row in rows]
    return jsonify(users)

# پروفایل فریلنسر 
@app.route("/freelancers/<int:id>")
def freelancer(id):
    db_conn = get_db()
    user = db_conn.execute("""
        SELECT u.*, GROUP_CONCAT(s.skill, ', ') AS skills
        FROM users u
        LEFT JOIN skills s ON u.id = s.user_id
        WHERE u.id = ?
        GROUP BY u.id
    """, (id,)).fetchone()
    if user is None:
        return "کاربر پیدا نشد", 404

    portfolios = db_conn.execute("SELECT * FROM portfolios WHERE user_id = ?", (id,)).fetchall()
    reviews = db_conn.execute("""
        SELECT r.*, u.username AS employer_name
        FROM reviews r
        JOIN users u ON r.employer_id = u.id
        WHERE r.freelancer_id=?
    """, (id,)).fetchall()

    return render_template("profile.html", user=user, portfolios=portfolios, reviews=reviews)

# پروفایل خود کاربر 
@app.route("/profile")
def my_profile():
    if "user_id" not in session:
        return redirect(url_for("login"))

    db = get_db()
    user_id = session["user_id"]

    user = db.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    skills = db.execute("SELECT skill FROM skills WHERE user_id=?", (user_id,)).fetchall()

    return render_template("my_profile.html", user=user, skills=[s["skill"] for s in skills])

# ویرایش پروفایل 
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
            file_obj = request.files["avatar"]
            if file_obj and file(file_obj.filename):
                filename = secure_filename(file_obj.filename)
                filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
                file_obj.save(filepath)
                avatar_path = filename

        if avatar_path:
            db.execute("UPDATE users SET bio=?, rate=?, job_title=?, location=?, avatar=? WHERE id=?",
                       (bio, rate, job_title, location, avatar_path, user_id))
        else:
            db.execute("UPDATE users SET bio=?, rate=?, job_title=?, location=? WHERE id=?",
                       (bio, rate, job_title, location, user_id))

        db.execute("DELETE FROM skills WHERE user_id=?", (user_id,))
        for skill in skills.split(","):
            skill = skill.strip()
            if skill:
                db.execute("INSERT INTO skills (user_id, skill) VALUES (?, ?)", (user_id, skill))

        db.commit()
        return redirect(url_for("my_profile"))

    user = db.execute("SELECT * FROM users WHERE id=?", (user_id,)).fetchone()
    skills = db.execute("SELECT skill FROM skills WHERE user_id=?", (user_id,)).fetchall()
    skills_str = ", ".join([s["skill"] for s in skills])

    return render_template("edit_profile.html", user=user, skills=skills_str)

# افزودن نظر برای فریلنسر 
@app.route("/freelancers/<int:freelancer_id>/reviews", methods=["GET", "POST"])
def freelancer_reviews(freelancer_id):
    if "user_id" not in session:
        return redirect(url_for("login"))

    db = get_db()
    employer_id = session["user_id"]

    if request.method == "POST":
        rating = request.form.get("rating")
        comment = request.form.get("comment", "")

        existing = db.execute(
            "SELECT * FROM reviews WHERE freelancer_id=? AND employer_id=?",
            (freelancer_id, employer_id)
        ).fetchone()

        if existing:
            return "نظر شما قبلا درمورد این فریلنسر ثبت شده است!", 400

        db.execute(
            "INSERT INTO reviews (freelancer_id, employer_id, rating, comment) VALUES (?, ?, ?, ?)",
            (freelancer_id, employer_id, rating, comment)
        )
        db.commit()
        return redirect(url_for("freelancer_reviews", freelancer_id=freelancer_id))

    reviews = db.execute("""
        SELECT r.*, u.username AS employer_name
        FROM reviews r
        JOIN users u ON r.employer_id = u.id
        WHERE r.freelancer_id=?
    """, (freelancer_id,)).fetchall()

    return render_template("reviews.html", reviews=reviews, freelancer_id=freelancer_id)

# علاقه ها
favorites = {}
c = "secret"

def require_auth(f):
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token or token != f"Bearer {c}":
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@app.route("/favorites/<username>", methods=["GET"])
@require_auth
def get_favorites(username):
    favorite = favorites.get(username, [])
    return jsonify({"favorites": favorite})

@app.route("/favorites/<username>", methods=["POST"])
@require_auth
def add_favorite(username):
    data = request.json
    if not data or "item" not in data:
        return jsonify({"error": "Missing 'item' in request"}), 400

    item = data["item"]
    favorites.setdefault(username, [])
    
    if item in favorites[username]:
        return jsonify({"message": "Item already in favorites"}), 409
    
    favorites[username].append(item)
    return jsonify({"message": "Added successfully", "favorites": favorites[username]}), 201

@app.route("/favorites/<username>", methods=["DELETE"])
@require_auth
def remove_favorite(username):
    data = request.json
    if not data or "item" not in data:
        return jsonify({"error": "Missing 'item' in request"}), 400

    item = data["item"]
    if username not in favorites or item not in favorites[username]:
        return jsonify({"message": "Item not found"}), 404
    
    favorites[username].remove(item)
    return jsonify({"message": "Removed successfully", "favorites": favorites[username]}), 200

profile = db.Table(
    "profile",
    db.Column("profile_id", db.Integer, db.ForeignKey("profiles.id")),
    db.Column("skill_id", db.Integer, db.ForeignKey("skills.id"))
)

class Profile(db.Model):
    __tablename__ = "profiles"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    bio = db.Column(db.Text, default="")
    city = db.Column(db.String(80), default="")
    skills = db.relationship("Skill", secondary=profile, backref="profiles")

    def f(self):
        return {
            "id": self.id,
            "name": self.name,
            "bio": self.bio,
            "city": self.city,
            "skills": [s.f_min() for s in self.skills]
        }

class Skill(db.Model):
    __tablename__ = "skills"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    description = db.Column(db.Text, default="")
    profiles = db.relationship("Profile", secondary=profile, backref="skills")

    def f(self):
        return {"id": self.id, "name": self.name, "description": self.description}

    def f_min(self):
        return {"id": self.id, "name": self.name}

@app.route("/init-sample-data", methods=["POST"])
def init_sample_data():
    db.drop_all()
    db.create_all()

    # برنامه نویس
    python = Skill(name="Python", description="Programming language for backend, AI, and automation")
    js = Skill(name="JavaScript", description="Frontend/Backend language")
    flask_skill = Skill(name="Flask", description="Python microframework")
    django = Skill(name="Django", description="Python web framework")
    react = Skill(name="React", description="Frontend framework")
    sql = Skill(name="SQL", description="Database query language")
    java = Skill(name="Java", description="Enterprise and Android programming language")
    csharp = Skill(name="C#", description=".NET programming language for apps and games")
    # گرافیک و طراحی
    photoshop = Skill(name="Photoshop", description="Image editing and graphic design")
    illustrator = Skill(name="Illustrator", description="Vector graphics and logo design")
    figma = Skill(name="Figma", description="UI/UX design and prototyping")
    after_effects = Skill(name="After Effects", description="Motion graphics and animation")
    blender = Skill(name="Blender", description="3D modeling and animation")
    canva = Skill(name="Canva", description="Simple graphic design tool")
    # ترجمه
    content_writing = Skill(name="Content Writing", description="Creating articles, blogs, and marketing text")
    copywriting = Skill(name="Copywriting", description="Persuasive writing for marketing and sales")
    translation = Skill(name="Translation", description="Translating texts between languages")
    seo_writing = Skill(name="SEO Writing", description="Writing optimized content for search engines")
    editing = Skill(name="Editing", description="Proofreading and improving texts")
    # ویدیو و انیمیشن
    video_editing = Skill(name="Video Editing", description="Cutting, editing, and post-production")
    premiere = Skill(name="Adobe Premiere", description="Professional video editing software")
    after_effects_motion = Skill(name="After Effects Motion", description="Advanced motion design")
    animation_2d = Skill(name="2D Animation", description="Creating animations in 2D style")
    animation_3d = Skill(name="3D Animation", description="Creating animations in 3D style")
    voice_over = Skill(name="Voice Over", description="Narration and voice recording")
    # موزیک و صدا
    music_production = Skill(name="Music Production", description="Creating and mixing music")
    sound_design = Skill(name="Sound Design", description="Designing custom sounds and effects")
    voice_acting = Skill(name="Voice Acting", description="Performing character voices")
    djing = Skill(name="DJing", description="Mixing and performing live music")
    # هوش مصنوعی
    machine_learning = Skill(name="Machine Learning", description="Building predictive models")
    deep_learning = Skill(name="Deep Learning", description="Neural networks and advanced AI")
    nlp = Skill(name="NLP", description="Natural Language Processing")
    data_analysis = Skill(name="Data Analysis", description="Working with large datasets and insights")
    computer_vision = Skill(name="Computer Vision", description="Image recognition and AI vision")
    # دیجیتال مارکت
    social_media = Skill(name="Social Media Marketing", description="Managing social media campaigns")
    seo = Skill(name="SEO", description="Search Engine Optimization for websites")
    sem = Skill(name="SEM", description="Search Engine Marketing with ads")
    branding = Skill(name="Branding", description="Building brand identity and strategy")
    email_marketing = Skill(name="Email Marketing", description="Campaigns via email")
    content_marketing = Skill(name="Content Marketing", description="Strategy and content creation for growth")

    db.session.add_all([
        python, js, flask_skill, django, react, sql, java, csharp,
        photoshop, illustrator, figma, after_effects, blender, canva,
        content_writing, copywriting, translation, seo_writing, editing,
        video_editing, premiere, after_effects_motion, animation_2d, animation_3d, voice_over,
        music_production, sound_design, voice_acting, djing,
        machine_learning, deep_learning, nlp, data_analysis, computer_vision,
        social_media, seo, sem, branding, email_marketing, content_marketing
    ])
    db.session.commit()
    return jsonify({"message": "Sample data initialized"}), 201

# جستجو
@app.route("/search", methods=["GET"])
def search():
    q = request.args.get("q", "").strip()
    try:
        limit = int(request.args.get("limit", 20))
        offset = int(request.args.get("offset", 0))
    except ValueError:
        return jsonify({"error": "limit and offset must be integers"}), 400

    if q == "":
        return jsonify({"error": "query parameter 'q' is required"}), 400

    like_pattern = f"%{q}%"
    matching_skills = Skill.query.filter(
        db.or_(
            Skill.name.ilike(like_pattern),
            Skill.description.ilike(like_pattern)
        )
    ).all()

    if matching_skills:
        skill_ids = [s.id for s in matching_skills]
        profiles_via_skills = Profile.query.join(profile).filter(profile.c.skill_id.in_(skill_ids))
    else:
        profiles_via_skills = Profile.query.filter(False)

    profiles_direct = Profile.query.filter(
        db.or_(
            Profile.name.ilike(like_pattern),
            Profile.bio.ilike(like_pattern),
            Profile.city.ilike(like_pattern)
        )
    )

    profiles_direct_list = profiles_direct.all()
    profiles_via_skills_list = profiles_via_skills.all()
    unique_profiles = {}
    for p in profiles_direct_list + profiles_via_skills_list:
        unique_profiles[p.id] = p
    all_profiles = list(unique_profiles.values())
    total_profiles = len(all_profiles)
    paged_profiles = all_profiles[offset: offset + limit]

    skills_serialized = [s.f() for s in matching_skills]
    profiles_serialized = [p.f() for p in paged_profiles]

    return jsonify({
        "q": q,
        "skills": skills_serialized,
        "profiles": profiles_serialized,
        "total_profiles": total_profiles,
        "limit": limit,
        "offset": offset
    }), 200
@app.route("/robots.txt")
def robots_txt():
    return "User-agent: *\nDisallow: /profile/edit\nDisallow: /admin\n", 200, {"Content-Type": "text/plain"}

@app.route("/sitemap.xml")
def sitemap():
    urls = [
        url_for('index', _external=True),
        url_for('register', _external=True),
        url_for('login', _external=True),
        url_for('comment_form', _external=True),
        url_for('get_users', _external=True)
    ]
    sitemap_xml = render_template_string("""<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
        {% for url in urls %}
        <url>
            <loc>{{ url }}</loc>
            <changefreq>weekly</changefreq>
            <priority>0.8</priority>
        </url>
        {% endfor %}
    </urlset>""", urls=urls)
    return sitemap_xml, 200, {"Content-Type": "application/xml"}

if __name__ == "__main__":
    app.run(debug=True)  
