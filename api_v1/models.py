from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from api_v1 import db, login_manager

class Anggota(UserMixin, db.Model):
    __tablename__ = 'anggota'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    telegram = db.Column(db.String(64), unique=True, nullable=False)
    github = db.Column(db.String(15), unique=True, nullable=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)

    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Anggota: {}>'.format(self.email)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Anggota.query.get(int(user_id))

class Kegiatan(db.Model):
    __tablename__='kegiatan'
    id = db.Column(db.Integer, primary_key=True)
    tema =  db.Column(db.Text, nullable=False)
    pembicara = db.Column(db.Text,  nullable=False)
    tempat = db.Column(db.Text,  nullable=False)
    tanggal = db.Column(db.Text, nullable=False)
    status_kegiatan = db.Column(db.Text, nullable=False)
    jumlah_seat = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Kegiatan: {}>'.format(self.tema)