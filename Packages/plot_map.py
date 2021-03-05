import json
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from folium.features import DivIcon
import folium



with open("geojson.json") as f:
    geojson = json.load(f)    
# df = pd.read_csv("data/sports_provider_Amsterdam.csv")

sport_template = dict(
    layout = go.Layout(font=dict(
                            family="Old Standard TT",
                            ),
                    #    paper_bgcolor="#EAE7D6",
                        plot_bgcolor='rgba(0,0,0,0)',
                        hoverlabel=dict(
                                   bordercolor="black",
                                   bgcolor ="white",
                                   font_size=15,
                                   font_family="Rockwell"),
                       title=dict(xanchor="center",
                                  yanchor="top",
                                  yref="paper",
                                  ),
                        margin={"r":0,"t":100,"l":0,"b":0},
                        coloraxis_colorbar=dict(
                                  outlinewidth = 0),
))


def plot_district_choropleth(pallete="fall", 
                             df=None, 
                             geojson=geojson,
                             template=sport_template):
    '''
    pallette examples:
        - blues, magenta, burg, purpor, teal, inferno,
          purp, tealgrn
    '''
    district_count = pd.DataFrame(df.groupby("Stadsdeel").count()["Naam"]).reset_index()
    district_count = district_count.rename(columns={"Stadsdeel": "District", "Naam": "Count"})
    district_count["text"] = district_count["District"] + '<br>' + '<br>'+district_count["Count"].astype(str) + " Sports Providers in the District."

    fig=px.choropleth(district_count,
                      geojson=geojson,
                      locations="District",
                      color="Count",
                      color_continuous_scale=pallete,
                      range_color=(1,207),
                      labels={"Count": "Number of Sports Providers"},
                      hover_name="District",
                      hover_data=["Count"],
                      featureidkey="properties.Stadsdeel",
                      projection="mercator",
                      title = "Amsterdam Sports Provider Concentration<br>(Hover for break down)")
    fig.update_geos(visible=False, # hide the base map and frame.
                    fitbounds="locations") #automatically zoom the map to show just the area of interest.
   
    fig.update_traces(go.Choropleth(
                    hovertemplate = district_count["text"],
                    marker_line_color='white',
                ))

    fig.update_layout(template=template)

    return fig

def plot_treemap_all(pallete="fall", df=None, template=sport_template):
    fig = px.treemap(df,
                     path = ["All", "Sport_en"],
                     color = "Sport_count",
                     color_continuous_scale=pallete,
                     range_color = [1, 75],
                     hover_name = "Sport_en",
                     color_continuous_midpoint=np.average(df["Sport_count"]),
                     maxdepth=3
                    )

    fig.update_traces(go.Treemap(
        textinfo = "label",
        texttemplate = "%{label}<br><br>Percentage: %{percentParent:.1%} <br>Count: %{value}<br>",
        hovertemplate = "  %{label}  ",
        outsidetextfont = {"size": 20},
    )
                     )

    fig.update_layout(
        title = dict(
            text = "Proportion of Sports Type<br> (Click to Expand)"),
        coloraxis_colorbar=dict(
            title="Counts",
            tickvals=[10,30, 50, 70]),
        template=template
    )
    
    return fig

def plot_treemap_district(pallete="fall", df=None, template=sport_template):
    fig = px.treemap(df,
                     path = ["All", 'Stadsdeel',"Sport_en"],
                     color = "sport_count_in_district",
                     color_continuous_scale=pallete,
                     range_color = [1, 22],
                     hover_name = "Sport_en",
                     color_continuous_midpoint=np.average(df["sport_count_in_district"]),
                     maxdepth=3
                    )

    fig.update_traces(go.Treemap(
        hovertemplate = "%{label}",
        texttemplate = "%{label}<br><br>Percentage: %{percentParent:.1%} <br>Count: %{value}<br>",
        outsidetextfont = {"size": 20}
    )
                     )

    fig.update_layout(
        title = dict(
            text = "Proportion of Sports Type<br>(Click to Expand)",),
        coloraxis_colorbar=dict(
            title="Counts",
        ),
        template=template,
    )
    
    return fig

def plot_choropleth_openstreet(df=None, c="OrRd"):
  
    # Initialize the map: 52.3676° N, 4.9041° E
    m = folium.Map(location=[52.3676, 4.9041], zoom_start=11)
    
    district_count = pd.DataFrame(df.groupby("Stadsdeel").count()["Naam"]).reset_index()
    district_count = district_count.rename(columns={"Stadsdeel": "District", "Naam": "Count"})
    district_count["text"] = district_count["District"] + '<br>' + '<br>'+district_count["Count"].astype(str) + " Sports Providers in the District."

    # Add the color for the chloropleth:
    m.choropleth(
    geo_data=geojson,
    name='choropleth',
    data=district_count,
    columns=['District', 'Count'],
    key_on='feature.properties.Stadsdeel',
    fill_color=c,
    fill_opacity=0.7,
    line_color="white",
    legend_name='Number of Sports Providers'
    )
    folium.LayerControl().add_to(m)


    for district in geojson["features"]:
        
        lon, lat = np.array(district["geometry"]["coordinates"]).mean(axis=1).flatten()
        name = district["properties"]["Stadsdeel"]
        folium.map.Marker(
            [lat, lon],
            icon=DivIcon(
                icon_size=(8,8),
                icon_anchor=(15,10),
                html=f'<div style="font-size: 10pt; text_algnment=center;">{name}</div>',
                )
            ).add_to(m)

    return m
