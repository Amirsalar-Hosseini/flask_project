from flask import Flask, render_template, request
from sqlalchemy.orm import DeclarativeBase, mapped_column
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String


app = Flask(__name__)

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
db.init_app(app)

class User(db.Model):
    __tablename__ = 'users'
    id = mapped_column(Integer, primary_key=True)
    username = mapped_column(String(50), unique=True)
    email = mapped_column(String(100), nullable=False)


with app.app_context():
    db.create_all()


@app.route('/')
def say_hello():
    return render_template("home.html", name="amirsalar")

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/signup', methods=['GET', 'POST'])
def create_user():
    if request.method == 'GET':
        cu = User(username='amir', email='amir@amir.com')
        db.session.add(cu)
        db.session.commit()
        return render_template('signup.html')


if __name__ == '__main__':
    app.run(debug=True)