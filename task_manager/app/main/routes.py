from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user, logout_user
from werkzeug.security import check_password_hash
from datetime import datetime
from ..extensions import db
from ..models import User, Tasks
from ..forms import TaskForm, UpdateForm

# Define the Blueprint
main = Blueprint('main', __name__)


@main.route("/", methods=["POST", "GET"])
@login_required
def home():
    form = TaskForm()
    if form.validate_on_submit():
        task = Tasks(
            title=form.title.data,
            description=form.description.data,
            due_date=form.due_date.data,
            priority=form.priority.data,
            category=form.category.data,
            author=current_user
        )
        db.session.add(task)
        db.session.commit()
        return redirect(url_for('main.home'))

    tasks = Tasks.query.filter_by(author=current_user).order_by(Tasks.due_date.asc()).all()

    current_hour = datetime.now().hour
    if 5 <= current_hour < 12:
        greeting = "Good Morning"
    elif 12 <= current_hour < 17:
        greeting = "Good Afternoon"
    else:
        greeting = "Good Evening"

    today_date = datetime.now().strftime('%A, %d %B')

    return render_template("main/home.html", form=form, tasks=tasks, greeting=greeting, today_date=today_date)


@main.route("/delete/<int:id>")
@login_required
def delete_task(id):
    task = Tasks.query.get_or_404(id)
    # Security check: Ensure the task belongs to the current user
    if task.author != current_user:
        flash("You do not have permission to delete this task.", category="error")
        return redirect(url_for("main.home"))

    db.session.delete(task)
    db.session.commit()
    flash("Task Dismissed")
    return redirect(url_for("main.home"))


@main.route("/settings", methods=["POST", "GET"])
@login_required
def settings():
    form = UpdateForm()
    if form.validate_on_submit():
        existing_user = User.query.filter(User.email == form.email.data, User.id != current_user.id).first()
        if existing_user:
            flash("An account already exists with this email.", category="error")
        else:
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash("Profile Updated successfully", category="success")
            return redirect(url_for("main.settings"))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email

    return render_template("main/settings.html", form=form)


@main.route("/delete-account", methods=["POST"])
@login_required
def delete_account():
    input_password = request.form.get('password')
    if check_password_hash(current_user.password, input_password):
        try:
            tasks = Tasks.query.filter_by(user_id=current_user.id).all()
            for task in tasks:
                db.session.delete(task)

            db.session.delete(current_user)
            db.session.commit()

            logout_user()
            flash("Your account has been deleted.", category="info")
            return redirect(url_for('auth.register'))

        except Exception as e:
            db.session.rollback()
            flash("An error occurred while deleting data.", category="error")
            return redirect(url_for('main.settings'))
    else:
        flash("Incorrect password. Account deletion cancelled.", category="error")
        return redirect(url_for('main.settings'))


@main.route('/calendar')
@login_required
def calendar_view():
    return render_template("main/calendar.html")


@main.route('/api/tasks')
@login_required
def get_tasks_api():
    tasks = Tasks.query.filter_by(user_id=current_user.id).all()
    events = []
    for task in tasks:
        events.append({
            'id': task.id,
            'title': task.title,
            'date': task.due_date.strftime('%Y-%m-%d'),
            'priority': task.priority,
            'category': task.category,
            'status': task.status
        })
    return jsonify(events)