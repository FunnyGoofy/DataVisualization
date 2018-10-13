# Create a polynomial line graph with those arguments
from __future__ import absolute_import, print_function
from bokeh.application.handlers import Handler, ServerLifecycleHandler
from bokeh.util.callback_manager import _check_callback
import timeit
from bokeh import  events
from bokeh.events import Event, Tap
from threading import Thread
from bokeh.models import TapTool
import queue
import threading
from bokeh.themes import Theme
from bokeh.plotting import curdoc
from DataVisualizationWebApp import server_lifecycle
#from bokeh.application.handlers.server_lifecycle import ServerLifecycleHandler
from bokeh.application.handlers import Handler
from DataVisualizationWebApp import all_main_plot
from DataVisualizationWebApp import utility as uHelper
from bokeh.models.callbacks import CustomJS
from DataVisualizationWebApp import sub_novos_plot
from DataVisualizationWebApp import driller_hybrid_novos_vs_plot
from bokeh.models.widgets import Panel, Tabs 
#from bokeh.util.logconfig import basicConfig, bokeh_logger as bl
#import logging
import sys
#logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
#bl.info('info......')
#bl.error('error.......')
#bl.warning('Warning.......')

def plot_doc(doc): 
    #m_session_context = doc.session_context
    Handler.on_session_created = server_lifecycle.on_session_created(curdoc().session_context)

    uHelper.show_subplot()
    uHelper.hide_subplot()
    uHelper.set_xAxis_ticker()
    uHelper.reset_xAxis_ticker()
    uHelper.rigs_combx.on_change('value', uHelper.rigs_combx_change)
    uHelper.jobs_combx.on_change('value', uHelper.jobs_combx_change)
    uHelper.crewshift_combx.on_change('value', uHelper.crewshift_combx_change)
    uHelper.main_plot.x_range.js_on_change('start', uHelper.ticker_cb)
    uHelper.main_plot.x_range.js_on_change('end', uHelper.ticker_cb)
    uHelper.main_plot.js_on_event(events.Reset, uHelper.ticker_cb_reset)
    uHelper.checkbox_group_1.on_change('active', uHelper.checkbox_callback_1)
    uHelper.checkbox_group_2.on_change('active', uHelper.checkbox_callback_2)
    uHelper.checkbox_group_3.on_change('active', uHelper.checkbox_callback_3)   
    uHelper.main_plot.js_on_event(events.DoubleTap, uHelper.hide_subplot_callback)
    uHelper.checkbox_group_1.js_on_change('change', uHelper.hide_subplot_callback)
    uHelper.checkbox_group_2.js_on_change('change', uHelper.hide_subplot_callback)
    uHelper.checkbox_group_3.js_on_change('change', uHelper.hide_subplot_callback)
    uHelper.rigs_combx.js_on_change('value', uHelper.hide_subplot_callback)
    uHelper.jobs_combx.js_on_change('value', uHelper.hide_subplot_callback)
    uHelper.crewshift_combx.js_on_change('value', uHelper.hide_subplot_callback)
    uHelper.tabs.on_change('active', uHelper.grey_out_connection_type_callback)
    from_comboBx_group = False    
    uHelper.update_main_plot_queue = queue.Queue()
    uHelper.update_main_plot_event = threading.Event()
    selected_rig, selected_job = uHelper.rigs_combx.value, uHelper.jobs_combx.value

    update_main_plot_thread = Thread(name='update_main_plot_thread', \
                                     target =  lambda q, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12: \
                                                q.put(all_main_plot.update_main_plot_chart(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, arg10, arg11, arg12)), \
                                     args = (uHelper.update_main_plot_queue, \
                                             doc, \
                                             uHelper.update_main_plot_event, \
                                             uHelper.mainplot_source, \
                                             uHelper.main_plot, \
                                             uHelper.mainplot_data_all, \
                                             uHelper.checkbox_group_1_selections, \
                                             uHelper.checkbox_group_2_selections,\
                                             uHelper.checkbox_group_3_selections, \
                                             uHelper.all_connection_dict,\
                                             selected_rig, \
                                             selected_job, \
                                             from_comboBx_group))
    update_main_plot_thread.start()
    #update_main_plot_event.wait()
    uHelper.update_main_plot_event.set()

    uHelper.update_driller_hybrid_novos_vs_queue = queue.Queue()
    #not used, may be used in future 
    uHelper.update_driller_hybrid_novos_vs_event = threading.Event()

    update_driller_hybrid_novos_vs_plot_thread = Thread(name='update_driller_hybrid_novos_vs_plot_thread', \
                                                        target =  lambda q, arg1, arg2, arg3, arg4, \
                                                                         arg5, arg6, arg7, arg8, arg9, arg10, \
                                                                         arg11, arg12, arg13, arg14, arg15: \
                                                                  q.put(driller_hybrid_novos_vs_plot.update_driller_hybrid_novos_vs_charts(arg1, arg2, arg3, arg4, arg5,\
                                                                                                                                          arg6, arg7, arg8, arg9, arg10, \
                                                                                                                                          arg11, arg12, arg13, arg14, arg15)), \
                                                         args = (uHelper.update_driller_hybrid_novos_vs_queue, \
                                                                 doc, \
                                                                 uHelper.update_driller_hybrid_novos_vs_event, \
                                                                 uHelper.driller_vs_plot, \
                                                                 uHelper.driller_vs_plot_source, \
                                                                 uHelper.hybrid_vs_plot, \
                                                                 uHelper.hybrid_vs_plot_source, \
                                                                 uHelper.novos_vs_plot, \
                                                                 uHelper.novos_vs_plot_source, 
                                                                 uHelper.checkbox_group_1_selections, \
                                                                 uHelper.checkbox_group_2_selections,\
                                                                 uHelper.checkbox_group_3_selections, \
                                                                 uHelper.all_connection_dict,\
                                                                 selected_rig, \
                                                                 selected_job, \
                                                                 from_comboBx_group))
    update_driller_hybrid_novos_vs_plot_thread.start()
    #update_main_plot_event.wait()
    uHelper.update_driller_hybrid_novos_vs_event.set()


    #uHelper.main_plot.js_on_event(Tap, CustomJS.from_py_func(uHelper.update_subplot)) 

    doc.add_root(uHelper.main_layout)
    doc.theme = Theme(filename="theme.yaml")   
    
