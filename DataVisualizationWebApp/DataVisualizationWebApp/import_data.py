import pypyodbc
import threading
import queue
import pandas as pd
from bokeh.models import ColumnDataSource
from DataVisualizationWebApp import utility as uHelper
import timeit
import time
import asyncio
from functools import lru_cache

rig_id_str = "rig_id"
job_id_str = 'job_id'
crew_shift_str = 'crew_shift'
depth_ft_str = "depth_ft"

def remove_empty_depth(in_dict):
        out_dict = {}
        out_dict.update([(key, in_dict[key]) for key in in_dict.keys() if ((str(in_dict[depth_ft_str]) != ''))])
    
        return out_dict

#@lru_cache(maxsize=None)
def setup_db_connection():
    uHelper.connection = pypyodbc.connect('Driver={SQL Server};'
                            'Server=SQLWDBP04;'
                            'Database=NOVOS;'
                            'uid=PDPerformance;'
                            'pwd=pTepJ1281S9kpC')
    return uHelper.connection

#@lru_cache(maxsize=None)
#async def retrieve_data(connection, rig_id = -1):
def retrieve_data(rig_id = -1):
    #while True: 
    uHelper.connection = pypyodbc.connect('Driver={SQL Server};'
                            'Server=SQLWDBP04;'
                            'Database=NOVOS;'
                            'uid=PDPerformance;'
                            'pwd=pTepJ1281S9kpC')
    connection = uHelper.connection
    cursor_1 = connection.cursor()
    cursor_2 = connection.cursor()
    cursor_3 = connection.cursor()
    print ("-------------------- 1 ---------------------------")
    start_time_retrieve_1 = timeit.default_timer()
        
    rigs_list = []
    select_all_connection = None
    if rig_id == -1:
        select_all_rigs = ("SELECT rig_id FROM all_connection")
        cursor_1.execute(select_all_rigs) 
        rigs = cursor_1.fetchall()
        rigs_set = set()
        for row in rigs:
            rigs_set.add(row[0])
        rigs_list = list(sorted(rigs_set))
        select_all_connection = ("SELECT * FROM all_connection WHERE rig_id = %d;" % (rigs_list[0])) 
    else:
        select_all_connection = ("SELECT * FROM all_connection WHERE rig_id = %d;" % (rig_id)) 
     
    cursor_2.execute(select_all_connection) 
    desc = cursor_2.description
    column_names = [col[0] for col in desc]
    all_connection_dict = [dict(zip(column_names, row)) 
            for row in cursor_2.fetchall()]
    all_connection_dict = {k: [dic[k] for dic in all_connection_dict] for k in all_connection_dict[0]}    
    all_connection_table = pd.DataFrame.from_dict(all_connection_dict)
    #print(all_connection_table)
    #print(all_connection_table['all_post_slip_time'])
    print(timeit.default_timer() - start_time_retrieve_1)

    print ("-------------------- 2 ---------------------------")
    start_time_retrieve_2 = timeit.default_timer()
    novos_connection_dict = None
    novos_connection_table = None
    novos_source = None
    select_novos_connection = None
    if rig_id == -1:
        select_novos_connection = ("SELECT epoch, job_id, rig_id, date_time, status, type, depth_m, \
                                            depth_ft, visualization_depth, edr_depth_ft, is_connection, \
                                            connection_phase,connection_type, novos_b2s, novos_s2b, survey, backream \
                                            FROM novos_connection WHERE rig_id = %d;" % (rigs_list[0])) 
    else:
        select_novos_connection = ("SELECT epoch, job_id, rig_id, date_time, status, type, depth_m, \
                                            depth_ft, visualization_depth, edr_depth_ft, is_connection, \
                                            connection_phase,connection_type, novos_b2s, novos_s2b, survey, backream \
                                            FROM novos_connection WHERE rig_id = %d;" % (rig_id)) 

    cursor_3.execute(select_novos_connection)
    if cursor_3.rowcount != 0:
        desc = cursor_3.description
        column_names = [col[0] for col in desc]
        novos_connection_dict = [dict(zip(column_names, row)) 
                for row in cursor_3.fetchall()]
        print(timeit.default_timer() - start_time_retrieve_2)

        print ("---------------------- 3 -------------------------")
        start_time_retrieve_3 = timeit.default_timer()
        #uHelper.connection.close()
        #all_connection_dict = {k: [dic[k] for dic in all_connection_dict] for k in all_connection_dict[0]}
        #novos_connection_dict = {k: [dic[k] for dic in novos_connection_dict] for k in novos_connection_dict[0]}

        #def remove_empty_depth(in_dict):
        #    out_dict = {}
        #    out_dict.update([(key, in_dict[key]) for key in in_dict.keys() if ((in_dict[depth_ft_str] != ''))])
        #    return out_dict

        #novos_connection_dict_without_emptydepth = remove_empty_depth(novos_connection_dict)
        novos_connection_table = pd.DataFrame.from_dict(novos_connection_dict)
        novos_connection_dict = {}
        novos_connection_dict["epoch"] = novos_connection_table["epoch"] 
        novos_connection_dict["job_id"] = novos_connection_table["job_id"]
        novos_connection_dict["rig_id"] = novos_connection_table["rig_id"]
        novos_connection_dict["date_time"] = novos_connection_table["date_time"]
        novos_connection_dict["status"] = novos_connection_table["status"]
        novos_connection_dict["type"] = novos_connection_table["type"]
        novos_connection_dict["depth_m"] = novos_connection_table["depth_m"]
        novos_connection_dict["depth_ft"] = novos_connection_table["depth_ft"]
        novos_connection_dict["visualization_depth"] = novos_connection_table["visualization_depth"]
        novos_connection_dict["edr_depth_ft"] = novos_connection_table["edr_depth_ft"]
        novos_connection_dict["is_connection"]  = novos_connection_table["is_connection"]
        novos_connection_dict["connection_phase"] = novos_connection_table["connection_phase"]
        novos_connection_dict["connection_type"]  = novos_connection_table["connection_type"]
        novos_connection_dict["novos_b2s"] = novos_connection_table["novos_b2s"]
        novos_connection_dict["novos_s2b"] = novos_connection_table["novos_s2b"]
        novos_connection_dict["survey"]  = novos_connection_table["survey"]
        novos_connection_dict["backream"] = novos_connection_table["backream"]


        #novos_source = ColumnDataSource(data=novos_connection_dict)
        print(timeit.default_timer() - start_time_retrieve_3)
    connection.close()
    jobs_list = all_connection_table[uHelper.job_id_str].unique().tolist()
    crewshift_list = all_connection_table[uHelper.crew_shift_str].unique().tolist()

    uHelper.all_connection_dict, uHelper.novos_connection_dict, \
    uHelper.all_connection_table, uHelper.novos_connection_table, \
    uHelper.novos_source, uHelper.rigs_list, \
    uHelper.jobs_list, uHelper.crewshift_list = all_connection_dict, \
                                                novos_connection_dict, \
                                                all_connection_table, \
                                                novos_connection_table, \
                                                novos_source, \
                                                rigs_list, \
                                                jobs_list, \
                                                crewshift_list
    cursor_1.close()
    cursor_2.close()
    cursor_3.close()
    #await asyncio.sleep(500)



#Production Server name: SQLWDBP04 
# SQLWDBQ01
@lru_cache(maxsize = None)
def import_all_data():
    connection = pypyodbc.connect('Driver={SQL Server};'
                            'Server=SQLWDBP04;'
                            'Database=NOVOS;'
                            'uid=PDPerformance;'
                            'pwd=pTepJ1281S9kpC')
    print ("-------------------- 1 ---------------------------")
    start_time_retrieve_1 = timeit.default_timer()
    cursor = connection.cursor()
    select_all_connection = ("SELECT * FROM all_connection") 
    #select_all_connection = ("SELECT * FROM all_connection_test Where rig_id in ('566','867','572') ") 
    cursor.execute(select_all_connection) 
    desc = cursor.description
    column_names = [col[0] for col in desc]
    all_connection_dict = [dict(zip(column_names, row)) 
            for row in cursor.fetchall()]

    print(timeit.default_timer() - start_time_retrieve_1)
    print ("-------------------- 1 ---------------------------")
    start_time_retrieve_1 = timeit.default_timer()
    select_novos_connection = ("SELECT * FROM novos_connection") 
    #select_novos_connection = ("SELECT * FROM novos_connection_test Where rig_id in ('566','867','572') ") 
    cursor.execute(select_novos_connection) 
    desc = cursor.description
    column_names = [col[0] for col in desc]
    novos_connection_dict = [dict(zip(column_names, row)) 
            for row in cursor.fetchall()]
    
    print(timeit.default_timer() - start_time_retrieve_1)
    connection.close()
    all_connection_dict = {k: [dic[k] for dic in all_connection_dict] for k in all_connection_dict[0]}
    novos_connection_dict = {k: [dic[k] for dic in novos_connection_dict] for k in novos_connection_dict[0]}
    all_connection_table = pd.DataFrame.from_dict(all_connection_dict)
    novos_connection_table = pd.DataFrame.from_dict(novos_connection_dict)

    #def remove_empty_depth(in_dict):
    #    out_dict = {}
    #    out_dict.update([(key, in_dict[key]) for key in in_dict.keys() if ((in_dict[depth_ft_str] != ''))])
    #    return out_dict

    novos_connection_dict_without_emptydepth = remove_empty_depth(novos_connection_dict)
    novos_source = ColumnDataSource(data=novos_connection_dict_without_emptydepth)

    rigs_list = all_connection_table[rig_id_str].unique().tolist()
    jobs_list = all_connection_table[job_id_str].unique().tolist()
    crewshift_list = all_connection_table[crew_shift_str].unique().tolist()
    return all_connection_dict, novos_connection_dict, all_connection_table, novos_connection_table, novos_source, rigs_list, jobs_list, crewshift_list


#def import_records(db_records_rig_event, rig_id = -1):
#    if rig_id == -1:
#        return 
#
#    connection = pypyodbc.connect('Driver={SQL Server};'
#                            'Server=SQLWDBP04;'
#                            'Database=NOVOS;'
#                            'uid=PDPerformance;'
#                            'pwd=pTepJ1281S9kpC')
#    cursor = connection.cursor()
#    select_all_connection = ("SELECT * FROM all_connection Where rig_id=?", rig_id) 
#    cursor.execute(select_all_connection) 
#    desc = cursor.description
#    column_names = [col[0] for col in desc]
#    connection_dict = [dict(zip(column_names, row)) 
#            for row in cursor.fetchall()]
#
#    select_novos_connection = ("SELECT * FROM novos_connection Where rig_id=?", rig_id) 
#    cursor.execute(select_novos_connection) 
#    desc = cursor.description
#    column_names = [col[0] for col in desc]
#    novos_connection_dict = [dict(zip(column_names, row)) 
#            for row in cursor.fetchall()]
#    connection.close()
#    connection_dict = {k: [dic[k] for dic in connection_dict] for k in connection_dict[0]}
#    novos_connection_dict = {k: [dic[k] for dic in novos_connection_dict] for k in novos_connection_dict[0]}
#    connection_table = pd.DataFrame.from_dict(connection_dict)
#    novos_connection_table = pd.DataFrame.from_dict(novos_connection_dict)
#    
#    novos_connection_dict_without_emptydepth = remove_empty_depth(novos_connection_dict)
#    novos_source = ColumnDataSource(data=novos_connection_dict_without_emptydepth)
#
#    rigs_list = connection_table[rig_id_str].unique().tolist()
#    jobs_list = connection_table[job_id_str].unique().tolist()
#    crewshift_list = connection_table[crew_shift_str].unique().tolist()
#    
#    db_records_rig_event.set()
#    
#    return connection_dict, novos_connection_dict, connection_table, novos_connection_table, novos_source, rigs_list, jobs_list, crewshift_list

