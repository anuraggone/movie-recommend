import streamlit as st
import pickle
import requests

import streamlit as st

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Rye&display=swap');

    html, body, [class*="st-"] {
        font-family: 'Rye', sans-serif;
    }

    .stMarkdown h1 {
        font-family: 'Rye', monospace; /* Change to your desired font */
        color: #d7d0c6; /* Change to your desired color */
        font-size: 42px; /* Adjust font size if needed */
        font-weight: bold;
    }

    .stButton>button {
        background-color: #04132A ;
        font-size: 18px ; 
        border-radius: 10px ; 
        padding: 10px 20px ; 
        border: 2px solid #d5e4fb ; 

      /* hover color */
       .stButton > button:hover {
        background-color: #150656 !important;  /* Darker green on hover */
        color: white !important;
    }
    }
    .animated-background {
        position: fixed;
        top: 0;
        left: 0;
        width: 100vw;
        height: 100vh;
        background-image: url("https://i.postimg.cc/cJrbTLxt/bg.jpg");
        background-size: cover;
        background-position: center;
        z-index: -1;
        animation: zoomInOut 20s infinite ease-in-out;
        filter: brightness(0.5);
    }

   /* animation part bg zoom in and zoom out effect ( not neccessary) */
    @keyframes zoomInOut {
        0% {
            transform: scale(1);
        }
        50% {
            transform: scale(1.1);
        }
        100% {
            transform: scale(1);
        }
    }

    /* App content background */
    .stApp {
        background-color: rgba(0, 0, 0, 0.5); /* optional dark overlay */
        padding: 20px;
        border-radius: 12px;
    }


    </style>

    <!-- Add animated background div -->
    <div class="animated-background"></div>
    """,
    unsafe_allow_html=True
)

#function for fetching poster
def fetch_posters(movie_id):
    X = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=9880d08c155680a8b763c3bf2dd33c81&language=en-US'.format(movie_id))
    print(X)
    data = X.json()
    print(data)
    return "https://image.tmdb.org/t/p/w185"+ data['poster_path']


# Creating a function for pulling recommendations for the model 
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []  # Empty list to store recommendation
    recommended_movies_posters = []  # Empty list to store posters
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)  # Add all five movies
        recommended_movies_posters.append(fetch_posters(movie_id))

    return recommended_movies,recommended_movies_posters # Return the full list AFTER the loop


# Load pickled data 
# pickle connects model data with this front-end python code
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movies_list = movies['title'].values

st.title('Movies to watch')

# Option is the input box 
selected_movie= st.selectbox("Let me know your choice",
movies['title'].values
)

# this is the recommendation button


if st.button("Find similar movies", icon="📽️", use_container_width=True, type="primary"):
    Names,posters =recommend(selected_movie)
    if Names:
        col1, col2, col3 ,col4, col5 = st.columns(5)

        with col1:
          st.text(Names[0])
          st.image(posters[0],  use_container_width='auto')

        with col2:
          st.text(Names[1])
          st.image(posters[1],  use_container_width='auto')

        with col3:
          st.text(Names[2])
          st.image(posters[2],  use_container_width='auto')

        with col4:
          st.text(Names[3])
          st.image(posters[3],  use_container_width='auto')

        with col5:
          st.text(Names[4])
          st.image(posters[4], use_container_width='auto')
st.html(
    """
    <style>
    [data-testid="stExpander"] {
        background-color:#04132A ;  # Change to your desired color
    }
    </style>
    """
)

with st.expander("About me " ):
    st.write('''

This is a movie recommendation system I built from scratch,                 combining my love for film and technology.
Feel free to check out more of my projects on GitHub, and follow me on Instagram where I share photography and short film-style reels.
I’m also on LinkedIn — let’s connect!    
             [GitHub](https://github.com/anuraggone)  
             [Instagram](https://www.instagram.com/chillinghead/profilecard/?igsh=MXJ0bDJ3djlzZ2NrMQ==)  
             [Instagram](https://www.linkedin.com/in/anuragupadhyay15?utm_source=share&utm_campaign=share_via&utm_content=profile&utm_medium=android_app)  
    ''')
 
    
