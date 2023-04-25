from fastapi import FastAPI
import pymysql

app = FastAPI()

# MySQL 연결 정보
mysql_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',
    'db': 'database_name',
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor
}

# MySQL 연결 객체 생성
conn = pymysql.connect(**mysql_config)

# API 루트 경로
@app.get("/")
async def root():
    return {"message": "Hello World"}

# MySQL 데이터 조회
@app.get("/users")
async def get_users():
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()
    return {'users': rows}
