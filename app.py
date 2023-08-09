from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

# /// = relative path, //// = absolute path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    subtitle = db.Column(db.String(100))
    complete = db.Column(db.Boolean)

class user(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100))
    mail = db.Column(db.String(100))
    password = db.Column(db.String(20))

@app.route('/trangtru')
def index():
    # show all todo
    todo_list = Todo.query.all()
    #print(todo_list)
    return render_template('base.html', todo_list = todo_list)

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        uname = request.form["uname"]
        passw = request.form["passw"]

        login = user.query.filter_by(username=uname, password = passw).first()
        if login is not None:
            flash('You were successfully logged in')
            return redirect(url_for("index"), )
    return render_template("login.html")

@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        uname = request.form["uname"]
        email = request.form["email"]
        passw = request.form["passw"]

        register = user(username=uname, mail=email, password=passw)
        db.session.add(register)
        db.session.commit()

        return redirect(url_for("login"))
    return render_template('register.html')

@app.route('/add', methods=["POST"])
def add():

    title =  request.form.get("title")
    subtitle = request.form.get("subtitle")
    new_todo = Todo(title = title, subtitle=subtitle, complete = False)
    db.session.add(new_todo)
    db.session.commit() 
    return redirect(url_for("base"))

@app.route('/update/<int:todo_id>', methods=["POST"])
def update(todo_id):

    todo = Todo.query.get(todo_id) 
    todo.title = request.form.get("title")  
    todo.subtitle = request.form.get("subtitle")  
    db.session.commit()  
    return redirect(url_for('index'))

@app.route('/delete/<int:todo_id>')
def delete(todo_id):

    todo = Todo.query.filter_by(id = todo_id).first()
    db.session.delete(todo)
    db.session.commit() 
    return redirect(url_for("index"))

@app.route('/edit/<int:todo_id>')
def edit(todo_id):

    todo = Todo.query.get(todo_id)  
    return render_template('edit.html', todo=todo)

@app.route("/active/<int:todo_id>")
def active(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))



if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True)