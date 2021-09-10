import sqlite3
from datetime import datetime


class Database:
    def __init__(self, path_to_db="data/main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(
            self,
            sql: str,
            parameters: list = None,
            fetchone=False,
            fetchall=False,
            commit=False,
    ):

        if not parameters:
            parameters = []
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()

        return data

    # Функции для Usera

    def create_table_users(self):
        sql = """
        CREATE TABLE if not exists users (
            id int NOT NULL,
            first_name varchar(255)  ,
            last_name varchar(255)  ,
            phone_number varchar(255)   ,
            email varchar(255),
            is_registered BOOLEAN,
            PRIMARY KEY (id)
            );
"""
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([f"{item} = ?" for item in parameters])
        return sql, tuple(parameters.values())

    def admin_add_users(self, id: int, is_registered: bool):
        sql = """
                   INSERT INTO users(id,is_registered) VALUES(?,?)
          """
        self.execute(sql, parameters=(id, is_registered), commit=True)

    def add_user(
            self,
            first_name: str,
            last_name: str,
            phone_number: str,
            email: str,
            is_registered: bool,
            id: int,
    ):
        # SQL_EXAMPLE = "INSERT INTO Users(id, Name, email) VALUES(1, 'John', 'John@gmail.com')"

        sql = """
           UPDATE users SET first_name =?,last_name=?,phone_number=?,email=?,is_registered=? WHERE id=?
            """
        self.execute(
            sql,
            parameters=(first_name, last_name, phone_number, email, is_registered, id),
            commit=True,
        )

    def select_all_users(self):
        sql = """
            SELECT * FROM users WHERE 
            """
        return self.execute(sql, fetchall=True)

    def select_all_tg_id(self):
        sql = """
            SELECT  id FROM users
        """

        return self.execute(sql, fetchall=True)

    def select_isregis(self, id: int):
        sql = """
        SELECT id=? FROM users WHERE is_registered
        """
        return self.execute(sql, parameters=(id,), fetchone=True, commit=True)

    # def select_user(self, **kwargs):
    # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
    # sql = "SELECT * FROM Users WHERE"
    # sql, parameters = self.format_args(sql, kwargs)
    # return self.execute(sql, parameters, fetchone=True)
    def get_users(self):
        sql = """
        SELECT * FROM users 
        """
        return self.execute(sql, fetchall=True, commit=True)

    def select_user(self, id: int):
        sql = "SELECT  first_name,last_name,phone_number,email FROM users WHERE id=? "

        return self.execute(sql, parameters=(id,), fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM users;", fetchone=True)

    def select_task_get(self, user_id: int):
        sql = "SELECT  name,description,date1,sprint_id FROM tasks WHERE user_id=? and task_done = TRUE "

        return self.execute(sql, parameters=(user_id,), fetchall=True, commit=True)

    def done_task(self, user_id: int):
        sql = "SELECT task_done From tasks WHERE user_id=?"
        return self.execute(sql, parameters=(user_id,), fetchall=True, commit=True)

    def get_user_tasks(self):
        sql = """
        SELECT * FROM tasks WHERE user_id IS NULL 
        """
        return self.execute(sql, fetchall=True, commit=True)

    # Функции АДМИНА
    def get_admin_tasks(self):
        sql = """
        SELECT * FROM tasks  
        """
        return self.execute(sql, fetchall=True, commit=True)

    # def count_tasks(self):
    #     return self.execute("SELECT COUNT(id) FROM tasks;", fetchone=True)

    # Функции для Tasks
    def create_table_Tasks(self):
        sql = """
                CREATE TABLE if not exists tasks (
                    id INTEGER primary key AUTOINCREMENT,
                    description varchar(255) NOT NULL ,
                    date1 DATETIME,
                    name varchar(255)NOT NULL ,
                    user_id  int NULL ,
                    sprint_id int NULL ,
                    task_done BOOLEAN default TRUE,
                    FOREIGN KEY (sprint_id)REFERENCES Sprint(id)
                    FOREIGN KEY (user_id) REFERENCES users(id)
                    );
        """
        self.execute(sql, commit=True)

    def add_tasks(self, name: str, description: str, date1: datetime, sprint_id):
        sql = """
                   INSERT INTO tasks(name,description,date1,sprint_id) VALUES(?, ?,?,?)
          """
        self.execute(sql, parameters=(name, description, date1, sprint_id), commit=True)

    def select_tasks(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM Users where id=1 AND Name='John'"
        sql = "SELECT * FROM tasks WHERE"
        sql, parameters = self.format_args(sql, kwargs)
        return self.execute(sql, parameters, fetchone=True)

    def count_tasks(self):
        return self.execute("SELECT COUNT(*) FROM tasks;", fetchone=True)

    # Функции Админа :
    def create_table_Admin(self):
        sql = """
                CREATE TABLE if not exists admin (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id  INTEGER NULL ,
                   FOREIGN KEY (user_id) REFERENCES users(id)
                    );
        """
        self.execute(sql, commit=True)

    def add_id_task(self, user_id: int, id: int):
        sql = """
            UPDATE tasks SET user_id=? WHERE id=?
        """
        self.execute(sql, parameters=(user_id, id), fetchone=True, commit=True)

    def update_task_user(self, task_done: bool, name_task: str):
        sql = """
            UPDATE tasks SET task_done=?  WHERE name =?
        """
        self.execute(sql, parameters=(task_done, name_task), fetchone=True, commit=True)

    def admin_add_user(self, user_id: int):
        sql = """
                   INSERT INTO admin(user_id) VALUES(?)
          """
        self.execute(sql, parameters=(user_id,), commit=True)

    def admin_Retro(self, Sprint_id: int):
        sql = """
        SELECT Mood,Good,Bad,user_id FROM Retro WHERE Sprint_id=?
        """
        return self.execute(sql, parameters=(Sprint_id,), fetchall=True, commit=True)

    # Функции Sprint :
    def create_table_Sprint(self):
        sql = """
                CREATE TABLE if not exists Sprint (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name_Sprint VARCHAR(255),
                    from_date DATE NOT NULL ,
                    last_date DATE NOT NULL ,
                   FOREIGN KEY (id) REFERENCES admin(id)
                    );
        """
        self.execute(sql, commit=True)

    def add_Sprint(self, name_Sprint: str, from_date: datetime, last_date: datetime):
        sql = "INSERT INTO Sprint(name_Sprint,from_date,last_date) VALUES (?,?,?)"

        self.execute(sql, parameters=(name_Sprint, from_date, last_date), commit=True)

    def sprint_all(self):
        sql = """
        SELECT * FROM Sprint
        """
        return self.execute(sql, fetchall=True, commit=True)

    def add_id_sprint(self, user_id: int, id: int):
        sql = """
            UPDATE tasks SET user_id=? WHERE id=?
        """
        self.execute(sql, parameters=(user_id, id), fetchone=True, commit=True)
        # RETRO функции

    def create_table_Retro(self):
        sql = """
                CREATE TABLE if not exists Retro (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    Mood VARCHAR(255),
                    Good VARCHAR(255),
                    Bad VARCHAR(255),
                    Sprint_id INTEGER ,
                    user_id INTEGER ,
                   FOREIGN KEY (user_id) REFERENCES users(id),
                   FOREIGN KEY (Sprint_id) REFERENCES Sprint(id)
                    );
        """
        self.execute(sql, commit=True)

    def add_Retro(self, Mood: str, Good: str, Bad: str, Sprint_id: int, user_id: int, ):
        sql = "INSERT INTO Retro(Mood,Good,Bad,Sprint_id,user_id) VALUES (?,?,?,?,?)"

        self.execute(sql, parameters=(Mood, Good, Bad, Sprint_id, user_id), commit=True)

    def add_Retro_Mood(self, Mood: str, Sprint_id: int, user_id: int):
        sql = "INSERT INTO Retro(Mood,Sprint_id,user_id) VALUES (?,?,?)"
        self.execute(sql, parameters=(Mood, Sprint_id, user_id), commit=True)

    def add_Retro_Good(self, Good: str, Sprint_id: int, user_id: int):
        sql = "INSERT INTO Retro(Good,Sprint_id,user_id) VALUES (?,?,?)"
        self.execute(sql, parameters=(Good, Sprint_id, user_id), commit=True)

    def add_Retro_Bad(self, Bad: str, Sprint_id: int, user_id: int):
        sql = "INSERT INTO Retro(Bad,Sprint_id,user_id) VALUES (?,?,?)"
        self.execute(sql, parameters=(Bad, Sprint_id, user_id), commit=True)

    def clear_table_users(self):
        sql = "DRop TABLE users WHERE id and first_name"
        self.execute(sql, commit=True)

    def clear_table_Retro(self):
        sql = "DROP TABLE Retro"
        self.execute(sql, commit=True)

    def clear_table_tasks(self):
        sql = "DROP TABLE tasks"
        self.execute(sql, commit=True)

    def clear_table_Sprint(self):
        sql = "DROP TABLE Sprint"
        self.execute(sql,commit=True)

    def clear_table_admin(self):
        sql = "DROP TABLE admin"
        self.execute(sql,commit=True)


def logger(statement):
    print(
        f"""
    _____________________________________________________        
    Executing: 
    {statement}
    _____________________________________________________
    """
    )
