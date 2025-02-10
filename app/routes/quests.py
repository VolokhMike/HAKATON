import sqlite3

from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_required

from app import app
from connection import get_db_connection


@app.get("/")
def get_start():
    if current_user.is_authenticated:
        return redirect(url_for("get_menu_page"))
    else:
        return redirect(url_for("get_signup"))
    

@app.get("/menu/")
def get_menu_page():
    if not current_user.email_verified:
        return redirect(url_for("get_verification"))
    elif current_user.username == "admin" and current_user.password == "@dm1n":
        return render_template("admin_page.html")
    return render_template("menu.html")


@app.get("/add_quests/")
@login_required
def get_add_quests():
    conn = get_db_connection()
    quests = conn.execute('SELECT * FROM quests').fetchall()
    conn.close()
    return render_template("add_quests.html", quests=quests)


@app.post("/add_quests/")
@login_required
def post_add_quests():
    name = request.form.get('name')
    description = request.form.get('description')
    points = request.form.get('points')
    answer = request.form.get('answer')
    
    if not all([name, description, points]):
        return "All fields must be filled", 400
    
    try:
        conn = get_db_connection()
        conn.execute('INSERT INTO quests (name, description, points, answer) VALUES (?, ?, ?, ?)', 
                     (name, description, points, answer))
        conn.commit()
        conn.close()
        return redirect(url_for('get_add_quests'))
    except sqlite3.Error as e:
        return f"Database error: {str(e)}", 500
