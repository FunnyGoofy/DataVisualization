"""
The flask application package.
"""

from flask import Flask
from  flask_caching import Cache

app = Flask(__name__)

# Check Configuring Flask-Cache section for more details
cache = Cache(app,config={'CACHE_TYPE': 'simple'})
import DataVisualizationWebApp.views
