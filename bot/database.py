import psycopg2
from secret import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT

def get_connection():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        return conn
    except Exception as e:
        print(f"Error: Unable to connect to the database\n{e}")
        return None

def create_order(order_details):
    conn = get_connection()
    if not conn:
        return
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "INSERT INTO orders (details) VALUES (%s) RETURNING id;", 
                (order_details,)
            )
            order_id = cursor.fetchone()[0]
            conn.commit()
            return order_id
    except Exception as e:
        print(f"Error: Unable to insert data into database\n{e}")
    finally:
        conn.close()
