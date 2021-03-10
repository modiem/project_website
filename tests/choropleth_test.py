from Packages.choropleth import plot_choropleth
from Packages.gcp import get_gyms
import plotly.graph_objects as go
import json

def test_plot_choropleth():
    df = get_gyms()
    with open("geojson.json") as f:
                geojson=json.load(f)
    featuredId = "Stadsdeel"
    location_col="Stadsdeel"
    fig = plot_choropleth(df=df,
                        geojson=geojson,
                        location_col=location_col,
                        featureid=featuredId)
    assert isinstance(fig, go.Figure)



