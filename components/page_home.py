import dash_html_components as html

home_page = html.Div(
    [
    html.Div(
        [
         html.Div(html.Img(src='/assets/images/home_icon.svg', 
                    className="main-img"), 
                className="home-logo"
                ),
        html.H1("Something really interesting", className="home-title"),
        html.H3("You'll probably like this app", className="home-subtitle"),
        ],
        className="home-cont"
    ),

    ],
    className="page-contents")