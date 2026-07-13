from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for

from extensions import db
from models import Booking, Trek, User
from utils import login_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')


@admin_bp.route('')
@login_required(role='admin')
def dashboard():
    metrics = {
        'users': User.query.filter_by(role='trekker').count(),
        'staff': User.query.filter_by(role='staff').count(),
        'pending_staff': User.query.filter_by(role='staff', approved=False).count(),
        'treks': Trek.query.count(),
        'bookings': Booking.query.count(),
    }
    recent_treks = Trek.query.order_by(Trek.created_at.desc()).limit(5).all()
    pending_staff = User.query.filter_by(role='staff', approved=False).all()
    return render_template('admin/dashboard.html', metrics=metrics, recent_treks=recent_treks, pending_staff=pending_staff)


@admin_bp.route('/treks')
@login_required(role='admin')
def treks():
    all_treks = Trek.query.order_by(Trek.start_date.asc()).all()
    return render_template('admin/treks.html', treks=all_treks)


@admin_bp.route('/trek/create', methods=['GET', 'POST'])
@login_required(role='admin')
def create_trek():
    staff_members = User.query.filter_by(role='staff', approved=True, blacklisted=False).all()
    if request.method == 'POST':
        trek = Trek(
            name=request.form['name'],
            location=request.form['location'],
            difficulty=request.form['difficulty'],
            duration_days=int(request.form['duration_days']),
            available_slots=int(request.form['available_slots']),
            description=request.form.get('description', ''),
            start_date=datetime.strptime(request.form['start_date'], '%Y-%m-%d').date(),
            end_date=datetime.strptime(request.form['end_date'], '%Y-%m-%d').date(),
            status=request.form['status'],
            staff_id=int(request.form['staff_id']) if request.form.get('staff_id') else None,
        )
        db.session.add(trek)
        db.session.commit()
        flash('Trek created successfully.', 'success')
        return redirect(url_for('admin.treks'))
    return render_template('admin/trek_form.html', trek=None, staff_members=staff_members)


@admin_bp.route('/trek/<int:trek_id>/edit', methods=['GET', 'POST'])
@login_required(role='admin')
def edit_trek(trek_id):
    trek = db.session.get(Trek, trek_id)
    staff_members = User.query.filter_by(role='staff', approved=True, blacklisted=False).all()
    if request.method == 'POST':
        trek.name = request.form['name']
        trek.location = request.form['location']
        trek.difficulty = request.form['difficulty']
        trek.duration_days = int(request.form['duration_days'])
        trek.available_slots = int(request.form['available_slots'])
        trek.description = request.form.get('description', '')
        trek.start_date = datetime.strptime(request.form['start_date'], '%Y-%m-%d').date()
        trek.end_date = datetime.strptime(request.form['end_date'], '%Y-%m-%d').date()
        trek.status = request.form['status']
        trek.staff_id = int(request.form['staff_id']) if request.form.get('staff_id') else None
        db.session.commit()
        flash('Trek updated successfully.', 'success')
        return redirect(url_for('admin.treks'))
    return render_template('admin/trek_form.html', trek=trek, staff_members=staff_members)


@admin_bp.route('/trek/<int:trek_id>/delete', methods=['POST'])
@login_required(role='admin')
def delete_trek(trek_id):
    trek = db.session.get(Trek, trek_id)
    if trek:
        db.session.delete(trek)
        db.session.commit()
        flash('Trek deleted successfully.', 'info')
    return redirect(url_for('admin.treks'))


@admin_bp.route('/staff')
@login_required(role='admin')
def manage_staff():
    staff_members = User.query.filter_by(role='staff').order_by(User.created_at.desc()).all()
    return render_template('admin/staff.html', staff_members=staff_members)


@admin_bp.route('/users')
@login_required(role='admin')
def manage_users():
    users = User.query.filter_by(role='trekker').order_by(User.created_at.desc()).all()
    return render_template('admin/users.html', users=users)


@admin_bp.route('/approve-staff/<int:user_id>', methods=['POST'])
@login_required(role='admin')
def approve_staff(user_id):
    user = db.session.get(User, user_id)
    if user and user.role == 'staff':
        user.approved = True
        db.session.commit()
        flash('Staff approved.', 'success')
    return redirect(url_for('admin.manage_staff'))


@admin_bp.route('/toggle-blacklist/<int:user_id>', methods=['POST'])
@login_required(role='admin')
def toggle_blacklist(user_id):
    user = db.session.get(User, user_id)
    if user and user.role != 'admin':
        user.blacklisted = not user.blacklisted
        db.session.commit()
        flash('Blacklist status updated.', 'warning')
    return redirect(request.referrer or url_for('admin.dashboard'))


@admin_bp.route('/search')
@login_required(role='admin')
def search():
    q = request.args.get('q', '').strip()
    matched_treks, users, staff_members = [], [], []
    if q:
        if q.isdigit():
            matched_treks = Trek.query.filter(
                (Trek.id == int(q)) | Trek.name.ilike(f'%{q}%') | Trek.location.ilike(f'%{q}%')
            ).all()
            users = User.query.filter(User.role == 'trekker').filter(
                (User.id == int(q)) | User.name.ilike(f'%{q}%') | User.email.ilike(f'%{q}%')
            ).all()
            staff_members = User.query.filter(User.role == 'staff').filter(
                (User.id == int(q)) | User.name.ilike(f'%{q}%') | User.email.ilike(f'%{q}%')
            ).all()
        else:
            matched_treks = Trek.query.filter(Trek.name.ilike(f'%{q}%') | Trek.location.ilike(f'%{q}%')).all()
            users = User.query.filter(User.role == 'trekker').filter(
                User.name.ilike(f'%{q}%') | User.email.ilike(f'%{q}%')
            ).all()
            staff_members = User.query.filter(User.role == 'staff').filter(
                User.name.ilike(f'%{q}%') | User.email.ilike(f'%{q}%')
            ).all()
    return render_template('admin/search.html', q=q, treks=matched_treks, users=users, staff_members=staff_members)