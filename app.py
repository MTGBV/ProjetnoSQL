import streamlit as st
from mongodb.mongo_queries import get_films_by_year, get_films_after_year, get_average_votes_in_2007
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Exploration de Films avec MongoDB")
st.markdown("Cette application vous permet d'explorer une base de données de films.")

menu = st.sidebar.selectbox("Sélectionner une section", ["MongoDB", "Analyse"])

if menu == "MongoDB":
    st.header("Requêtes MongoDB")
    year = st.number_input("Entrez une année pour voir les films", min_value=1900, max_value=2025)
    if year:
        films = get_films_by_year(year)
        st.write(films)

    if st.button("Films après 1999"):
        films_after_1999 = get_films_after_year(1999)
        st.write(f"Films après 1999: {len(films_after_1999)}")

    if st.button("Moyenne des votes 2007"):
        avg_votes = get_average_votes_in_2007()
        st.write(f"Moyenne des votes des films de 2007: {avg_votes}")

elif menu == "Analyse":
    st.header("Analyse des Données")
    films_data = get_films_after_year(1990)
    years = [film['year'] for film in films_data]
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(years, bins=30, kde=False, ax=ax)
    ax.set_title("Nombre de films par année")
    ax.set_xlabel("Année")
    ax.set_ylabel("Nombre de films")
    st.pyplot(fig)
