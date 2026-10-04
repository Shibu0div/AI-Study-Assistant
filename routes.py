from flask import render_template,request , redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from models import User

from aws_backend.study_modes import summarize_topic, generate_quiz, generate_flashcards
from aws_backend.rag import explain_from_knowledge_base

def register_routes(app,db,bcrypt):
    @app.route("/")
    def index():
        return render_template('index.html')
    @app.route('/signup',methods=['GET','POST'])
    def signup():
        if request.method == 'GET':
            return render_template('signup.html')
        elif request.method == 'POST':
            username = request.form.get('username')
            email_id = request.form.get('email_id')
            password = request.form.get('password')

            hashed_password = bcrypt.generate_password_hash(password)
            user = User(username=username,email_id=email_id,password=hashed_password) # pyright: ignore[reportCallIssue]
            db.session.add(user) 
            db.session.commit()
            return redirect(url_for('index'))
    @app.route('/login',methods=['GET','POST'])
    def login():
        if request.method == 'GET':
            return render_template('login.html')
        elif request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')

            user = User.query.filter(User.username == username).first()

            # assert user is not None
            if user and bcrypt.check_password_hash(user.password, password):
                login_user(user)
                return  redirect(url_for('index'))
            else:
                return "Invalid username or password", 401
    @app.route('/logout')
    def logout():
            logout_user()
            return redirect(url_for('login'))
    @app.route("/study")
    @login_required
    def study():
        return render_template("study.html")
    
    @app.route("/ask", methods=["POST"])
    @login_required
    def ask():
        question = request.form.get("question")

        result = explain_from_knowledge_base(question)

        return render_template(
            "answer.html",
            question=question,
            answer=result["answer"],
            tokens=result["total_tokens"]
        )
    @app.route("/summarize", methods=["POST"])
    @login_required
    def summarize():
        topic = request.form.get("question")

        result = summarize_topic(topic)

        return render_template(
            "answer.html",
            question=topic,
            answer=result["answer"],
            tokens=result["total_tokens"]
        )

    @app.route("/quiz", methods=["POST"])
    @login_required
    def quiz():
        topic = request.form.get("question", "").strip()
        num_questions = request.form.get("num_questions", type=int) or 5

        if not topic:
            return "Please enter a topic.", 400
        if not 1 <= num_questions <= 20:
            return "Number of questions must be between 1 and 20.", 400

        result = generate_quiz(topic, num_questions)

        return render_template(
            "quiz.html",
            topic=topic,
            quiz=result.get("quiz", []),
            tokens=result.get("total_tokens", 0)
        )



    @app.route("/flashcards", methods=["POST"])
    @login_required
    def flashcards():
        topic = request.form.get("question", "").strip()

        if not topic:
            return "Please enter a topic.", 400

        result = generate_flashcards(topic, num_cards=5)

        return render_template(
            "flashcards.html",
            topic=topic,
            cards=result.get("cards", []),
            tokens=result.get("total_tokens", 0)
        )
