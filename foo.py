"""Blogly application."""

from app import app, connect_db

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
connect_db(app)
