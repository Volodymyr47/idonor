from environs import Env


env = Env()
env.read_env()

POSTGRES_USER = env.str('POSTGRES_USER')
POSTGRES_PASSWD = env.str('POSTGRES_PASSWD')
SECRET_KEY = env.str('SECRET_KEY')
