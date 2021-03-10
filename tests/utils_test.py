from Packages.utils import geocoder_here, reverse_geocoder_here, movie_api_response, get_poster
from PIL.Image import Image


def test_geocoder_here():
    coords = geocoder_here("NewYork libery")
    assert isinstance(coords["lat"], float)

def test_reverse_geocoder_here():
    adress=reverse_geocoder_here((41.79, -74.74))
    assert isinstance(adress["adress"], str)

def test_get_poster():
    poster = get_poster("Time of the Gypsies")
    assert isinstance(poster, Image)