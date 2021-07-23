from dash_html_components.Tr import Tr
import plotly.graph_objects as go

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
            margin=dict(l=50, b=10, t=50, r=10, pad=0),
            )

def model_fig(traces, xlab, ylab, ledge):

    fig = go.Figure(data=traces, layout=standard_layout(ledge))
    fig.update_xaxes(title=xlab)
    fig.update_yaxes(title=ylab) # , fixedrange=True)

    fig.update_layout(legend=dict(x=1, 
                    y=1,
                    font=dict(size=10),
                    yanchor="bottom",
                    xanchor="right",
                    orientation="h",
                    bgcolor="rgba(255,255,255,0.5)"))

    return fig


def get_traces(xs, ys, clrs, names):
    traces = []

    for x, y, clr, name in zip(xs, ys, clrs, names):
        trc = go.Scatter(x=x,
                y=y,
                line=dict(color=clr),
                name=name,
                mode="lines")

        traces.append(trc)
    return traces

def get_traces_scan_fig(xs, ys, clrs, names, showledge):
    traces = []

    for x, y, clr, name, sl in zip(xs, ys, clrs, names, showledge):
        trc = go.Scatter(x=x,
                y=y,
                line=dict(color=clr),
                showlegend=sl,
                name=name,
                mode="lines")

        traces.append(trc)
    return traces