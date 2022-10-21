""" Models for a melon tasting reservation scheduler. """

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy()

class User(db.Model):
    """A user"""

    __tablename__ = "users"

    user_id = db.Column(UUID(as_uuid=True), primary_key=True)
    username = db.Column(db.String, nullable=False)

    reservations = db.relationship("Reservation", back_populates="user")

    def __repr__(self):
        return f"<User user_id={self.user_id} username={self.username}>"

class Reservation(db.Model):
    """A reservation to taste melons"""

    __tablename__ = "reservations"

    reservation_id = db.Column(UUID(as_uuid=True), primary_key=True)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.user_id"), nullable = False)
    datetime = db.Column(db.DateTime)

    user = db.relationship("User", back_populates="reservations")

    def __repr__(self):
        return f"<Reservation reservation_id={self.reservation_id} datetime={self.datetime}>"

def connect_to_db(flask_app, db_uri="postgresql:///melon-scheduler", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")

if __name__ == "__main__":
    from server import app

    connect_to_db(app)