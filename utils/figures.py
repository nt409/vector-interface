import plotly.graph_objects as go
import numpy as np


# all possible modebar buttons:
#  ["zoom2d",
#     "pan2d",
#     "select2d",
#     "lasso2d",
#     "zoomIn2d",
#     "zoomOut2d",
#     "autoScale2d",
#     "resetScale2d",
#     "hoverClosestCartesian",
#     "hoverCompareCartesian",
#     "zoom3d",
#     "pan3d",
#     "resetCameraDefault3d",
#     "resetCameraLastSave3d",
#     "hoverClosest3d",
#     "orbitRotation",
#     "tableRotation",
#     "zoomInGeo",
#     "zoomOutGeo",
#     "resetGeo",
#     "hoverClosestGeo",
#     "toImage",
#     "sendDataToCloud",
#     "hoverClosestGl2d",
#     "hoverClosestPie",
#     "toggleHover",
#     "resetViews",
#     "toggleSpikelines",
#     "resetViewMapbox"]}

MODEBAR_CONFIG = {"modeBarButtonsToRemove": [
    'pan2d',
    'toImage',
    'select2d',
    "zoomIn2d",
    "zoomOut2d",
    'toggleSpikelines',
    'hoverCompareCartesian',
    'hoverClosestCartesian',
    'lasso2d'
    ]}

def standard_layout(legend_on):
    return go.Layout(
            font = dict(size=12),
            template="plotly_white",
            height=400,
            showlegend=legend_on,
            xaxis=dict(showgrid=False),
            margin= dict(l=50, b=10, t=10, r=10, pad=0),
            )

def model_fig(x, y, clr, n_points):
    traces = []
    x = np.random.normal(size=n_points)
    y = np.random.normal(size=n_points)

    points = go.Scatter(x=x,
            y=y,
            line=dict(color=clr),
            mode="markers")

    traces.append(points)

    fig = go.Figure(data=traces, layout=standard_layout(False))
    fig.update_xaxes(title="xlab")

    return fig



