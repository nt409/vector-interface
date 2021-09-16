import dash_html_components as html

# alt + Z for text wrap

text_about_full_explanation = html.Div([

    # text
    "This page offers a short explanation of the model found in the paper ",

    html.I("'Epidemiological and ecological consequences of virus manipulation of host and vector in plant virus transmission'"),
    
    " by Nik J. Cunniffe, Nick P. Taylor, Frédéric M. Hamelin and Michael J. Jeger.",
    
    ], className="small-text mrgn-bttm-big")



description = html.Div([
        
    # text
    html.P("We propose a model of plant-virus-vector interactions. We are interested in the effect of plant and vector infection status on vector preferences from landing, settling and feeding, to reproduction and flight."),
    
    html.P("The model tracks the amount of healthy and infected plant material as well as the amount of viruliferous and non-viruliferous vectors (Figure 1). The model includes planting, harvesting, roguing and infection of plants, and birth, death, infection and loss of infectivity of vectors. "),

    # fig 1
    html.Img(src="/assets/images/diagram.png",
        className="image",
        id="diagram-image",
        ),

    html.Div(
        [
        html.Span("Figure 1: ", className="bold"),
        html.Span("model diagram. (A) Compartments in the epidemiological model. All arrows corresponding to transitions causing hosts or vectors to leave a compartment are labelled with per capita rates, apart from those corresponding to infection of hosts or acquisition of the virus by vectors (i.e. from S -> I and from X -> Z) which are labelled with net rates. The rate of planting of hosts and birth of vectors are also labelled with net rates. (B) Schematic showing how the flying, settling, and feeding behaviours of vectors are modelled.", className="italic")
        ],
    className="mrgn-bttm-big"
    ),

    # text
    html.P("Virus transmission can be described as persistent or non-persistent depending on the rates of acquisition, retention and inoculation of virus. Persistent tranmssion is characterised by a closer association of the virus with the vector. The model considers persistent and non-persistent transmission separately (Figure 2)."),


    # fig 2
    html.Img(src="/assets/images/eqns.png",
        className="image",
        id="eqn-image"),

    html.Div(
        [
        html.Span("Figure 2: ", className="bold"),
        html.Span("model equations. For the full model derivation, see the paper (links at the top of the page and in the footer). See Figure 1 for a description of what the different functions represent.", className="italic")
        ],
    className="mrgn-bttm-big"
    ),

    ], className="small-text")




explan_page =  html.Div(
    [
    html.H1(
    "Model explanation",
    className="page-title"
    ),

    text_about_full_explanation,


    html.Div(
        html.A("Read paper",
            href="https://www.biorxiv.org/content/10.1101/2021.09.08.459452v1.full", 
            className="button-link-text"),
        className="button mrgn-bttm-big"
    ),

    description,

    ],
    className="page-contents",
    id="explan-page")