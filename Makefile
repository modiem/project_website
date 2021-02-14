# ----------------------------------
#         LOCAL SET UP
# ----------------------------------

install_requirements:
	@pip install -r requirements.txt

# ---------------------------------------
#         STREAMLIT & HEROKU COMMANDS
# ----------------------------------------
APP_NAME=my-dazzling-project

streamlit:
	-@streamlit run app.py

heroku_login:
	-@heroku login

heroku_create_app:
	-@heroku create ${APP_NAME}

heroku_set_var:
	-@heroku config:set []

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
