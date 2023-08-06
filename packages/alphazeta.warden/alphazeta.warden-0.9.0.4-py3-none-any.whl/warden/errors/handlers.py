from flask import Blueprint, render_template, current_app
from utils import diags
import sys

errors = Blueprint('errors', __name__)


@errors.app_errorhandler(404)
# abort(404) will call this function
def page_not_found(error):
    return render_template('errors/404.html', current_app=current_app), 404


@errors.app_errorhandler(403)
# abort(403) will call this function
def page_not_found_403(error):
    return render_template('errors/403.html', current_app=current_app), 403


@errors.app_errorhandler(500)
# abort(500) will call this function
def page_not_found_500(error):
    # get latest traceback info
    import traceback
    trace = traceback.format_exc()
    return render_template('errors/500.html', error=error, traceback=trace,
                           current_app=current_app,
                           diags=diags(error)), 500
