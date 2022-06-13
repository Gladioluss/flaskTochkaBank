import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from os import getenv
from dotenv import load_dotenv
import json

from models import Product

load_dotenv()
FIREBASE_API_KEY = {
        "type": getenv("TYPE"),
        "project_id": getenv("PROJECT_ID"),
        "private_key_id": getenv("PRIVATE_KEY_ID"),
        "private_key": getenv("PRIVATE_KEY").replace('\\n', '\n'),
        "client_email": getenv("CLIENT_EMAIL"),
        "client_id": getenv("CLIENT_ID"),
        "auth_uri": getenv("AUTH_URI"),
        "token_uri": getenv("TOKEN_URI"),
        "auth_provider_x509_cert_url": getenv("AUTH_PROVIDER_X509_CERT_URL"),
        "client_x509_cert_url": getenv("CLIENT_X509_CERT_URL")

}
URL_DATABASE = getenv("URL_DATABASE")


class MetaSingleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(MetaSingleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class Database(metaclass=MetaSingleton):
    connection = None

    def connect(self):
        if self.connection is None:
            cred = credentials.Certificate(FIREBASE_API_KEY)
            firebase_admin.initialize_app(cred, {
                'databaseURL': URL_DATABASE
            })

            self.connection = 1
            return Database

    def add_new_user(self, username, email:str, password) -> None:
        ref = db.reference('/')
        ref.child('users').update({
            f"user_{email.replace('@', '').replace('.', '')}": {
                    'username': username,
                    'email': email,
                    'password': password
                }
                })

    def check_user_exists(self, email) -> object:
        ref = db.reference('/')
        res = ref.child('users').child(f"user_{email.replace('@', '').replace('.', '')}").get()
        return res
