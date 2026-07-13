from flask import Blueprint, redirect, render_template, request, url_for

from models import Trek
from utils import current_user, login_required

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    difficulty = request.args.get('difficulty', '')
    location = request.args.get('location', '')
    query = Trek.query.filter(Trek.status.in_(['Approved', 'Open']))
    if difficulty:
        query = query.filter_by(difficulty=difficulty)
    if location:
        query = query.filter(Trek.location.ilike(f'%{location}%'))
    treks = query.order_by(Trek.start_date.asc()).all()
    return render_template('index.html', treks=treks, difficulty=difficulty, location=location)


@main_bp.route('/dashboard')
@login_required()
def dashboard():
    user = current_user()
    if user.role == 'admin':
        return redirect(url_for('admin.dashboard'))
    if user.role == 'staff':
        if not user.approved:
            return redirect(url_for('auth.pending_approval'))
        return redirect(url_for('staff.dashboard'))
    return redirect(url_for('user.dashboard'))