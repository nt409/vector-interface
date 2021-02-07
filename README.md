# Dash app template for scientific projects

## TOC
- Setup
- Useful libraries
- How to deploy your app to get it online

---

## Setup

### Virtual Environment
Run this command to create a virtual environment
`python -m venv path/to/virtual_env` ... I just called mine venv

Activate with
`venv\Scripts\activate`

### Install requirements
Get pipenv
`pip install pipenv`

Install requirements:
`python -m pipenv install -r requirements.txt`

Sometimes this is fiddly or doesn't work on it's own. Certainly you need:
`python -m pipenv install dash`
and you may find you need other packages - add them as you go



---

## Useful libraries

### Plotly

Dash is designed with Plotly in mind. It produces interactive figures.

I use plotly for all my visualisations in python - can do anything you would want a graphing language to do. There are versions for R and javascript too.

Documentation [here](https://plotly.com/python/)

### Dash core components

Documentation [here](https://dash.plotly.com/dash-core-components)

### Dash bootstrap components

Useful and well documented library of components [here](https://dash-bootstrap-components.opensource.faculty.ai/docs/components/alert/)

I used collapse, input, tooltips/popovers... there are loads more but once you get into custom CSS you might find that can give you a better result



## Tools

### CSS

Language for styling websites. Optional, but can allow you to dramatically improve the appearance of the project - needs to be in `assets` folder.

### JS

You might want to include some of your own javascript for user interactions (combined with CSS you can animate things). Most of this can be done with dash but not always as customisable or as attractively

### Google analytics
Can be a useful tool - follow their documentation and add into `app.index_string`


## Useful websites

### Icons and images
Put into `assets/images`

[Iconfinder](https://www.iconfinder.com/search/?q=calendar&price=free) is very useful for free icons

[Unsplash](https://unsplash.com/) is great for free images

### Color scheme

Lots of good sites - but something like [colorhunt.co](https://colorhunt.co/) is a good start and will save you time, and [colormind.io](http://colormind.io/) is cool too

### Favicon

Use [favicon.io](https://favicon.io/favicon-generator/) to generate your favicon.


### Design tips

There's a youtube channel called [Design Course](https://www.youtube.com/watch?v=8gNrZ4lAnAw&ab_channel=DesignCourse) which I found extremely helpful.

Briefly, the most important things (in his opinion) are:
- **alignment**
- **typography** (pick a good font and get line-height and font-sizes right)
- **visual hierarchy** (which element on the page is actually important)
- **colour & contrast** (used to achieve VH, and also just make it look nice)
- **white-space** (keeping things appropriately close or far)
- **scale** (appropriate size of elements, used to achieve VH)

 The video linked is a particularly good introduction to html and CSS. When writing dash apps you are effectively using a python wrapper to write html (strictly speaking it actually compiles into html via React.js...). The details of this aren't particulary important but if you can write dash then you can basically write html and vice versa.

---

## Deploy via Heroku
Go to [heroku](https://dashboard.heroku.com/apps) and sign in to your account/register for one (free tier is fine unless you are expecting lots of traffic)

You can link the project to a github repo. If it has the same folder structure as this you will be fine (so need app.py on top level, not within `src` or any other folder).

### Procfile

You will need to include a 'Procfile' in the folder - which is simply a file with no file extension (i.e. no `.txt` or similar). Your procfile should contain a single line `web: gunicorn app:server`.

### Requirements.txt

You also need a requirements.txt which you might get from running `pip freeze > requirements.txt`, but I have found this step a bit fiddly at times too.
