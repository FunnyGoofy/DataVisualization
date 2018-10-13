# Create a polynomial line graph with those arguments
import flask
from bokeh.models import FactorRange, Spacer
from bokeh.embed import components
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
import pandas as pd
from bokeh.layouts import row, column, gridplot, widgetbox
from bokeh.models.widgets import PreText, Select, CheckboxGroup
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
import threading
from bokeh.client import session
from functools import  partial
from tornado import gen
from bokeh.document import without_document_lock
from timeit import timeit
from DataVisualizationWebApp import utility as uHelper


lock = threading.RLock()
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
main_plot = None
visualization_depth_str = "visualization_depth"


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


#def get_all_dataset(get_all_data_event, all_connection_dict):
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

def get_all_data(get_all_data_event, all_connection_dict):
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
    depth_list = list(map(float, all_connection_table[visualization_depth_str]))
    depth_list.sort(key=float)
    b2s_list = list(map(float, all_connection_table[pre_slip_time_str]))
    s2s_list = list(map(float, all_connection_table[slip_to_slip_str]))
    s2b_list = list(map(float, all_connection_table[post_slip_time_str]))
    survey_list = list(map(float, all_connection_table[survey_time_str]))
    ream_list = list(map(float, all_connection_table[backream_time_str]))

    hole_depth_list_redunent_indices, hole_depth_list_unique = remove_redunent_items(hole_depth_list)
    hole_depth_list = []
    hole_depth_list = hole_depth_list_unique.copy()

    depth_list_redunent_indices, depth_list_unique = remove_redunent_items(depth_list)
    depth_list = []
    depth_list = depth_list_unique.copy()
    b2s_list = delete_redunent_items(depth_list_redunent_indices, b2s_list)
    s2s_list = delete_redunent_items(depth_list_redunent_indices, s2s_list)
    s2b_list = delete_redunent_items(depth_list_redunent_indices, s2b_list)
    survey_list = delete_redunent_items(depth_list_redunent_indices, survey_list)
    ream_list = delete_redunent_items(depth_list_redunent_indices, ream_list)


    b2s_s2s_list = list(map(add, b2s_list, s2s_list))
    b2s_s2s_s2b_list = list(map(add, b2s_s2s_list, s2b_list))
    b2s_s2s_s2b_survey_list = list(map(add, b2s_s2s_s2b_list, survey_list))
    b2s_s2s_s2b__survey_ream_list = list(map(add, b2s_s2s_s2b_survey_list, ream_list))
        
    # could be a function
    rig_job_dict = {}
    rig_job_dict['HoleDepthRef'] = []
    rig_job_dict['HoleDepth'] = []
    rig_job_dict['VBarTop'] = []
    rig_job_dict['VBarBottom'] = []
    rig_job_dict['VBarColors'] = []
    rig_job_dict['VBarType'] = []
    rig_job_dict['HoleDepthRef'] = hole_depth_list + hole_depth_list + hole_depth_list + hole_depth_list + hole_depth_list
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
    get_all_data_event.set()    
    return rig_job_dict, depth_list

def update_checkBx_groups_dict(all_connection_dict, \
                               rig, \
                               job, \
                               checkbox_group_1_selections = [], \
                               checkbox_group_2_selections = []):
    #1. get jobs table
    #TODO: use all_connection_table
    all_connection_table = {}
    all_connection_table = pd.DataFrame.from_dict(all_connection_dict)
        
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

    #2. generate a table based on selections from 3 groups
    global well_selection_str 
    main_plot_group1_dict = {}
    group_1_table = selected_job_table
    if not checkbox_group_1_selections:
        group_1_query = '{} in ["Build", "Vertical", "Lateral"]'.format(well_selection_str)
        main_plot_group1_dict = group_1_table.query(group_1_query).to_dict('dict')
    else:
        for selected in checkbox_group_1_selections:
            if selected == 'Build':
                build_dict={}
                build_query = '{} in ["Build",]'.format(well_selection_str)
                build_dict = group_1_table.query(build_query).to_dict('dict')
                #to merge multiple dicts with same key
                if not bool(main_plot_group1_dict):
                    main_plot_group1_dict = build_dict
                else:
                    main_plot_group1_dict = uHelper.merge(main_plot_group1_dict, build_dict)
            elif selected == 'Vertical':
                vertical_dict={}
                vertical_query = '{} in ["Vertical",]'.format(well_selection_str)
                vertical_dict = group_1_table.query(vertical_query).to_dict('dict')
                if not bool(main_plot_group1_dict):
                    main_plot_group1_dict = vertical_dict
                else:
                    main_plot_group1_dict = uHelper.merge(main_plot_group1_dict, vertical_dict)
            elif selected == "Lateral":
                lateral_dict={}
                lateral_query = '{} in ["Lateral",]'.format(well_selection_str)
                lateral_dict = group_1_table.query(lateral_query).to_dict('dict')
                if not bool(main_plot_group1_dict):
                    main_plot_group1_dict = lateral_dict
                else:
                    main_plot_group1_dict = uHelper.merge(main_plot_group1_dict, lateral_dict)

        
    global connection_type_str
    main_plot_group2_dict = {}
    group_2_table = pd.DataFrame.from_dict(main_plot_group1_dict)
    if not checkbox_group_2_selections:
        group_2_query = '{} in ["Driller", "Hybrid", "Novos"]'.format(connection_type_str)
        main_plot_group2_dict = group_2_table.query(group_2_query).to_dict('dict')
    else:
        for selected in checkbox_group_2_selections:
            if selected == 'Driller':
                driller_dict = {}
                driller_query = '{} in ["Driller",]'.format(connection_type_str)
                driller_dict = group_2_table.query(driller_query).to_dict('dict')
                if not bool(main_plot_group2_dict):
                    main_plot_group2_dict = driller_dict
                else:
                    main_plot_group2_dict = uHelper.merge(main_plot_group2_dict, driller_dict)
                    
            elif selected == 'Hybrid':
                hybrid_dict = {}
                hybrid_query = '{} in ["Hybrid",]'.format(connection_type_str)
                hybrid_dict = group_2_table.query(hybrid_query).to_dict('dict')
                if not bool(main_plot_group2_dict):
                    main_plot_group2_dict = hybrid_dict
                else:
                    main_plot_group2_dict = uHelper.merge(main_plot_group2_dict, hybrid_dict)

            elif selected == "Novos":
                novos_dict = {}
                novos_query = '{} in ["Novos",]'.format(connection_type_str)
                novos_dict = group_2_table.query(novos_query).to_dict('dict')
                if not bool(main_plot_group2_dict):
                    main_plot_group2_dict = novos_dict
                else:
                    main_plot_group2_dict = uHelper.merge(main_plot_group2_dict, novos_dict)

    return main_plot_group2_dict   

def update_main_plot_dict(in_main_plot_dict, checkbox_group_3_selections = []):
    "update main dict"
    wellSel_connType_groups_table = pd.DataFrame.from_dict(in_main_plot_dict)
        
    global hole_depth_str
    global pre_slip_time_str 
    global post_slip_time_str
    global survey_time_str
    global backream_time_str 
    global slip_to_slip_str
    global visualization_depth_str

    depth_list = []
    depth_list_display = []
    b2s_list = []
    s2s_list = []
    s2b_list = []
    survey_list = []
    ream_list = []
    b2s_s2s_list = []
    b2s_s2s_s2b_list = []
    b2s_s2s_s2b_survey_list = []
    b2s_s2s_s2b__survey_ream_list = []
        
    depth_list = list(map(float, wellSel_connType_groups_table[hole_depth_str]))
    depth_list_length = len(depth_list)
    depth_list_display = list(map(float, wellSel_connType_groups_table[visualization_depth_str]))
    depth_list_display_length = len(depth_list_display)
    b2s_list = list(map(float, wellSel_connType_groups_table[pre_slip_time_str]))
    b2s_list_length = len(b2s_list)
    s2s_list = list(map(float, wellSel_connType_groups_table[slip_to_slip_str]))
    s2b_list = list(map(float, wellSel_connType_groups_table[post_slip_time_str]))
    survey_list = list(map(float, wellSel_connType_groups_table[survey_time_str]))
    ream_list = list(map(float, wellSel_connType_groups_table[backream_time_str]))
    
    # could be a function
    main_plot_dict = {}
    main_plot_dict['VBarTop'] = []
    main_plot_dict['VBarBottom'] = []
    main_plot_dict['VBarColors'] = []
    main_plot_dict['VBarType'] = []
    main_plot_dict['HoleDepth'] = []
    main_plot_dict['HoleDepthRef'] = []
        
    main_plot_list = []
    main_plot_depth_list = [] 
    main_plot_depth_list_ref = [] 
    main_plot_top_list = []
    main_plot_bottom_list = []
    main_plot_color_list = []
    main_plot_type_list = []
    if not checkbox_group_3_selections:
        b2s_s2s_list = list(map(add, b2s_list, s2s_list))
        b2s_s2s_s2b_list = list(map(add, b2s_s2s_list, s2b_list))
        b2s_s2s_s2b_survey_list = list(map(add, b2s_s2s_s2b_list, survey_list))
        b2s_s2s_s2b__survey_ream_list = list(map(add, b2s_s2s_s2b_survey_list, ream_list))

        main_plot_depth_list = depth_list_display + depth_list_display + depth_list_display + depth_list_display + depth_list_display
        main_plot_depth_list_ref = depth_list + depth_list + depth_list + depth_list + depth_list
        main_plot_top_list = b2s_list + b2s_s2s_list + b2s_s2s_s2b_list + b2s_s2s_s2b_survey_list + b2s_s2s_s2b__survey_ream_list
        main_plot_bottom_list = [ 0 for item in b2s_list] + b2s_list + b2s_s2s_list + b2s_s2s_s2b_list + b2s_s2s_s2b_survey_list
        main_plot_color_list = [ "#01B8AA" for item in b2s_list] \
                                    +  [ "#000000" for item in b2s_s2s_list] \
                                    +  [ "#FD625E" for item in b2s_s2s_s2b_list] \
                                    +  [ "#F2C80F" for item in b2s_s2s_s2b_survey_list]\
                                    +  [ "#A66999" for item in b2s_s2s_s2b__survey_ream_list]

        main_plot_type_list = ['B2S' for item in b2s_list] \
                                    + ['S2S' for item in s2s_list] \
                                    + ['S2B' for item in s2b_list] \
                                    + ['Survey' for item in survey_list] \
                                    + ['Ream' for item in ream_list] 
    else:
        for selected in checkbox_group_3_selections:
            if selected == 'B2S':
                main_plot_depth_list = main_plot_depth_list + depth_list_display
                main_plot_depth_list_ref = main_plot_depth_list_ref + depth_list
                main_plot_list = main_plot_list + b2s_list
                main_plot_type_list = main_plot_type_list + ['B2S' for item in b2s_list] 
                main_plot_color_list = main_plot_color_list  + [ "#01B8AA" for item in b2s_list]

            elif selected == 'S2S':
                main_plot_depth_list = main_plot_depth_list + depth_list_display
                main_plot_depth_list_ref = main_plot_depth_list_ref + depth_list
                main_plot_list = main_plot_list + s2s_list
                main_plot_type_list = main_plot_type_list + ['S2S' for item in s2s_list] 
                main_plot_color_list = main_plot_color_list  + [ "#000000" for item in s2s_list]

            elif selected == "S2B":
                main_plot_depth_list = main_plot_depth_list + depth_list_display
                main_plot_depth_list_ref = main_plot_depth_list_ref + depth_list
                main_plot_list = main_plot_list + s2b_list
                main_plot_type_list = main_plot_type_list + ['S2B' for item in s2b_list] 
                main_plot_color_list = main_plot_color_list  + [ "#FD625E" for item in s2b_list]

            elif selected == "Survey":
                main_plot_depth_list = main_plot_depth_list + depth_list_display
                main_plot_depth_list_ref = main_plot_depth_list_ref + depth_list
                main_plot_list = main_plot_list + survey_list
                main_plot_type_list = main_plot_type_list + ['Survey' for item in survey_list] 
                main_plot_color_list = main_plot_color_list  + [ "#F2C80F" for item in survey_list]

            elif selected == "BackReam":
                main_plot_depth_list = main_plot_depth_list + depth_list_display
                main_plot_depth_list_ref = main_plot_depth_list_ref + depth_list
                main_plot_list = main_plot_list + ream_list
                main_plot_type_list = main_plot_type_list + ['BackReam' for item in ream_list] 
                main_plot_color_list = main_plot_color_list  + [ "#A66999" for item in ream_list]
                
        # generate top&bottom values  
        section_length = len(depth_list_display)
        section_length_ref = len(depth_list)
        main_plot_top_list = main_plot_list
        connectionPhase_selections = int(len(main_plot_list) / len(depth_list_display))
        connectionPhase_selections_ref = int(len(main_plot_list) / len(depth_list))
        for i in range(0, connectionPhase_selections):
            if i > 0 :
                prev_section_head = (i - 1) * section_length
                current_section_head = i * section_length
                temp_list = [(main_plot_top_list[prev_section_head + k] + main_plot_list[current_section_head + k]) for k in range(0, section_length)]
                main_plot_top_list = main_plot_top_list + temp_list
            else:
                main_plot_top_list = [main_plot_list[k] for k in range(0, section_length)]
                    
        bottom_list_slice_upbound = (connectionPhase_selections - 1) * section_length
        main_plot_bottom_list = [ 0 for k in range(0, section_length)]
        if (connectionPhase_selections - 1) > 0:
            main_plot_bottom_list = main_plot_bottom_list + main_plot_top_list[:bottom_list_slice_upbound]
        else:
            main_plot_bottom_list = main_plot_bottom_list
        print("check the length of slice")
        print(len(main_plot_top_list))
        print(len(main_plot_bottom_list))

    main_plot_dict['HoleDepthRef'] = main_plot_depth_list_ref
    main_plot_dict['HoleDepth'] = main_plot_depth_list
    main_plot_dict['VBarTop'] = main_plot_top_list
    main_plot_dict['VBarBottom'] = main_plot_bottom_list
    main_plot_dict['VBarColors'] = main_plot_color_list
    main_plot_dict['VBarType'] = main_plot_type_list
    
    main_plot_depth_list_length = len(main_plot_depth_list)
    main_plot_top_list_length = len(main_plot_top_list)
    return main_plot_dict, depth_list_display, depth_list

def updateSourceData(in_mainplot_data_type, in_mainplot_data, depth_list_latest):
    new_list = []

    in_mainplot_data_length = len(in_mainplot_data[in_mainplot_data_type])
    i = 0
    for item in depth_list_latest: 
        if item != '-1':
            if i >= in_mainplot_data_length:
                if in_mainplot_data_type == 'VBarColors':
                    new_list.append('white')
                else:
                    new_list.append('')
            else:  
                var = in_mainplot_data[in_mainplot_data_type][i]
                new_list.append(var)
                i = i + 1
        else:
            if in_mainplot_data_type == 'VBarColors':
                new_list.append('white')
            else:
                new_list.append('')
   
    return new_list
 

def update_holeDepth_list(mainplot_data, mainplot_data_all, depth_list, depth_ref_list):
    mainplot_data_length = len(mainplot_data['HoleDepth'])
    mainplot_data_all_length = len(mainplot_data_all['HoleDepth'])
    mainplot_data_holeDepth_list = []
    mainplot_data_holeDepthRef_list = []

    depth_list = depth_list.copy()
    depth_ref_list = depth_ref_list.copy()
    depth_list_length = len(depth_list)
    depth_ref_list_length = len(depth_ref_list)
    #is_depth_list_empty = True if (len(depth_list) == 0) else False
    #if is_depth_list_empty:
    #    selected_conn_phase_len = 5
    #    depth_list = mainplot_data_all['HoleDepth'][:selected_conn_phase_len]
    for item in mainplot_data_all['HoleDepth']:
        if item in depth_list:
            mainplot_data_holeDepth_list.append(item)
            ind = depth_list.index(item)
            mainplot_data_holeDepthRef_list.append(depth_ref_list[ind])
        else:
            mainplot_data_holeDepth_list.append('-1')
            mainplot_data_holeDepthRef_list.append('-1')
    
    return mainplot_data_holeDepth_list, mainplot_data_holeDepthRef_list   

@gen.coroutine    
def update_main_plot_source(main_plot, main_plot_dict, depth_list, depth_ref_list, mainplot_data_all, mainplot_source):
    depth_list_latest = []
    VBarTop_list = []
    VBarBottom_list = [] 
    VBarColors_list =  []
    VBarType_list = []

    depth_list_latest, uHelper.depth_ref_list = update_holeDepth_list(main_plot_dict, mainplot_data_all, depth_list, depth_ref_list)
    VBarTop_list = updateSourceData('VBarTop', main_plot_dict, depth_list_latest)
    VBarBottom_list = updateSourceData('VBarBottom', main_plot_dict, depth_list_latest)
    VBarColors_list = updateSourceData('VBarColors', main_plot_dict, depth_list_latest)
    VBarType_list = updateSourceData('VBarType', main_plot_dict, depth_list_latest)

    is_depth_list_empty = True if (len(depth_list) == 0) else False
    if is_depth_list_empty:
        selected_conn_phase_len = 5
        depth_list_latest[0] =  mainplot_data_all['HoleDepth'][0]
        uHelper.depth_ref_list[0] = mainplot_data_all['HoleDepthRef'][0]
        VBarTop_list[0] = 0
        VBarBottom_list[0] = 0 
        VBarColors_list[:selected_conn_phase_len] = ["#01B8AA", "#000000", "#FD625E", "#F2C80F", "#A66999"]
        VBarType_list[:selected_conn_phase_len] = ['B2S', 'S2S', 'S2B', 'Survey', 'BackReam']    
        main_plot.x_range.factors = ['']
    else:
        depth_list_latest, uHelper.depth_ref_list = update_holeDepth_list(main_plot_dict, mainplot_data_all, depth_list, depth_ref_list)
        VBarTop_list = updateSourceData('VBarTop', main_plot_dict, depth_list_latest)
        VBarBottom_list = updateSourceData('VBarBottom', main_plot_dict, depth_list_latest)
        VBarColors_list = updateSourceData('VBarColors', main_plot_dict, depth_list_latest)
        VBarType_list = updateSourceData('VBarType', main_plot_dict, depth_list_latest)
        depth_list_length = len(depth_list)
        main_plot.x_range.factors = depth_list[:]
    
    #dur = []
    #for index, vbartpye in enumerate(VBarType_list):
    #    top_num = 0.0
    #    bottom_num = 0.0
    #    if VBarTop_list[index] == '':
    #        top_num = 0.0
    #    else:
    #        top_num = float(VBarTop_list[index])
    #
    #    if VBarBottom_list[index] == '':
    #        bottom_num = 0.0
    #    else:
    #        bottom_num = float(VBarBottom_list[index])
    #    dur.append(str(top_num - bottom_num))

    mainplot_source.data = dict(HoleDepthRef = uHelper.depth_ref_list.copy(), \
                            HoleDepth = depth_list_latest.copy(), \
                            VBarTop = VBarTop_list.copy(), \
                            VBarBottom = VBarBottom_list.copy(), \
                            VBarColors = VBarColors_list.copy(), \
                            VBarType = VBarType_list.copy())

    #for index, vbartpye in enumerate(VBarType_list):
    #    main_plot.add_tools(HoverTool(tooltips=[('Depth:', '@HoleDepthRef{%0.2f}'),
    #                                            ('Connection type:', '@VBarType')]))


@without_document_lock
def update_main_plot_chart( doc, \
                            update_main_plot_event, \
                            mainplot_source, \
                            main_plot, \
                            mainplot_data_all, \
                            checkbox_group_1_selections, \
                            checkbox_group_2_selections,\
                            checkbox_group_3_selections, \
                            all_connection_dict,\
                            rig, \
                            job, \
                            from_comboBx_group):
    update_main_plot_event.wait()        
    
    #main_plot_dict = {}
    depth_list = []
   
    if from_comboBx_group == True:
        uHelper.main_plot_dict = update_checkBx_groups_dict(all_connection_dict, \
                                                    rig, \
                                                    job, \
                                                    checkbox_group_1_selections, \
                                                    checkbox_group_2_selections)
        uHelper.main_plot_dict, depth_list, depth_ref_list = update_main_plot_dict(uHelper.main_plot_dict, checkbox_group_3_selections)
    else:
        uHelper.main_plot_dict = update_checkBx_groups_dict(all_connection_dict, \
                                                    rig, \
                                                    job)
        uHelper.main_plot_dict, depth_list, depth_ref_list  = update_main_plot_dict(uHelper.main_plot_dict)
        
    depth_list = ["{0:.2f}".format(item) for item in depth_list]
    #depth_list = [str(item) for item in depth_list]
    depth_ref_list = [str(item) for item in depth_ref_list]
    #depth_list = [str(x) for x in depth_list]
    doc.add_next_tick_callback(partial(update_main_plot_source, \
                                       main_plot = main_plot,  \
                                       main_plot_dict = uHelper.main_plot_dict, \
                                       depth_list = depth_list, \
                                       depth_ref_list = depth_ref_list, \
                                       mainplot_data_all = mainplot_data_all, \
                                       mainplot_source = mainplot_source))

    
