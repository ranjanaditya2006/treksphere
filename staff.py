from flask import Blueprint, flash, redirect, render_template, request, url_for

from extensions import db
from models import Booking, Trek
from utils import current_user, login_required

staff_bp = Blueprint('staff', __name__, url_prefix='/staff')


@staff_bp.route('')
@login_required(role='staff')
def dashboard():
    user = current_user()
    if not user.approved:
        return redirect(url_for('auth.pending_approval'))
    treks = Trek.query.filter_by(staff_id=user.id).order_by(Trek.start_date.asc()).all()
    return render_template('staff/dashboard.html', treks=treks)


@staff_bp.route('/trek/<int:trek_id>/update', methods=['GET', 'POST'])
@login_required(role='staff')
def update_trek(trek_id):
    user = current_user()
    if not user.approved:
        return redirect(url_for('auth.pending_approval'))
    trek = Trek.query.filter_by(id=trek_id, staff_id=user.id).first_or_404()
    if request.method == 'POST':
        trek.available_slots = int(request.form['available_slots'])
        trek.status = request.form['status']
        trek.description = request.form.get('description', trek.description)
        db.session.commit()
        flash('Trek details updated.', 'success')
        return redirect(url_for('staff.dashboard'))
    bookings = Booking.query.filter_by(trek_id=trek.id).order_by(Booking.booking_date.desc()).all()
    return render_template('staff/trek_update.html', trek=trek, bookings=bookings)