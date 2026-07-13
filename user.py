from flask import Blueprint, flash, redirect, render_template, url_for

from extensions import db
from models import Booking, Trek
from utils import current_user, login_required

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('')
@login_required(role='trekker')
def dashboard():
    user = current_user()
    bookings = Booking.query.filter_by(user_id=user.id).order_by(Booking.booking_date.desc()).all()
    open_treks = Trek.query.filter(Trek.status.in_(['Approved', 'Open'])).order_by(Trek.start_date.asc()).all()
    return render_template('user/dashboard.html', bookings=bookings, open_treks=open_treks)


@user_bp.route('/book/<int:trek_id>', methods=['POST'])
@login_required(role='trekker')
def book_trek(trek_id):
    user = current_user()
    trek = db.session.get(Trek, trek_id)
    if not trek or trek.status not in ['Approved', 'Open']:
        flash('Trek not available for booking.', 'danger')
        return redirect(url_for('main.index'))
    existing = Booking.query.filter_by(user_id=user.id, trek_id=trek.id, status='Booked').first()
    if existing:
        flash('You have already booked this trek.', 'warning')
        return redirect(url_for('user.dashboard'))
    if trek.remaining_slots <= 0:
        flash('No slots available for this trek.', 'danger')
        return redirect(url_for('main.index'))
    booking = Booking(user_id=user.id, trek_id=trek.id, status='Booked')
    db.session.add(booking)
    db.session.commit()
    flash('Trek booked successfully.', 'success')
    return redirect(url_for('user.dashboard'))


@user_bp.route('/booking/<int:booking_id>/cancel', methods=['POST'])
@login_required(role='trekker')
def cancel_booking(booking_id):
    booking = db.session.get(Booking, booking_id)
    user = current_user()
    if not booking or booking.user_id != user.id:
        flash('Booking not found.', 'danger')
        return redirect(url_for('user.dashboard'))
    booking.status = 'Cancelled'
    db.session.commit()
    flash('Booking cancelled.', 'info')
    return redirect(url_for('user.dashboard'))