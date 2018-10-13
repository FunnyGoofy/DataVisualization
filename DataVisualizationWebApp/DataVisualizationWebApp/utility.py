from bokeh.models  import CategoricalTicker
from bokeh.core.properties import Int
from bokeh.models import FactorRange, Spacer, Legend
from bokeh.embed import components
from bokeh.plotting import figure, curdoc
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
import pandas as pd
from bokeh.layouts import row, column, gridplot, widgetbox
from bokeh.models import ColumnDataSource, TapTool, VBar, Rect
from bokeh.models.widgets import PreText, Select, CheckboxGroup
from bokeh.models.widgets import Panel, Tabs  
from bokeh.io.state import curstate
from bokeh.resources import Resources
from bokeh.themes import Theme
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
from DataVisualizationWebApp import driller_hybrid_novos_vs_plot

#from DataVisualizationWebApp import utility as uHelper
#from bokeh.application.handlers.server_lifecycle import ServerLifecycleHandler

screen_width = None
#plot_width = None
plot_width = 1400
version = None
width_coefficient = 0.90
rig_id_str = "rig_id"
job_id_str = 'job_id'
crew_shift_str = 'crew_shift'
well_selection_str = "well_section"
connection_type_str = "connection_type"
connection_phase_str = "connection_phase"
type_str = "type"
status_str = "status"
hole_depth_str = 'hole_depth'
pre_slip_time_str = 'pre_slip_time'
post_slip_time_str = "post_slip_time"
survey_time_str = "survey_time"
backream_time_str = "backream_time"
slip_to_slip_str = "slip_to_slip"
depth_ft_str = "depth_ft"
edr_depth_ft = 'edr_depth_ft'
selected_rig = ''
selected_job  = ''
sizing_mode = 'scale_width'
visualization_depth_str = "visualization_depth"
rigs_combx = None
jobs_combx = None
crewshift_combx = None

all_connection_dict = {}
novos_connection_dict = {}
all_connection_table = None
novos_connection_table = None
rigs_list = []
jobs_list = []
crewshift_list = []
novos_source = None 
main_plot = None
mainplot_source = None
well_connnection_source = None
db_records_rig_queue = None
db_records_rig_event = None
update_drillingconn_wellsect_queue = None
update_drillingconn_wellsect_event = None
update_drillingconn_wellsect_thread = None
drillingconn_wellsect_condition = None    
update_b2s_s2b_queue = None 
update_b2s_s2b_event = None
update_main_plot_queue = None
update_main_plot_event = None
mainplot_data_all = None 
checkbox_group_1_selections = None 
checkbox_group_2_selections = None 
checkbox_group_3_selections = None 
all_connection_dict = None 
subplot_source = None
well_connection_textbox_source = None
default_rig_number = ''
rigs_list = []
default_job_number = ''
jobs_list = []
main_layout = None
checkbox_group_1 = None
checkbox_group_2 = None
checkbox_group_3 = None
m_color_white = "white"
sub_plot = None
#subplotColorsLength = None
#subplotSource = None
novos_Source = None
subplot_Source = None
#subplotColorsLength = None
b2s_datasource = None
update_b2s_s2b_queue = None
update_b2s_s2b_event = None
s2b_datasource = None
update_drillingconn_wellsect_queue  = None
update_drillingconn_wellsect_event  = None
well_connection_textbox_source      = None
m_well_selection = None
m_well_connection = None
m_well_conn_phase = None
spacer_1 = None
spacer_2 = None
spacer_3 = None
spacer_4 = None
menu_column_1_layout = None
well_selection_layout = None
well_connection_layout = None
well_conn_phase_layout = None
menu_column_2_layout = None
menu_middle_layout = None
menu_top_layout = None
menu_bottom_layout = None
menu_layout = None
sidebar_layout = None
main_row = None
hide_subplot_callback = None
subplot_colors_length = None
tapcallback = None
ticker_cb_reset = None
hide_subplot_callback = None
ticker_cb = None
main_plot_dict = {}
depth_ref_list = []
driller_vs_plot = None
driller_vs_plot_source = None
hybrid_vs_plot = None
hybrid_vs_plot_source = None
novos_vs_plot = None
novos_vs_plot_source = None
driller_vs_dataset = None
color_list = ["#01B8AA", "#000000", "#FD625E", "#F2C80F", "#A66999"]
connection_phase_list = ["B2S", "S2S", "S2B", "Survey", "BackReam"]
update_driller_hybrid_novos_vs_queue = None
update_driller_hybrid_novos_vs_event = None
driller_hybrid_novos_vs_plot_dict = None
driller_vs_plot_dict = None
hybrid_vs_plot_dict = None
novos_vs_plot_dict = None 
x_range = ['1', '2', '3', '4', '5']
tabs = None
database_que = None
get_all_data_queue = None 
get_all_data_event = None 
get_all_data_thread = None

def merge(a, b, path=None):
    "merges b into a"
    if path is None: path = []
    for key in b:
        if key in a:
            if isinstance(a[key], dict) and isinstance(b[key], dict):
                merge(a[key], b[key], path + [str(key)])
            elif a[key] == b[key]:
                pass # same leaf value
            else:
                raise Exception('Conflict at %s' % '.'.join(path + [str(key)]))
        else:
            a[key] = b[key]
    return a




def customize_ticker():
    JS_CODE = """
        import {CategoricalTicker} from "models/tickers/categorical_ticker"
        import * as p from "core/properties"

        export class MyTicker extends CategoricalTicker
            type: "MyTicker"
        
            @define {
            nth: [ p.Int, 1 ]
            }
        
            get_ticks: (start, end, range, cross_loc) ->
                ticks = super(start, end, range, cross_loc)
                ticks.major = ticks.major.filter((element, index) => index % this.nth == 0)
                return ticks
        """

    class MyTicker(CategoricalTicker):
        __implementation__ = JS_CODE
        nth = Int(default=1)

    mTicker = MyTicker(nth=5)
    return mTicker 

def get_default_value(all_connection_table, comboBx, selectedRig = '', selectedJob = ''):
    global rig_id_str
    global job_id_str
    global crew_shift_str

    default_number = ''
    comboBx_list = []
    if comboBx == 'Rigs':
        comboBx_list = all_connection_table[rig_id_str].unique().tolist()
    elif comboBx == 'Jobs':
        target = []
        selectedRig = int(selectedRig)
        target.append(selectedRig)
        target.append('')
        rigs_query = "{} in @target".format(rig_id_str)
        selected_rig_table = all_connection_table.query(rigs_query)
        comboBx_list = selected_rig_table[job_id_str].unique().tolist()
    elif comboBx == 'CrewShift':
        #TODO need to test
        rigs_query = "{} in @selectedRig".format(rig_id_str)
        selected_rig_table = all_connection_table.query(rigs_query)
        jobs_query = "{} in @selectedJob".format(job_id_str)
        selected_job_table = selected_rig_table.query(jobs_query)

        comboBx_list = selected_job_table[crew_shift_str].unique().tolist()
        comboBx_list.insert(0, ' ')

    # maybe need logic to handle no records in table. it is 0
    if len(comboBx_list) >= 1:
        default_number = comboBx_list[0]

    return default_number, comboBx_list

def get_data(all_connection_dict, rig = -1, job = -1):
    global hole_depth_str
    global pre_slip_time_str 
    global post_slip_time_str
    global survey_time_str
    global backream_time_str 
    global slip_to_slip_str
    global visualization_depth_str

    all_connection_table = {}
    all_connection_table = pd.DataFrame.from_dict(all_connection_dict)
        
    depth_ref_list = []
    depth_list = []
    b2s_list = []
    s2s_list = []
    s2b_list = []
    survey_list = []
    ream_list = []
    b2s_s2s_list = []
    b2s_s2s_s2b_list = []
    b2s_s2s_s2b_survey_list = []
    b2s_s2s_s2b__survey_ream_list = []
    if(( rig == -1) or (job == -1)):
        depth_ref_list = list(map(float, all_connection_table[hole_depth_str]))
        depth_ref_list.sort(key=float)
        depth_list = list(map(float, all_connection_table[visualization_depth_str]))
        depth_list.sort(key=float)
        b2s_list = list(map(float, all_connection_table[pre_slip_time_str]))
        s2s_list = list(map(float, all_connection_table[slip_to_slip_str]))
        s2b_list = list(map(float, all_connection_table[post_slip_time_str]))
        survey_list = list(map(float, all_connection_table[survey_time_str]))
        ream_list = list(map(float, all_connection_table[backream_time_str]))
    else:
        global rig_id_str
        global job_id_str
            
        rig_target = []
        rig_target.append(int(rig))
        rig_target.append('')
        rigs_query = "{} in @rig_target".format(rig_id_str)
        selected_rig_table = all_connection_table.query(rigs_query)

        job_target = []
        job_target.append(int(job))
        job_target.append('')
        jobs_query = "{} in @job_target".format(job_id_str)
        selected_job_table = selected_rig_table.query(jobs_query)

        depth_ref_list = list(map(float, selected_job_table[hole_depth_str]))
        depth_ref_list.sort(key=float)
        depth_list = list(map(float, selected_job_table[visualization_depth_str]))
        depth_list.sort(key=float)
        b2s_list = list(map(float, selected_job_table[pre_slip_time_str]))
        s2s_list = list(map(float, selected_job_table[slip_to_slip_str]))
        s2b_list = list(map(float, selected_job_table[post_slip_time_str]))
        survey_list = list(map(float, all_connection_table[survey_time_str]))
        ream_list = list(map(float, all_connection_table[backream_time_str]))

    b2s_s2s_list = list(map(add, b2s_list, s2s_list))
    b2s_s2s_s2b_list = list(map(add, b2s_s2s_list, s2b_list))
    b2s_s2s_s2b_survey_list = list(map(add, b2s_s2s_s2b_list, survey_list))
    b2s_s2s_s2b__survey_ream_list = list(map(add, b2s_s2s_s2b_survey_list, ream_list))
        
    # could be a function
    rig_job_dict = {}
    rig_job_dict['VBarTop'] = []
    rig_job_dict['VBarBottom'] = []
    rig_job_dict['VBarColors'] = []
    rig_job_dict['VBarType'] = []
    rig_job_dict['HoleDepthRef'] = depth_ref_list + depth_ref_list + depth_ref_list + depth_ref_list + depth_ref_list
    rig_job_dict['HoleDepth'] = depth_list + depth_list + depth_list + depth_list + depth_list
    rig_job_dict['VBarTop'] = b2s_list + b2s_s2s_list + b2s_s2s_s2b_list + b2s_s2s_s2b_survey_list + b2s_s2s_s2b__survey_ream_list
    rig_job_dict['VBarBottom'] = [ 0 for item in b2s_list] + b2s_list  + b2s_s2s_list + b2s_s2s_s2b_list + b2s_s2s_s2b_survey_list
    rig_job_dict['VBarColors'] = [ "#01B8AA" for item in b2s_list] \
                                    +  [ "#000000" for item in b2s_s2s_list] \
                                    +  [ "#FD625E" for item in b2s_s2s_s2b_list] \
                                    +  [ "#F2C80F" for item in b2s_s2s_s2b_survey_list]\
                                    +  [ "#A66999" for item in b2s_s2s_s2b__survey_ream_list]
    rig_job_dict['VBarType'] =  ['B2S' for item in b2s_s2s_s2b_list] \
                                    + ['S2S' for item in b2s_s2s_s2b_list] \
                                    + ['S2B' for item in b2s_s2s_s2b_list] \
                                    + ['Survey' for item in b2s_s2s_s2b_list] \
                                    + ['Ream' for item in b2s_s2s_s2b_list] 
        
    return rig_job_dict, depth_list 

def update(all_connection_dict, rig = -1, job = -1, selected = None):
    rig_job_dict = {}
    depth_list = []
    if selected != None:
        rig_job_dict, depth_list = get_data(all_connection_dict)
    else:
        rig_job_dict, depth_list = get_data(all_connection_dict, rig, job)
    return rig_job_dict, depth_list

def update_combBx_values(val, lst, columnName = ''):
    global selected_rig
    global rig_id_str
    global job_id_str
    global all_connection_table
    global jobs_list
    global crewShift_list

    if val == '':
        return [x for x in lst]
    else:
        target = []
        target.append(int(val))
        target.append('')
        if columnName == 'JobNumber':
            selected_rig = int(val)
            rigs_query = "{} in @target".format(rig_id_str)
            selected_rig_table = all_connection_table.query(rigs_query)
            jobs_list = selected_rig_table[job_id_str].unique().tolist()
            return jobs_list
        elif columnName == 'CrewShift':
            selected_rig = str(selected_rig)
            rigs_query = "{} in @selected_rig".format(rig_id_str)
            selected_rig_table = all_connection_table.query(rigs_query)
            jobs_query = "{} in @target".format(job_id_str)
            selected_job_table = selected_rig_table.query(jobs_query)
            crewShift_list = selected_job_table[crew_shift_str].unique().tolist()
            return crewShift_list
    
@gen.coroutine
def update_1st_chart(selected_rig, selected_job):
    global update_drillingconn_wellsect_queue
    global update_drillingconn_wellsect_event
    global all_connection_dict
    global well_connnection_source
    global well_connection_textbox_source

    update_drillingconn_wellsect_queue.put(drillingconn_wellsect_plot.update_well_selection_data(update_drillingconn_wellsect_event, all_connection_dict, selected_rig, selected_job))
    update_drillingconn_wellsect_event.wait()
    well_connection_colors, x, well_connnection_counts, well_connnection_data = update_drillingconn_wellsect_queue.get()
    well_connnection_source.data = dict(colors = well_connection_colors, \
                                        x = x, \
                                        counts = well_connnection_counts)

    well_connection_textbox_source.data = dict(x = [600,], \
                                                y = [450,], \
                                                txt = [('Total Connections: %d' % sum(well_connnection_counts)),] )

@gen.coroutine
def update_2nd_chart(selected_rig, selected_job):
    global update_b2s_s2b_queue 
    global update_b2s_s2b_event 
    global novos_connection_table
    global b2s_datasource
    global s2b_datasource

    update_b2s_s2b_queue.put(b2s_s2b_plot.update_b2s_s2b_data(update_b2s_s2b_event, novos_connection_table, selected_rig, selected_job))
    update_b2s_s2b_event.wait()
    b2s_canceled_list, b2s_completed_list, \
    b2s_exception_list,b2s_failed_list, \
    s2b_canceled_list, s2b_completed_list, \
    s2b_exception_list, s2b_failed_list = update_b2s_s2b_queue.get()

    b2s_datasource.data = dict(Canceled = b2s_canceled_list, \
                                Completed = b2s_completed_list, \
                                Exception = b2s_exception_list, \
                                Failed = b2s_failed_list)

    s2b_datasource.data = dict(Canceled = s2b_canceled_list, \
                                Completed = s2b_completed_list, \
                                Exception = s2b_exception_list, \
                                Failed = s2b_failed_list)

@gen.coroutine
def update_main_plot(selected_rig, \
                selected_job, \
                from_comboBx_group, \
                checkbox_group_1_selections = [],\
                checkbox_group_2_selections = [], \
                checkbox_group_3_selections = []):
    global update_main_plot_event
    global mainplot_source 
    global main_plot 
    global mainplot_data_all 
    global all_connection_dict
    global update_main_plot_queue
   
    doc = curdoc()
    update_main_plot_queue.put(all_main_plot.update_main_plot_chart(doc, \
                                            update_main_plot_event, \
                                            mainplot_source, \
                                            main_plot, \
                                            mainplot_data_all, \
                                            checkbox_group_1_selections, \
                                            checkbox_group_2_selections,\
                                            checkbox_group_3_selections, \
                                            all_connection_dict,\
                                            selected_rig, \
                                            selected_job, \
                                            from_comboBx_group))
    update_main_plot_event.set()

def update_driller_hybrid_novos_vs_plot(selected_rig, \
                                        selected_job, \
                                        from_comboBx_group, \
                                        checkbox_group_1_selections = [],\
                                        checkbox_group_2_selections = [], \
                                        checkbox_group_3_selections = []):
    global update_driller_hybrid_novos_vs_event
    global update_driller_hybrid_novos_vs_queue
    global driller_vs_plot
    global driller_vs_plot_source
    global hybrid_vs_plot
    global hybrid_vs_plot_source
    global novos_vs_plot
    global novos_vs_plot_source

    doc = curdoc()
    update_driller_hybrid_novos_vs_queue.put(driller_hybrid_novos_vs_plot.\
                                             update_driller_hybrid_novos_vs_charts(doc,\
                                                                                 update_driller_hybrid_novos_vs_event, \
                                                                                 driller_vs_plot, \
                                                                                 driller_vs_plot_source, \
                                                                                 hybrid_vs_plot, \
                                                                                 hybrid_vs_plot_source, \
                                                                                 novos_vs_plot, \
                                                                                 novos_vs_plot_source, \
                                                                                 checkbox_group_1_selections, \
                                                                                 checkbox_group_2_selections,\
                                                                                 checkbox_group_3_selections, \
                                                                                 all_connection_dict,\
                                                                                 selected_rig, \
                                                                                 selected_job, \
                                                                                 from_comboBx_group))
    update_driller_hybrid_novos_vs_event.set()  

def rigs_combx_change(attrname, old, new):
    global selected_rig
    global selected_job
    
    selected_rig = int(new)
    import_data.retrieve_data(selected_rig)    

    global get_all_data_queue 
    global get_all_data_event
    global all_connection_dict
    global mainplot_data_all

    get_all_data_queue.put(all_main_plot.get_all_data(get_all_data_event, all_connection_dict))
    get_all_data_event.wait()
    mainplot_data_all, depth_list_all = get_all_data_queue.get()
    mainplot_data_all['HoleDepth'] = ["{0:.2f}".format(x) for x in mainplot_data_all['HoleDepth']]

    new_jobs_list = update_combBx_values(new, jobs_list, 'JobNumber')
    new_jobs_list = [str(x) for x in new_jobs_list]
    jobs_combx.options = new_jobs_list
    if len(new_jobs_list) > 0:
        first_selected_job = new_jobs_list[0]
    else:
        first_selected_job = '0'
    
    rig, job = new, first_selected_job
    selected_rig = rig
    selected_job = job
    jobs_combx.value = first_selected_job

def jobs_combx_change(attrname, old, new):
    global all_connection_dict
    global well_connnection_source
    global selected_rig
    global selected_job
        
    rig, job = rigs_combx.value, new
    selected_rig = rig
    selected_job = job
        
    crewShift_list = update_combBx_values(new, rigs_list, 'CrewShift')
    crewShift_list = [str(x) for x in crewShift_list]
    crewshift_combx.options = crewShift_list
    update_1st_chart(selected_rig, selected_job)
    update_2nd_chart(selected_rig, selected_job)
    # update main_plot datasource
    from_comboBx_group = False
    update_main_plot(selected_rig, selected_job, from_comboBx_group)  
    update_driller_hybrid_novos_vs_plot(selected_rig, selected_job, from_comboBx_group)

def crewshift_combx_change(attrname, old, new):
    pass
    #crewshift_combx.options = update_combBx_values(new, rig_number_list, 'Crewshift')


def checkbox_callback_1(attr, old, new):
    checkbox_group_1_selections = [checkbox_group_1.labels[i] for i in 
                    checkbox_group_1.active]
    checkbox_group_2_selections = [checkbox_group_2.labels[i] for i in 
                    checkbox_group_2.active]
    checkbox_group_3_selections = [checkbox_group_3.labels[i] for i in 
                    checkbox_group_3.active]

    selected_rig, selected_job = rigs_combx.value, jobs_combx.value
    from_comboBx_group = True
    update_main_plot(selected_rig, \
                     selected_job, \
                     from_comboBx_group, \
                     checkbox_group_1_selections, \
                     checkbox_group_2_selections, \
                     checkbox_group_3_selections) 
    update_driller_hybrid_novos_vs_plot(selected_rig, \
                                        selected_job, \
                                        from_comboBx_group, \
                                        checkbox_group_1_selections,\
                                        checkbox_group_2_selections, \
                                        checkbox_group_3_selections)
 
def checkbox_callback_2(attr, old, new):
    checkbox_group_1_selections = [checkbox_group_1.labels[i] for i in 
                    checkbox_group_1.active]
    checkbox_group_2_selections = [checkbox_group_2.labels[i] for i in 
                    checkbox_group_2.active]
    checkbox_group_3_selections = [checkbox_group_3.labels[i] for i in 
                    checkbox_group_3.active]

    selected_rig, selected_job = rigs_combx.value, jobs_combx.value
    from_comboBx_group = True
    update_main_plot(selected_rig, \
                     selected_job, \
                     from_comboBx_group, \
                     checkbox_group_1_selections, \
                     checkbox_group_2_selections, \
                     checkbox_group_3_selections) 
    update_driller_hybrid_novos_vs_plot(selected_rig, \
                                        selected_job, \
                                        from_comboBx_group, \
                                        checkbox_group_1_selections,\
                                        checkbox_group_2_selections, \
                                        checkbox_group_3_selections)
 

def checkbox_callback_3(attr, old, new):    
    checkbox_group_1_selections = [checkbox_group_1.labels[i] for i in 
                    checkbox_group_1.active]
    checkbox_group_2_selections = [checkbox_group_2.labels[i] for i in 
                    checkbox_group_2.active]
    checkbox_group_3_selections = [checkbox_group_3.labels[i] for i in 
                    checkbox_group_3.active]
    selected_rig, selected_job = rigs_combx.value, jobs_combx.value
    from_comboBx_group = True
    update_main_plot(selected_rig, \
                     selected_job, \
                     from_comboBx_group, \
                     checkbox_group_1_selections, \
                     checkbox_group_2_selections, \
                     checkbox_group_3_selections) 
    update_driller_hybrid_novos_vs_plot(selected_rig, \
                                        selected_job, \
                                        from_comboBx_group, \
                                        checkbox_group_1_selections,\
                                        checkbox_group_2_selections, \
                                        checkbox_group_3_selections)
 
def get_novos_job_table(novos_connection_table, selected_rig, selected_job):
    global rig_id_str
    global job_id_str

    rig = selected_rig
    job = selected_job
    rig_target = []
    rig_target.append(int(rig))
    rig_target.append('')
    rigs_query = "{} in @rig_target".format(rig_id_str)
    selected_rig_table = novos_connection_table.query(rigs_query)

    job_target = []
    job_target.append(int(job))
    job_target.append('')
    jobs_query = "{} in @job_target".format(job_id_str)
    selected_job_table = selected_rig_table.query(jobs_query)
    return selected_job_table


def show_subplot():
    global novos_connection_dict
    global depth_ft_str
    global mainplot_source
    global novos_source
    global subplot_source
    global subplot_colors_length
    global novos_length
    global sub_plot 
    global tapcallback
    global mainplot_data_all
    global all_connection_dict

    #hole_depth_list = all_connection_dict["hole_depth"]
    
    #novos_length = len(novos_connection_dict[depth_ft_str])
    #tapcallback = CustomJS(args=dict(allSource = mainplot_source, \
    #                               novos_source = novos_source, \
    #                               subplotSource = subplot_source, \
    #                               subplotColorsLength = subplot_colors_length, \
    #                               novosLength = novos_length, \
    #                               subplot = sub_plot, \
    #                               holeDepthList = hole_depth_list \
    #                               ),\
    #                               code = sub_novos_plot.m_code) 

def reset_xAxis_ticker():
    global main_plot
    global ticker_cb_reset

    ticker_cb_reset = CustomJS(args=dict(ticker = main_plot.xaxis[0].ticker),\
                                         code="""
                                                ticker.nth = 10
                                            """)

def hide_subplot():
    global subplot_source
    global subplot_colors_length
    global novos_length
    global sub_plot
    global m_color_white
    global hide_subplot_callback

    hide_subplot_callback =  CustomJS(args=dict(m_color = m_color_white, \
                                                subplot = sub_plot, \
                                                subplotColorsLength = subplot_colors_length, \
                                                subplotSource = subplot_source), code="""
                                                    for(i = 0; i < subplotColorsLength; i++) {
                                                        subplotSource.data['B2SColors'][i] = 'white' 
                                                        subplotSource.data['B2STextColors'][i] = 'white' 
    
                                                    }
                                                    subplotSource.change.emit()
                                                    subplot.background_fill_color = 'white' 
                                                """)


def set_xAxis_ticker():
    global main_plot
    global ticker_cb

    ticker_cb = CustomJS(args=dict(ticker = main_plot.xaxis[0].ticker), \
                                code="""
                                if (Math.abs(cb_obj.start-cb_obj.end) > 20000) {
                                    ticker.nth = 200
                                }else if (Math.abs(cb_obj.start-cb_obj.end) > 2000) {
                                    ticker.nth = 20
                                }else if (Math.abs(cb_obj.start-cb_obj.end) > 30) {
                                    ticker.nth = 10
                                }else {
                                    ticker.nth = 1
                                }
                          """)

def handler(attr, old, new):
    global subplot_source
    global index2
    global novos_connection_dict
    global depth_ft_str
    global novos_connection_table
    global selected_rig
    global selected_job
    global all_connection_dict
    global all_connection_table
    global sub_plot

    print('attr: {} old: {} new: {}'.format(attr, old, new))
    if len(old.indices) < 1 :  
        return
    
    selected_vbar_id = old.indices[0]
    index_new = new.indices[0]
    
    B2SColorsList = ['red','red','red','red','red', 'red','red','red','red','red','red', 'red']
    TextList = ['', '', '', '', '', '', '', '', '', '', '', '']
    B2STextList = ['Cleanhole - Active', 'Cleanhole - Completed', 'Setboxheight - Active', 'Setboxheight - Completed', 'Setweight - Active', 'Setweight - Completed', 'Offbottom-Active', 'Unweightbit - Active', 'Unweightbit - Completed', 'Clearbit - Active', 'Clearbit - Completed', 'Offbottom - Completed']
    textXList = [2, 12, 22, 32, 42, 52, 2, 12, 22, 32, 42, 52]
    B2STextColorsList = ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black']
    B2SHideColorsList = ['white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white']
    subplotXList = [5, 15, 25, 35, 45, 55, 5, 15, 25, 35, 45, 55]
    subplotYList = [10, 10, 10, 10, 10, 10, 25, 25, 25, 25, 25, 25]

    #subplot_source.data = dict(B2SColors = B2SColorsList,
    #                          Text = TextList,
    #                          B2SText = B2STextList,
    #                          text_x = textXList,
    #                          B2STextColors = B2STextColorsList,
    #                          B2SHideColors = B2SHideColorsList,
    #                          subplot_x = subplotXList,
    #                          subplot_y = subplotYList) 
   
    holedepth = mainplot_source.data['HoleDepthRef'][selected_vbar_id]
    hole_depth_value = round(float(holedepth),2)
    
    vbarType = mainplot_source.data['VBarType'][selected_vbar_id]
    if vbarType == 'S2S':
         subplot_source.data = dict(B2SColors = B2SHideColorsList,
                                    Text = TextList,
                                    B2SText = B2STextList,
                                    text_x = textXList,
                                    B2STextColors = B2STextColorsList,
                                    B2SHideColors = B2SHideColorsList,
                                    subplot_x = subplotXList,
                                    subplot_y = subplotYList)
         return
    selected_rig, selected_job = rigs_combx.value, jobs_combx.value
    selected_rig_table = get_novos_job_table(novos_connection_table, selected_rig, selected_job)
    selected_novos_connection_dict = selected_rig_table.to_dict('dict')
    novos_length = len(selected_novos_connection_dict[depth_ft_str])
    edr_depth_ft_list = list(selected_novos_connection_dict['edr_depth_ft'].values())
    connection_phase_list = list(selected_novos_connection_dict['connection_phase'].values())
    type_list = list(selected_novos_connection_dict['type'].values())
    status_list = list(selected_novos_connection_dict['status'].values()) 
        
    for i in range(novos_length):
        if edr_depth_ft_list[i] == None:
            continue
        
        if vbarType == None:
            continue
        
        novos_edr_value = round(float((edr_depth_ft_list[i])), 2)
        
        if (hole_depth_value < novos_edr_value):
            if (vbarType == 'B2S') : 
                if (B2SColorsList[0] == 'red'):
                    TextList[0] = 'CleanHole-Active'
                if (B2SColorsList[1] == 'red'):
                    TextList[1] = 'CleanHole-Completed' 
                if (B2SColorsList[2] == 'red'):
                    TextList[2] = 'SetBoxHeight-Active' 
                if (B2SColorsList[3] == 'red'):
                    TextList[3] = 'SetBoxHeight-Completed' 
                if (B2SColorsList[4] == 'red'):
                    TextList[4] = 'SetWeight-Active'
                if (B2SColorsList[5] == 'red'):
                    TextList[5] = 'SetWeight-Completed' 
                if (B2SColorsList[6] == 'red'):
                    TextList[6] = 'Offbottom-Active' 
                if (B2SColorsList[7] == 'red'):
                    TextList[7] = 'Unweightbit-Active' 
                if (B2SColorsList[8] == 'red'):
                    TextList[8] = 'Unweightbit-Completed' 
                if (B2SColorsList[9] == 'red'):
                    TextList[9] = 'ClearBit-Active' 
                if (B2SColorsList[10] == 'red'):
                    TextList[10] = 'ClearBit-Completed' 
                if (B2SColorsList[11] == 'red'):
                    TextList[11] = 'Offbottom-Completed' 
            elif vbarType == 'S2B':
                if(B2SColorsList[0] == 'red'):
                    TextList[0] = 'TagBottom-Active'    
                if (B2SColorsList[1] == 'red'):
                    TextList[1] = 'TagBottom-Completed' 
                if (B2SColorsList[6] == 'red'):
                    TextList[6] = 'AddStand-Active' 
                if (B2SColorsList[7] == 'red'):
                    TextList[7] = 'AddStand-Completed' 
                if (B2SColorsList[8] == 'red'):
                    TextList[8] = 'TakeWeight-Active' 
                if (B2SColorsList[9] == 'red'):
                    TextList[9] = 'TakeWeight-Completed' 
                if (B2SColorsList[10] == 'red'):
                    TextList[10] = 'FlowSetpoint-Active' 
                if (B2SColorsList[11] == 'red'):
                    TextList[11] = 'RotateDrill-Active'  
                B2SColorsList[2] = 'white' 
                B2SColorsList[3] = 'white' 
                B2SColorsList[4] = 'white' 
                B2SColorsList[5] = 'white' 
                TextList[2] = '' 
                TextList[3] = '' 
                TextList[4] = '' 
                TextList[5] = '' 
                
            else:                
                B2SColorsList[0] = 'white' 
                B2SColorsList[1] = 'white' 
                B2SColorsList[2] = 'white' 
                B2SColorsList[3] = 'white' 
                B2SColorsList[4] = 'white' 
                B2SColorsList[5] = 'white' 
                B2SColorsList[6] = 'white' 
                B2SColorsList[7] = 'white' 
                B2SColorsList[8] = 'white' 
                B2SColorsList[9] = 'white' 
                B2SColorsList[10] = 'white' 
                B2SColorsList[11] = 'white' 

                TextList[0] = '' 
                TextList[1] = '' 
                TextList[2] = '' 
                TextList[3] = '' 
                TextList[4] = '' 
                TextList[5] = ''   
                TextList[6] = '' 
                TextList[7] = '' 
                TextList[8] = '' 
                TextList[9] = '' 
                TextList[10] = '' 
                TextList[11] = '' 


            subplot_source.data = dict(B2SColors = B2SColorsList,
                              Text = TextList,
                              B2SText = B2STextList,
                              text_x = textXList,
                              B2STextColors = B2STextColorsList,
                              B2SHideColors = B2SHideColorsList,
                              subplot_x = subplotXList,
                              subplot_y = subplotYList)
            break
        
        if (novos_edr_value == hole_depth_value):
            if (vbarType == 'B2S') : 
                if (connection_phase_list[i] == vbarType) :
                    if (type_list[i] == None) :
                        continue
                    
                    if (type_list[i] == 'OffBottom'):
                        if status_list[i] == None:
                            continue
                        if status_list[i] == 'Active':
                            B2SColorsList[6] = 'green'
                            TextList[6] = 'Offbottom-Active' 
                        elif status_list[i] == 'Completed' : 
                            B2SColorsList[11] = 'green'
                            TextList[11] = 'Offbottom-Completed' 
                        else:
                            if (B2SColorsList[6] != 'green') :
                                B2SColorsList[6] = 'yellow'
                                TextList[6] = 'Offbottom-Active' 
                            if (B2SColorsList[11] != 'green') :
                                B2SColorsList[11] = 'yellow'
                                TextList[11] = 'Offbottom-Completed' 
                        if (B2SColorsList[11] == 'green'):
                            B2SColorsList[6] = 'green'
                            TextList[6] = 'Offbottom-Active'
                        continue
                    elif (type_list[i] == 'UnWeightBit') :
                        if (status_list[i] == None):
                            continue
                        if status_list[i] == 'Active' :
                            B2SColorsList[7] = 'green'
                            TextList[7] = 'Unweightbit-Active'
                        elif (status_list[i] == 'Completed'): 
                            B2SColorsList[8] = 'green' 
                            TextList[8] = 'Unweightbit-Completed' 
                        else:
                            if B2SColorsList[7] != 'green' :
                               B2SColorsList[7] = 'yellow' 
                               TextList[7] = 'Unweightbit-Active' 
                            if B2SColorsList[8] != 'green':
                               B2SColorsList[8] = 'yellow' 
                               TextList[8] = 'Unweightbit-Completed' 
                        if B2SColorsList[8] == 'green' :
                           B2SColorsList[7] = 'green' 
                           TextList[7] = 'Unweightbit-Active'
                        continue
                    elif (type_list[i] == 'ClearBit') :
                        if (status_list[i] == None):
                            continue
                        if (status_list[i] == 'Active'):
                           B2SColorsList[9] = 'green' 
                           TextList[9] = 'ClearBit-Active'
                        elif (status_list[i] == 'Completed') :
                           B2SColorsList[10] = 'green'
                           TextList[10] = 'ClearBit-Completed' 
                        else : 
                            if (B2SColorsList[9] != 'green') :
                                TextList[9] = 'ClearBit-Active' 
                                B2SColorsList[9] = 'yellow'
                            if (B2SColorsList[10] != 'green'):
                                TextList[10] = 'ClearBit-Completed'
                                B2SColorsList[10] = 'yellow' 
                        if (B2SColorsList[10] == 'green'):
                            B2SColorsList[9] = 'green' 
                            TextList[9] = 'ClearBit-Active'
                        continue
                    elif type_list[i] == 'CleanHole':
                        if status_list[i] == None:
                            continue
                        if status_list[i] == 'Active': 
                           B2SColorsList[0] = 'green' 
                           TextList[0] = 'CleanHole-Active' 
                        elif status_list[i] == 'Completed': 
                           B2SColorsList[1] = 'green' 
                           TextList[1] = 'CleanHole-Completed' 
                        else:
                            if B2SColorsList[0] != 'green':
                               TextList[0] = 'CleanHole-Active' 
                               B2SColorsList[0] = 'yellow' 
                            if B2SColorsList[1] != 'green':
                               TextList[1] = 'CleanHole-Completed' 
                               B2SColorsList[1] = 'yellow' 
                        if B2SColorsList[1] == 'green':
                           B2SColorsList[0] = 'green' 
                           TextList[0] = 'CleanHole-Active'
                        continue
                    elif type_list[i] == 'SetBoxHeight':
                        if status_list[i] == None :
                            continue
                        if (status_list[i] == 'Active'): 
                            TextList[2] = 'SetBoxHeight-Active' 
                            B2SColorsList[2] = 'green' 
                        elif (status_list[i] == 'Completed'): 
                            TextList[3] = 'SetBoxHeight-Completed' 
                            B2SColorsList[3] = 'green' 
                        else:
                            if (B2SColorsList[2] != 'green'):
                                TextList[2] = 'SetBoxHeight-Active' 
                                B2SColorsList[2] = 'yellow' 
                            if (B2SColorsList[3] != 'green'):
                                TextList[3] = 'SetBoxHeight-Completed' 
                                B2SColorsList[3] = 'yellow'
                        if (B2SColorsList[3] == 'green') :
                            B2SColorsList[2] = 'green' 
                            TextList[2] = 'SetBoxHeight-Active'
                        continue
                    elif (type_list[i] == 'SetWeight') :
                        if (status_list[i] == 'Active') :
                            TextList[4] = 'SetWeight-Active' 
                            B2SColorsList[4] = 'green'
                        elif status_list[i] == 'Completed' :
                            TextList[5] = 'SetWeight-Completed' 
                            B2SColorsList[5] = 'green' 
                        else:
                            if (B2SColorsList[4] != 'green'):
                                TextList[4] = 'SetWeight-Active' 
                                B2SColorsList[4] = 'yellow' 
                            if (B2SColorsList[5] != 'green'):
                                TextList[5] = 'SetWeight-Completed' 
                                B2SColorsList[5] = 'yellow' 
                        if (B2SColorsList[5] == 'green') :
                            B2SColorsList[4] = 'green'
                            TextList[4] = 'SetWeight-Active'
                        continue
                    
                    if (B2SColorsList[0] == 'red'):
                        TextList[0] = 'CleanHole-Active'
                    if (B2SColorsList[1] == 'red'):
                        TextList[1] = 'CleanHole-Completed' 
                    if (B2SColorsList[2] == 'red'):
                        TextList[2] = 'SetBoxHeight-Active' 
                    if (B2SColorsList[3] == 'red'):
                        TextList[3] = 'SetBoxHeight-Completed' 
                    if (B2SColorsList[4] == 'red'):
                        TextList[4] = 'SetWeight-Active'
                    if (B2SColorsList[5] == 'red'):
                        TextList[5] = 'SetWeight-Completed' 
                    if (B2SColorsList[6] == 'red'):
                        TextList[6] = 'Offbottom-Active' 
                    if (B2SColorsList[7] == 'red'):
                        TextList[7] = 'Unweightbit-Active' 
                    if (B2SColorsList[8] == 'red'):
                        TextList[8] = 'Unweightbit-Completed' 
                    if (B2SColorsList[9] == 'red'):
                        TextList[9] = 'ClearBit-Active' 
                    if (B2SColorsList[10] == 'red'):
                        TextList[10] = 'ClearBit-Completed' 
                    if (B2SColorsList[11] == 'red'):
                        TextList[11] = 'Offbottom-Completed' 
                    continue
            elif vbarType == 'S2B':
                if (connection_phase_list[i] == vbarType):
                    if (type_list[i] == 'AddStand'):
                        if (status_list[i] == 'Active'): 
                            TextList[6] = 'AddStand-Active' 
                            B2SColorsList[6] = 'green'
                        elif status_list[i] == 'Completed': 
                            TextList[7] = 'AddStand-Completed' 
                            B2SColorsList[7] = 'green' 
                        else:
                            if (B2SColorsList[6] != 'green'):
                                TextList[6] = 'AddStand-Active' 
                                B2SColorsList[6] = 'yellow' 
                            if (B2SColorsList[7] != 'green'):
                                TextList[7] = 'AddStand-Completed' 
                                B2SColorsList[7] = 'yellow' 
                        
                        if (B2SColorsList[7] == 'green') :
                            B2SColorsList[6] = 'green' 
                            TextList[6] = 'AddStand-Active'
                            
                        continue
                    elif (type_list[i] == 'TakeWeight') :
                        if status_list[i] == 'Active' : 
                            TextList[8] = 'TakeWeight-Active' 
                            B2SColorsList[8] = 'green' 
                        elif status_list[i] == 'Completed':
                            B2SColorsList[9] = 'green' 
                            TextList[9] = 'TakeWeight-Completed' 
                        else:
                            if (B2SColorsList[8] != 'green'):
                                TextList[8] = 'TakeWeight-Active' 
                                B2SColorsList[8] = 'yellow' 
                            if (B2SColorsList[9] != 'green'):
                                TextList[9] = 'TakeWeight-Completed' 
                                B2SColorsList[9] = 'yellow' 
                        
                        if (B2SColorsList[9] == 'green') :
                            B2SColorsList[8] = 'green' 
                            TextList[8] = 'TakeWeight-Active'
                        continue
                    elif type_list[i] == 'FlowSetpoint':
                        if (status_list[i] == 'Active') : 
                           B2SColorsList[10] = 'green' 
                           TextList[10] = 'FlowSetpoint-Active' 
                        else:
                            if (B2SColorsList[10] != 'green') :
                                TextList[10] = 'FlowSetpoint-Active' 
                                B2SColorsList[10] = 'yellow' 
                        continue
                    elif (type_list[i] == 'RotateDrill'):
                        if (status_list[i] == 'Active'):
                            TextList[11] = 'RotateDrill-Active' 
                            B2SColorsList[11] = 'green' 
                        else:
                            if (B2SColorsList[11] != 'green'):
                                TextList[11] = 'RotateDrill-Active' 
                                B2SColorsList[11] = 'yellow' 
                        continue
                    elif (type_list[i] == 'TagBottom'):
                        if (status_list[i] == 'Active'):
                            TextList[0] = 'TagBottom-Active' 
                            B2SColorsList[0] = 'green' 
                        elif (status_list[i] == 'Completed') :
                            TextList[1] = 'TagBottom-Completed' 
                            B2SColorsList[1] = 'green' 
                        else:
                            if (B2SColorsList[0] != 'green'):
                                TextList[0] = 'TagBottom-Active' 
                                B2SColorsList[0] = 'yellow'
                            if (B2SColorsList[1] != 'green'):
                                TextList[1] = 'TagBottom-Completed' 
                                B2SColorsList[1] = 'yellow' 
                                
                        if (B2SColorsList[1] == 'green') :
                            B2SColorsList[0] = 'green' 
                            TextList[0] = 'TagBottom-Active'
                        continue
                    
                    if(B2SColorsList[0] == 'red'):
                        TextList[0] = 'TagBottom-Active'    
                    if (B2SColorsList[1] == 'red'):
                        TextList[1] = 'TagBottom-Completed' 
                    if (B2SColorsList[6] == 'red'):
                        TextList[6] = 'AddStand-Active' 
                    if (B2SColorsList[7] == 'red'):
                        TextList[7] = 'AddStand-Completed' 
                    if (B2SColorsList[8] == 'red'):
                        TextList[8] = 'TakeWeight-Active' 
                    if (B2SColorsList[9] == 'red'):
                        TextList[9] = 'TakeWeight-Completed' 
                    if (B2SColorsList[10] == 'red'):
                        TextList[10] = 'FlowSetpoint-Active' 
                    if (B2SColorsList[11] == 'red'):
                        TextList[11] = 'RotateDrill-Active' 
                    
                    B2SColorsList[2] = 'white' 
                    B2SColorsList[3] = 'white' 
                    B2SColorsList[4] = 'white' 
                    B2SColorsList[5] = 'white' 
                    TextList[2] = '' 
                    TextList[3] = '' 
                    TextList[4] = '' 
                    TextList[5] = ''  
                    continue
            else:                
                B2SColorsList[0] = 'white' 
                B2SColorsList[1] = 'white' 
                B2SColorsList[2] = 'white' 
                B2SColorsList[3] = 'white' 
                B2SColorsList[4] = 'white' 
                B2SColorsList[5] = 'white' 
                B2SColorsList[6] = 'white' 
                B2SColorsList[7] = 'white' 
                B2SColorsList[8] = 'white' 
                B2SColorsList[9] = 'white' 
                B2SColorsList[10] = 'white' 
                B2SColorsList[11] = 'white' 

                TextList[0] = '' 
                TextList[1] = '' 
                TextList[2] = '' 
                TextList[3] = '' 
                TextList[4] = '' 
                TextList[5] = ''   
                TextList[6] = '' 
                TextList[7] = '' 
                TextList[8] = '' 
                TextList[9] = '' 
                TextList[10] = '' 
                TextList[11] = '' 
                continue   
    
    if (vbarType == 'B2S') : 
        if (B2SColorsList[0] == 'red'):
            TextList[0] = 'CleanHole-Active'
        if (B2SColorsList[1] == 'red'):
            TextList[1] = 'CleanHole-Completed' 
        if (B2SColorsList[2] == 'red'):
            TextList[2] = 'SetBoxHeight-Active' 
        if (B2SColorsList[3] == 'red'):
            TextList[3] = 'SetBoxHeight-Completed' 
        if (B2SColorsList[4] == 'red'):
            TextList[4] = 'SetWeight-Active'
        if (B2SColorsList[5] == 'red'):
            TextList[5] = 'SetWeight-Completed' 
        if (B2SColorsList[6] == 'red'):
            TextList[6] = 'Offbottom-Active' 
        if (B2SColorsList[7] == 'red'):
            TextList[7] = 'Unweightbit-Active' 
        if (B2SColorsList[8] == 'red'):
            TextList[8] = 'Unweightbit-Completed' 
        if (B2SColorsList[9] == 'red'):
            TextList[9] = 'ClearBit-Active' 
        if (B2SColorsList[10] == 'red'):
            TextList[10] = 'ClearBit-Completed' 
        if (B2SColorsList[11] == 'red'):
            TextList[11] = 'Offbottom-Completed' 
    elif vbarType == 'S2B':
        if(B2SColorsList[0] == 'red'):
            TextList[0] = 'TagBottom-Active'    
        if (B2SColorsList[1] == 'red'):
            TextList[1] = 'TagBottom-Completed' 
        if (B2SColorsList[6] == 'red'):
            TextList[6] = 'AddStand-Active' 
        if (B2SColorsList[7] == 'red'):
            TextList[7] = 'AddStand-Completed' 
        if (B2SColorsList[8] == 'red'):
            TextList[8] = 'TakeWeight-Active' 
        if (B2SColorsList[9] == 'red'):
            TextList[9] = 'TakeWeight-Completed' 
        if (B2SColorsList[10] == 'red'):
            TextList[10] = 'FlowSetpoint-Active' 
        if (B2SColorsList[11] == 'red'):
            TextList[11] = 'RotateDrill-Active'  
        B2SColorsList[2] = 'white' 
        B2SColorsList[3] = 'white' 
        B2SColorsList[4] = 'white' 
        B2SColorsList[5] = 'white' 
        TextList[2] = '' 
        TextList[3] = '' 
        TextList[4] = '' 
        TextList[5] = ''  
    else:                
        B2SColorsList[0] = 'white' 
        B2SColorsList[1] = 'white' 
        B2SColorsList[2] = 'white' 
        B2SColorsList[3] = 'white' 
        B2SColorsList[4] = 'white' 
        B2SColorsList[5] = 'white' 
        B2SColorsList[6] = 'white' 
        B2SColorsList[7] = 'white' 
        B2SColorsList[8] = 'white' 
        B2SColorsList[9] = 'white' 
        B2SColorsList[10] = 'white' 
        B2SColorsList[11] = 'white' 

        TextList[0] = '' 
        TextList[1] = '' 
        TextList[2] = '' 
        TextList[3] = '' 
        TextList[4] = '' 
        TextList[5] = ''   
        TextList[6] = '' 
        TextList[7] = '' 
        TextList[8] = '' 
        TextList[9] = '' 
        TextList[10] = '' 
        TextList[11] = '' 

    subplot_source.data = dict(B2SColors = B2SColorsList,
                              Text = TextList,
                              B2SText = B2STextList,
                              text_x = textXList,
                              B2STextColors = B2STextColorsList,
                              B2SHideColors = B2SHideColorsList,
                              subplot_x = subplotXList,
                              subplot_y = subplotYList) 
    return
     

def update_subplot(window=None):
    global selectedVbarIndexSource
    global index2

    #index = allSource.selected.indices
    index = selectedVbarIndexSource.data['index'][0]
    #selection = require("core/util/selection")
    #indices = selection.get_indices(allSource)
    global novos_connection_dict
    global depth_ft_str
    global subplot_colors_length
    #global mainplot_source
    global novos_source
    global subplot_source
    global sub_plot

    novos_length = len(novos_connection_dict[depth_ft_str])
    subplotColorsLength = subplot_colors_length
    #allSource = mainplot_source
    novosSource = novos_source
    subplotSource = subplot_source 
    subplot = sub_plot
    m_color = subplot.background_fill_color
    subplot.background_fill_color = 'black'
    #subplot.background_fill_color = 'white'

    subplotSource.data['B2SColors'][0] = 'red' 
    subplotSource.data['B2SColors'][1] = 'red' 
    subplotSource.data['B2SColors'][2] = 'red' 
    subplotSource.data['B2SColors'][3] = 'red' 
    subplotSource.data['B2SColors'][4] = 'red' 
    subplotSource.data['B2SColors'][5] = 'red' 
    subplotSource.data['B2SColors'][6] = 'red' 
    subplotSource.data['B2SColors'][7] = 'red' 
    subplotSource.data['B2SColors'][8] = 'red' 
    subplotSource.data['B2SColors'][9] = 'red' 
    subplotSource.data['B2SColors'][10] = 'red' 
    subplotSource.data['B2SColors'][11] = 'red'
    subplotSource.change.emit() 

def remove_redunent_items(list_raw):
    list_redunent_indices = []
    list_unique = []
    i = 0
    for item in list_raw:
        if item not in list_unique:
            list_unique.append(item)
        else:
            list_redunent_indices.append(i)
        i = i + 1
    return list_redunent_indices, list_unique

def delete_redunent_items(list_indices, list_target):
    for index in list_indices:
        del list_target[index]
    return list_target

def get_all_dataset(all_connection_dict):
    global hole_depth_str
    global pre_slip_time_str 
    global post_slip_time_str
    global survey_time_str
    global backream_time_str 
    global slip_to_slip_str
    global visualization_depth_str

    all_connection_table = {}
    all_connection_table = pd.DataFrame.from_dict(all_connection_dict)
    
    hole_depth_list = list(map(float, all_connection_table[hole_depth_str]))
    hole_depth_list.sort(key=float)
    display_depth_list = list(map(float, all_connection_table[visualization_depth_str]))
    display_depth_list.sort(key=float)
    b2s_list = list(map(float, all_connection_table[pre_slip_time_str]))
    s2s_list = list(map(float, all_connection_table[slip_to_slip_str]))
    s2b_list = list(map(float, all_connection_table[post_slip_time_str]))
    survey_list = list(map(float, all_connection_table[survey_time_str]))
    ream_list = list(map(float, all_connection_table[backream_time_str]))

    hole_depth_list_redunent_indices, hole_depth_list_unique = remove_redunent_items(hole_depth_list)
    hole_depth_list = []
    hole_depth_list = hole_depth_list_unique.copy()

    depth_list_redunent_indices, depth_list_unique = remove_redunent_items(display_depth_list)
    display_depth_list = []
    display_depth_list = depth_list_unique.copy()
    b2s_list = delete_redunent_items(depth_list_redunent_indices, b2s_list)
    s2s_list = delete_redunent_items(depth_list_redunent_indices, s2s_list)
    s2b_list = delete_redunent_items(depth_list_redunent_indices, s2b_list)
    survey_list = delete_redunent_items(depth_list_redunent_indices, survey_list)
    ream_list = delete_redunent_items(depth_list_redunent_indices, ream_list)

    # could be a function
    rig_job_dict = {}
    rig_job_dict['HoleDepthRef'] = []
    rig_job_dict['HoleDepth'] = []
    rig_job_dict['B2S'] = []
    rig_job_dict['S2S'] = []
    rig_job_dict['S2B'] = []
    rig_job_dict['Survey'] = []
    rig_job_dict['BackReam'] =[]
    rig_job_dict['HoleDepthRef'] = hole_depth_list
    rig_job_dict['HoleDepth'] = display_depth_list
    rig_job_dict['B2S'] = b2s_list
    rig_job_dict['S2S'] = s2s_list
    rig_job_dict['S2B'] = s2b_list
    rig_job_dict['Survey'] = survey_list
    rig_job_dict['BackReam'] = ream_list
    
    #get_all_data_event.set()    
    return rig_job_dict, display_depth_list

def grey_out_connection_type_callback(attr, old, new):
    if new == 2:
        checkbox_group_2.disabled = True
    else:
        checkbox_group_2.disabled = False