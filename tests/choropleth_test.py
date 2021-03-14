from Packages.choropleth import plot_choropleth
from Packages.gcp import get_gyms
import json
from plotly.graph_objects import Figure

with open("geojson.json") as f:
    geojson=json.load(f)

def test_plot_choropleth():
    fig = plot_choropleth(df=get_gyms(),
                        geojson=geojson,
                        location_col = "Stadsdeel",
                         featureid="Stadsdeel")
    assert isinstance(fig, Figure)
    