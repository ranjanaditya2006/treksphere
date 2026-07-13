from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from extensions import db
from models import User
from utils import current_user, login_required

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register/<role>', methods=['GET', 'POST'])
def register(role):
    if role not in ['staff', 'trekker']:
        flash('Invalid registration type.', 'danger')
        return redirect(url_for('main.index'))
    if request.method == 'POST':
        name = request.form['name'].strip()
        email = request.form['email'].strip().lower()
        password = request.form['password']
        phone = request.form.get('phone', '').strip()
        if User.query.filter_by(email=email).first():
            flash('Email already registered.', 'warning')
            return redirect(request.url)
        user = User(
            name=name,
            email=email,
            phone=phone,
            role=role,
            approved=True if role == 'trekker' else False,
        )
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful. You can login now.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('register.html', role=role)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email'].strip().lower()
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash('Invalid email or password.', 'danger')
            return redirect(url_for('auth.login'))
        if user.blacklisted:
            flash('Your account has been blacklisted.', 'danger')
            return redirect(url_for('auth.login'))
        session['user_id'] = user.id
        if user.role == 'staff' and not user.approved:
            return redirect(url_for('auth.pending_approval'))
        return redirect(url_for('main.dashboard'))
    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('main.index'))


@auth_bp.route('/pending-approval')
@login_required(role='staff')
def pending_approval():
    user = current_user()
    if user.approved:
        return redirect(url_for('staff.dashboard'))
    return render_template('pending_approval.html')