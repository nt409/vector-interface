import plotly.graph_objects as go
import numpy as np



def plot_quartics(df, max_n_plot):
    for i in range(min(df.shape[0], max_n_plot)):
        row = df.iloc[i,:]
        QuarticPlot(row)



class QuarticPlot:
    def __init__(self, row) -> None:
        self.row = row
        fig = self.get_plot()
        fig.write_image(f"../figs/{row.trans_type}_eqm_{row.bio_realistic}_roots.png")
        fig.show()

        



    def get_plot(self):
        row = self.row

        coefs = row.coefficients
        
        L = 1 + row.mu/row.rho
        N = row.N
        
        xmax = N/L
        
        x = np.linspace(0, xmax, 100)
        y = [self.quartic(coefs, xx) for xx in x]

        data = [
                go.Scatter(x=[0,xmax], y=[0,0], mode="lines", name="zero-line"),
                go.Scatter(x=x, y=y, mode="lines", name="quartic"),
                ]
        
        title = self.get_fig_title(row)

        layout = dict(title=title,
                        height=800,
                        width=1600,
                        xaxis=dict(title="I value at eqm"), 
                        yaxis=dict(title="quartic - 0 at eqm"),
                        font=dict(size=18),
                        title_font=dict(size=12))

        fig = go.Figure(data, layout)

        return fig

    def quartic(self, coefs, x):
        if isinstance(coefs, str):
            coefs = self.get_coefs_from_string(coefs)
        
        out = 0
        n = len(coefs)
        for i in range(n):
            out += coefs[n-1-i] * (x**i)
        return out

    @staticmethod
    def get_coefs_from_string(string):
        string_use = string[1:-1]

        out = string_use.split(",")
        out = list(map(float, out))

        return out

    @staticmethod
    def get_fig_title(row):
        title_list = [f"{key}: {round(row[key],3)}, " if key not in ["bio_realistic", "stable_BR", "coefficients", "trans_type"]
                                    else "" for key in row.keys()]
        
        joined = f"<b>N roots: {row.bio_realistic},</b><br>trans_type: {row.trans_type},<br>" +  "".join(title_list[1:])

        var = "nu_m"

        splitted = joined.split(var)
        
        title = splitted[0] + "<br>" + var + splitted[1][:-2]
        
        return title