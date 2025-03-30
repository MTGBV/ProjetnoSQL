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
from neo4j_folder.neo4j_queries import (
    get_top_actor_by_film_count,
    get_actors_who_played_with_anne_hathaway,
    get_top_actor_by_revenue,
    get_average_votes,
    get_most_common_genre,
    get_films_with_my_coactors,
    get_director_with_most_actors,
    get_most_connected_films,
    get_top_actors_by_director_diversity,
    recommend_films_by_genre,
    create_influence_relationships,
    get_shortest_path_between_actors,
    get_films_same_genre_diff_directors,
    get_genre_based_recommendations,
    create_director_competition_relationships,
    get_director_competitions,
    get_top_director_actor_collaborations
)
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
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
        from neo4j_folder.neo4j_load import load_data_to_neo4j
        load_data_to_neo4j()
        st.success("Import Neo4j terminé")

    #question 14
    if st.button("Acteur ayant joué dans le plus grand nombre de films"):
        result = get_top_actor_by_film_count()
        st.write(f"L'acteur ayant joué dans le plus de films est **{result['actor']}** avec **{result['film_count']}** films.")

    # Question 15 : Acteurs ayant joué avec Anne Hathaway
    if st.button("Acteurs ayant joué avec Anne Hathaway"):
        actors = get_actors_who_played_with_anne_hathaway()
        if actors:
            st.subheader("Acteurs ayant partagé l'affiche avec Anne Hathaway 🎭")
            st.write(", ".join(actors))
        else:
            st.warning("Aucun acteur trouvé ou Anne Hathaway absente de la base.")

    # Question 16 : Acteur avec les plus gros revenus cumulés
    if st.button("Acteur avec les plus gros revenus cumulés"):
        result = get_top_actor_by_revenue()
        if result:
            st.write(
                f"L'acteur ayant généré le plus de revenus est **{result['actor']}** "
                f"avec un total de **{result['total_revenue']:.2f} millions de dollars**."
            )
        else:
            st.warning("Aucune donnée de revenus disponible.")

    # Question 17 : Moyenne des votes
    if st.button("Moyenne des votes (Neo4j)"):
        avg_votes = get_average_votes()
        if avg_votes:
            st.success(f"La moyenne des votes des films est **{avg_votes:.2f}**.")
        else:
            st.warning("Aucune donnée de vote disponible.")

    # Question 18 : Genre le plus représenté
    if st.button("Genre le plus représenté"):
        result = get_most_common_genre()
        if result:
            st.info(f"Le genre le plus représenté est **{result['genre']}** avec **{result['occurrence']}** films.")
        else:
            st.warning("Aucun genre trouvé dans la base Neo4j.")

    # Question 19 : Films des co-acteurs
    if st.button("Films joués par les co-acteurs de mon film"):
        from neo4j_folder.neo4j_queries import get_films_with_my_coactors
        films = get_films_with_my_coactors("Tanguy Vuillemin") 
        if films:
            st.success("🎬 Films dans lesquels les co-acteurs ont également joué avec Tanguy Vuillemin :")
            for title in films:
                st.markdown(f"- {title}")
        else:
            st.warning("Aucun film trouvé ou nom d'acteur incorrect.")

    # Question 20 : Réalisateur avec le plus d'acteurs distincts
    if st.button("Réalisateur avec le plus d'acteurs distincts"):
        from neo4j_folder.neo4j_queries import get_director_with_most_actors
        result = get_director_with_most_actors()
        if result:
            st.info(f"🎬 Le réalisateur **{result['director']}** a travaillé avec **{result['actor_count']}** acteurs différents.")
        else:
            st.warning("Aucun résultat trouvé.")

    # Question 21 : Films les plus connectés
    if st.button("Films les plus connectés (acteurs en commun)"):
        films = get_most_connected_films()
        if films:
            st.subheader("🎞️ Films ayant le plus d'acteurs en commun avec d'autres")
            for film in films:
                st.write(f"**{film['film']}** — {film['related_films']} connexions")
        else:
            st.warning("Aucune donnée trouvée.")

    # Question 22 : Acteurs avec le plus de réalisateurs différents
    if st.button("Top 5 acteurs par diversité de réalisateurs"):
        top_actors = get_top_actors_by_director_diversity()
        if top_actors:
            st.subheader("🎭 Acteurs ayant travaillé avec le plus de réalisateurs différents")
            for actor in top_actors:
                st.write(f"**{actor['actor']}** — {actor['directors_count']} réalisateurs")
        else:
            st.warning("Aucun acteur trouvé.")

    # Question 23 : Recommander un film à un acteur selon ses genres
    actor_input = st.text_input("Nom de l'acteur pour recommandation de films")
    if st.button("Recommander un film basé sur les genres"):
        from neo4j_folder.neo4j_queries import recommend_films_by_genre
        if actor_input:
            recommendations = recommend_films_by_genre(actor_input)
            if recommendations:
                st.subheader(f"🎥 Films recommandés pour {actor_input}")
                for rec in recommendations:
                    st.write(f"- **{rec['recommended_film']}** (Genres correspondants : {rec['matched_genres']})")
            else:
                st.warning("Aucune recommandation trouvée.")
        else:
            st.warning("Veuillez entrer un nom d'acteur.")

    # Question 24 : Influences entre réalisateurs
    if st.button("Créer les relations d'influence entre réalisateurs"):
        from neo4j_folder.neo4j_queries import create_influence_relationships
        results = create_influence_relationships()
        if results:
            st.subheader("🔁 Relations d'influence créées")
            for res in results:
                st.write(f"**{res['from_director']}** → **{res['to_director']}** (Genres partagés : {res['shared_genres']})")
        else:
            st.warning("Aucune influence détectée.")

    # Question 25 : Chemin le plus court entre deux acteurs
    actor1 = st.text_input("Acteur 1")
    actor2 = st.text_input("Acteur 2")

    if st.button("Trouver le chemin le plus court"):
        from neo4j_folder.neo4j_queries import get_shortest_path_between_actors
        if actor1 and actor2:
            path = get_shortest_path_between_actors(actor1, actor2)
            if path:
                st.success(" ➡️  ".join(str(p) if p is not None else "Inconnu" for p in path))

            else:
                st.warning("Aucun chemin trouvé entre ces deux acteurs.")
        else:
            st.warning("Veuillez entrer les deux noms.")

    # Question 27 : Films avec mêmes genres mais réalisateurs différents
    if st.button("Films similaires par genre mais réalisateurs différents"):
        films = get_films_same_genre_diff_directors()
        if films:
            st.subheader("🎞️ Films ayant un genre en commun mais des réalisateurs différents")
            for row in films:
                st.markdown(f"- **{row['film1']}** (🎬 {row['director1']}) et **{row['film2']}** (🎬 {row['director2']}) — Genre : *{row['genre']}*")
        else:
            st.warning("Aucun résultat trouvé.")

    # Question 28 : Recommandation de films par genre préféré d'un acteur
    st.subheader("🎯 Recommander des films à un acteur")

    actor_input = st.text_input("Entrez le nom d’un acteur pour obtenir des recommandations basées sur ses genres préférés")

    if st.button("Recommander des films"):
        if actor_input:
            recs = get_genre_based_recommendations(actor_input)
            if recs:
                st.success(f"🎬 Recommandations pour **{actor_input}** :")
                for r in recs:
                    st.markdown(f"- **{r['title']}** ({r['year']}) — Genre : *{r['genre']}*")
            else:
                st.warning("Aucune recommandation trouvée.")
        else:
            st.info("Veuillez entrer un nom d'acteur.")

    # Question 29 : Créer les relations de concurrence entre réalisateurs
    if st.button("Créer relations de concurrence entre réalisateurs"):
        create_director_competition_relationships()
        st.success("Relations de concurrence entre réalisateurs créées avec succès !")

    # Visualiser les relations de concurrence entre réalisateurs
    if st.button("Afficher les réalisateurs en concurrence"):
        from neo4j_folder.neo4j_queries import get_director_competitions
        edges = get_director_competitions()

        if edges:
            st.subheader("🎥 Réseaux de réalisateurs en concurrence")

            

            G = nx.DiGraph()
            for edge in edges:
                G.add_edge(edge["source"], edge["target"])

            plt.figure(figsize=(12, 8))
            pos = nx.spring_layout(G, k=0.5)
            nx.draw(G, pos, with_labels=True, node_color="skyblue", node_size=1500, edge_color="gray", arrows=True)
            st.pyplot(plt)
        else:
            st.info("Aucune relation de concurrence trouvée.")

    #question 30
    if st.button("Collaborations fréquentes réalisateur-acteur"):
        from neo4j_folder.neo4j_connection import get_neo4j_driver
        from neo4j_folder.neo4j_queries import get_top_director_actor_collaborations

        driver = get_neo4j_driver()
        result = get_top_director_actor_collaborations(driver)

        if result:
            st.subheader("🎬 Collaborations fréquentes réalisateur ↔️ acteur")
            for row in result:
                st.markdown(f"**{row['director']}** 🎥 **{row['actor']}** — {row['collaborations']} films — "
                            f"💰 Moy. revenus: {row['avg_revenue']:.2f} M$ — ⭐ Moy. rating: {row['avg_rating']}")
        else:
            st.warning("Aucune collaboration fréquente trouvée.")
