import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def create_data(conn, data):
    sql = ''' INSERT INTO data(name,elo)
              VALUES(?,?) '''
    cur = conn.cursor()
    cur.execute(sql, data)
    conn.commit()
    return cur.lastrowid


def create_history(conn, task):
    sql = ''' INSERT INTO history(id,player1,player1_elo,player2,player2_elo,team1_score,player3,player3_elo,player4,player4_elo,team2_score)
              VALUES(?,?,?,?,?,?,?,?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    return cur.lastrowid


def main():
    database = r"/Users/ethan/Desktop/My Stuff/Coding Fun/Machine_Learning/dye/pythonsqlite.db"
    # create a database connection
    conn = create_connection(database)
    with conn:
        # create a new project
        data = ('Cool App with SQLite & Python', '2015-01-01', '2015-01-30');
        project_id = create_data(conn, data)

        # tasks
        history = ('Analyze the requirements of the app', 1, 1, project_id, '2015-01-01', '2015-01-02')
        task_2 = ('Confirm with user about the top requirements', 1, 1, project_id, '2015-01-03', '2015-01-05')

        # create tasks
        create_history(conn, history)

def update_task(conn, task):
    """
    update priority, begin_date, and end date of a task
    :param conn:
    :param task:
    :return: project id
    """
    sql = ''' UPDATE tasks
              SET elo = ?
              WHERE id = ?'''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()

def main():
    database = r"C:\sqlite\db\pythonsqlite.db"

    # create a database connection
    conn = create_connection(database)
    with conn:
        update_task(conn, (2, '2015-01-04', '2015-01-06', 2))


if __name__ == '__main__':
    main()