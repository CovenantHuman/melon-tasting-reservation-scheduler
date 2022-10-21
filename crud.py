""" CRUD operations for a melon tasting reservation scheduler. """

from model import db, User, Reservation, connect_to_db
import uuid

def create_user(username):
    """Create a new user"""
    user = User(user_id=uuid.uuid4(), username=username)
    return user

def get_user_by_username(username):
    """Find a user by their username"""
    return User.query.filter(User.username == username).first()

def create_reservation(user, datetime):
    """Create a new reservation"""
    reservation = Reservation(reservation_id=uuid.uuid4(), user_id=user.user_id, datetime=datetime)
    return reservation

def get_reservation_by_datetime(datetime):
    return Reservation.query.filter(Reservation.datetime == datetime).first()

def get_reservations_by_user(user):
    return Reservation.query.filter(Reservation.user_id == user.user_id).all()

if __name__ == "__main__":
    from server import app
    connect_to_db(app)