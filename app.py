import streamlit as st 
import datetime
import time
import requests
import pandas as pd
from PIL import Image
from Packages.utils import geocoder_here, reverse_geocoder_here
from Packages.utils import query_api, format_name, get_poster, get_movie_info
# from Packages.confirm_button_hack import cache_on_button_press
from Packages.gcp import get_movie_name_lst

st.set_page_config(
    page_title="My project gallary",
    page_icon="🎃",
    layout="centered", # wide
    initial_sidebar_state="auto") # collapsed
CSS='''
            h1, h2, h3, h4 {
                text-align: center;
                color: #1D3C26
            }
            body {
                color: #1D3C26
            }
        '''
st.write(f'<style>{CSS}</style>', unsafe_allow_html=True)

st.sidebar.markdown('## Navigation')
page = st.sidebar.radio("Go to", ("Home", "Taxifare Prediction", "Movie Recommendation"))

def main():
    if page == "Home":
        css= '''
                    h1 {
                        color: #EADFCE;
                        text-align: center;
                    }
                    body {
                        background-color: #1D3C26;
                    }
                    '''
        st.write(f'<style>{css}</style>', unsafe_allow_html=True)

        
        "# Welcome to my project gallary!"
        
        col1, col2, col3 = st.beta_columns(3)

        
        image = Image.open("img/circle-me.png")
        col2.image(image, use_column_width=True)

    if page == "Taxifare Prediction":

        '''
        # Taxi Fare Prediction

        This page queries a [taxi fare model API]
        (https://predict-taxifare-iwuisdewea-ez.a.run.app/predict_fare)
        '''



        ## input pickup time
        pickup_date = st.date_input('pickup date', value=datetime.datetime.today())
        pickup_time = st.time_input('pickup time', value=datetime.datetime.now())
        pickup_datetime = f'{pickup_date} {pickup_time}UTC'

        geo = st.radio("Select a Geo Format:", ("by address", "by coordinates"))
        if geo == "by coordinates":
            ## Get coordinates from user input and get address
            #pickup place
            pickup_lng = st.number_input('pickup longitude', value=40.7614327)
            pickup_lat = st.number_input('pickup latitude', value=-73.9798156)
            pickup_adress = reverse_geocoder_here((pickup_lng, pickup_lat))['adress']
            pickup_longitude = reverse_geocoder_here((pickup_lng, pickup_lat))['lng']
            pickup_latitude = reverse_geocoder_here((pickup_lng, pickup_lat))['lat']
            st.info(f"The pickup address: {pickup_adress}")
            #dropoff place
            dropoff_lng = st.number_input('dropoff longitude', value=40.6413111)
            dropoff_lat = st.number_input('dropoff latitude', value=-73.7803331)
            dropoff_adress = reverse_geocoder_here((dropoff_lng, dropoff_lat))['adress']
            dropoff_longitude = reverse_geocoder_here((dropoff_lng, dropoff_lat))['lng']
            dropoff_latitude = reverse_geocoder_here((dropoff_lng, dropoff_lat))['lat'] 
            st.info(f"The dropoff address: {dropoff_adress}")

        if geo == "by address":
            ## Get address from user input
            pickup_adress = st.text_input("pickup address", "251 Church St, New York, NY 10013")
            dropoff_adress = st.text_input("dropoff address", "434 6th Ave, New York, NY 10011")
            ## Get coordinates
            try:
                pickup_latitude = geocoder_here(pickup_adress)['lat']
                pickup_longitude = geocoder_here(pickup_adress)['lng']
                dropoff_latitude = geocoder_here(dropoff_adress)['lat']
                dropoff_longitude = geocoder_here(dropoff_adress)['lng']
            except:
                st.error("Couln't retrive coordinates from the adreess.")

        ## Draw a map
        map_data = pd.DataFrame({"lat":[pickup_latitude,dropoff_latitude], 
                                 "lon":[pickup_longitude,dropoff_longitude]})
        st.map(data=map_data)

        passenger_count = st.number_input('passenger_count', min_value=1, max_value=8, step=1, value=1)

        ### Forat input
        params = dict(
            key='2012-10-06 12:10:20.0000001',
            pickup_datetime=pickup_datetime,
            pickup_longitude=pickup_longitude,
            pickup_latitude=pickup_latitude,
            dropoff_longitude=dropoff_longitude,
            dropoff_latitude=dropoff_latitude,
            passenger_count=passenger_count
        )

        pred = query_api("taxifare", params)["prediction"]

        if st.button('Calculate Taxifare'):
            st.markdown(f"Taxi Fare: `${round(pred, 2)}`")
    
    if page == "Movie Recommendation":
        
        '''
        # Movie Recommendation

        This page queries a [movie recommendation API]
        (https://movie-recommender-5i6qxbf74a-ez.a.run.app/recommendation)
        '''


        @st.cache
        def get_select_box_data():
            return get_movie_name_lst().tolist()
        name_lst = get_select_box_data()
        

        ############################################
        ### Get & format params from user input ####
        ############################################
        "**☝️ To get started, please select one or more movies you've enjoyed!**"
        options = st.multiselect('Type and select the title...', name_lst, ["Shawshank Redemption, The (1994)"])
        samples = ", '".join([f"{option}" for option in options])
        
        "**👉 How many recommendaitons do you want to see?**"
        n_movies = st.slider('Select from 1 to 10: ', 1, 10, 1)
        
        "**👉 Tweak Recommendation Basis (Optional)**"
        '''
        By default, recommendations would be talored based on a hybrid of `Metadata (Genres, Tag)` and `Viewer Rating` of the chosen movies.  
        Optionally, you can change the recommendation basis down below.
        '''
        basis="hybrid"
        with st.beta_expander("Change basis"):
            basis=st.radio("", ["metadata", "rating", "hybrid"])

        '''
        
          
        '''
        
        params = dict(samples=samples,
                      n_movies=n_movies,
                      basis=basis)
        

        ###########################################
        # Query api to get recommendation results #
        ###########################################
        if samples:
            recommendations = query_api("movie_recommendation", params)["recommendations"]
    
        def display_recommendation(i, recommendations):
            recommendation=recommendations[i]
            title=format_name(recommendation["name"])["title"]
            img = get_poster(recommendation['name'])
            info = get_movie_info(recommendation['name'])
            similarity = round(recommendation['similarity'], 3) * 100
            ###########################################
            # The 1st column display movie infomations.
            ############################################
            col1, col2 = st.beta_columns(2)
            col1.markdown(f"#### `{similarity}%` Similarity")
            col1.markdown(f"### :clapper: {title}")
            for k,v in info.items():
                if k != "Poster" and v and v != "N/A":
                    col1.markdown(f" :small_orange_diamond: **{k}:** {v}")
            ##################################
            #  The 2ed column show the poster
            #################################
            if img:
                col2.image(img, use_column_width=True)

        ################
        ### Display ####
        ################
        _, col_m, _ = st.beta_columns(3)
        confirm = col_m.empty()

        if confirm.button("📬 Check it!"):
            # confirm.markdown(f'<div style="text-align: center;">🕛</div>',unsafe_allow_html=True)
            display_recommendation(0, recommendations)
            for i in range(len(recommendations)):
                if i > 0:
                    title = format_name(recommendations[i]['name'])["title"]
                    with st.beta_expander(f"🍿 No.{i+1}: {title}"):
                        display_recommendation(i,recommendations)
                        

if __name__ == "__main__":
    main()
