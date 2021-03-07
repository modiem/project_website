import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

template = dict(
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
                        margin={"r":0,"t":0,"l":0,"b":0},
                        coloraxis_colorbar=dict(
                                  outlinewidth = 0),
))

def plot_choropleth(df=None, 
                    geojson=None, 
                    location_col=None, 
                    featureid=None, 
                    pallete="crul",
                    template=template):

    df.loc[:, "Count"] = 1
    df = pd.DataFrame(df.groupby(location_col).count()["Count"])
    df.loc[:, "text"] = df.index + '<br>' + '<br>'+ "Count:" + df["Count"].astype(str) 

    fig=px.choropleth(df,
                      geojson=geojson,
                      locations=df.index,
                      color="Count",
                      color_continuous_scale=pallete,
                      featureidkey=f"properties.{featureid}",
                      projection="mercator",
                      )
    fig.update_geos(visible=False, # hide the base map and frame.
                    fitbounds="locations") #automatically zoom the map to show just the area of interest.
   
    fig.update_traces(go.Choropleth(
                    hovertemplate = df["text"],
                    marker_line_color='white',
                ))

    fig.update_layout(template=template)

    return fig


    