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


def get_traces_clr_nm(xs, ys, clrs, names):
    traces = []

    for x, y, clr, name in zip(xs, ys, clrs, names):
        trc = dict(x=x,
                y=y,
                line=dict(color=clr),
                name=name,
                mode="lines")

        traces.append(trc)
    return traces






def get_term_inc_fig(xs, ys, stab, x_info, ylab_str):

    clrs = ["rgb(151,251,151)" if ss is not True 
                    else "rgb(0,89,0)"
                            for ss in stab]
    
    names = ["Stable" if ss is True else "Unstable" for ss in stab]

    showledge = get_showlegend(xs)
    
    trcs = get_traces_clr_nm_lgd(xs, ys, clrs, names, showledge)

    ylab = f"Terminal incidence: {ylab_str}" + u" at t=\u221E"

    annotz = get_annotz(xs, ys, x_info)

    fig = model_fig_with_annotation(trcs, x_info["lab"], ylab, True, annotz)

    return fig


def get_showlegend(xs):
    
    showledge = [False, False, True, True]

    # if one of traces are empty, use other option to fill legend
    if not xs[-2]:
        showledge[-4] = True
    if not xs[-1]:
        showledge[-3] = True

    return showledge





def get_annotz(xvals, yvals, x_info):
    all_xs = flatten_list_of_lists(xvals)
    all_ys = flatten_list_of_lists(yvals)
    
    xmin = min(all_xs)
    xmax = max(all_xs)
    xmid = 0.5*(xmin + xmax)
    yuse = min(all_ys) - 0.08 * (max(all_ys) - min(all_ys))

    if x_info["low"]=="NA" or x_info["high"]=="NA":
        return []

    low = round(x_info["low"], 3)
    high = round(x_info["high"], 3)

    # xval = x_info["value"]
    
    return [dict(x=xmin, y=yuse, xref="x", yref="y", font=dict(color="#295939"), 
                    xanchor="center", text=f"<b>{low}%</b>", ax=0, ay=18, showarrow=True, 
                    arrowhead=2),
            # dict(x=xval, y=yuse, xref="x", yref="y", font=dict(color="#295939"), 
            #         xanchor="center", text="<b>baseline</b>", ax=0, ay=-18, showarrow=True,
            #         arrowhead=2),
            dict(x=xmid, y=yuse, xref="x", yref="y", font=dict(color="#295939"), 
                    xanchor="center", text="<b>of baseline</b>", showarrow=False),
            dict(x=xmax, y=yuse, xref="x", yref="y", font=dict(color="#295939"), 
                    xanchor="center", text=f"<b>{high}%</b>", ax=0, ay=18, showarrow=True, 
                    arrowhead=2),
            ]

def flatten_list_of_lists(lol):
    out = []
    for x in lol:
        out.extend(x)
    return out

def get_traces_clr_nm_lgd(xs, ys, clrs, names, showledge):
    traces = []

    for x, y, clr, name, sl in zip(xs, ys, clrs, names, showledge):
        trc = dict(x=x,
                y=y,
                line=dict(color=clr, width=3),
                showlegend=sl,
                name=name,
                mode="lines")

        traces.append(trc)
    return traces


def model_fig_with_annotation(traces, xlab, ylab, ledge, annotation):

    fig = go.Figure(data=traces, layout=standard_layout(ledge))

    fig.update_xaxes(title=xlab)
    fig.update_yaxes(title=ylab) # , fixedrange=True)

    fig.update_layout(
                annotations=annotation,
                legend=dict(x=1, 
                    y=1,
                    font=dict(size=10),
                    yanchor="bottom",
                    xanchor="right",
                    orientation="h",
                    bgcolor="rgba(255,255,255,0.5)"))

    return fig
