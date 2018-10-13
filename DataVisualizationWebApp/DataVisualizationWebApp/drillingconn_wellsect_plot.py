# Create a polynomial line graph with those arguments
import flask
from bokeh.models import FactorRange, Spacer
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
import pandas as pd
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
from DataVisualizationWebApp import utility as uHelper
from threading import Thread
import queue
import threading
from tornado import gen
from bokeh.document import without_document_lock

lock = threading.RLock()
#well_connnection_source = None

def add_misseditems(in_dict):
        if 'Driller' in in_dict:
            pass
        else:
            in_dict['Driller'] = 0
        
        if 'Hybrid' in in_dict:
            pass
        else:
            in_dict['Hybrid'] = 0

        if 'Novos' in in_dict:
            pass
        else:
            in_dict['Novos'] = 0
        return in_dict


def generate_well_selectin_colors(m_colors ,in_well_connnection_data):
    colors_list = []
    driller_list = in_well_connnection_data['Driller']
    driller_list_length = len(driller_list)
    for item in in_well_connnection_data['well_selection']:
        colors_list += m_colors[:driller_list_length]
    return colors_list


def update_well_selection_data(update_drillingconn_wellsect_event, all_connection_dict, rig = -1, job = -1):
        #TODO:
        #create a function to get selected jobs table
        #need logic to handle rig == -1 and job == -1
        rig_id_str = uHelper.rig_id_str
        job_id_str = uHelper.job_id_str
        well_selection_str = uHelper.well_selection_str 
        connection_type_str = uHelper.connection_type_str

        all_connection_table = {}
        all_connection_table = pd.DataFrame.from_dict(all_connection_dict)
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

        #1st chart
        build_query = '{} in ["Build",]'.format(well_selection_str)
        build_table = selected_job_table.query(build_query)
        build_count = build_table.groupby(connection_type_str).size().to_dict()
        vertical_query = '{} in ["Vertical",]'.format(well_selection_str)
        vertical_table = selected_job_table.query(vertical_query)
        vertical_count = vertical_table.groupby(connection_type_str).size().to_dict()
        lateral_query = '{} in ["Lateral",]'.format(well_selection_str)
        lateral_table = selected_job_table.query(lateral_query)
        lateral_count = lateral_table.groupby(connection_type_str).size().to_dict()
        
        build_count = add_misseditems(build_count)
        vertical_count = add_misseditems(vertical_count)
        lateral_count = add_misseditems(lateral_count)
        
        drilling_connection_by_well_selection = {"Build" : build_count, "Vertical" : vertical_count, "Lateral" : lateral_count }
        well_selection_list = ["Vertical", "Build", "Lateral"]
        collection_type_keys_list = list(build_count.keys())
    
        well_connnection_data = {'well_selection': well_selection_list,
                       'Driller' : [vertical_count['Driller'], build_count['Driller'], lateral_count['Driller']],
                       'Hybrid'  : [vertical_count['Hybrid'], build_count['Hybrid'], lateral_count['Hybrid']],
                       'Novos'   : [vertical_count['Novos'], build_count['Novos'], lateral_count['Novos']],
                       }

        x = [ (well_selection, collection_type) for  well_selection in well_selection_list for collection_type in collection_type_keys_list]
        counts = sum(zip(well_connnection_data['Driller'], well_connnection_data['Hybrid'], well_connnection_data['Novos']), ())
       
        m_colors = ["#b6960b", "#00ffb6", "#00ff0d", "#F2C80F"]

        well_connection_colors = generate_well_selectin_colors(m_colors, well_connnection_data)
        update_drillingconn_wellsect_event.set()
        return well_connection_colors, x, counts, well_connnection_data

#@gen.coroutine
#@without_document_lock
#def update_well_selection_chart(all_connection_dict, selected_rig, selected_job):
#    global well_connnection_source
#    well_connection_colors, x, well_connnection_counts, well_connnection_data = update_well_selection_data(all_connection_dict, selected_rig, selected_job)
#    well_connnection_source.data = dict(colors = well_connection_colors, \
#                                            x = x, \
#                                            counts = well_connnection_counts)
    
    
