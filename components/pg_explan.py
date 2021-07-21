import dash_html_components as html





explan_page =  html.Div(
    [
    html.H1(
    "Model explanation",
    className="page-title"
    ),


    html.Div(
        html.A("Read full paper",
            href="/", 
            className="button-text"),
        className="button"
    ),

    html.Div([
        
    html.P("Longer description to go here (Figure 1)."),


    html.Img(src="/assets/images/Fig_one.png", className="image"),

    html.Div(
        [
        html.Span("Figure 1: ", className="bold"),
        html.Span("text about fig 1", className="italic")
        ]
    ),
    ], className="small-text")

    ],
    className="page-contents")