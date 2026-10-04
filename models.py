from app import db
from flask_login import UserMixin 

class User(db.Model, UserMixin):
    __tablename__ = "users" 

    uid = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.String(255), nullable=False, unique=True)  # Changed db.Text -> db.String(255)
    username = db.Column(db.String(150), nullable=False)               # Changed db.Text -> db.String(150)
    password = db.Column(db.String(255), nullable=False)               # Changed db.Text -> db.String(255)
    role = db.Column(db.String(50)) 

    def get_id(self):
        return self.uid