from operator import attrgetter
from time import time
from typing import Union
from import_functions.check_and_import import check_and_import_db
from db_functions.connect_to_db import cursor


from fastapi import FastAPI
from schemas import Movie
from threading import Thread
from time import sleep
app = FastAPI()


@app.get("/import_cvs")
def import_cvs():
    check_and_import_db()
    sleep(1)
    return {"Hello": "World"}

@app.put("/update_movies/{movie_id}")
async def update_movies(movie_id: str, movie: Movie):
    UPDATE_QUERY= """UPDATE movies SET movie_name = %s, movie_minutes = %s WHERE id = %s"""
    cursor.execute(UPDATE_QUERY,(movie.name, movie.minutes, movie_id,))
    return True

@app.delete("/delete_movies/{movie_id}")
def delete_user(movie_id: int):
    DELETE_QUERY = """DELETE FROM movies WHERE id = %s """
    cursor.execute(DELETE_QUERY,(movie_id,))
    return True

@app.post("/add_movies")
def add_movies(movie: Movie):
    INSERT_QUERY = """INSERT INTO movies(movie_name, movie_minutes) VALUES(%s,%s)"""
    cursor.execute(INSERT_QUERY,(movie.name,movie.minutes))
    return True

@app.get("/get_movies")
def get_movies():
    cursor.execute("""SELECT id, movie_name, movie_minutes FROM movies""")
    resp = cursor.fetchall()
    if resp != []:
        return resp
    else:
        return {"error":"error"}
    

@app.get("/get_ideal_movies")
def get_ideal_movies(d: int):
    longest_possible_time = d-30
    cursor.execute("""SELECT id, movie_name, movie_minutes FROM movies """)
    resp = cursor.fetchall()
    list_of_posible_movies = []
    orgin_resp = resp
    for index, movie in enumerate(resp):
        if movie['movie_minutes'] <= longest_possible_time:
            for m in orgin_resp:
                if movie['movie_name'] != m['movie_name']:
                    if movie['movie_minutes'] + m['movie_minutes'] <= longest_possible_time:
                        format={}
                        format['minutes'] = movie['movie_minutes'] + m['movie_minutes']
                        format['movies'] = movie['movie_name'] + "," + m['movie_name']
                        list_of_posible_movies.append(format)
                        del resp[index]
    
    #list_of_posible.append({'minutes': 200, 'movies': 'The Usual Suspects equal,Trainspotting equal'}) #230
    list_of_posible_movies = sorted(list_of_posible_movies, key=lambda x: x['minutes'], reverse=True)

    if list_of_posible_movies != []:
        #options = list_of_posible[0:2] if len(list_of_posible) > 2 else list_of_posible[0]
        options = list_of_posible_movies[0:2] if list_of_posible_movies[0]['minutes'] == list_of_posible_movies[1]['minutes'] else list_of_posible_movies[0]
        
        return options
    
    return []