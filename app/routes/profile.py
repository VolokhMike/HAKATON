import sqlite3

from flask import render_template, redirect, url_for, request
from flask_login import current_user, login_required

from app import app
from connection import get_db_connection


@app.get("/profile/")
@login_required
def get_profile_page():
	user_id = request.args.get('user_id', current_user.user_id)
	
	conn = get_db_connection()
	cursor = conn.cursor()
	cursor.execute("""
		SELECT users.username, users.gmail, profile.* FROM users 
		LEFT JOIN profile ON users.user_id = profile.user_id 
		WHERE users.user_id = ?""", (user_id,))
	profile = cursor.fetchone()
	cursor.execute("SELECT * FROM quests")
	quests = cursor.fetchall()
	conn.close()
	return render_template("profile.html", profile=profile, quests=quests, is_owner=str(user_id) == str(current_user.user_id))


@app.get("/edit_profile/")
@login_required
def get_edit_profile_page():
	if 'user_id' in request.args:
		user_id = request.args.get('user_id')
		if str(user_id) != str(current_user.user_id):
			return redirect(url_for('get_profile_page', user_id=user_id))
	
	conn = get_db_connection()
	cursor = conn.cursor()
	cursor.execute("""
		SELECT users.username, users.gmail, profile.*  FROM users 
		LEFT JOIN profile ON users.user_id = profile.user_id 
		WHERE users.user_id = ?""", (current_user.user_id,))
	profile = cursor.fetchone()
	conn.close()
	return render_template("edit_profile.html", profile=profile)


@app.post("/edit_profile/")
@login_required
def post_edit_profile_page():
	if 'user_id' in request.form and str(request.form['user_id']) != str(current_user.user_id):
		return redirect(url_for('get_profile_page'))

	conn = get_db_connection()
	cursor = conn.cursor()
	cursor.execute("""
		UPDATE users SET username = ?, gmail = ? WHERE user_id = ? """, 
		(request.form['username'], request.form['gmail'], current_user.user_id))
	cursor.execute("SELECT * FROM profile WHERE user_id = ?", (current_user.user_id,))
	profile_exists = cursor.fetchone()

	if profile_exists:
		cursor.execute("""
			UPDATE profile SET photo = ?, prof_description = ? WHERE user_id = ? """, 
			(request.form['photo'], request.form['prof_description'], current_user.user_id))
	else:
		cursor.execute("""
			INSERT INTO profile (user_id, photo, prof_description, points) VALUES (?, ?, ?, 0)""", 
			(current_user.user_id, request.form['photo'], request.form['prof_description']))
	
	conn.commit()
	conn.close()
	return redirect(url_for('get_profile_page'))
