# Dash app template for scientific projects

#### Virtual Environment
Run this command to create a virtual environment
`python -m venv path/to/virtual_env` ... I just called mine venv

Activate with
`venv\Scripts\activate`

#### Install requirements
Get pipenv
`pip install pipenv`

Install requirements:
`python -m pipenv install -r requirements.txt`


#### Icons and images
Put into `assets/images`

[Iconfinder](https://www.iconfinder.com/search/?q=calendar&price=free) is very useful for free icons

[Unsplash](https://unsplash.com/) is great for free images

## Useful Libraries

#### Plotly

Dash is designed with Plotly in mind. I use plotly for all my visualisations in python - can do anything you would want a graphing language to do. There are versions for R and javascript too.

Documentation [here](https://plotly.com/python/)

#### Dash core components

Documentation [here](https://dash.plotly.com/dash-core-components)


#### Dash bootstrap components

Useful and well documented library of components [here](https://dash-bootstrap-components.opensource.faculty.ai/docs/components/alert/)

I used collapse, input, tooltips/popovers... there are loads more but once you get into custom CSS you might find that can give you a better result

#### CSS

Optional, but can allow you to dramatically improve the appearance of the project - needs to be in `assets/main.css`

#### Color scheme

Lots of good sites - but something like [colorhunt.co](https://colorhunt.co/) is a good start and will save you time


#### Favicon

Use [favicon.io](https://favicon.io/favicon-generator/) to generate your favicon.

#### Google analytics
Can be a useful tool - follow their documentation and add into `app.index_string`