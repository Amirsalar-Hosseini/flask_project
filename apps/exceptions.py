from flask import render_template

def page_not_found(e):
    return render_template('404.html'), 404

def server_error(e):
    return render_template('500.html'), 500

def permission_error(e):
    return render_template('403.html'), 500