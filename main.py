from typing import Union
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import pymysql

load_dotenv()

app = FastAPI()

def get_db_connection():
    return pymysql.connect(
        host=os.environ.get('DB_HOST'),
        user=os.environ.get('DB_USER'),
        password=os.environ.get('DB_PW'),
        database=os.environ.get('DB_NAME')
    )

def get_db_cursor(db):
    return db.cursor()

class Item(BaseModel):
    name: str
    phonenum: str

@app.post("/")
def insert_data(item: Item):
    db = get_db_connection()
    cursor = get_db_cursor(db)
    try:
        sql = "INSERT INTO test_table (name, phonenum) VALUES (%s, %s)"
        cursor.execute(sql, (item.name, item.phonenum))
        db.commit()
        return {"message": f"데이터가 성공적으로 삽입되었습니다. 이름: {item.name}, 값: {item.phonenum}"}
    except Exception as e:
        print(f"Error in insert_data: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        db.close()

@app.delete("/")
def delete_data(item: Item):
    db = get_db_connection()
    cursor = get_db_cursor(db)
    try:
        sql = "DELETE FROM test_table WHERE name = %s"
        cursor.execute(sql, (item.name,))
        db.commit()
        return {"message": f"데이터가 성공적으로 삭제되었습니다. 이름: {item.name}"}
    except Exception as e:
        print(f"Error in delete_data: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        db.close()

@app.get("/")
def show_data():
    db = get_db_connection()
    cursor = get_db_cursor(db)
    try:
        sql = "SELECT * FROM test_table"
        cursor.execute(sql,)
        rows = cursor.fetchall()
        return {"data": rows}
    except Exception as e:
        print(f"Error in show_data: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cursor.close()
        db.close()