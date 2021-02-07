import dash_html_components as html
import dash_bootstrap_components as dbc


header = html.Header(html.Div([
            html.Div([
                html.A("MyWebsiteName", href="/", className="navLinkTitle"),
            ],
            className="website-name",
            ),

            html.Div(
                html.Img(src='/assets/images/menu.svg',id="hamburger"),
                id="menu-button",
                className="hide-desktop"),


            html.Div([
                html.Nav(
                    children=[
                            html.Div([
                                dbc.Collapse([
                                    html.Div(html.A("Data", href="/data", className="navLink navlink-mb")),
                                    html.Div(html.A("Model", href="/model", className="navLink navlink-mb")),
                                ],
                                id="nav-menu",
                                is_open=False),
                            ],
                            className="hide-desktop",
                            id="mobile-navs"
                            ),
                            
                            html.Div([
                                html.Div(html.A("Data", href="/data", className="navLink")),
                                html.Div(html.A("Model", href="/model", className="navLink rightmost-link")),
                            ],
                            className="desktop-links show-desktop hide-mobile",
                            ),
                ]),
            ],
            id="main-nav-links"
            ),
        
        ],
        className="header-wrapper nav-bar"
        )
        )