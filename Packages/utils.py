import herepy

HERE_API_KEY = 'hghATdDoB9O87DeDmJ3uZlcLjx5j7vsfL9eivAGhRRI'

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
    return adress