# ----------------------------------
#         LOCAL SET UP
# ----------------------------------

install_requirements:
	@pip install -r requirements.txt

# ---------------------------------------
#         STREAMLIT & HEROKU COMMANDS
# ----------------------------------------
APP_NAME=modiem

streamlit:
	-@streamlit run app.py

heroku_login:
	-@heroku login

heroku_create_app:
	-@heroku create ${APP_NAME}

heroku_set_var:
	-@heroku config:set GOOGLEMAP_API_KEY=${GOOGLEMAP_API_KEY}
	-@heroku config:set HERE_API_KEY=${HERE_API_KEY}
	-@heroku config:set OMDB_API_KEY=${OMDB_API_KEY}

heroku_google_var:
	-@heroku config:set GOOGLE_CREDENTIALS=${GOOGLE_CREDENTIALS}
	-@heroku config:set GOOGLE_APPLICATION_CREDENTIALS="google-credentials.json"
	-@heroku buildpacks:add https://github.com/gerywahyunugraha/heroku-google-application-credentials-buildpack

deploy_heroku:
	-@git push heroku master
	-@heroku ps:scale web=1

# ----------------------------------
#    LOCAL INSTALL COMMANDS
# ----------------------------------
install:
	@pip install . -U

clean:
	@rm -fr */__pycache__
	@rm -fr __init__.py
	@rm -fr build
	@rm -fr dist
	@rm -fr *.dist-info
	@rm -fr *.egg-info
	-@rm model.joblib
