from Packages.gcp import get_movie_name_lst, get_gyms
import pandas as pd 
import numpy as np

def test_get_movie_name_lst():
    df = get_movie_name_lst()
    assert isinstance(df, np.ndarray)

def test_get_gyms():
    df = get_gyms()
    assert isinstance(df, pd.DataFrame)