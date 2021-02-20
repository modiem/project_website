import os
import io
import re
import herepy
import requests
from PIL import Image


HERE_API_KEY=os.environ.get('HERE_API_KEY')
POSTER_API_KEY=os.environ.get("POSTER_API_KEY")

###################
#  GEOCODER HERE  #
###################

def geocoder_here(adress, token=HERE_API_KEY):
    """
    adress: NewYork libery
     ==>  {'lat': 41.79854, 'lng': -74.74493}
    """
    geocoderApi = herepy.GeocoderApi(api_key=token)
    res = geocoderApi.free_form(adress)
    res = res.as_dict()
    coords = res["items"][0]["position"]
    coords = {k.lower(): v for k, v in coords.items()}
    return coords

def reverse_geocoder_here(coords, token=HERE_API_KEY):
    """
    coords: (41.79, -74.74)
    ==> 36 Liberty Commons Way, Liberty, NY 12754-3009, United States
    """
    geocoderReverseApi = herepy.GeocoderReverseApi(token)
    res = geocoderReverseApi.retrieve_addresses(coords)
    res = res.as_dict()
    adress = res['items'][0]['address']['label']
    lat = res['items'][0]['position']['lat']
    lng = res['items'][0]['position']['lng']
    return {"adress":adress, "lat":lat, "lng":lng}


###################
#  API Query      #
###################
urls=dict(
    taxifare="https://predict-taxifare-iwuisdewea-ez.a.run.app/predict_fare",
    movie_recommendation="https://movie-recommender-5i6qxbf74a-ez.a.run.app/recommendation",
    poster="http://www.omdbapi.com"
    )

def query_api(which, params):
    '''
    Input: 
        - which api. 
        - params.
    Output: response
    '''
    url = urls[which]
    response = requests.get(url, params=params)
    response = response.json()
    return response

def format_name(name):
    '''
    Format teh name in the list and return cleaned title and produced year.
    '''
    info={}
    if ", The (" in name:        
        info["title"] = re.sub(r", The \(\d+\)", "", name).strip()
    else:
        info["title"] = name.split(" (")[0].strip()
    info["year"] = name.split("(")[-1][-5:-1]
    return info

def movie_api_response(name):
    '''
    Fetch movie infomation from api.
    '''
    title = format_name(name)["title"]
    year = format_name(name)["year"]

    ## Construct params
    params=dict(
    apikey=POSTER_API_KEY,
    t=title,
    y=year)
    try:
        response=query_api("poster", params)     
        return response
    except:
        return None
    
def get_movie_info(name):
    response=movie_api_response(name)
    if response:
        info_lst={}
        for k in ["Runtime", "imdbRating", "Genre", "Director",  "Actors", "Awards",  "Plot"]:
            info_lst[f"{k.capitalize()}"] = response.get(k, 'No Information')
        return info_lst
    else: 
        return None

def get_poster(name):
    '''
    Fetch movie poster from api.
    '''

    response=movie_api_response(name)
    if response:
        poster_url=response["Poster"]
        # return poster_url
        r = requests.get(poster_url, timeout=4.0)
        img =  Image.open(io.BytesIO(r.content))
        #     im.save(f"{title}.png")
        # img=Image.open(f"{title}.png")
        return img
    else:
        return None

# def clean_img(title):
#     for f in os.listdir():
#         if f.endswith(".png"):
#             os.remove(f)
#             print(f"{f} removed.")
