import sqlite3
from typing import List
import datetime
from model import Todo

conn = sqlite3.connect('todos.db')
c = conn.cursor()


def create_table():
    c.execute("""CREATE TABLE IF NOT EXISTS todos (
            namespace text,
            deploy text,
            version text,
            date_added text,
            date_match text,
            status integer,
            position integer
            )""")


create_table()


def insert_todo(todo: Todo):
    c.execute('select count(*) FROM todos')
    count = c.fetchone()[0]
    todo.position = count if count else 0
    with conn:
        c.execute('INSERT INTO todos VALUES (:namespace, :deploy, :version, :date_added, :date_match, :status, :position)',
        {'namespace': todo.namespace, 'deploy': todo.deploy, 'version': todo.version, 'date_added': todo.date_added,
         'date_match': todo.date_match, 'status': todo.status, 'position': todo.position })


def get_all_todos() -> List[Todo]:
    c.execute('select * from todos')
    results = c.fetchall()
    todos = []
    for result in results:
        todos.append(Todo(*result))
    return todos


def delete_todo(position):
    c.execute('select count(*) from todos')
    count = c.fetchone()[0]

    with conn:
        c.execute("DELETE from todos WHERE position=:position", {"position": position})
        for pos in range(position+1, count):
            change_position(pos, pos-1, False)


def change_position(old_position: int, new_position: int, commit=True):
    c.execute('UPDATE todos SET position = :position_new WHERE position = :position_old',
                {'position_old': old_position, 'position_new': new_position})
    if commit:
        conn.commit()


def update_todo(position: int, namespace: str,  deploy: str, version: str):
    with conn:
        if namespace is not None and deploy is not None and version is not None:
            c.execute('UPDATE todos SET namespace = :namespace, deploy = :deploy, version = :version WHERE position = :position',
                      {'position': position, 'namespace': namespace, 'deploy': deploy, 'version': version})
        elif namespace is not None:
            c.execute('UPDATE todos SET namespace = :namespace WHERE position = :position',
                      {'position': position, 'namespace': namespace})
        elif deploy is not None:
            c.execute('UPDATE todos SET deploy = :deploy WHERE position = :position',
                      {'position': position, 'deploy': deploy})
        elif version is not None:
            c.execute('UPDATE todos SET version = :version WHERE position = :position',
                      {'position': position, 'version': version})


def match_todo(position: int):
    with conn:
        c.execute('UPDATE todos SET status = 2, date_match = :date_match WHERE position = :position',
                  {'position': position, 'date_match': datetime.datetime.now().isoformat()})
