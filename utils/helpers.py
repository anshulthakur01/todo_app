import mysql.connector

from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME
from utils.enums import TODO_TABLE_NAME


def sidebar_content():
    conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    cursor = conn.cursor()

    query = """
    SELECT
    COUNT(CASE WHEN created_at >= CURRENT_DATE THEN 1 END) AS today_count,
    COUNT(*) AS total_count,
    COUNT(CASE WHEN priority = 'high' THEN 1 END) AS high_priority_count
    FROM todo_tasks;
    """

    try:
        cursor.execute(query)
        # Fetch the result from the query
        result = cursor.fetchone()

        # Unpack the result counts
        today_count = result[0]
        total_count = result[1]
        high_priority_count = result[2]

        return {
            "total_count": total_count,
            "today_count": today_count,
            "high_priority_count": high_priority_count
        }

    except mysql.connector.Error as err:
        # Corrected error message for query execution
        print(f"Error executing query: {err}")
    finally:
        # Clean up resources
        cursor.close()
        conn.close()

def create_table(table_query: str):
    conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    cursor = conn.cursor()

    try:
        cursor.execute(table_query)
        print("Table created successfully.")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")
    finally:
        cursor.close()
        conn.close()

def get_task_list():
    query = f"SELECT * FROM {TODO_TABLE_NAME};"

    conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query)
    return cursor.fetchall()

def get_task(field: str, value):
    query = f"SELECT * FROM {TODO_TABLE_NAME} WHERE {field} = %s;"
    conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(query, (value,))
        return cursor.fetchone()
    finally:
        conn.close()


def create_todo_task(data: dict):
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["%s"] * len(data))

    query = f"INSERT INTO todo_tasks({columns}) VALUES ({placeholders})"
    conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(query, tuple(data.values()))
        conn.commit()
        return cursor.fetchone()
    finally:
        cursor.close()
        conn.close()


def edit_todo_task(data: dict, id):
    # Generate the SET clause dynamically based on the keys in the `data` dictionary
    set_clause = ", ".join([f"{key} = %s" for key in data.keys()])

    query = f"""
    UPDATE todo_tasks 
    SET {set_clause} 
    WHERE id = %s;
    """

    conn = mysql.connector.connect(host=DB_HOST, user=DB_USER, password=DB_PASSWORD, database=DB_NAME)
    cursor = conn.cursor()

    try:
        # Execute the query with the data values and task ID
        cursor.execute(query, tuple(data.values()) + (id,))
        conn.commit()
        return {"success": True, "affected_rows": cursor.rowcount}
    except mysql.connector.Error as err:
        print(f"Error updating task: {err}")
        return {"success": False, "error": str(err)}
    finally:
        cursor.close()
        conn.close()

def delete_todo_task(field, value):
    query = f"DELETE FROM {TODO_TABLE_NAME} WHERE {field} = %s;"
    conn = mysql.connector.connect(
        host=DB_HOST, 
        user=DB_USER, 
        password=DB_PASSWORD, 
        database=DB_NAME
    )
    cursor = conn.cursor()

    try:
        cursor.execute(query, (value,))
        conn.commit()
        return {"success": True, "affected_rows": cursor.rowcount}
    except mysql.connector.Error as err:
        print(f"Error deleting task: {err}")
        return {"success": False, "error": str(err)}
    finally:
        cursor.close()
        conn.close()