from Packages.plot_map import plot_path
import folium


def test_plot_path():
    m = plot_path(45.5236, 46, -122.6750, -121)
    assert isinstance(m, folium.Map)