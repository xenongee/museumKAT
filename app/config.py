class Configuration(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:katdiplom1337@217.182.100.219/museumkat_db'
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://museum-admin:museumpassword@localhost/museumkat_db'

    SQLALCHEMY_POOL_RECYCLE = 299
    SECRET_KEY = "KAT Diplom Project"

    # Flask Security
    SECURITY_PASSWORD_SALT = 'flaskmuskat'
    SECURITY_PASSWORD_HASH = 'sha512_crypt'

    # Flask Compress
    COMPRESS_MIMETYPES = ['text/html', 'text/css', 'text/xml', 'application/json', 'application/javascript']
    COMPRESS_LEVEL = 6
    COMPRESS_MIN_SIZE = 500

    UPLOAD_IMAGE_FOLDER = 'static/files/images/'
    UPLOAD_FOLDER = 'static/files/documents/'
