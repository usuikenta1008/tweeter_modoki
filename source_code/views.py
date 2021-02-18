from flask import render_template
from source_code import app

# index or '/' is the landing page of your website.
# it's the first page that appears when someone navigates into your website.
# 
@app.route('/')
def index():
    return render_template('index.html')