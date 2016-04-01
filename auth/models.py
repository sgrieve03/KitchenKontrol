from db import user


class User():
    email = ""
    user_id = ""
    admin = False
    name = ""    
    
    def __init__(self, user_id=user_id, admin=False):
        self.email = user.get_email(user_id) 
        self.user_id = user_id
        self.admin = admin
        self.name = self.get_name()

    def is_authenticated(self):
        if self.user_id == "":
            return False
        else:
            return True

    def is_active(self):
        return True

    def get_name(self):
        return user.get_name(self.user_id)

    def is_admin(self):
        admin = user.get_admin(self.user_id)
        if admin:
            return True
        else:
            return False

    def get_id(self):
        return self.user_id
    
    def is_anonymous(self):
        return False

    def __repr__(self):
        return '<User %r>' % (self.user_id)
