"""Blogly application."""

from flask import Flask, render_template, request, redirect
from models import db, connect_db, User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

connect_db(app)


@app.route('/')
def home_page():
    return (redirect('/users/'))


@app.route('/users/')
def users_page():
    users = User.query.all()
    sorted_users = sorted(users, key=lambda x: x.last_name + x.first_name)
    return (render_template('home.html', is_userlist=True, users=sorted_users))


@app.route('/users/new/')
def new_user_page():
    return (render_template('home.html', newuser=True))


@app.route('/users/new/', methods=['POST'])
def new_user_post_page():
    first_name = request.form.get('first')
    last_name = request.form.get('last')
    image_file = request.form.get('image')
    if (image_file != ''):
        new_user = User(first_name=first_name,
                        last_name=last_name, image_url=image_file)
    else:
        new_user = User(first_name=first_name,
                        last_name=last_name)
    db.session.add(new_user)
    db.session.commit()
    print(new_user)

    return (redirect('/users/'))


@app.route('/users/<int:id>/')
def user_page(id):
    user = User.query.get(id)
    print('HERE IS USER', id, user)
    return (render_template('home.html', user=user))


@app.route('/users/<int:id>/edit/')
def edit_user_page(id):
    user = User.query.get(id)
    return (render_template('home.html', edit_user=user))


@app.route('/users/<int:id>/edit/', methods=['POST'])
def edit_user_post_page(id):
    user = User.query.get(id)
    user.first_name = request.form.get('first')
    user.last_name = request.form.get('last')
    user.image_url = request.form.get('image')
    db.session.add(user)
    db.session.commit()
    return (redirect(f"/users/{id}/"))


@app.route('/users/<int:id>/delete/')
def delete_user_post_page(id):
    user = User.query.get(id)
    print(user)
    db.session.delete(user)
    db.session.commit()
    return (redirect('/users/'))


def seed():
    barney = User(first_name='Barney', last_name='Rubble',
                  image_url="images/barney.jpg")
    betty = User(first_name='Betty', last_name='Rubble',
                 image_url="images/betty.jpg")
    mrslate = User(first_name='George', last_name='Slate')
    db.session.add(barney)
    db.session.add(betty)
    db.session.add(mrslate)
    db.session.commit()
