import flask
from bokeh.models import FactorRange, Spacer
from bokeh.embed import components
from bokeh.plotting import figure, curdoc
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
import pandas as pd
from bokeh.layouts import row, column, gridplot, widgetbox
from bokeh.models import ColumnDataSource, TapTool, VBar, Rect
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
from DataVisualizationWebApp import utility as uHelper

subplot = None
subplot_source  = None
subplot_dict = None
depth_ft_str = "edr_depth_ft"

def create_sub_plot(doc):
    global subplot
    global subplot_source
    global subplot_dict 

    subplot_dict = {}
    subplot_dict['B2SText'] = ['Cleanhole - Active', 'Cleanhole - Completed', 'Setboxheight - Active', 'Setboxheight - Completed', 'Setweight - Active', 'Setweight - Completed', 'Offbottom-Active', 'Unweightbit - Active', 'Unweightbit - Completed', 'Clearbit - Active', 'Clearbit - Completed', 'Offbottom - Completed']
    subplot_dict['text_x'] = [2, 12, 22, 32, 42, 52, 2, 12, 22, 32, 42, 52]
    subplot_dict['B2SColors'] = ['white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white']
    subplot_dict['B2STextColors'] = ['black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black', 'black']
    subplot_dict['B2SHideColors'] = ['white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white']
    subplot_dict['subplot_x'] = [5, 15, 25, 35, 45, 55, 5, 15, 25, 35, 45, 55]
    subplot_dict['subplot_y'] = [10, 10, 10, 10, 10, 10, 25, 25, 25, 25, 25, 25]
    subplot_dict['B2SArrowColors'] = ['#ebebe0', '#ebebe0', '#ebebe0', '#ebebe0', '#ebebe0', '#ebebe0', '#ebebe0', '#ebebe0', '#ebebe0', '#ebebe0', '#ebebe0', '#ebebe0']
    subplot_dict['ArrowStartX'] = [10, 18, 26, 34, 42, 42, 10, 18, 26, 34, 42, 42]
    subplot_dict['ArrowEndX'] = [12, 20, 28, 36, 44, 44, 12, 20, 28, 36, 44, 44]
    subplot_dict['ArrowY'] = [20, 20, 20, 20, 20, 20, 25, 25, 25, 25, 25, 25]
    subplot_dict['arrow_end_y'] = [20, 20, 20, 20, 20, 20, 25, 25, 25, 25, 25, 25]
    subplot_dict['Text'] = ['', '', '', '','', '', '', '','', '', '', '']
    
    
    uHelper.subplot_source = ColumnDataSource(data=subplot_dict)
    doc.add_root(subplot_source)
    # 3. plot     
    uHelper.subplot = figure(x_range = [0, 60], y_range = [0, 30], \
                     plot_width=1540, plot_height= 350, \
                     toolbar_location=None, \
                     sizing_mode='scale_both')
    subplot_height = 40
    subplot_weight = 175

    subplot.rect(x='subplot_x', y='subplot_y', width=subplot_weight, height=subplot_height, color="B2SColors",
          width_units="screen", height_units="screen", source=subplot_source)
    b2s_text = Text(x='text_x', y='subplot_y', text_color="B2STextColors", text="Text", text_font_size="10pt")
    subplot.add_glyph(subplot_source, b2s_text)
    
    subplot.xaxis.visible = None
    subplot.yaxis.visible = None
    subplot.background_fill_color = "white"
    m_color_white = subplot.background_fill_color
    subplot.outline_line_color = None
    doc.add_root(subplot)
    return subplot, subplot_source, subplot_dict

m_selected_index_code = """
    selection = require("core/util/selection")
    indices = selection.get_indices(allSource)
    
    console.log('------------- javascript ----------------------')
    console.log(indices.length)

    for (i = 0; i < indices.length; i++) 
    {
        console.log('------------- enter 1st loop ----------------------')

        ind = indices[i]
        console.log(ind)
        console.log(' +++++++++++++++++++++++++++++++++++++++++ ')
        selectedVbarIndexSource.data['index'][0] = ind
        console.log(ind)
        console.log('-------------     ----------------------')
        console.log(selectedVbarIndexSource.data['index'][0])
        index2[0] = ind
        selectedVbarIndexSource.change.emit()
        break   
     }
"""



m_code = """
    selection = require("core/util/selection")
    indices = selection.get_indices(allSource)
    m_color = subplot.background_fill_color
    subplot.background_fill_color = 'white' 
	
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
    
    console.log('------------- javascript ----------------------')
    console.log(indices.length)

    for (i = 0; i < indices.length; i++) 
    {
        console.log('------------- enter 1st loop ----------------------')

        ind = indices[i]
        var holedepth = allSource.data['HoleDepth'][ind]
        console.log(ind)
        console.log('-------------------------- hole depth 1 --------------------------')
        console.log(holedepth)
        
        var holedepth = allSource.data['HoleDepthRef'][ind]
        holedepth = parseFloat(holedepth)
        var hole_depth_value = holedepth.toFixed(2)
        console.log('-------------------------- hole depth 2 --------------------------')
        console.log(hole_depth_value)
        
        vbarType = allSource.data['VBarType'][ind]
        if(vbarType === 'S2S')  
        {
            console.log('-------------------------- s2s --------------------------')
            subplotSource.data['B2SColors'][0] = 'white' 
            subplotSource.data['B2SColors'][1] = 'white' 
            subplotSource.data['B2SColors'][2] = 'white' 
            subplotSource.data['B2SColors'][3] = 'white' 
            subplotSource.data['B2SColors'][4] = 'white' 
            subplotSource.data['B2SColors'][5] = 'white' 
            subplotSource.data['B2SColors'][6] = 'white' 
            subplotSource.data['B2SColors'][7] = 'white' 
            subplotSource.data['B2SColors'][8] = 'white' 
            subplotSource.data['B2SColors'][9] = 'white' 
            subplotSource.data['B2SColors'][10] = 'white' 
            subplotSource.data['B2SColors'][11] = 'white' 

            subplotSource.data['Text'][0] = '' 
            subplotSource.data['Text'][1] = '' 
            subplotSource.data['Text'][2] = '' 
            subplotSource.data['Text'][3] = '' 
            subplotSource.data['Text'][4] = '' 
            subplotSource.data['Text'][5] = ''   
            subplotSource.data['Text'][6] = '' 
            subplotSource.data['Text'][7] = '' 
            subplotSource.data['Text'][8] = '' 
            subplotSource.data['Text'][9] = '' 
            subplotSource.data['Text'][10] = '' 
            subplotSource.data['Text'][11] = '' 
            subplotSource.change.emit()
            break    
        }



        for(i = 0; i < novosLength; i++) 
        {
            console.log('------------- enter 2nd loop ----------------------')
            console.log(novosLength)
            console.log(i)

            if (novosSource.data['edr_depth_ft'][i] === null)
                continue
            
            if (vbarType === null)
                continue

            
            var novos_edr_value = parseFloat(novosSource.data['edr_depth_ft'][i]).toFixed(2)
            if (parseFloat(hole_depth_value) < parseFloat(novos_edr_value))
            {
	            console.log('******************* break  ******************************')
	            break
            }

            if (parseFloat(novos_edr_value) === parseFloat(hole_depth_value))
            {
                console.log("---novosSource.data['edr_depth_ft'][i] == hole_depth_value---")

                if(vbarType === 'B2S') 
                {
                    console.log("------------------ B2S ---------------------")
                    console.log(novosSource.data['connection_phase'][i])

                    if (novosSource.data['connection_phase'][i] === vbarType)
                    {
                        console.log(novosSource.data['type'][i])

                        if (novosSource.data['type'][i] === null)
                            continue

                        if (novosSource.data['type'][i] === 'OffBottom')
                        {
                            
                            if (novosSource.data['status'][i] === null)
                                continue

                            console.log(novosSource.data['status'][i])

                            if (novosSource.data['status'][i] === 'Active') 
                            {
                                console.log('--------------------------B2S  6 Active --------------------------')

                                subplotSource.data['B2SColors'][6] = 'green' 
                                subplotSource.data['Text'][6] = 'Offbottom-Active' 
                            } else if (novosSource.data['status'][i] === 'Completed') 
                            {
                                console.log('-------------------------- B2S 11 Completed--------------------------')
                                subplotSource.data['B2SColors'][11] = 'green' 
                                subplotSource.data['Text'][11] = 'Offbottom-Completed' 
                            } else 
                            {
                                if (subplotSource.data['B2SColors'][6] != 'green'){
                                    subplotSource.data['B2SColors'][6] = 'yellow'
                                    subplotSource.data['Text'][6] = 'Offbottom-Active' 
                                }
                                if (subplotSource.data['B2SColors'][11] != 'green'){
                                    subplotSource.data['B2SColors'][11] = 'yellow'
                                    subplotSource.data['Text'][11] = 'Offbottom-Completed' 
                                }
                            }
                            
                            if (subplotSource.data['B2SColors'][11] === 'green'){
		                        subplotSource.data['B2SColors'][6] = 'green' 
		                        subplotSource.data['Text'][6] = 'Offbottom-Active'
	                        }
                            subplotSource.change.emit()
                            continue
                        }else if (novosSource.data['type'][i] === 'UnWeightBit')
                        {
                            if (novosSource.data['status'][i] === null)
                                continue

                            if (novosSource.data['status'][i] === 'Active') 
                            {
                                subplotSource.data['B2SColors'][7] = 'green' 
                                subplotSource.data['Text'][7] = 'Unweightbit-Active' 

                            } else if (novosSource.data['status'][i] === 'Completed') 
                            {
                                 console.log('-------------------------- B2S 8 Completed--------------------------')

                                subplotSource.data['B2SColors'][8] = 'green' 
                                subplotSource.data['Text'][8] = 'Unweightbit-Completed' 
                            } else 
                            {
                                if (subplotSource.data['B2SColors'][7] != 'green'){
                                    subplotSource.data['B2SColors'][7] = 'yellow' 
                                    subplotSource.data['Text'][7] = 'Unweightbit-Active' 
                                }
                                if (subplotSource.data['B2SColors'][8] != 'green'){
                                    subplotSource.data['B2SColors'][8] = 'yellow' 
                                    subplotSource.data['Text'][8] = 'Unweightbit-Completed' 
                                }    
                            }

                            if (subplotSource.data['B2SColors'][8] === 'green'){
		                        subplotSource.data['B2SColors'][7] = 'green' 
		                        subplotSource.data['Text'][7] = 'Unweightbit-Active'
	                        }
                            subplotSource.change.emit()
                            continue
                        }else if (novosSource.data['type'][i] === 'ClearBit')
                        {
                            if (novosSource.data['status'][i] === null)
                                continue

                            if (novosSource.data['status'][i] === 'Active') 
                            {
                                subplotSource.data['B2SColors'][9] = 'green' 
                                subplotSource.data['Text'][9] = 'ClearBit-Active' 

                            } else if (novosSource.data['status'][i] === 'Completed') 
                            {
                                console.log('-------------------------- B2S 10 Completed--------------------------')

                                subplotSource.data['B2SColors'][10] = 'green' 
                                subplotSource.data['Text'][10] = 'ClearBit-Completed' 
                            } else 
                            {
                                if (subplotSource.data['B2SColors'][9] != 'green'){
                                    subplotSource.data['Text'][9] = 'ClearBit-Active' 
                                    subplotSource.data['B2SColors'][9] = 'yellow' 
                                }
                                if (subplotSource.data['B2SColors'][10] != 'green'){
                                    subplotSource.data['Text'][10] = 'ClearBit-Completed' 
                                    subplotSource.data['B2SColors'][10] = 'yellow' 
                                } 
                            }
                            
                            if (subplotSource.data['B2SColors'][10] === 'green'){
		                        subplotSource.data['B2SColors'][9] = 'green' 
		                        subplotSource.data['Text'][9] = 'ClearBit-Active'
	                        }

                            subplotSource.change.emit()
                            continue
                        }else if (novosSource.data['type'][i] === 'CleanHole')
                        {
                            if (novosSource.data['status'][i] === null)
                                continue


                            if (novosSource.data['status'][i] === 'Active') 
                            {
                                subplotSource.data['B2SColors'][0] = 'green' 
                                subplotSource.data['Text'][0] = 'CleanHole-Active' 
                            } else if (novosSource.data['status'][i] === 'Completed') 
                            {
                                console.log('-------------------------- B2S 1 Completed--------------------------')
                                subplotSource.data['B2SColors'][1] = 'green' 
                                subplotSource.data['Text'][1] = 'CleanHole-Completed' 
                            } else 
                            {
                                if (subplotSource.data['B2SColors'][0] != 'green'){
                                    subplotSource.data['Text'][0] = 'CleanHole-Active' 
                                    subplotSource.data['B2SColors'][0] = 'yellow' 
                                }
                                if (subplotSource.data['B2SColors'][1] != 'green'){
                                    subplotSource.data['Text'][1] = 'CleanHole-Completed' 
                                    subplotSource.data['B2SColors'][1] = 'yellow' 
                                }
                            }

                            if (subplotSource.data['B2SColors'][1] === 'green'){
		                        subplotSource.data['B2SColors'][0] = 'green' 
		                        subplotSource.data['Text'][0] = 'CleanHole-Active'
	                        }

                            subplotSource.change.emit()
                            continue
                        }else if (novosSource.data['type'][i] === 'SetBoxHeight')
                        {
                            if (novosSource.data['status'][i] === null)
                                continue


                            if (novosSource.data['status'][i] === 'Active') 
                            {
                                subplotSource.data['Text'][2] = 'SetBoxHeight-Active' 
                                subplotSource.data['B2SColors'][2] = 'green' 
                            } else if (novosSource.data['status'][i] === 'Completed') 
                            {
                                console.log('-------------------------- B2S 3 Completed--------------------------')
                                subplotSource.data['Text'][3] = 'SetBoxHeight-Completed' 
                                subplotSource.data['B2SColors'][3] = 'green' 
                            } else {
                                if (subplotSource.data['B2SColors'][2] != 'green'){
                                    subplotSource.data['Text'][2] = 'SetBoxHeight-Active' 
                                    subplotSource.data['B2SColors'][2] = 'yellow' 
                                }
                                if (subplotSource.data['B2SColors'][3] != 'green'){
                                    subplotSource.data['Text'][3] = 'SetBoxHeight-Completed' 
                                    subplotSource.data['B2SColors'][3] = 'yellow' 
                                } 
                            }

                            if (subplotSource.data['B2SColors'][3] === 'green'){
		                        subplotSource.data['B2SColors'][2] = 'green' 
		                        subplotSource.data['Text'][2] = 'SetBoxHeight-Active'
	                        }
                            subplotSource.change.emit()
                            continue
                        }else if (novosSource.data['type'][i] === 'SetWeight')
                        {
                            if (novosSource.data['status'][i] === 'Active') 
                            {
                                subplotSource.data['Text'][4] = 'SetWeight-Active' 
                                subplotSource.data['B2SColors'][4] = 'green' 
                            } else if (novosSource.data['status'][i] === 'Completed') 
                            {
                                console.log('-------------------------- B2S 5 Completed--------------------------')
                                subplotSource.data['Text'][5] = 'SetWeight-Completed' 
                                subplotSource.data['B2SColors'][5] = 'green' 
                            } else {
                                if (subplotSource.data['B2SColors'][4] != 'green'){
                                    subplotSource.data['Text'][4] = 'SetWeight-Active' 
                                    subplotSource.data['B2SColors'][4] = 'yellow' 
                                }
                                if (subplotSource.data['B2SColors'][5] != 'green'){
                                    subplotSource.data['Text'][5] = 'SetWeight-Completed' 
                                    subplotSource.data['B2SColors'][5] = 'yellow' 
                                }
                            }

                            if (subplotSource.data['B2SColors'][5] === 'green'){
		                        subplotSource.data['B2SColors'][4] = 'green' 
		                        subplotSource.data['Text'][4] = 'SetWeight-Active'
	                        }

                            subplotSource.change.emit()
                            continue
                        }   
                        
                        if (subplotSource.data['B2SColors'][0] === 'red')
                        {
                            subplotSource.data['Text'][0] = 'CleanHole-Active' 
                        }
                        if (subplotSource.data['B2SColors'][1] === 'red')
                        {
                            subplotSource.data['Text'][1] = 'CleanHole-Completed' 
                        }

                        if (subplotSource.data['B2SColors'][2] === 'red')
                        {
                            subplotSource.data['Text'][2] = 'SetBoxHeight-Active' 
                        }

                        if (subplotSource.data['B2SColors'][3] === 'red')
                        {
                            subplotSource.data['Text'][3] = 'SetBoxHeight-Completed' 
                        } 

                        if (subplotSource.data['B2SColors'][4] === 'red')
                        {
                            subplotSource.data['Text'][4] = 'SetWeight-Active'
                        }

                        if (subplotSource.data['B2SColors'][5] === 'red')
                        {
                            subplotSource.data['Text'][5] = 'SetWeight-Completed' 
                        }
                        
                        if (subplotSource.data['B2SColors'][6] === 'red')
                        {
                            subplotSource.data['Text'][6] = 'Offbottom-Active' 
                        }
                        
                        if (subplotSource.data['B2SColors'][7] === 'red')
                        {
                            subplotSource.data['Text'][7] = 'Unweightbit-Active' 
                        }
              
                        if (subplotSource.data['B2SColors'][8] === 'red')
                        {
                            subplotSource.data['Text'][8] = 'Unweightbit-Completed' 
                        }  

                        if (subplotSource.data['B2SColors'][9] === 'red')
                        {
                            subplotSource.data['Text'][9] = 'ClearBit-Active' 
                        }

                        if (subplotSource.data['B2SColors'][10] === 'red')
                        {
                            subplotSource.data['Text'][10] = 'ClearBit-Completed' 
                        } 
                        
                        if (subplotSource.data['B2SColors'][11] === 'red')
                        {
                            subplotSource.data['Text'][11] = 'Offbottom-Completed' 
                        }
                        subplotSource.change.emit()
                        continue
                    }
                }else if(vbarType === 'S2B') 
                {
                    console.log('-------------------------- S2B --------------------------')
                    if (novosSource.data['connection_phase'][i] === vbarType){
                        if (novosSource.data['type'][i] === 'AddStand')
					    {
                            console.log('-------------------------- S2B AddStand--------------------------')
						    if (novosSource.data['status'][i] === 'Active') 
						    {
                                console.log('-------------------------- S2B AddStand Active --------------------------')
							    subplotSource.data['Text'][6] = 'AddStand-Active' 
							    subplotSource.data['B2SColors'][6] = 'green' 
						    } else if (novosSource.data['status'][i] === 'Completed') 
						    {
                                console.log('-------------------------- S2B AddStand Completed --------------------------')
							    subplotSource.data['Text'][7] = 'AddStand-Completed' 
							    subplotSource.data['B2SColors'][7] = 'green' 
						    } else 
						    {
							    if (subplotSource.data['B2SColors'][6] != 'green'){
								    subplotSource.data['Text'][6] = 'AddStand-Active' 
								    subplotSource.data['B2SColors'][6] = 'yellow' 
							    }
							    if (subplotSource.data['B2SColors'][7] != 'green'){
								    subplotSource.data['Text'][7] = 'AddStand-Completed' 
								    subplotSource.data['B2SColors'][7] = 'yellow' 
							    }
						    }

                            if (subplotSource.data['B2SColors'][7] === 'green'){
		                        subplotSource.data['B2SColors'][6] = 'green' 
		                        subplotSource.data['Text'][6] = 'AddStand-Active'
	                        }

						    subplotSource.change.emit()
						    continue
					    }else if (novosSource.data['type'][i] === 'TakeWeight')
                        {
                            if (novosSource.data['status'][i] === 'Active') 
                            {
                                subplotSource.data['Text'][8] = 'TakeWeight-Active' 
                                subplotSource.data['B2SColors'][8] = 'green' 
                            } else if (novosSource.data['status'][i] === 'Completed') 
                            {
                                subplotSource.data['B2SColors'][9] = 'green' 
                                subplotSource.data['Text'][9] = 'TakeWeight-Completed' 
                            } else 
                            {
                                if (subplotSource.data['B2SColors'][8] != 'green'){
                                    subplotSource.data['Text'][8] = 'TakeWeight-Active' 
                                    subplotSource.data['B2SColors'][8] = 'yellow' 
                                }
                                if (subplotSource.data['B2SColors'][9] != 'green'){
                                    subplotSource.data['Text'][9] = 'TakeWeight-Completed' 
                                    subplotSource.data['B2SColors'][9] = 'yellow' 
                                }    
                            }

                             if (subplotSource.data['B2SColors'][9] === 'green'){
		                        subplotSource.data['B2SColors'][8] = 'green' 
		                        subplotSource.data['Text'][8] = 'TakeWeight-Active'
	                        }

                            subplotSource.change.emit()
                            continue
                        }else if (novosSource.data['type'][i] === 'FlowSetpoint')
                        {
                            if (novosSource.data['status'][i] === 'Active') 
                            {
                                subplotSource.data['B2SColors'][10] = 'green' 
                                subplotSource.data['Text'][10] = 'FlowSetpoint-Active' 
                            } else 
                            {
                                if (subplotSource.data['B2SColors'][10] != 'green'){
                                    subplotSource.data['Text'][10] = 'FlowSetpoint-Active' 
                                    subplotSource.data['B2SColors'][10] = 'yellow' 
                                }                                                                
                            }
                            subplotSource.change.emit()
                            continue
                        }else if (novosSource.data['type'][i] === 'RotateDrill')
                        {
                            if (novosSource.data['status'][i] === 'Active') 
                            {
                                subplotSource.data['Text'][11] = 'RotateDrill-Active' 
                                subplotSource.data['B2SColors'][11] = 'green' 
                            } else {
                                if (subplotSource.data['B2SColors'][11] != 'green')
                                {
                                    subplotSource.data['Text'][11] = 'RotateDrill-Active' 
                                    subplotSource.data['B2SColors'][11] = 'yellow' 
                                }                                
                            }
                            subplotSource.change.emit()
                            continue
                        }else if (novosSource.data['type'][i] === 'TagBottom')
                        {
                            if (novosSource.data['status'][i] === 'Active') 
                            {
                                console.log('--------------------------TagBottom Active --------------------------')
                                subplotSource.data['Text'][0] = 'TagBottom-Active' 
                                subplotSource.data['B2SColors'][0] = 'green' 
                            } else if (novosSource.data['status'][i] === 'Completed') 
                            {
                                console.log('--------------------------TagBottom completed --------------------------')
                                subplotSource.data['Text'][1] = 'TagBottom-Completed' 
                                subplotSource.data['B2SColors'][1] = 'green' 
                            } else {
                                if (subplotSource.data['B2SColors'][0] != 'green'){
                                    subplotSource.data['Text'][0] = 'TagBottom-Active' 
                                    subplotSource.data['B2SColors'][0] = 'yellow'
                                }
                                if (subplotSource.data['B2SColors'][1] != 'green'){
                                    subplotSource.data['Text'][1] = 'TagBottom-Completed' 
                                    subplotSource.data['B2SColors'][1] = 'yellow' 
                                }                                
                            }

                            if (subplotSource.data['B2SColors'][1] === 'green'){
		                        subplotSource.data['B2SColors'][0] = 'green' 
		                        subplotSource.data['Text'][0] = 'TagBottom-Active'
	                        }

                            subplotSource.change.emit()
                            continue
                        }

                        if(subplotSource.data['B2SColors'][0] === 'red')
                        {
                            subplotSource.data['Text'][0] = 'TagBottom-Active'    
                        }

                        if (subplotSource.data['B2SColors'][1] === 'red')
                        {
                            subplotSource.data['Text'][1] = 'TagBottom-Completed' 
                        }

                        if (subplotSource.data['B2SColors'][6] === 'red')
                        {
							subplotSource.data['Text'][6] = 'AddStand-Active' 
						}
						
                        if (subplotSource.data['B2SColors'][7] === 'red')
                        {
							subplotSource.data['Text'][7] = 'AddStand-Completed' 
						}

                        if (subplotSource.data['B2SColors'][8] === 'red')
                        {
                            subplotSource.data['Text'][8] = 'TakeWeight-Active' 
                        }
                        
                        if (subplotSource.data['B2SColors'][9] === 'red')
                        {
                            subplotSource.data['Text'][9] = 'TakeWeight-Completed' 
                        }    

                        if (subplotSource.data['B2SColors'][10] === 'red')
                        {
                            subplotSource.data['Text'][10] = 'FlowSetpoint-Active' 
                        }

                        if (subplotSource.data['B2SColors'][11] === 'red')
                        {
                            subplotSource.data['Text'][11] = 'RotateDrill-Active' 
                        }

                        subplotSource.data['B2SColors'][2] = 'white' 
	                    subplotSource.data['B2SColors'][3] = 'white' 
	                    subplotSource.data['B2SColors'][4] = 'white' 
	                    subplotSource.data['B2SColors'][5] = 'white' 
                        subplotSource.data['Text'][2] = '' 
                        subplotSource.data['Text'][3] = '' 
                        subplotSource.data['Text'][4] = '' 
                        subplotSource.data['Text'][5] = ''  
                        subplotSource.change.emit()
                        continue
                    }
               }else 
               {
                    console.log('-------------------------- s2s --------------------------')
                    subplotSource.data['B2SColors'][0] = 'white' 
                    subplotSource.data['B2SColors'][1] = 'white' 
                    subplotSource.data['B2SColors'][2] = 'white' 
                    subplotSource.data['B2SColors'][3] = 'white' 
                    subplotSource.data['B2SColors'][4] = 'white' 
                    subplotSource.data['B2SColors'][5] = 'white' 
                    subplotSource.data['B2SColors'][6] = 'white' 
                    subplotSource.data['B2SColors'][7] = 'white' 
                    subplotSource.data['B2SColors'][8] = 'white' 
                    subplotSource.data['B2SColors'][9] = 'white' 
                    subplotSource.data['B2SColors'][10] = 'white' 
                    subplotSource.data['B2SColors'][11] = 'white' 

                    subplotSource.data['Text'][0] = '' 
                    subplotSource.data['Text'][1] = '' 
                    subplotSource.data['Text'][2] = '' 
                    subplotSource.data['Text'][3] = '' 
                    subplotSource.data['Text'][4] = '' 
                    subplotSource.data['Text'][5] = ''   
                    subplotSource.data['Text'][6] = '' 
                    subplotSource.data['Text'][7] = '' 
                    subplotSource.data['Text'][8] = '' 
                    subplotSource.data['Text'][9] = '' 
                    subplotSource.data['Text'][10] = '' 
                    subplotSource.data['Text'][11] = '' 
                    subplotSource.change.emit()
                    continue   
               }
            }
        }
    }
    """

def show_hide_subplot(mainplot_source, \
                      novos_source, \
                      novos_length):
    global m_code
    global subplot
    global subplot_source
    global subplot_dict


    subplot_colors_length = len(subplot_dict['B2SColors'])
    
    return CustomJS(args=dict(allSource=mainplot_source, \
                                          novosSource=novos_source, \
                                          subplotSource=subplot_source, \
                                          subplotColorsLength=subplot_colors_length, \
                                          novosLength=novos_length, \
                                          subplot=subplot \
                                         ),\
                                code=m_code)
