"""
This script runs the DataVisualizationWebApp application using a development server.
"""

from DataVisualizationWebApp import app, views
from threading import Thread
import socket
import queue
import threading
from DataVisualizationWebApp import import_data
from cheroot.wsgi import Server as WSGIServer
from bokeh.settings import settings as settingManger
from DataVisualizationWebApp import utility as uHelper

settingManger.log_level("fatal")
settingManger.pretty(False)
bokeh_thread = Thread(name='Bokeh_Server', target=views.bk_worker)
bokeh_thread.start()

#uHelper.database_que = queue.Queue()
#database_thread = Thread(name='Database_Server', target =  lambda q, arg1: q.put(import_data.import_all_data(arg1)), args = (uHelper.database_que, ''))
#database_thread.start()

#bk_plter.all_connection_dict, bk_plter.novos_connection_dict, \
#bk_plter.all_connection_table, bk_plter.novos_connection_table, \
#bk_plter.novos_source, bk_plter.rigs_list, \
#bk_plter.jobs_list, bk_plter.crewshift_list = que.get()

if __name__ == '__main__':
    server = WSGIServer(bind_addr=('127.0.0.1', 8011), wsgi_app=app, numthreads=100)
    try:
        server.start()
    except KeyboardInterrupt:
        server.stop()
