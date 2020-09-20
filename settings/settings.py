import os

# Redis
redis_server = os.environ.get("REDIS_HOST", "127.0.0.1")
redis_port = os.environ.get("REDIS_PORT", 6379)
redis_pool_minsize = 5
redis_pool_maxsize = 10


# MySQL
user = os.environ.get("MYSQL_USER")
password = os.environ.get("MYSQL_PASSWORD")
root_password = os.environ.get("MYSQL_ROOT_PASSWORD")
database_name = os.environ.get("MYSQL_DATABASE")
db_host = os.environ.get("MYSQL_HOST")

# dialect+driver://username:password@host:port/database
sqlalchemy = ""
DB_URL = f'mysql+mysqldb://{user}:{password}@{db_host}/{database_name}'