import dash_html_components as html


footer = html.Footer([

        html.Div(
                html.Div([
                        html.A("Model", href="/", className="footer-navlink"),
                        html.A("Parameter Scan", href="/param-scan", className="footer-navlink"),
                        html.A("Explanation", href="/explanation", className="footer-navlink"),
                ],
                className="footer-wrapper footer-link-cont",
                ),
                className="footer-links"),

        html.Div(
                html.Div([
                "An interface to accompany the paper:",
                html.A("\nEpidemiological and ecological consequences of virus manipulation of host and vector in plant virus transmission\n", className="italic footer-txt", href="/"),
                "by Nik J. Cunniffe, Nick P. Taylor, Frédéric M. Hamelin and Michael J. Jeger",
                ],
                className="footer-wrapper"),
        className="foot-container",
        ),
        
        ],
        )