import os
from dotenv import load_dotenv


# dotenv = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
abs_file_path = os.path.realpath(__file__)
project_dir = os.path.dirname(os.path.dirname(abs_file_path))
dotenv_path = os.path.join(project_dir, '.env')
load_dotenv(dotenv_path)

class DevelopmentConfig:
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{password}@{host}/{db_name}?charset=utf8'.format(**{
        'user': os.environ.get('MYSQL_USER') ,
        'password': os.environ.get('MYSQL_PASSWORD'),
        'host': os.environ.get('DB_HOST'),
        'db_name': os.environ.get('MYSQL_DATABASE')
    })

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False

Config = DevelopmentConfig


if __name__ == '__main__':
    print(dotenv)
    # if output is ./env it's correct