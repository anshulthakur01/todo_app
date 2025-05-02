from utils.enums import TODO_TABLE_NAME, STATUS_CHOICES, PRIORITY_CHOICES
from utils.helpers import create_table


todo_table_query = f"""
    CREATE TABLE IF NOT EXISTS {TODO_TABLE_NAME} (
        id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
        task VARCHAR(255) NOT NULL,
        description TEXT,
        status ENUM{STATUS_CHOICES},
        priority ENUM{PRIORITY_CHOICES},
        due_date DATETIME,
        updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
"""


def create_tables():
    """ Create tables in database """
    create_table(todo_table_query)
