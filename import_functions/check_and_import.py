from db_functions.connect_to_db import cursor
import time


def if_exist_table(): 
    cursor.execute("""SELECT EXISTS(SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename  = 'movies');""")
    resp = cursor.fetchone()
    print(resp)
    if resp['exists'] == False:
        return False
    else:
        return True

def check_and_import_db():

    isThereTable = if_exist_table()
    print(isThereTable)
    if isThereTable == False:
        cursor.execute("""CREATE TABLE movies(
            id serial PRIMARY KEY,
            movie_name VARCHAR(50),
            movie_minutes INT
            );""")
    
    cursor.execute("""SELECT COUNT(id) FROM movies""")
    resp = cursor.fetchone()
    print(resp)
    if resp['count'] > 0:
        print("db var kayıtlar eklenmiş")
    else:
        print("db var kayıtlar eklenmemiş")
        import_csv()



def import_csv():
    with open('/app/movies.csv', 'r') as f:
        next(f)
        cursor.copy_from(f,'movies',sep='	',columns=("movie_name", "movie_minutes"), null='')

    return True                 
    
if __name__ == "__main__":
    check_and_import_db()
