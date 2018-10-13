from bokeh.models import FactorRange, Spacer, Legend
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.util.string import  decode_utf8,  encode_utf8
import pandas as pd
from bokeh.layouts import row, column, gridplot, widgetbox
from bokeh.models import ColumnDataSource, TapTool, VBar, Rect
from bokeh.models.widgets import PreText, Select, CheckboxGroup
from bokeh.models.widgets import Panel, Tabs  
from bokeh.io.state import curstate
from bokeh.resources import Resources
from bokeh import  events
from bokeh.events import Event, Tap
from bokeh.models.widgets import Div
from pandas import DataFrame
from bokeh.core.properties import value
from bokeh.layouts import layout
from bokeh.plotting import figure
from bokeh.models import HoverTool, Range1d
from numpy import pi
from operator import add
from bokeh.models import Arrow, NormalHead, VeeHead, Text
from bokeh.models.callbacks import CustomJS
from bokeh.models.glyphs import Text, Line
from itertools import chain
import pypyodbc
from threading import Thread
import queue
import threading
from DataVisualizationWebApp import drillingconn_wellsect_plot
from DataVisualizationWebApp import b2s_s2b_plot
from DataVisualizationWebApp import all_main_plot
from DataVisualizationWebApp import sub_novos_plot
from tornado import gen
from bokeh.models import TickFormatter
from DataVisualizationWebApp import import_data
from bokeh.models import LabelSet, Label
import timeit
from DataVisualizationWebApp import utility as uHelper
from bokeh.layouts import widgetbox
import ctypes
import math
import asyncio
import time

#from bokeh.application.handlers.server_lifecycle import ServerLifecycleHandler

async def multiple_tasks():
    input_coroutines = [import_data. retrieve_novos_data(uHelper.connection), import_data.retrieve_data(uHelper.connection)]
    await asyncio.gather(*input_coroutines, return_exceptions=True)


#@gen.coroutine
def on_server_loaded(server_context):
    ''' If present, this function is called when the server first starts. '''
    print ("on_server_loaded start")
    
    
    
    #import_data.setup_db_connection()
        
    
    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(multiple_tasks())
    #loop.run_until_complete(import_data.retrieve_novos_data(uHelper.connection))
    #loop.close()
    
    #import_data.import_all_data()
    #uHelper.database_que = queue.Queue()
    #database_thread = Thread(name='Database_Server', \
    #                         target =  lambda q, arg1: \
    #                             q.put(import_data.retrieve_data(uHelper.connection)),\
    #                             args = (uHelper.database_que, ''))
    #database_thread.start()
    #tasks = [gevent.spawn(retrieve_data),]
    #gevent.joinall(tasks)
    #uHelper.all_connection_dict, uHelper.novos_connection_dict, \
    #uHelper.all_connection_table, uHelper.novos_connection_table, \
    #uHelper.novos_source, uHelper.rigs_list, \
    #uHelper.jobs_list, uHelper.crewshift_list = uHelper.database_que.get()
    print ("on_server_loaded end ")


@gen.coroutine
def on_server_unloaded(server_context):
    ''' If present, this function is called when the server shuts down. '''
    print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print("on_server_unloaded")

#@gen.coroutine
def on_session_created(session_context):
    ''' If present, this function is called when a session is created. '''
    print ("-----------------------------------------------")
    start_time_database = timeit.default_timer()
    print("on_session_created -- begin")
    #import_data.setup_db_connection()
    #import_data.retrieve_data(uHelper.connection)
    import_data.retrieve_data()
    #uHelper.database_que.put(import_data.retrieve_data(uHelper.connection))
    #uHelper.all_connection_dict, uHelper.novos_connection_dict, \
    #uHelper.all_connection_table, uHelper.novos_connection_table, \
    #uHelper.novos_source, uHelper.rigs_list, \
    #uHelper.jobs_list, uHelper.crewshift_list = uHelper.database_que.get()

    print("on_session_created -- after")
    print("\n retrieving time: ")
    print(timeit.default_timer() - start_time_database)

    default_rig_number, rigs_list = uHelper.get_default_value(uHelper.all_connection_table, comboBx = 'Rigs')
    default_rig_number = str(default_rig_number)
    rigs_list = []
    rigs_list = [str(item) for item in uHelper.rigs_list]
    uHelper.rigs_combx = Select(title='Rigs:', value=default_rig_number, width = 100, sizing_mode = uHelper.sizing_mode, options = uHelper.update_combBx_values('', rigs_list))


    default_job_number, jobs_list = uHelper.get_default_value(uHelper.all_connection_table, comboBx = 'Jobs', selectedRig = uHelper.rigs_combx.value) # TODO: add condition to determine 0 exists or not
    default_job_number = str(default_job_number)
    jobs_list = []
    jobs_list = [str(item) for item in uHelper.jobs_list]
    uHelper.default_job_number = default_job_number
    uHelper.jobs_list = jobs_list
    uHelper.jobs_combx = Select(title='Jobs:', value=default_job_number, width = 100, sizing_mode = uHelper.sizing_mode, options = uHelper.update_combBx_values('', jobs_list))

    default_crew, crewshift_list = uHelper.get_default_value(uHelper.all_connection_table, comboBx = 'CrewShift', selectedRig = uHelper.rigs_combx.value, selectedJob = uHelper.jobs_combx.value)
    default_crew = str(default_crew)
    crewshift_list = [str(item) for item in crewshift_list]
    uHelper.crewshift_combx = Select(title='CrewShift:', value=default_crew, width = 100, sizing_mode = uHelper.sizing_mode, options = uHelper.update_combBx_values('', crewshift_list))
    
    # 2. checkbox group
    uHelper.checkbox_group_1 = CheckboxGroup(labels=["Build", "Lateral", "Vertical"], \
                                             active=[], \
                                             name = 'wellSelection')

    uHelper.checkbox_group_2 = CheckboxGroup(labels=["Driller", "Novos", "Hybrid"], \
                                             active=[], \
                                             name = 'connectionType')
    
    uHelper.checkbox_group_3 = CheckboxGroup(labels=["B2S", "S2S", "S2B", "Survey", "BackReam"], \
                                             active=[], \
                                             name = 'connectionPhase')
    
    rig, job = uHelper.rigs_combx.value, uHelper.jobs_combx.value

    # 1st chart
    uHelper.update_drillingconn_wellsect_queue = queue.Queue()
    uHelper.update_drillingconn_wellsect_event = threading.Event()
    update_drillingconn_wellsect_thread = Thread(name='update_drillingconn_wellsect_thread', \
                                                 target =  lambda q, arg1, arg2, arg3, arg4: \
                                                           q.put(drillingconn_wellsect_plot.update_well_selection_data(arg1, arg2, arg3, arg4)), \
                                                 args = (uHelper.update_drillingconn_wellsect_queue, \
                                                         uHelper.update_drillingconn_wellsect_event, \
                                                         uHelper.all_connection_dict, rig, job))
    update_drillingconn_wellsect_thread.start()
    uHelper.update_drillingconn_wellsect_event.wait()
    well_connection_colors, x, well_connnection_counts, well_connnection_data = uHelper.update_drillingconn_wellsect_queue.get()
    uHelper.well_connnection_source = ColumnDataSource(data=dict(colors = well_connection_colors, \
                                                         x = x, \
                                                         counts = well_connnection_counts))
    well_connection_chart = figure(x_range = FactorRange(*x), \
                                   plot_width = 1310, \
                                   plot_height = 430, \
                                   sizing_mode = uHelper.sizing_mode, \
                                   title = "Drilling Connection Breakdown By Well Section")
                                   #title = "Drilling Connection Breakdown By Well Section", \
                                   #output_backend = "webgl")
    well_connection_chart.vbar(x = 'x', \
                               width = 0.2, \
                               bottom = 0, \
                               top = 'counts', \
                               color = 'colors', \
                               source = uHelper.well_connnection_source)
    
    total_connections = sum(well_connnection_counts)
    uHelper.well_connection_textbox_source = ColumnDataSource(data=dict(x = [600,], \
                                                                y = [450,],  \
                                                                txt= ['Total Connections: %d' % (total_connections),]))
    well_connection_chart_textbox = LabelSet(x='x', y='y', x_units='screen', y_units='screen', \
                                            text='txt', source = uHelper.well_connection_textbox_source,\
                                            text_font_size="12pt", border_line_color='black', \
                                            border_line_width=1, text_font_style='bold')
    well_connection_chart.add_layout(well_connection_chart_textbox)
    well_connection_chart.title.align = 'center'
    well_connection_chart.title.text_font_size = '15pt'
    well_connection_chart.toolbar.active_drag = None
    well_connection_chart.toolbar.logo = None
    well_connection_chart.toolbar_location = None
    well_connection_chart.y_range.start = 0
    well_connection_chart.x_range.range_padding = 0.1
    well_connection_chart.xaxis.major_label_orientation = 1
    well_connection_chart.xgrid.grid_line_color = None

    for well_item in well_connnection_data['well_selection']:
        for sub_item in well_connnection_data['Driller']:
            well_connection_chart.add_tools(HoverTool(tooltips=[(str(well_item), "@counts")]))
    
    print("\n1st chart loading time \n")    

    ### 2nd chart(b2s s2b)
    start_time_2nd_chart = timeit.default_timer()
    uHelper.update_b2s_s2b_queue = queue.Queue()
    uHelper.update_b2s_s2b_event = threading.Event()
    update_b2s_s2b_thread = threading.Thread(name='update_b2s_s2b_thread', \
                                             target =  lambda q, arg1, arg2, arg3, arg4: \
                                                       q.put(b2s_s2b_plot.update_b2s_s2b_data(arg1, arg2, arg3, arg4)), \
                                             args = (uHelper.update_b2s_s2b_queue, uHelper.update_b2s_s2b_event, uHelper.novos_connection_table, rig, job))
    update_b2s_s2b_thread.start()
    uHelper.update_b2s_s2b_event.wait()

    b2s_canceled_list, b2s_completed_list, \
    b2s_exception_list,b2s_failed_list, \
    s2b_canceled_list, s2b_completed_list, \
    s2b_exception_list, s2b_failed_list = uHelper.update_b2s_s2b_queue.get()

    b2s_s2b_status = ["Canceled", "Completed", "Exception", "Failed"]
    b2s_s2b_colors = ["#F2C80F", "#00ff0d", "#F2C80F", "#ff4600"]
    b2s_connection_phase = ['OffBottom', 'UnWeightBit', 'ClearBit', 'CleanHole', 'SetBoxHeight', 'SetWeight']
    b2s_figure = figure(x_range = b2s_connection_phase, \
                        plot_width = 600, \
                        plot_height = 300, \
                        sizing_mode = uHelper.sizing_mode, \
                        title="Bottom to Slip")
    uHelper.b2s_datasource = ColumnDataSource(data=dict(b2s_connection_phase = b2s_connection_phase, \
                                                Canceled = b2s_canceled_list, \
                                                Completed = b2s_completed_list, \
                                                Exception = b2s_exception_list, \
                                                Failed = b2s_failed_list))
    b2s_figure.vbar_stack(b2s_s2b_status, \
                          x='b2s_connection_phase', \
                          width = 0.2, \
                          color = b2s_s2b_colors, \
                          source = uHelper.b2s_datasource)
    b2s_figure.title.align = 'center'
    b2s_figure.toolbar.active_drag = None
    b2s_figure.toolbar.logo = None
    b2s_figure.toolbar_location = None
    b2s_figure.y_range.start = 0
    b2s_figure.x_range.range_padding = 0.1
    b2s_figure.xaxis.major_label_orientation = 1
    b2s_figure.xgrid.grid_line_color = None
    b2s_figure.ygrid.grid_line_color = None

    s2b_connection_phase = ['AddStand', 'TakeWeight', 'FlowSetpoint', 'RotateDrill', 'TagBottom']
    s2b_figure = figure(x_range = s2b_connection_phase, \
                        plot_width = 670, \
                        plot_height = 300, \
                        sizing_mode = uHelper.sizing_mode, \
                        title="Slip to Bottom")
    uHelper.s2b_datasource = ColumnDataSource(data=dict(s2b_connection_phase = s2b_connection_phase, \
                                                Canceled = s2b_canceled_list, \
                                                Completed = s2b_completed_list, \
                                                Exception = s2b_exception_list, \
                                                Failed = s2b_failed_list))
    s2b_figure.vbar_stack(b2s_s2b_status, \
                          x = 's2b_connection_phase', \
                          width = 0.2, \
                          color = b2s_s2b_colors, \
                          source = uHelper.s2b_datasource, \
                          legend= [value(x) for x in b2s_s2b_status])
    s2b_figure.title.align = 'center'
    s2b_figure.toolbar.active_drag = None
    s2b_figure.toolbar.logo = None
    s2b_figure.toolbar_location = None
    s2b_figure.y_range.start = 0
    s2b_figure.x_range.range_padding = 0.1
    s2b_figure.xaxis.major_label_orientation = 1
    s2b_figure.xgrid.grid_line_color = None
    s2b_figure.ygrid.grid_line_color = None
    s2b_figure.legend.location = "top_right"
    s2b_figure.legend.orientation = "vertical"

    new_legend = s2b_figure.legend[0]
    s2b_figure.legend[0].plot = None
    s2b_figure.add_layout(new_legend, 'right')

    line_figure = figure(x_range=(0, 100), \
                         y_range=(0, 300),  \
                         plot_width = 120, \
                         plot_height = 300)
    line_figure.line(x=[50, 50], \
                     y= [0, 300], \
                     line_width = 3, \
                     line_color='black')
    line_figure.xaxis.visible = None
    line_figure.yaxis.visible = None
    line_figure.toolbar.logo = None
    line_figure.toolbar_location = None
    line_figure.toolbar.active_drag = None
    line_figure.min_border_left = 10
    line_figure.min_border_right = 10
    line_figure.min_border_top = 0
    line_figure.min_border_bottom = 0

    #summary_layout = layout(row(b2s_figure, line_figure, s2b_figure), sizing_mode = uHelper.sizing_mode)
    print("\n 2nd chart loading time \n")
    print(timeit.default_timer() - start_time_2nd_chart)

    mTicker = uHelper.customize_ticker()
    start_time_main_chart = timeit.default_timer()
    uHelper.get_all_data_queue = queue.Queue()
    uHelper.get_all_data_event = threading.Event()
    uHelper.get_all_data_thread = threading.Thread(name = 'get_all_data_thread', \
                                           target =  lambda q, arg1, arg2: \
                                                  q.put(all_main_plot.get_all_data(arg1, arg2)), args = (uHelper.get_all_data_queue, uHelper.get_all_data_event, uHelper.all_connection_dict))
    uHelper.get_all_data_thread.start()    
    uHelper.get_all_data_event.wait()
    uHelper.mainplot_data_all, depth_list_all = uHelper.get_all_data_queue.get()
    
    depth_list_all = [str(x) for x in depth_list_all]
    uHelper.main_plot = figure(x_range=FactorRange(), \
                       y_range = (0, 50), \
                       plot_width = uHelper.plot_width, \
                       plot_height = 400, \
                       tools = "tap, pan, box_zoom, reset", \
                       sizing_mode = uHelper.sizing_mode, \
                       title="Overall Connection Times",\
                       id="main_plot_id")

    uHelper.main_plot.xaxis.ticker = mTicker
    uHelper.main_plot.title.align = 'center'
    uHelper.main_plot.legend.click_policy="hide"
    uHelper.main_plot.title.text_font_size = '15pt'
    uHelper.main_plot.x_range.factors = []
    uHelper.main_plot.x_range.factors = depth_list_all

    uHelper.mainplot_data_all['HoleDepth'] = ["{0:.2f}".format(x) for x in uHelper.mainplot_data_all['HoleDepth']]
    #mainplot_data_all['HoleDepth'] = [str(x) for x in mainplot_data_all['HoleDepth']]
    #TODO: 20181001
    #dur = []
    #for index, item in enumerate(uHelper.mainplot_data_all['VBarTop']):
    #    top_num = 0.0
    #    bottom_num = 0.0
    #    if uHelper.mainplot_data_all['VBarTop'][index] == '':
    #        top_num = 0.0
    #    else:
    #        top_num = float(uHelper.mainplot_data_all['VBarTop'][index])
    #
    #    if uHelper.mainplot_data_all['VBarBottom'][index] == '':
    #        bottom_num = 0.0
    #    else:
    #        bottom_num = float( uHelper.mainplot_data_all['VBarBottom'][index])
    #    dur.append(str(top_num - bottom_num))


    uHelper.mainplot_source = ColumnDataSource(data=dict(HoleDepthRef = uHelper.mainplot_data_all['HoleDepthRef'], \
                                                 HoleDepth = uHelper.mainplot_data_all['HoleDepth'], \
                                                 VBarTop = uHelper.mainplot_data_all['VBarTop'], \
                                                 VBarBottom = uHelper.mainplot_data_all['VBarBottom'], \
                                                 VBarColors = uHelper.mainplot_data_all['VBarColors'], \
                                                 VBarType = uHelper.mainplot_data_all['VBarType'])) 
    main_plot_vbars = uHelper.main_plot.vbar(x = 'HoleDepth', \
                   width = 0.1, \
                   bottom = 'VBarBottom', \
                   top = 'VBarTop', \
                   color = 'VBarColors', \
                   source = uHelper.mainplot_source, \
                   legend = 'VBarType')
    uHelper.main_plot.legend.location = "top_right"
    uHelper.main_plot.legend.orientation = "vertical"

    new_legend = uHelper.main_plot.legend[0]
    uHelper.main_plot.legend[0].plot = None
    uHelper.main_plot.add_layout(new_legend, 'right')
        
    # layout
    uHelper.m_well_selection = Div(text='Well Section:', height=1)
    uHelper.m_well_connection = Div(text='Connection Type:', height=1)
    uHelper.m_well_conn_phase = Div(text='Connection Phase:', height=1)
    
    start_time_rest_chart = timeit.default_timer()
    uHelper.version = Div(text='Version: 1.1.1', width=200, height=30)
    uHelper.version.css_classes = ["version"]
    #sidebar menu
    uHelper.spacer_1 = Spacer(width=200, height=10)
    uHelper.spacer_2 = Spacer(width=200, height=30)
    uHelper.spacer_3 = Spacer(width=200, height=30)

    uHelper.menu_column_1_layout = column(uHelper.spacer_3, widgetbox(uHelper.rigs_combx), widgetbox(uHelper.jobs_combx), widgetbox(uHelper.crewshift_combx))
    uHelper.menu_column_1_layout.css_classes = ["sidebarmenucombxlayout"] 
    uHelper.well_selection_layout = column(uHelper.m_well_selection, uHelper.checkbox_group_1)
    uHelper.well_connection_layout = column(uHelper.m_well_connection, uHelper.checkbox_group_2)
    uHelper.well_conn_phase_layout = column(uHelper.m_well_conn_phase, uHelper.checkbox_group_3)
    uHelper.menu_column_2_layout = column(uHelper.well_selection_layout, uHelper.well_connection_layout, uHelper.well_conn_phase_layout)
    uHelper.menu_column_2_layout.css_classes = ["sidebarmenucheckbxlayout"] 
    uHelper.menu_middle_layout = layout(column(uHelper.menu_column_1_layout, uHelper.menu_column_2_layout))
    uHelper.menu_middle_layout.css_classes = ["sidebarmenumiddlelayout"] 
    uHelper.menu_top_layout = layout(column(uHelper.spacer_1, uHelper.version))
    uHelper.menu_top_layout.css_classes = ["sidebarmenutoplayout"] 
    uHelper.menu_bottom_layout = layout(column(uHelper.spacer_2))
    uHelper.menu_bottom_layout.css_classes = ["sidebarmenubottomlayout"] 
    
    
    uHelper.menu_layout = layout(column(uHelper.menu_top_layout, uHelper.menu_middle_layout, uHelper.menu_bottom_layout))
    uHelper.menu_layout.css_classes = ["menulayout"]

    #sub_plot
    #sub_plot, subplot_source, subplot_dict = sub_novos_plot.create_sub_plot(doc)
    subplot_dict = {}
    subplot_dict['B2SText'] = ['Cleanhole - Active', 'Cleanhole - Completed', 'Setboxheight - Active', 'Setboxheight - Completed', 'Setweight - Active', 'Setweight - Completed', 'Offbottom-Active', 'Unweightbit - Active', 'Unweightbit - Completed', 'Clearbit - Active', 'Clearbit - Completed', 'Offbottom - Completed']
    subplot_dict['text_x'] = [2, 12, 22, 32, 42, 52, 2, 12, 22, 32, 42, 52]
    subplot_dict['B2SColors'] = ['white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white']
    subplot_dict['B2STextColors'] = ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black']
    subplot_dict['B2SHideColors'] = ['white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white']
    subplot_dict['subplot_x'] = [5, 15, 25, 35, 45, 55, 5, 15, 25, 35, 45, 55]
    subplot_dict['subplot_y'] = [10, 10, 10, 10, 10, 10, 25, 25, 25, 25, 25, 25]
    subplot_dict['Text'] = ['', '', '', '','', '', '', '','', '', '', '']
    
    
    uHelper.subplot_source = ColumnDataSource(data = subplot_dict)
    # 3. plot     
    uHelper.sub_plot = figure(x_range = [0, 60], \
                      y_range = [0, 30], \
                      plot_width=1540, \
                      plot_height= 350, \
                      toolbar_location=None, \
                      sizing_mode='scale_both')
    subplot_height = 40
    subplot_weight = 175

    uHelper.sub_plot.rect(x = 'subplot_x', \
                  y = 'subplot_y', \
                  width = subplot_weight, \
                  height = subplot_height, \
                  color = "B2SColors", \
                  width_units = "screen", \
                  height_units = "screen", \
                  source = uHelper.subplot_source)
    b2s_text = Text(x = 'text_x', \
                    y = 'subplot_y', \
                    text_color = "B2STextColors", \
                    text = "Text", \
                    text_font_size = "10pt")
    uHelper.sub_plot.add_glyph(uHelper.subplot_source, b2s_text)
    uHelper.sub_plot.xaxis.visible = None
    uHelper.sub_plot.yaxis.visible = None
    uHelper.sub_plot.background_fill_color = "#01B8AA"
    uHelper.sub_plot.background_fill_color = "white"
    uHelper.m_color_white = uHelper.sub_plot.background_fill_color
    uHelper.sub_plot.outline_line_color = None
    uHelper.sub_plot.title.align = 'center'
    uHelper.sub_plot.title.text_font_size = '15pt'

    uHelper.m_color_white = "white"
    uHelper.subplot_colors_length = len(subplot_dict['B2SColors'])
    #hide_subplot_callback =  CustomJS(args=dict(m_color=m_color_white, subplot=sub_plot, subplotColorsLength=subplot_colors_length, subplotSource=subplot_source), code="""
    #hide_subplot_callback =  CustomJS(args=dict(m_color = uHelper.m_color_white, \
    #                                            subplot = uHelper.sub_plot, \
    #                                            subplotColorsLength = subplot_colors_length, \
    #                                            subplotSource = uHelper.subplot_source), code="""
    #                                                for(i = 0; i < subplotColorsLength; i++) {
    #                                                    subplotSource.data['B2SColors'][i] = 'white' 
    #                                                    subplotSource.data['B2STextColors'][i] = 'white' 
    #
    #                                                }
    #                                                subplotSource.change.emit()
    #                                                subplot.background_fill_color = 'white' 
    #                                            """)
    #
    uHelper.main_plot.toolbar.logo = None 
    uHelper.main_plot.toolbar_location = "above"
    uHelper.main_plot.css_classes = ["mainplot"] 

    #drillingConnectionBreakdown_column = column(well_connection_chart, uHelper.main_plot, uHelper.sub_plot)
    drillingConnectionBreakdown_column = column(well_connection_chart)
    drillingConnectionBreakdown_column.sizing_mode = uHelper.sizing_mode
    drillingConnectionBreakdown_layout = layout(drillingConnectionBreakdown_column, sizing_mode = uHelper.sizing_mode)   
    activity_type_stats_top = row(b2s_figure, line_figure, s2b_figure)
    activity_type_stats_bottom = column(uHelper.main_plot, uHelper.sub_plot)
    summary_layout = layout(column(activity_type_stats_top, activity_type_stats_bottom))
         
    right_layout = layout(row(summary_layout))
    
    #taptool = uHelper.main_plot.select(type=TapTool)
    #uHelper.main_plot.js_on_event(Tap, uHelper.tapcallback)
    #novos_length = len(uHelper.novos_connection_dict[uHelper.depth_ft_str])
    #uHelper.main_plot.js_on_event(Tap, CustomJS(args=dict(allSource = uHelper.mainplot_source, \
    #                                novosSource = uHelper.novos_source, \
    #                                subplotSource = uHelper.subplot_source, \
    #                                subplotColorsLength = uHelper.subplot_colors_length, \
    #                                novosLength = novos_length, \
    #                                subplot = uHelper.sub_plot \
    #                                ),\
    #                                code = sub_novos_plot.m_code)) 

    #20180727start
    tabMain = Panel(title='Main', child=drillingConnectionBreakdown_layout)
    tabMain.tags=["MainTag"]
    tabMain.name="MainName"

    tabActivitytypeStats = Panel(title='Over Connection Analysis', child=right_layout)
    tabActivitytypeStats.tags=["activitytypestatsTag"]
    tabActivitytypeStats.name="ActivitytypeStatsName"
    
    #####################################################
    #start 20180928
    #depth_list_all = [str(x) for x in depth_list_all]
    uHelper.driller_vs_plot = figure(x_range=FactorRange(), \
                                     y_range = (0, 50), \
                                     plot_width = uHelper.plot_width, \
                                     plot_height = 250, \
                                     tools = "tap, pan, box_zoom, reset",\
                                     sizing_mode = uHelper.sizing_mode)
       
    uHelper.driller_vs_dataset, driller_vs_display_depth_list = all_main_plot.get_all_dataset(uHelper.all_connection_dict)
    driller_vs_display_depth_list = [str(x) for x in driller_vs_display_depth_list]
    #uHelper.driller_vs_dataset['HoleDepth'] = ["{0:.2f}".format(x) for x in uHelper.driller_vs_dataset['HoleDepth']]
    #uHelper.driller_vs_dataset['HoleDepth'] = [str(x) for x in  uHelper.driller_vs_dataset['HoleDepth']]    
   
    uHelper.driller_vs_plot.toolbar.logo = None 
    uHelper.driller_vs_plot.toolbar_location = "above"
    uHelper.driller_vs_plot.css_classes = ["DrillerVSPlot"] 
    uHelper.driller_vs_plot.xaxis.ticker = mTicker
    uHelper.driller_vs_plot.title.align = 'center'
    uHelper.driller_vs_plot.legend.click_policy="hide"
    uHelper.driller_vs_plot.x_range.factors = []
    #uHelper.driller_vs_plot.x_range.factors = driller_vs_display_depth_list
    uHelper.driller_vs_plot.yaxis.axis_label = "Driller"
    uHelper.driller_vs_plot.axis.axis_label_text_font_style = "bold"

    uHelper.driller_vs_plot_source = ColumnDataSource(data=dict(HoleDepthRef = [], \
                                                             HoleDepth = [],\
                                                             B2S = [], \
                                                             S2S = [], \
                                                             S2B = [], \
                                                             Survey = [], \
                                                             BackReam = []))
    
    driller_vs_plot_vbars = uHelper.driller_vs_plot.vbar_stack(uHelper.connection_phase_list,\
                                                               x = 'HoleDepth', \
                                                               width = 0.1, \
                                                               color = uHelper.color_list, \
                                                               source = uHelper.driller_vs_plot_source, \
                                                               legend = [value(x) for x in uHelper.connection_phase_list])
    uHelper.driller_vs_plot.legend.location = "top_left"
    uHelper.driller_vs_plot.legend.orientation = "horizontal"
    driller_vs_new_legend = uHelper.driller_vs_plot.legend[0]
    uHelper.driller_vs_plot.legend[0].plot = None
    uHelper.driller_vs_plot.add_layout(driller_vs_new_legend, 'above')

    uHelper.hybrid_vs_plot = figure(x_range=FactorRange(), \
                       y_range = (0, 50), \
                       plot_width = uHelper.plot_width, \
                       plot_height = 250, \
                       tools = "tap, pan, box_zoom, reset", \
                       sizing_mode = uHelper.sizing_mode)

    #uHelper.mainplot_data_all['HoleDepth'] = ["{0:.2f}".format(x) for x in uHelper.mainplot_data_all['HoleDepth']]
    #mainplot_data_all['HoleDepth'] = [str(x) for x in mainplot_data_all['HoleDepth']]    
    
    uHelper.hybrid_vs_plot.toolbar.logo = None 
    uHelper.hybrid_vs_plot.toolbar_location = "above"
    uHelper.hybrid_vs_plot.css_classes = ["HybridVSPlot"] 
    uHelper.hybrid_vs_plot.xaxis.ticker = mTicker
    uHelper.hybrid_vs_plot.title.align = 'center'
    uHelper.hybrid_vs_plot.x_range.factors = []
    uHelper.hybrid_vs_plot.x_range.factors = driller_vs_display_depth_list
    uHelper.hybrid_vs_plot.yaxis.axis_label = "Hybrid"
    uHelper.hybrid_vs_plot.axis.axis_label_text_font_style = "bold"
    uHelper.hybrid_vs_plot_source = ColumnDataSource(data=dict(HoleDepthRef = [], \
                                                             HoleDepth = [],\
                                                             B2S = [], \
                                                             S2S = [], \
                                                             S2B = [], \
                                                             Survey = [], \
                                                             BackReam = [])) 
    hybrid_vs_plot_vbars = uHelper.hybrid_vs_plot.vbar_stack(uHelper.connection_phase_list,\
                                                               x = 'HoleDepth', \
                                                               width = 0.1, \
                                                               color = uHelper.color_list, \
                                                               source = uHelper.hybrid_vs_plot_source, \
                                                               legend = [value(x) for x in uHelper.connection_phase_list])
    uHelper.hybrid_vs_plot.legend.location = "top_left"
    uHelper.hybrid_vs_plot.legend.orientation = "horizontal"
    hybrid_vs_plot_new_legend = uHelper.hybrid_vs_plot.legend[0]
    uHelper.hybrid_vs_plot.legend[0].plot = None
    uHelper.hybrid_vs_plot.add_layout(hybrid_vs_plot_new_legend, 'above')

    uHelper.novos_vs_plot = figure(x_range=FactorRange(), \
                       y_range = (0, 50), \
                       plot_width = uHelper.plot_width, \
                       plot_height = 250, \
                       tools = "tap, pan, box_zoom, reset", \
                       sizing_mode = uHelper.sizing_mode)

    #uHelper.mainplot_data_all['HoleDepth'] = ["{0:.2f}".format(x) for x in uHelper.mainplot_data_all['HoleDepth']]
    #mainplot_data_all['HoleDepth'] = [str(x) for x in mainplot_data_all['HoleDepth']]    
   
    uHelper.novos_vs_plot.toolbar.logo = None 
    uHelper.novos_vs_plot.toolbar_location = "above"
    uHelper.novos_vs_plot.css_classes = ["NovosVSPlot"] 
    uHelper.novos_vs_plot.xaxis.ticker = mTicker
    uHelper.novos_vs_plot.title.align = 'center'
    uHelper.novos_vs_plot.x_range.factors = []
    uHelper.novos_vs_plot.x_range.factors = driller_vs_display_depth_list   
    uHelper.novos_vs_plot.yaxis.axis_label = "NOVOS"
    uHelper.novos_vs_plot.axis.axis_label_text_font_style = "bold"

    uHelper.novos_vs_plot_source = ColumnDataSource(data=dict(HoleDepthRef = [], \
                                                             HoleDepth = [],\
                                                             B2S = [], \
                                                             S2S = [], \
                                                             S2B = [], \
                                                             Survey = [], \
                                                             BackReam = [])) 
    novos_vs_plot_vbars = uHelper.novos_vs_plot.vbar_stack(uHelper.connection_phase_list,\
                                                               x = 'HoleDepth', \
                                                               width = 0.1, \
                                                               color = uHelper.color_list, \
                                                               source = uHelper.novos_vs_plot_source, \
                                                               legend = [value(x) for x in uHelper.connection_phase_list])
    uHelper.novos_vs_plot.legend.location = "top_left"
    uHelper.novos_vs_plot.legend.orientation = "horizontal"
    novos_vs_plot_new_legend = uHelper.novos_vs_plot.legend[0]
    uHelper.novos_vs_plot.legend[0].plot = None
    uHelper.novos_vs_plot.add_layout(novos_vs_plot_new_legend, 'above')

    vs_driller_hybrid_novos_column = column(uHelper.driller_vs_plot, uHelper.hybrid_vs_plot, uHelper.novos_vs_plot)
    vs_driller_hybrid_novos_column.sizing_mode = uHelper.sizing_mode
    vs_driller_hybrid_novos_layout = layout(vs_driller_hybrid_novos_column, sizing_mode = uHelper.sizing_mode) 
    vsDrillerHybridNOVOS = Panel(child = vs_driller_hybrid_novos_layout, title = "Driller vs Hybrid vs Novos")
    vsDrillerHybridNOVOS.name = "vsDrillerHybridNOVOSName"
    vsDrillerHybridNOVOS.tags = ["vsDrillerHybridNOVOSTag"]
    #end 20180928
    ##################################



    p3 = figure(plot_width=uHelper.plot_width, plot_height=300, toolbar_location=None)
    #p3.line([1, 2, 3, 4, 5], [16, 17, 12, 10, 18], line_width=3, color="red", alpha=0.5)
    #tabNovosConfigConnectionAnalysis = Panel(child=None, title="Novos Config Connection Analysis")
    p3.text([65,65,65],[65,65,65], text=[ "Coming Soon"], alpha=0.5, text_font_size="50pt", text_baseline="middle", text_align="center")
    p3.xaxis.visible = None
    p3.yaxis.visible = None
    p3.background_fill_color = "white"
    p3.outline_line_color = None
    tabNovosConfigConnectionAnalysis = Panel(child=p3, title="Activity type Stats")
    tabNovosConfigConnectionAnalysis.name="NovosConfigConnectionAnalysisName"
    tabNovosConfigConnectionAnalysis.tags=["NovosConfigConnectionAnalysisTag"]

    p6 = figure(plot_width=uHelper.plot_width, plot_height=300, toolbar_location=None)
    #p6.line([1, 2, 3, 4, 5], [16, 17, 12, 10, 18], line_width=3, color="orange", alpha=0.5)
    p6.text([65,65,65],[65,65,65], text=[ "Coming Soon"], alpha=0.5, text_font_size="50pt", text_baseline="middle", text_align="center")
    p6.xaxis.visible = None
    p6.yaxis.visible = None
    p6.background_fill_color = "white"
    p6.outline_line_color = None
    #tabDistributioncharts = Panel(child=None, title="Distribution charts")
    tabDistributioncharts = Panel(child=p6, title="Distribution charts")
    tabDistributioncharts.name="DistributionchartsName"
    tabDistributioncharts.tags=["DistributionchartsTag"]

    p7 = figure(plot_width=uHelper.plot_width, plot_height=300, toolbar_location=None)
    #p7.line([1, 2, 3, 4, 5], [16, 17, 12, 10, 18], line_width=3, color="black", alpha=0.5)
    p7.text([65,65,65],[65,65,65], text=[ "Coming Soon"], alpha=0.5, text_font_size="50pt", text_baseline="middle", text_align="center")
    p7.xaxis.visible = None
    p7.yaxis.visible = None
    p7.background_fill_color = "white"
    p7.outline_line_color = None
    tabDuplicateofContinuousinDepth = Panel(child=p7, title="Config Connection Analysis")
    #tabDuplicateofContinuousinDepth = Panel(child=None, title="Duplicate of Continuous in Depth")
    tabDuplicateofContinuousinDepth.name="DuplicateofContinuousinDepthName"
    tabDuplicateofContinuousinDepth.tags=["DuplicateofContinuousinDepthTag"]
    
    about_div = Div(text="""<p> Data Visualization <br> 
                            Copyright 2018 Precision Drilling Corporation. All rights reserved.<br> 
                            Version 1.1.1(Official Build)<br>
                            <br>
                            <h3>Technical Support</h3>
                            <h4>Email:</h4>
                            <ul style="list-style-type:circle">
                                 <li>KFransisco@precisiondrilling.com</li>
                                 <li>peng.wang@precisiondrilling.com</li>
                            </ul>
                            <h4>Phone:</h4>
                            <ul style="list-style-type:circle">
                              <li>403-716-4704</li>
                              <li>403-716-4631</li>
                            </ul>
                            <h4>Release Note:</h4>
                            <ul style="list-style-type:circle">
                              <li>Added "Driller vs Hybrid vs Novos" tab <br></li>
                              <li>Moved "main plot" from "Main" tab to "Over Connection Analysis" Tab</li>
                              <li>Deleted "Continuous in Depth" and "Driller vs Novos" tabs</li>
                              <li>"Connection Type" Checklist is greyed out, when "Driller vs Hybrid vs Novos" tab is activated</li>
                              <li>Colors are now consistent with what we have in "PowerBI"</li>
                              <li>"Wheel zoom" is removed from  plot "tool bar"</li>
                              <li>Display the latest dataset, whenever user clicks "Reload this page" from browser</li>
                            </ul>
                            </p>""",
                     width=uHelper.plot_width, height=900)
    about_div.css_classes = ["aboutDiv"] 
    #about_figure = figure(plot_width=uHelper.plot_width, plot_height=300, toolbar_location=None)
    #p7.line([1, 2, 3, 4, 5], [16, 17, 12, 10, 18], line_width=3, color="black", alpha=0.5)
    #about_figure.text([65,65,65],[65,65,65], text=[ "Coming Soon"], alpha=0.5, text_font_size="50pt", text_baseline="middle", text_align="center")
    #about_figure.xaxis.visible = None
    #about_figure.yaxis.visible = None
    #about_figure.background_fill_color = "white"
    #about_figure.outline_line_color = None
    tabAboutPanel = Panel(child = about_div, title = "About", width = uHelper.plot_width, height = 900)
    #tabDuplicateofContinuousinDepth = Panel(child=None, title="Duplicate of Continuous in Depth")
    tabAboutPanel.name="AboutPanelName"
    tabAboutPanel.tags=["AboutPanelTag"]


    uHelper.tabs = Tabs(tabs=[tabMain, \
                      tabActivitytypeStats, \
                      vsDrillerHybridNOVOS, \
                      tabNovosConfigConnectionAnalysis, \
                      tabDistributioncharts, \
                      tabDuplicateofContinuousinDepth, \
                      tabAboutPanel], width= uHelper.plot_width, sizing_mode='scale_width')
    
    uHelper.tabs.css_classes = ["tabsbackgroundcolorblack"]
    print("\n main chart loading time \n")    
    print(timeit.default_timer() - start_time_rest_chart)

    uHelper.spacer_4 = Spacer(width=120, height=350)
    uHelper.sidebar_layout = layout(column(uHelper.menu_layout, uHelper.spacer_4))
    uHelper.sidebar_layout.css_classes = ["sidebarlayout"] 
    tabs_row = row(uHelper.tabs)
    tabs_row.sizing_mode = uHelper.sizing_mode
    main_row = row(uHelper.sidebar_layout, tabs_row)
    main_row.sizing_mode = uHelper.sizing_mode
    uHelper.main_row = main_row
    uHelper.main_row.css_classes = ["mainrowlayout"] 
    uHelper.main_layout = layout(uHelper.main_row, sizing_mode='scale_width')# uHelper.sizing_mode)
    uHelper.main_layout.css_classes = ["mainlayout"]
    
    #vbar_clicked_index_dict = {}
    #vbar_clicked_index_dict['index'] = [-1, ]
    #uHelper.selectedVbarIndexSource = ColumnDataSource(data = vbar_clicked_index_dict)    
    #taptool = uHelper.main_plot.select(type=TapTool)
    ##uHelper.main_plot.js_on_event(Tap, uHelper.tapcallback)
    ##novos_length = len(uHelper.novos_connection_dict[uHelper.depth_ft_str])
    #
    start_time_all = timeit.default_timer()
    #uHelper.main_plot.js_on_event(Tap, CustomJS(args=dict(allSource = uHelper.mainplot_source,  
    #                                                      selectedVbarIndexSource =  uHelper.selectedVbarIndexSource, \
    #                                                      index2 = uHelper.index2), \
    #                                   code = sub_novos_plot.m_selected_index_code))
    
    main_plot_vbars.data_source.on_change('selected', uHelper.handler)
    #uHelper.main_plot.js_on_event(Tap, CustomJS.from_py_func(uHelper.update_subplot))
    print("\nbk_plotter loading time \n")    
    print(timeit.default_timer() - start_time_all)
    

def on_session_destroyed(session_context):
    ''' If present, this function is called when a session is closed. '''
    print ("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
    print("on_session_destroyed")

