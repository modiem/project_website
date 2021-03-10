import streamlit as st 
import datetime
import time
import requests
import pandas as pd
from io import StringIO
import json
from PIL import Image
from Packages.utils import geocoder_here, reverse_geocoder_here
from Packages.utils import query_api, format_name, get_poster, get_movie_info
# from Packages.confirm_button_hack import cache_on_button_press
from Packages.gcp import get_movie_name_lst, get_gyms
from Packages import plot_map
from Packages import choropleth
from streamlit_folium import folium_static

st.set_page_config(
    page_title="My project",
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
page = st.sidebar.radio("Go to", ("Home",  "Taxifare Prediction", "Movie Recommendation", "Plot Choropleth Map", "TreeMap"))

def main():
    @st.cache
    def get_gym_df():
        return get_gyms()
    if page == "Home":
        css= '''
                    h1, p {
                        color: #EADFCE;
                        text-align: center;
                    }
                    body {
                        background-color: #1D3C26;
                    }
                    '''
        st.write(f'<style>{css}</style>', unsafe_allow_html=True)

        '''
        # Welcom to my project gallery!
        '''
        
        
        col1, col2, col3 = st.beta_columns(3)

        image = Image.open("img/circle-me.png")
        col2.image(image, use_column_width=True)

        '''
        
        👉 [Source Code](https://github.com/modiem/project_website)

        '''
        st.write('<a href = "mailto: moyang.diem@example.com">👉 Contact me</a>', unsafe_allow_html=True)
        
    if page == "Plot Choropleth Map":
        '''
        # Plot Choropleth Map 
        ## Step-by-step guidance
        ###
        > A choropleth map displays divided geographical areas or regions that are coloured in relation to a numeric variable. 
        > It allows to study how a variable evolutes along a territory. 
        
        '''
        example = st.checkbox("Example: Amsterdam gym distribution")

        if example:
            df = get_gym_df()
            location_col = "Stadsdeel"
            with open("geojson.json") as f:
                geojson=json.load(f)
            featureId = "Stadsdeel"
            example_map=choropleth.plot_choropleth(df=df,
                                    geojson=geojson,
                                    location_col=location_col,
                                    featureid=featureId)
            st.write(example_map)
            '''   
            [data source] (https://data.amsterdam.nl/)
            '''

        '''
        
        **Like what you see?**

        Simply follow these 3️⃣ steps to get your own choroploth map.🚀
        '''
        
        
        '''
        ### 🗃 Data File `.csv`
        **Require:** `location column` (A discrete color will be assined to each location on basis of density)

        '''
        df_ = None
        geojson_= None
        location_col_=None
        featureId_=None
        st.markdown('''
            ''')
        uploaded_file = st.file_uploader("Upload a csv file")
        if uploaded_file is not None:
            df_ = pd.read_csv(uploaded_file)
            st.success('Data file uploaded.')  
            with st.beta_expander("🔎 Print DataFrame Head"):
                st.write(df_.sample(5))    
            st.markdown('''
                👇🏻 Choose the location column (a discrete color will be assigned to this area)
                ''')   
            location_col_=st.selectbox("From columns", df_.columns.tolist())  
        '''  
        ### 📐 `GeoJSON` for BaseMap 
        **Require:** a identifying key under `features.properties` that can map to `location column`.
        
        [Example](https://maps.amsterdam.nl/open_geodata/geojson.php?KAARTLAAG=GEBIED_STADSDELEN&THEMA=gebiedsindeling)
        '''
        uploaded_file_geo = st.file_uploader("Upload a GeoJSON")
            
        if uploaded_file_geo is not None:
            stringio = StringIO(uploaded_file_geo.getvalue().decode("utf-8"))
            st.success('GeoJSON uploaded.')
            geojson_ = json.load(stringio)
            with st.beta_expander("🔎 Print the first feature"):
                st.write(geojson_["features"][0])
            st.markdown(
                '''
                👇🏻 Choose the identifying key from properties to draw a border line around.
                '''
            )
            if geojson_:
                featureId_ = st.selectbox("From properties", list(geojson_["features"][0]["properties"].keys()))
        '''
        ### 🪴 Styling
        '''        
        pallete = st.selectbox("Choose color pallet", ['teal','brwnyl', 'cividis', 'fall', 'geyser', 'deep', 'tempo'])

        '''
        ## 
        '''
        if df_ and geojson_ and location_col_ and featureId_:
            result_map=choropleth.plot_choropleth(df=df_,
                                    geojson=geojson_,
                                    location_col=location_col_,
                                    featureid=featureId_,
                                    pallete=pallete)
            st.write(result_map)

        

    if page == "Taxifare Prediction":
       
        css= '''
                    body {
                        background-color: #C1CDCD;
                    }
                    '''
        st.write(f'<style>{css}</style>', unsafe_allow_html=True)
        '''
        # Taxi Fare Prediction

        This page queries a [Taxifare Model API]
        (https://github.com/modiem/taxifare)
         built with FastAPI, Docker, Google Cloud Run.
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

        col1, col2, col3 = st.beta_columns(3)
        if col2.button('Calculate Taxifare'):
            col2.markdown(f"Taxi Fare: `${round(pred, 2)}`")
    
    if page == "Movie Recommendation":
        css= '''
    
                    body {
                        background-color: #EAE7D6;
                    }
                    '''
        st.write(f'<style>{css}</style>', unsafe_allow_html=True)
        
        '''
        # Movie Recommendation

        This page queries a [movie recommendation API](https://github.com/modiem/Movie-Recommendation)
         built with FastAPI, Docker, Google Cloud Run.
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
        
        "**👉 How many recommendaitons do you want?**"
        n_movies = st.slider('Select from 1 to 10: ', 1, 10, 1)
        st.write(n_movies)
        
        "**👉 (Optional) Tweak Recommendation Basis **"
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
                        
    if page == "TreeMap":
        css= '''
    
                    body {
                        background-color: #effaf6;
                    }
                    '''
        st.write(f'<style>{css}</style>', unsafe_allow_html=True)
        
        
        df = get_gym_df()
        

        '''
        # Gyms in Amsterdam 🌳
        '''
        text = '''
        This TreeMap interactively displays the proportion of different  in each district.
        '''
        st.markdown(f'<p style="text-align: center; font-style: oblique;">{text}</p>', unsafe_allow_html=True)

        
        pallete= "tempo"
        # '👉 Choose your own pallate': ['brwnyl', 'teal', 'cividis', 'fall', 'geyser', 'deep', 'tempo']
      
        text = '''
        💡 Click node/leaf for details.
        (Full-Sceen View Recommended)
        '''
        st.markdown(f'<p style="text-align: center; ">{text}</p>', unsafe_allow_html=True)

        st.write(plot_map.plot_treemap_district(pallete=pallete, df=df))
        # with st.beta_expander("🍩 Divided in city districts"):
            
        with st.beta_expander("🏙️ Amsterdam as a Whole"):
            st.write(plot_map.plot_treemap_all(pallete=pallete, df=df))

        '''    



        #    
        Data from [Amsterdam Municipality Website] (https://data.amsterdam.nl/)
        '''


if __name__ == "__main__":
    main()
