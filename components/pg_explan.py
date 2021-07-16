import dash_html_components as html





explan_page =  html.Div(
    [
    html.H1(
    "Model explanation",
    className="page-title"
    ),

    html.A("Link to paper", href="/"),
    ],
    className="page-contents")