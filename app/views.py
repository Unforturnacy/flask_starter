"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file contains the routes for your application.
"""
import os

from flask_login import login_required
from app import app
from flask import render_template, request, redirect, send_from_directory, url_for, flash
from .models import Property,  PropertyForm
from werkzeug.utils import secure_filename
from . import db
###
# Routing for your application.
###

@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html', name="Mary Jane")

@app.route('/properties/create', methods=['GET', 'POST'])
def createProp():
    form = PropertyForm()
    if request.method == 'POST' and form.validate():

        photo = request.files['photo']
        file_name = secure_filename(photo.filename)


        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], file_name))

        prop = Property(form.title.data,form.description.data, form.no_bedroom.data, form.no_bathroom.data,
                        form.location.data, form.price.data,form.type.data,file_name)
        db.session.add(prop)
        db.session.commit()
        flash('Property Successfully created!', 'success')
        return redirect(url_for('properties'))
    
       
    return render_template('create.html', form = form)

@app.route('/properties')
def properties():
    properties = Property.query.all()
    return render_template('properties.html', properties=properties)

@app.route('/properties/<propertyid>')
def property(propertyid):
    property = Property.query.get(propertyid)
    return render_template('property.html', property=property)

@app.route('/uploads/<filename>')
def get_image(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)
###
# The functions below should be applicable to all Flask apps.
###

# Display Flask WTF errors as Flash messages
def flash_errors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'danger')

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
