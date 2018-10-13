"""
Routes and views for the flask application.
"""

from datetime import datetime
from DataVisualizationWebApp  import bk_plotter as bk_plter
from flask import Flask, render_template, request
from DataVisualizationWebApp import app
from bokeh.embed import server_document
from bokeh.layouts import column
from bokeh.plotting import figure, curdoc
from bokeh.server.server import Server
from bokeh.themes import Theme
from tornado.ioloop import IOLoop
import timeit
from bokeh.application.handlers import Handler
import asyncio
#from bokeh.application.handlers.server_lifecycle import ServerLifecycleHandler
from bokeh.application import Application
from bokeh.application.handlers import FunctionHandler
from tornado.httpserver import HTTPServer
from bokeh.server.tornado import BokehTornado
from bokeh.server.util import bind_sockets
from DataVisualizationWebApp import server_lifecycle
from bokeh.settings import settings

#paramater
@app.route('/', methods=['GET'])
def bkapp_page():
    """Renders the home page.""" 
    #myurl="http://172.20.101.16:5006/bk_plotter"
    #with pull_session(url=url, app_path="/DataVisualizationWebApp/bk_plotter") as mysession:
#    script = autoload_server(None, app_path="/DataVisualizationWebApp/bk_plotter", session_id=session.id, url=url)
        #script = server_session(None, mysession.id, url=myurl)
        #return render_template("embed.html", script=script, template="Flask")
    start_time_bk_page = timeit.default_timer()
    script = server_document('http://localhost:5006/bk_plotter')
    print("\nbk_page loading time \n")    
    print(timeit.default_timer() - start_time_bk_page)
    return render_template("embed.html", script=script, template="Flask") 



    #script = server_document('http://localhost:5006/bk_plotter')
    #return render_template("embed.html", script=script, template="Flask")

#@app.route('/', methods=['GET'])
#@app.route('/home', methods=['GET'])
#def index():
#   return render_template("index.html")

@app.route('/contact')
def contact():
   return bk_plter.plot_html()
    
@app.route('/about')
def about():
    return bk_bar__stacked_plter.plot_bar_stacked()

def bk_worker():
    # Can't pass num_procs > 1 in this configuration. If you need to run multiple
    # processes, see e.g. flask_gunicorn_embed.py
    #ServerLifecycleHandler(filename = "server_lifecycle.py")
    #20180706
    start_time_server = timeit.default_timer()
    server = Server({'/bk_plotter': bk_plter.plot_doc}, \
                    io_loop=IOLoop(), \
                    allow_websocket_origin=["localhost:8011"], \
                    websocket_max_message_size = 9999999999 * 1024 * 1024)
  
    settings.log_level('fatal')
    settings.py_log_level('fatal')
    #server = Server({'/bk_plotter': bk_plter.plot_doc}, io_loop=IOLoop(), allow_websocket_origin=["172.20.101.16"], host="http://172.20.101.16:5006")
    #server = Server({'/bk_plotter': bk_plter.plot_doc}, io_loop=IOLoop(), allow_websocket_origin=["*"])
    server.start()
    Handler.on_server_loaded = server_lifecycle.on_server_loaded(server)
    server.io_loop.start()
    print("\nserver loading time \n")    
    print(timeit.default_timer() - start_time_server)
    