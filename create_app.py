"""Blogly application."""


from models import db, connect_db, User
from flask import Flask, render_template, request, redirect
from os import getenv

def create_app():

    # print('db:', getenv('SQL_DB'))
    # print('echo:', getenv('SQL_ECHO'))
    db = getenv('SQL_DB')
    echo = getenv('SQL_ECHO')

    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = db
    app.config['SQLALCHEMY_ECHO'] = eval(echo)

    make_routes(app)
    connect_db(app)
    return(app)
    

def make_routes(my_app):

    @my_app.route('/')
    def home_page():
        return (redirect('/users/'))


    @my_app.route('/users/')
    def users_page():
        users = User.query.all()
        sorted_users = sorted(users, key=lambda x: x.last_name + x.first_name)
        return (render_template('home.html', is_userlist=True, users=sorted_users))


    @my_app.route('/users/new/')
    def new_user_page():
        return (render_template('home.html', newuser=True))


    @my_app.route('/users/new/', methods=['POST'])
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


    @my_app.route('/users/<int:id>/')
    def user_page(id):
        user = db.session.get(User, id)
        # print('HERE IS USER', id, user)
        return (render_template('home.html', user=user))


    @my_app.route('/users/<int:id>/edit/')
    def edit_user_page(id):
        user = db.session.get(User,id)
        return (render_template('home.html', edit_user=user))


    @my_app.route('/users/<int:id>/edit/', methods=['POST'])
    def edit_user_post_page(id):
        user = User.query.get(id)
        user.first_name = request.form.get('first')
        user.last_name = request.form.get('last')
        user.image_url = request.form.get('image')
        db.session.add(user)
        db.session.commit()
        return (redirect(f"/users/{id}/"))


    @my_app.route('/users/<int:id>/delete/')
    def delete_user_post_page(id):
        user = User.query.get(id)
        print(user)
        db.session.delete(user)
        db.session.commit()
        return (redirect('/users/'))



