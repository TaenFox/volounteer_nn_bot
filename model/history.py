import db

def do_history(table, field, value, operator):
    query = f"INSERT INTO `{db.db_base}`.`history`  \
        (`table`,`field`,`new_value`,`storage`) \
VALUES ('{table}','{field}','{value}','{operator}')"
    db.cursor.execute(query)
    db.conn.commit()

def do_history_storage(field, value, operator):
    do_history('storages', field, value, operator)