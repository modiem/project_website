from Packages.gcp import get_credentials, get_movie_name_lst, get_gyms
from google.oauth2 import service_account
import pandas as pd

def test_get_credentials():
    gred = get_credentials()
    assert isinstance(gred, service_account.Credentials)

def test_get_movie_name_lst():
    lst = get_movie_name_lst()
    assert isinstance(lst, list)

def test_get_gyms():
    df = get_gyms()
    assert isinstance(df, pd.DataFrame)