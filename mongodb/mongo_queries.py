from mongodb.mongo_connection import get_mongo_connection

def get_films_by_year(year):
    db = get_mongo_connection()
    collection = db["films"]
    films = collection.find({"year": year})
    return list(films)

def get_films_after_year(year):
    db = get_mongo_connection()
    collection = db["films"]
    films = collection.find({"year": {"$gt": year}})
    return list(films)

def get_average_votes_in_2007():
    db = get_mongo_connection()
    collection = db["films"]
    films = collection.find({"year": 2007})
    
    # Filtrer les films qui ont un champ "votes" valide
    votes = [film["Votes"] for film in films if "Votes" in film and isinstance(film["Votes"], int)]
    
    if votes:
        return sum(votes) / len(votes)
    else:
        return 0
