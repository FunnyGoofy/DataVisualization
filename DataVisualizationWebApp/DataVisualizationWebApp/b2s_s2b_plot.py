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


connection_phase_str = "connection_phase"
type_str = "type"
status_str = "status"
rig_id_str = "rig_id"
job_id_str = 'job_id'

offbottom_pie_source = None
clearBit_pie_source = None
setWeight_pie_source = None
setBoxHeight_pie_source = None
unWeightBit_pie_source = None
cleanHole_pie_source = None
addStand_pie_source = None
takeWeight_pie_source = None
flowSetpoint_pie_source = None
rotateDrill_pie_source = None
tagBottom_pie_source = None

def calculate_percentage(in_dict):
    in_list = in_dict.values()
    total = sum(in_list)
    percents = []
    if total == 0:
        percents = [(value * 0.0) for value in in_list]
        percents = [int(round(value*100)) for value in percents]
    else: 
        percents = [(value * 1.0 / total) for value in in_list]
        percents = [int(round(value*100)) for value in percents]
    i = 0
    for key in in_dict.keys():
        in_dict[key] = percents[i]
        i = i + 1
    return in_dict 

def add_misseditems(in_dict):
        if 'Canceled' in in_dict:
            pass
        else:
            in_dict['Canceled'] = 0
        
        if 'Completed' in in_dict:
            pass
        else:
            in_dict['Completed'] = 0

        if 'Exception' in in_dict:
            pass
        else:
            in_dict['Exception'] = 0
        if 'Failed' in in_dict:
            pass
        else:
            in_dict['Failed'] = 0
        return in_dict



def update_b2s_s2b_data(update_b2s_s2b_event, novos_connection_table, selected_rig, selected_job):
    selected_rig_table = uHelper.get_novos_job_table(novos_connection_table, selected_rig, selected_job)
    b2s_s2b_status = ["Canceled", "Completed", "Exception", "Failed"]
    b2s_s2b_colors = ["#01B8AA", "#000000", "#FD625E", "#F2C80F"]
    status_query = '{} in ["Canceled", "Completed", "Exception", "Failed"]'.format(status_str)
   
    #####  b2s
    # pie offbottom
    connection_phase_query = '{} in ["B2S",]'.format(connection_phase_str)
    type_query = '{} in ["OffBottom",]'.format(type_str)
    offBottom_table = selected_rig_table.query(connection_phase_query).query(type_query).query(status_query)
    offBottom_pie_dict = offBottom_table.groupby(status_str).size().to_dict()

    # pie unWeightBit
    connection_phase_query = '{} in ["B2S",]'.format(connection_phase_str)
    type_query = '{} in ["UnWeightBit",]'.format(type_str)
    unWeightBit_table = selected_rig_table.query(connection_phase_query).query(type_query).query(status_query)
    unWeightBit_pie_dict = unWeightBit_table.groupby(status_str).size().to_dict()

    # pie clearbit
    connection_phase_query = '{} in ["B2S",]'.format(connection_phase_str)
    type_query = '{} in ["ClearBit",]'.format(type_str)
    clearBit_table = selected_rig_table.query(connection_phase_query).query(type_query).query(status_query)
    clearBit_pie_dict = clearBit_table.groupby(status_str).size().to_dict()

    # pie cleanHole
    connection_phase_query = '{} in ["B2S",]'.format(connection_phase_str)
    type_query = '{} in ["CleanHole",]'.format(type_str)
    cleanHole_table = selected_rig_table.query(connection_phase_query).query(type_query).query(status_query)
    cleanHole_pie_dict = cleanHole_table.groupby(status_str).size().to_dict()

    # pie setBoxHeight
    connection_phase_query = '{} in ["B2S",]'.format(connection_phase_str)
    type_query = '{} in ["SetBoxHeight",]'.format(type_str)
    setBoxHeight_table = selected_rig_table.query(connection_phase_query).query(type_query).query(status_query)
    setBoxHeight_pie_dict = setBoxHeight_table.groupby(status_str).size().to_dict()

    # pie setWeight
    connection_phase_query = '{} in ["B2S",]'.format(connection_phase_str)
    type_query = '{} in ["SetWeight",]'.format(type_str)
    setWeight_table = selected_rig_table.query(connection_phase_query).query(type_query).query(status_query)
    setWeight_pie_dict = setWeight_table.groupby(status_str).size().to_dict()
    
    offBottom_pie_dict = add_misseditems(offBottom_pie_dict)
    unWeightBit_pie_dict = add_misseditems(unWeightBit_pie_dict)
    clearBit_pie_dict = add_misseditems(clearBit_pie_dict)
    cleanHole_pie_dict = add_misseditems(cleanHole_pie_dict)
    setBoxHeight_pie_dict = add_misseditems(setBoxHeight_pie_dict)
    setWeight_pie_dict = add_misseditems(setWeight_pie_dict)

    # percent
    offBottom_pie_dict = calculate_percentage(offBottom_pie_dict)
    unWeightBit_pie_dict = calculate_percentage(unWeightBit_pie_dict)
    clearBit_pie_dict = calculate_percentage(clearBit_pie_dict)
    cleanHole_pie_dict = calculate_percentage(cleanHole_pie_dict)
    setBoxHeight_pie_dict = calculate_percentage(setBoxHeight_pie_dict)
    setWeight_pie_dict = calculate_percentage(setWeight_pie_dict)

    b2s_canceled_list = [offBottom_pie_dict["Canceled"], unWeightBit_pie_dict["Canceled"], clearBit_pie_dict["Canceled"], cleanHole_pie_dict["Canceled"], setBoxHeight_pie_dict["Canceled"], setWeight_pie_dict["Canceled"]] 
    b2s_completed_list = [offBottom_pie_dict["Completed"], unWeightBit_pie_dict["Completed"], clearBit_pie_dict["Completed"], cleanHole_pie_dict["Completed"], setBoxHeight_pie_dict["Completed"], setWeight_pie_dict["Completed"]] 
    b2s_exception_list = [offBottom_pie_dict["Exception"], unWeightBit_pie_dict["Exception"], clearBit_pie_dict["Exception"], cleanHole_pie_dict["Exception"], setBoxHeight_pie_dict["Exception"], setWeight_pie_dict["Exception"]] 
    b2s_failed_list = [offBottom_pie_dict["Failed"], unWeightBit_pie_dict["Failed"], clearBit_pie_dict["Failed"], cleanHole_pie_dict["Failed"], setBoxHeight_pie_dict["Failed"], setWeight_pie_dict["Failed"]]
   
    
    #######  s2b
    # pie addStand
    connection_phase_query = '{} in ["S2B",]'.format(connection_phase_str)
    type_query = '{} in ["AddStand",]'.format(type_str)
    status_query = '{} in ["Canceled", "Completed", "Exception", "Failed"]'.format(status_str)
    addStand_table = selected_rig_table.query(connection_phase_query).query(type_query).query(status_query)
    addStand_pie_dict = addStand_table.groupby(status_str).size().to_dict()

    # pie takeWeight
    connection_phase_query = '{} in ["S2B",]'.format(connection_phase_str)
    type_query = '{} in ["TakeWeight",]'.format(type_str)
    status_query = '{} in ["Canceled", "Completed", "Exception", "Failed"]'.format(status_str)
    takeWeight_table = selected_rig_table.query(connection_phase_query).query(type_query).query(status_query)
    takeWeight_pie_dict = takeWeight_table.groupby(status_str).size().to_dict()

    # pie flowSetpoint
    connection_phase_query = '{} in ["S2B",]'.format(connection_phase_str)
    type_query = '{} in ["FlowSetpoint",]'.format(type_str)
    status_query = '{} in ["Canceled", "Completed", "Exception", "Failed"]'.format(status_str)
    flowSetpoint_table = selected_rig_table.query(connection_phase_query).query(type_query).query(status_query)
    flowSetpoint_pie_dict = flowSetpoint_table.groupby(status_str).size().to_dict()

    # pie rotateDrill
    connection_phase_query = '{} in ["S2B",]'.format(connection_phase_str)
    type_query = '{} in ["RotateDrill",]'.format(type_str)
    status_query = '{} in ["Canceled", "Completed", "Exception", "Failed"]'.format(status_str)
    rotateDrill_table = selected_rig_table.query(connection_phase_query).query(type_query).query(status_query)
    rotateDrill_pie_dict = rotateDrill_table.groupby(status_str).size().to_dict()

    # pie tagBottom
    connection_phase_query = '{} in ["S2B",]'.format(connection_phase_str)
    type_query = '{} in ["TagBottom",]'.format(type_str)
    status_query = '{} in ["Canceled", "Completed", "Exception", "Failed"]'.format(status_str)
    tagBottom_table = selected_rig_table.query(connection_phase_query).query(type_query).query(status_query)
    tagBottom_pie_dict = tagBottom_table.groupby(status_str).size().to_dict()

    addStand_pie_dict = add_misseditems(addStand_pie_dict)
    takeWeight_pie_dict = add_misseditems(takeWeight_pie_dict)
    flowSetpoint_pie_dict = add_misseditems(flowSetpoint_pie_dict)
    rotateDrill_pie_dict = add_misseditems(rotateDrill_pie_dict)
    tagBottom_pie_dict = add_misseditems(tagBottom_pie_dict)

    #percent 
    addStand_pie_dict = calculate_percentage(addStand_pie_dict)
    takeWeight_pie_dict = calculate_percentage(takeWeight_pie_dict)
    flowSetpoint_pie_dict = calculate_percentage(flowSetpoint_pie_dict)
    rotateDrill_pie_dict = calculate_percentage(rotateDrill_pie_dict)
    tagBottom_pie_dict = calculate_percentage(tagBottom_pie_dict)

    s2b_canceled_list = [addStand_pie_dict["Canceled"], takeWeight_pie_dict["Canceled"], flowSetpoint_pie_dict["Canceled"], rotateDrill_pie_dict["Canceled"], tagBottom_pie_dict["Canceled"]] 
    s2b_completed_list = [addStand_pie_dict["Completed"], takeWeight_pie_dict["Completed"], flowSetpoint_pie_dict["Completed"], rotateDrill_pie_dict["Completed"], tagBottom_pie_dict["Completed"]] 
    s2b_exception_list = [addStand_pie_dict["Exception"], takeWeight_pie_dict["Exception"], flowSetpoint_pie_dict["Exception"], rotateDrill_pie_dict["Exception"], tagBottom_pie_dict["Exception"]] 
    s2b_failed_list =  [addStand_pie_dict["Failed"], takeWeight_pie_dict["Failed"], flowSetpoint_pie_dict["Failed"], rotateDrill_pie_dict["Failed"], tagBottom_pie_dict["Failed"]]
    
    update_b2s_s2b_event.set()
    return b2s_canceled_list, b2s_completed_list, b2s_exception_list,b2s_failed_list, s2b_canceled_list, s2b_completed_list, s2b_exception_list, s2b_failed_list
