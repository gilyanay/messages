import os


from mysql import MySqlClient

from dotenv import load_dotenv

load_dotenv()

mysql = MySqlClient.get_mysql_client(
    user=os.getenv("MYSQL_USER"),
    host=os.getenv("MYSQL_HOST"),
    scheme="messages",
    password=os.getenv("MYSQL_PASSWORD"),
)