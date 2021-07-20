import dash_html_components as html


footer = html.Footer([

        html.Div(
                html.Div([
                        # html.A("Home", href="/", className="footer-navlink"),
                        html.A("Model", href="/", className="footer-navlink"),
                        html.A("Explanation", href="/explanation", className="footer-navlink"),
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