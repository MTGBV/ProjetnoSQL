import streamlit as st
from mongodb.mongo_queries import (
    get_year_with_most_films,
    get_films_after_1999, 
    get_average_votes_in_2007, 
    get_films_count_by_year, 
    get_unique_genres, 
    get_highest_grossing_film, 
    get_directors_with_more_than_5_films, 
    get_movie_with_highest_revenue,
    get_genre_with_highest_average_revenue,
    get_top_director_by_total_revenue,
    get_top_genre_by_average_revenue,
    get_top_10_most_voted_movies,
    get_average_runtime_by_genre
)
import matplotlib.pyplot as plt
import seaborn as sns
from mongodb.mongo_connection import get_mongo_connection

db = get_mongo_connection()
collection = db["films"]

st.title("Exploration de Films avec MongoDB")
st.markdown("Cette application vous permet d'explorer une base de données de films.")

menu = st.sidebar.selectbox("Sélectionner une section", ["MongoDB", "Analyse", "Neo4j"])

if menu == "MongoDB":
    st.header("Requêtes MongoDB")

    # Question 1 : Afficher l'année où le plus grand nombre de films ont été sortis
    if st.button("Année avec le plus grand nombre de films"):
        year, count = get_year_with_most_films()
        st.write(f"L'année avec le plus grand nombre de films est {year} avec {count} films.")
    
    # Question 2 : Nombre de films sortis après 1999
    if st.button("Nombre de films après 1999"):
        films_after_1999 = get_films_after_1999()
        st.write(f"Le nombre de films sortis après 1999 est : {films_after_1999}")

    # Question 3 : Moyenne des votes des films sortis en 2007
    if st.button("Moyenne des votes des films de 2007"):
        avg_votes_2007 = get_average_votes_in_2007()
        st.write(f"La moyenne des votes des films de 2007 est : {avg_votes_2007}")
    
    # Question 4 : Histogramme du nombre de films par année
    if st.button("Histogramme du nombre de films par année"):
        years, counts = get_films_count_by_year()
        
        plt.figure(figsize=(12, 6))
        sns.barplot(x=years, y=counts)
        plt.xticks(rotation=90)
        plt.xlabel("Année")
        plt.ylabel("Nombre de films")
        plt.title("Nombre de films par année")
        st.pyplot(plt)

    # Question 5 : Genres disponibles dans la base
    if st.button("Afficher les genres disponibles"):
        genres = get_unique_genres()
        st.write("Genres disponibles dans la base de données :")
        st.write(", ".join(genres))

    # Question 6 : Film qui a généré le plus de revenus
    if st.button("Film avec le plus de revenus"):
        title, revenue = get_highest_grossing_film()
        if title:
            st.write(f"Le film ayant généré le plus de revenus est **{title}** avec **{revenue} millions $**.")
        else:
            st.write("Aucun film trouvé avec des données de revenus valides.")

    # Question 7 : Réalisateurs ayant réalisé plus de 5 films
    if st.button("Réalisateurs ayant réalisé plus de 5 films"):
        directors = get_directors_with_more_than_5_films()
        if directors:
            st.write("🎬 Réalisateurs ayant réalisé plus de 5 films :")
            for d in directors:
                st.write(f"- {d['director']} ({d['film_count']} films)")
        else:
            st.write("Aucun réalisateur avec plus de 5 films dans la base.")

        # Question 8 : Film avec les plus hauts revenus (par fonction dédiée)
    if st.button("Film avec les plus hauts revenus"):
        movie = get_movie_with_highest_revenue(collection)
        if movie:
            st.subheader("🎬 Film ayant généré le plus de revenus")
            st.markdown(f"**Titre** : {movie['title']}")
            st.markdown(f"**Revenus** : {movie['Revenue (Millions)']} millions de dollars 💰")
        else:
            st.warning("Aucun film trouvé avec des revenus renseignés.")

    # Question 9 : Genre avec la plus haute moyenne de revenus
    if st.button("Genre le plus rentable en moyenne"):
        top_genre = get_genre_with_highest_average_revenue(collection)
        if top_genre:
            st.success(f"Le genre **{top_genre['_id']}** a la moyenne de revenus la plus élevée : **{top_genre['average_revenue']:.2f} millions $**.")
        else:
            st.warning("Aucun genre trouvé avec des revenus valides.")

        # Question 10 : Réalisateur avec le revenu total le plus élevé
    if st.button("Réalisateur le plus rentable"):
        top_director = get_top_director_by_total_revenue(collection)
        if top_director:
            st.success(f"Le réalisateur **{top_director['_id']}** a généré le plus de revenus au total : **{top_director['total_revenue']:.2f} millions $**.")
        else:
            st.warning("Aucun réalisateur trouvé avec des données de revenus valides.")

        # Question 11 : Genre le plus rentable en moyenne
    if st.button("Genre le plus rentable (moyenne des revenus)"):
        top_genre = get_top_genre_by_average_revenue(collection)
        if top_genre:
            st.info(f"Le genre **{top_genre['_id']}** rapporte en moyenne **{top_genre['average_revenue']:.2f} millions $**.")
        else:
            st.warning("Aucun genre trouvé avec des données de revenus valides.")

        # Question 12 : Top 10 des films les plus votés
    if st.button("Top 10 films avec le plus de votes"):
        top_voted = get_top_10_most_voted_movies(collection)
        if top_voted:
            st.subheader("Films les plus votés :")
            for movie in top_voted:
                st.markdown(f"**{movie['title']}** — {movie['Votes']} votes")
        else:
            st.warning("Aucun film trouvé avec des données de votes.")

    # Question 13 : Durée moyenne des films par genre
    if st.button("Durée moyenne par genre"):
        avg_runtimes = get_average_runtime_by_genre(collection)
        if avg_runtimes:
            st.subheader("Durée moyenne des films par genre (en minutes)")
            for genre in avg_runtimes:
                st.markdown(f"- **{genre['_id']}** : {round(genre['average_runtime'], 2)} min")
        else:
            st.warning("Aucune donnée de durée trouvée pour les genres.")

    
elif menu == "Analyse":
    st.header("Analyse des Données")
    # Code d'analyse des données ici


elif menu == "Neo4j":
    st.header("Chargement MongoDB → Neo4j")
    if st.button("Exporter les films depuis MongoDB"):
        from mongodb.mongo_to_neo4j import export_mongodb_films_for_neo4j
        export_mongodb_films_for_neo4j()
        st.success("Export MongoDB terminé")

    if st.button("Importer dans Neo4j"):
        from neo4j.neo4j_load import load_data_to_neo4j
        load_data_to_neo4j()
        st.success("Import Neo4j terminé")
