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
    
    html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),

    html.Img(src="/assets/images/Fig_One.png",
        className="image"),


    html.Div(
        [
        html.Span("Figure 1: ", className="bold"),
        html.Span("text about fig 1", className="italic")
        ]
    ),
    ], className="small-text")

    ],
    className="page-contents")