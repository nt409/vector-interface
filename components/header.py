import dash_html_components as html
import dash_bootstrap_components as dbc


header = html.Header(html.Div([
            html.Div(
                html.Img(src='/assets/images/menu.svg',
                    id="hamburger"),
                id="menu-button",
                className="hide-desktop"),


            html.Div([
                html.Nav(
                    children=[
                            html.Div([
                                dbc.Collapse([
                                    html.Div(html.A("Model", href="/", className="navLink-mb")),
                                    html.Div(html.A("Parameter Scan", href="/param-scan", className="navLink-mb")),
                                    html.Div(html.A("Explanation", href="/explanation", className="navLink-mb")),
                                ],
                                id="nav-menu",
                                is_open=False),
                            ],
                            className="hide-desktop",
                            id="mobile-navs"
                            ),
                            
                            html.Div([
                                html.A("Model", href="/", className="navLink-dt"),
                                html.A("Parameter Scan", href="/param-scan", className="navLink-dt"),
                                html.A("Explanation", href="/explanation", className="navLink-dt"),
                            ],
                            className="desktop-links show-desktop hide-mobile",
                            ),
                ]),
            ],
            id="main-nav-links",
            ),
        
        ],
        className="header-wrapper nav-bar"
        )
        )