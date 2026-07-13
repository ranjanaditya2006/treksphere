"""Shared Flask extension instances.

Kept in their own module so both models.py and app.py can import the same
SQLAlchemy instance without circular imports.
"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()