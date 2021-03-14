from Packages.gcp import get_movie_name_lst

def test_get_movie_name_lst():
    lst = get_movie_name_lst()
    assert isinstance(lst, list)
