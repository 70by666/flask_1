from flask import url_for
from flask_login import UserMixin


class UserLogin(UserMixin):
    def from_db(self, user_id, db):
        self._user = db.get_user(user_id)
        return self
    
    def create(self, user):
        self._user = user
        return self
    
    def get_id(self):
        return str(self._user[0]) if self._user else "No id"

    def get_name(self):
        return self._user[1] if self._user else "No name"
    
    def get_email(self):
        return self._user[2] if self._user else "No email"

    def get_ava(self, app):
        img = self._user[4]
        if not img:
            try:
                with app.open_resource(app.root_path + url_for("static", filename="img/default.png"), "rb") as f:
                    img = f.read()
                    return img
            except FileNotFoundError as Ex:
                print(Ex)
        
        return img.tobytes()

    def get_reg_date(self):
        return self._user[-1] if self._user else "No reg date"

    def verify_ext(self, filename):
        ext = filename.split(".")[-1].lower()
        if ext == "png":
            return True
        
        return False
