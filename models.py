class User:
    object_name: str = 'User'
    username: str
    email: str
    password: str

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


class Product:

    def __init__(self, name,  cost, id, image):
        self.name = name
        self.cost = cost
        self.id = id
        self.image = image


class UserLogin:
    def create(self, user):
        self.__user = user
        return self

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False
