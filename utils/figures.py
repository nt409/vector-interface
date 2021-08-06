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
            showlegend=legend_on,
            xaxis=dict(showgrid=False),
            margin=dict(l=50, b=10, t=50, r=10, pad=0),
            )




class ModelRunFigure:
    def __init__(self, data, y_lab) -> None:
        self.traces = self.get_traces(data)
        self.fig = self.model_fig(y_lab)


    def model_fig(self, y_lab):

        fig = go.Figure(data=self.traces, layout=standard_layout(True))

        fig.update_xaxes(title="Time (days)")
        fig.update_yaxes(title=y_lab) # , fixedrange=True)

        fig.update_layout(
                height=300,
                legend=dict(x=1, 
                        y=1,
                        font=dict(size=10),
                        yanchor="bottom",
                        xanchor="right",
                        orientation="h",
                        bgcolor="rgba(255,255,255,0.5)"))

        return fig


    @staticmethod
    def get_traces(data):
        xs = data["xs"]
        ys = data["ys"]
        clrs = data["clrs"]
        names = data["names"]

        traces = []

        for x, y, clr, name in zip(xs, ys, clrs, names):
            trc = go.Scatter(x=x,
                    y=y,
                    line=dict(color=clr),
                    name=name,
                    mode="lines")

            traces.append(trc)

        return traces








class TerminalIncidenceFigure:
    def __init__(self, traces, x_info, which_inc) -> None:
        
        self.traces = traces

        # self.xs = data["xs"]
        # self.ys = data[f"{which_inc}_vals"]
        # self.stabs = data["stabs"]

        self.x_info = x_info

        self.which_inc = which_inc
        
        self.fig = self.get_term_inc_fig()


    def get_term_inc_fig(self):

        # clrs = ["rgb(151,251,151)" if ss is not True 
        #             else "rgb(0,89,0)" for ss in self.stabs]
        
        # dashes = [
        #         "dash",
        #         "dot",
        #         "dash",
        #         "dot",
        #         "solid",
        #         "solid"
        #         ]

        # names = [
        #             "Unstable (vect. present)",
        #             "Unstable (vect. dies out)",
        #             "Stable (vect. present)",
        #             "Stable (vect. dies out)",
        #             "Stable",
        #             "Unstable",
        #             ]

        # showledge = self.get_showlegend()
        
        # trcs = self.get_traces(clrs, names, showledge, dashes)
        # trcs = self.traces

        fig = go.Figure(data=self.traces, layout=standard_layout(True))
        
        fig = self.update_layout(fig)

        return fig



    # def get_showlegend(self):

    #     showledge = [True]*len(self.xs)

    #     # showledge[0] = False
    #     # showledge[2] = False

    #     # if not len(self.xs[-1]):
    #     #     # showledge[-1] = False
    #     #     showledge[0] = True
        
    #     # if not len(self.xs[-2]):
    #     #     # showledge[-2] = False
    #     #     showledge[2] = True

    #     return showledge



    # def get_traces(self, clrs, names, showledge, dashes):
    #     traces = []

    #     for x, y, clr, name, sl, dsh in zip(self.xs, self.ys, clrs, names, showledge, dashes):

    #         trc = go.Scatter(x=x,
    #                 y=y,
    #                 line=dict(color=clr, width=3, dash=dsh),
    #                 showlegend=sl,
    #                 name=name,
    #                 mode="lines")

    #         traces.append(trc)
        
    #     baseline_dot = self.get_baseline_trc()
    #     traces.append(baseline_dot)
    #     return traces


    # def get_baseline_trc(self):
    #     return go.Scatter(x=[self.x_info['value']],
    #                 y=[0],
    #                 marker=dict(color="red", size=12),
    #                 showlegend=True,
    #                 name="Baseline value",
    #                 mode="markers")



    def update_layout(self, fig):

        y_str = "I/(S+I)" if self.which_inc=="host" else "Z/(X+Z)"
                
        ylab = f"Terminal incidence: {y_str}" + u" at t=\u221E"
        
        annotz = self.get_annotations()

        fig.update_xaxes(title=self.x_info["lab"])
        fig.update_yaxes(title=ylab) # , fixedrange=True)

        fig.update_layout(
                    annotations=annotz,
                    height=400,
                    legend=dict(x=1, 
                        y=1,
                        font=dict(size=10),
                        yanchor="bottom",
                        xanchor="right",
                        orientation="h",
                        bgcolor="rgba(255,255,255,0.5)"))

        return fig



    def get_annotations(self):
        x_info = self.x_info

        if x_info["low"]=="NA" or x_info["high"]=="NA":
            return []

        all_xs = self.flatten_list_of_trace_vals("x")
        all_ys = self.flatten_list_of_trace_vals("y")
        
        xmin = min(all_xs)
        xmax = max(all_xs)

        xmid = 0.5*(xmin + xmax)       

        yuse = min(all_ys) - 0.08 * (max(all_ys) - min(all_ys))

        x_min_val = round(x_info["low"], 3)
        x_max_val = round(x_info["high"], 3)

        return [
            self.get_arrow_annotation(xmin, yuse, f"<b>{x_min_val}%</b>", ax=0, ay=18),
            self.get_text_annotation(xmid, yuse, "<b>of baseline</b>"),
            self.get_arrow_annotation(xmax, yuse, f"<b>{x_max_val}%</b>", ax=0, ay=18),
            ]

    
    
    def flatten_list_of_trace_vals(self, key):
        out = []
        for list_ in self.traces:
            vals = list_[key]
            out.extend(vals)
        return out


    @staticmethod
    def get_arrow_annotation(x, y, text, ax, ay):
        return dict(x=x, y=y, xref="x", yref="y", font=dict(color="#295939"), 
                        xanchor="center", text=text, ax=ax, ay=ay, 
                        showarrow=True, arrowhead=2)
    
    
    @staticmethod
    def get_text_annotation(x, y, text):
        return dict(x=x, y=y, xref="x", yref="y", font=dict(color="#295939"), 
                        xanchor="center", text=text, showarrow=False)


