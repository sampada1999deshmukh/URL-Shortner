from flask import render_template, request, abort, redirect
from . import bp
from .service import *


@bp.route('/')
def home():
    return render_template('home.html')


@bp.route('/shorten', methods=['GET', 'POST'])
def shorten_url():
    if request.method == 'POST':
        original_url = request.form['original_url']
        expiration_time = request.form.get('expiration_time')
        if not original_url:
            return render_template('index.html', error="Invalid URL")
        short_url = process_short_url_request(original_url, expiration_time)
        return render_template('index.html', short_url=short_url)
    return render_template('index.html')


@bp.route('/<short_id>', methods=['GET'])
def redirect_to_original(short_id):
    mapping = get_redirect_mapping(short_id)
    if not mapping:
        abort(404, description="URL not found or expired")
    log_access(short_id, request.remote_addr)
    return redirect(mapping.original_url)


@bp.route('/analytics/<short_id>', methods=['GET'])
def analytics(short_id):
    analytics_data = get_analytics_data(short_id)
    if not analytics_data:
        return render_template('error.html', error="Short URL not found")
    return render_template('analytics.html', analytics_data=analytics_data)