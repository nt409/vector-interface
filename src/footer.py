import dash_html_components as html


footer = html.Footer([

        html.Div(
                html.Div([
                html.A("Home", href="/", className="footer-navlink", id="footer-data"),
                html.A("Model", href="/model", className="footer-navlink", id="footer-vaccine-data"),
                ],
                className="footer-wrapper footer-link-cont",
                ),
                className="footer-links"),

        html.Div(
                html.Div([
                "Some footer text"
                    ],
                className="footer-wrapper"),
        className="foot-container",
        ),
        
        ],
        
        )