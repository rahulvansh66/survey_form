import sqlite3
from sqlite3 import Error
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

def select_all_tasks(conn, start_idx, db_name):
    cur = conn.cursor()
    cur.execute("SELECT * FROM "+db_name+" LIMIT "+str(start_idx)+", 3 ")
    pairset = cur.fetchall()
    return pairset

def get_summ_pairs(conn):
    with conn:
      
      tmp2 = conn.execute("SELECT curr_idx  FROM metadata WHERE var_name = 'pens_start_idx';")
      pens_start_idx = int(tmp2.fetchone()[0])

      rows = select_all_tasks(conn, pens_start_idx, 'user_pairs')
      rows.extend(select_all_tasks(conn, pens_start_idx, 'pens_pairs'))
      pens_start_idx += 3

      conn.execute("UPDATE metadata SET curr_idx = "+str(pens_start_idx)+" WHERE var_name = 'pens_start_idx';")

    print('pens_start_idx : ', pens_start_idx)
    
    return rows

def store_res(conn, pairs, name, res):
  
  for i in range(6):
    with conn:
      conn.execute("INSERT INTO response VALUES( ?,?,?,?,?,?)", (str(name), pairs[i][0], pairs[i][1], pairs[i][2], pairs[i][3], res[i]))

