
import folium
import numpy as np
from folium import plugins

def plot_path(pickup_latitude, pickup_longitude, dropoff_latitude, dropoff_longitude):
    '''
    This function will draw a line on map btw pick-up point and drop-off point.
    '''
    
    
    ## Use geocoder to get coodinates from address.
    pick_up = [pickup_latitude, pickup_longitude]
    drop_off = [dropoff_latitude, dropoff_longitude]
    route = [pick_up, drop_off]
    loc = list((np.array(pick_up) + np.array(drop_off))/2)

    ## base map
    m=folium.Map(loc)

    ## Draw two markers
    folium.Marker(
        pick_up, 
        popup=f"<i>Pickup Point</i>", 
        tootip="Click me!",
        icon=folium.Icon(
            color="blue", 
            icon="street-view", 
            prefix="fa"
        )).add_to(m)

    folium.Marker(
        drop_off, 
        popup=f"<i>Dropoff Point</i>", 
        tootip="Click me!",
        icon=folium.Icon(
            color="lightred", 
            icon="map-marker", 
            prefix="fa"
        )).add_to(m)
    
    ## Draw a Route btw two points
    plugins.AntPath(locations=route).add_to(m)
    
    return m
