import mysql.connector
import json

def get_connection():
    connection = mysql.connector.connect(
        host='localhost',
        database='ChatBot',
        user='root',
        password='password'
    )
    return connection


def add_source(user_id: int, pdf_name: str, pdf_id: list):
    connection = get_connection()
    cursor = connection.cursor()
    pdf_id_json = json.dumps(pdf_id)
    cursor.execute("INSERT INTO source (user_id, pdf_name, pdf_id) VALUES (%s, %s, %s)", (user_id, pdf_name, pdf_id_json))
    connection.commit()
    cursor.close()
    connection.close()
    

def remove_source(user_id: int, user_pdf_id: int):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT pdf_id FROM source WHERE user_id = %s AND id = %s", (user_id, user_pdf_id,))    
    result = cursor.fetchall() 

    cursor.execute("DELETE FROM source WHERE user_id = %s AND id = %s", (user_id, user_pdf_id))
    connection.commit()
    
    cursor.close()
    connection.close()

    return [row[0] for row in result]