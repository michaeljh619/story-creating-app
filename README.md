# Story Creating App
A web app for reading and making *choose your own adventure* stories.

# Tech
- Flask
- HTML, CSS, Javascript
- SQLAlchemy
- Python

# Installation
The structure of the project follows this package pattern from Flask:
http://flask.pocoo.org/docs/1.0/patterns/packages/

#### Linux
To install the package
- Navigate to the root folder of the project
- Export the flask app environment variable to tell Flask where the app is at
	`$ export FLASK_APP=storyApp`
- Export the environment variable to put in development
	`$ export FLASK_ENV=development`
- Install the package
	`$ pip install -e .`
- Run the app
	`flask run --host=0.0.0.0`

From here, the app will be listening on localhost. You can access the web app by opening a browser to localhost port 5000: http://localhost:5000/
