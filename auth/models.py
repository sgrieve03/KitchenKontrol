

class User():
    email = ""
    id = ""
    
    def __init__(self, email=""):
        self.email = email
        self.id = email
    
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def get_id(self):
        return self.id
    
    def is_anonymous(self):
        return False

    def __repr__(self):
        return '<User %r>' % (self.email)
