from flask import Flask, render_template, request, redirect, url_for
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

    def __repr__(self):
        return f"username : {self.username} with email  : {self.email}"


with app.app_context():
    db.create_all()


@app.route('/')
def home_page():
    return render_template("home.html", name="amirsalar")

@app.route('/about')
def about_page():
    return render_template('about.html')

@app.route('/signup', methods=['GET', 'POST'])
def create_user():
    if request.method == 'GET':
        cu = User(username='salar', email='salar@salar.com')
        db.session.add(cu)
        db.session.commit()
        return render_template('signup.html')

@app.route('/all-users')
def show_all_user():
    users = db.session.execute(db.select(User).order_by(User.id)).scalars()
    return render_template('all_users.html', users=users)

@app.route('/specific-user/<string:username>')
def show_specific_user(username):
    user = db.session.execute(db.select(User).where(User.username == username)).scalar()
    return render_template('specific_user.html', user=user)

@app.route('/user/<int:user_id>')
def delete_specific_user(user_id):
    user = db.session.execute(db.select(User).where(User.id == user_id)).scalar()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('home_page'))

if __name__ == '__main__':
    app.run(debug=True)