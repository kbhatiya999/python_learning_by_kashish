import fastapi

mysql_db = {
    # 'host': "136.243.32.134",
    'host': "localhost",
    'db': 'aditya_buildtab',
    'user': 'aditya_sendmaildb',
    'pass': 'sendmaildb@123',
    'port': '3306',
}


def get_db():
    return mysql_db

def create_app():
    app = fastapi.FastAPI('JOB_MATCH_CONFIG')

    return app


# url = "mysql://" + mysql_db['user'] + ":" + mysql_db['pass'] + "@" + mysql_db['host'] + ":" + mysql_db[
#         'port'] + "/" + mysql_db['db']