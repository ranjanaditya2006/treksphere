from datetime import date

from extensions import db
from models import Trek, User


def seed_admin():
    admin = User.query.filter_by(email='admin@trekapp.com').first()
    if not admin:
        admin = User(
            name='System Admin',
            email='admin@trekapp.com',
            phone='9999999999',
            role='admin',
            approved=True,
            blacklisted=False,
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()


def seed_sample_data():
    if Trek.query.count() > 0:
        return

    staff = User.query.filter_by(email='guide@trekapp.com').first()
    if not staff:
        staff = User(
            name='Aman Guide',
            email='guide@trekapp.com',
            phone='8888888888',
            role='staff',
            approved=True,
            blacklisted=False,
        )
        staff.set_password('staff123')
        db.session.add(staff)
        db.session.commit()

    demo_treks = [
        Trek(
            name='Triund Weekend Trek',
            location='Himachal Pradesh',
            difficulty='Easy',
            duration_days=2,
            available_slots=20,
            description='Scenic beginner-friendly Himalayan weekend trek.',
            start_date=date(2026, 8, 15),
            end_date=date(2026, 8, 16),
            status='Open',
            staff_id=staff.id,
        ),
        Trek(
            name='Hampta Pass Expedition',
            location='Manali',
            difficulty='Moderate',
            duration_days=5,
            available_slots=15,
            description='High-altitude crossover trek with dramatic valley views.',
            start_date=date(2026, 9, 10),
            end_date=date(2026, 9, 14),
            status='Approved',
            staff_id=staff.id,
        ),
        Trek(
            name='Kedarkantha Winter Trek',
            location='Uttarakhand',
            difficulty='Hard',
            duration_days=6,
            available_slots=12,
            description='Snow trek suited for fit trekkers with prior experience.',
            start_date=date(2026, 12, 20),
            end_date=date(2026, 12, 25),
            status='Pending',
        ),
    ]
    db.session.add_all(demo_treks)
    db.session.commit()