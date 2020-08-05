from bokeh.models import HoverTool, DataRange1d, LinearAxis, CustomJS
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.models.callbacks import CustomJS

import numpy as np
from .tools import heightMap, getHeightmapTicks, mapHeight, applyCloudColourState, applyVisColourState

set_w, set_h = 800, 100

def setLook(plot):
    # Style variables "sv"
    sv_maincolour = '#888888'
    sv_boldcolour = '#bbbbbb'
    sv_font = 'arial'

    plot.toolbar.active_drag = None
    plot.toolbar.active_scroll = None

    date_tick_format = " %d/%H%MZ"
    plot.xaxis.formatter = DatetimeTickFormatter(
        minutes=[date_tick_format],
        hourmin=[date_tick_format],
        hours=[date_tick_format],
        days=[date_tick_format],
    )
    plot.xaxis.ticker.desired_num_ticks = 10
    plot.xaxis.major_label_orientation = 3.1415/4

    plot.xgrid.visible = False
    plot.grid.grid_line_color = sv_maincolour
    plot.grid.grid_line_alpha = 0.2

    plot.axis.axis_line_width = 1
    plot.axis.axis_line_color = sv_maincolour
    plot.axis.major_tick_line_color = sv_maincolour
    plot.axis.minor_tick_line_color = None
    plot.axis.major_label_text_color = sv_maincolour
    plot.axis.axis_label_text_color = sv_maincolour

    plot.title.text_color = sv_boldcolour
    plot.title.text_font = sv_font
    plot.title.text_font_style = 'bold'

    plot.background_fill_color = "black"
    plot.background_fill_alpha = 0.2

    plot.border_fill_alpha = 0
    plot.outline_line_alpha = 0

    return True

def makeLinePlot(plot, data, y_name, colour, line_alpha=0.8):
    return plot.line(
                x='Time',
                y=y_name,
                source=data,
                line_color=colour,
                line_width=2,
                line_alpha=line_alpha,
                line_join='bevel',
                line_cap='round',
                line_dash='solid',
            )
def makeCirclePlot(plot, data, y_name, colour, size=8, alpha=0.5):
    return plot.circle(
                x='Time',
                y=y_name,
                source=data,
                size=size,
                fill_color=colour,
                fill_alpha=alpha,
                hover_alpha=0.9,
                line_alpha=0,
                hover_line_alpha=0
            )

def timeLineChart(data, y_name, details='', width=set_w, height=set_h):
    x_name = 'Time'
    #source = ColumnDataSource(data)

    if len(details['units'])>0:
        units = ' ('+details['units']+')'
    else:
        units = ''
    if len(details['icao'])>0:
        location = ' at '+details['icao'].upper()
    else:
        location = ''

    xdr = DataRange1d(start=data[x_name][0],end=data[x_name][-1])
   
    plot = figure(
        title = y_name+units+location,
        plot_width=width,
        plot_height=height,
        x_axis_type='datetime',
        x_range =xdr,
        toolbar_location=None,
        sizing_mode='stretch_both'
    )
    sv_plotcolour = '#eaea86'

    makeCirclePlot(plot, data, y_name, sv_plotcolour)
    line_plot = makeLinePlot(plot, data, y_name, sv_plotcolour)

    tooltip_str = '@{'+y_name+'} '+units[2:-1]+' at @Time{%H%MZ}'
    plot.add_tools(HoverTool(
        renderers=[line_plot],
        tooltips=tooltip_str,
        mode='vline', # use 'mouse' for only over points
        formatters={'@Time': 'datetime'},
        show_arrow=False,
    ))

    plot.yaxis.axis_label = y_name+units
    plot.add_layout(LinearAxis(axis_label=y_name+units), 'right')

    setLook(plot)

    return components(plot)

def timeLineChartWind(data, details='', width=set_w, height=set_h):
    x_name = 'Time'

    if len(details['icao'])>0:
        location = ' at '+details['icao'].upper()
    else:
        location = ''
    
    xdr = DataRange1d(start=data[x_name][0],end=data[x_name][-1])
    maxspd, minspd = max(np.nanmax(data['Wind Speed']), np.nanmax(data['Wind Gust']))+1, np.nanmax(min(data['Wind Speed'])-1,0)
    ydr = DataRange1d(start=minspd,end=maxspd)

    sv_plotcolour_spd = '#53f3ae'
    sv_plotcolour_dir = '#9f54bb'

    plot = figure(
        title = 'Wind'+location+' (Gusts shown only if reportable)',
        plot_width=width,
        plot_height=height,
        x_axis_type='datetime',
        x_range=xdr,
        y_range=ydr,
        toolbar_location=None,
        sizing_mode='stretch_both'
    )
    makeCirclePlot(plot, data, 'Wind Speed', sv_plotcolour_spd)
    speed_plot = makeLinePlot(plot, data, 'Wind Speed', sv_plotcolour_spd)
    plot.add_tools(HoverTool(
        renderers=[speed_plot],
        tooltips='@{Wind Direction} @{Wind Speed}KT at @Time{%H%MZ}',
        mode='vline', # use 'mouse' for only over points
        formatters={'@Time': 'datetime'},
        show_arrow=False,
    ))
    gust_plot_hidden = makeLinePlot(plot, data, 'Wind Gust', 'red', line_alpha=0)
    gust_plot = makeCirclePlot(plot, data, 'Wind Gust', sv_plotcolour_spd, size=12)
    plot.add_tools(HoverTool(
        renderers=[gust_plot_hidden],
        tooltips='Reported gust of @{Wind Gust}KT at @Time{%H%MZ}',
        mode='vline', # use 'mouse' for only over points
        formatters={'@Time': 'datetime'},
        show_arrow=False,
    ))
    plot.yaxis.axis_label = 'Wind speed/gust (KT)'

    setLook(plot)
    #plot.yaxis.axis_line_color = sv_plotcolour_spd
    #plot.yaxis.axis_label_text_color = sv_plotcolour_spd
    #plot.yaxis.major_label_text_color = sv_plotcolour_spd
    #plot.yaxis.major_tick_line_color = sv_plotcolour_spd

    plot.extra_y_ranges['dir'] = DataRange1d(start=0,end=360)
    plot.add_layout(LinearAxis(
        y_range_name='dir',
        axis_label='Wind direction (degrees)',
        axis_line_color=sv_plotcolour_dir,
        axis_label_text_color=sv_plotcolour_dir,
        major_label_text_color=sv_plotcolour_dir,
        major_tick_line_color=sv_plotcolour_dir,
        minor_tick_line_color=sv_plotcolour_dir
    ), 'right')
    dir_plot = makeLinePlot(plot, data, 'Wind Direction', sv_plotcolour_dir, line_alpha=0.5)
    dir_plot.y_range_name='dir'
    
    return components(plot)

def timeLineChartTempDewpt(data, details='', width=set_w, height=set_h):
    x_name = 'Time'

    if len(details['icao'])>0:
        location = ' at '+details['icao'].upper()
    else:
        location = ''
    
    xdr = DataRange1d(start=data[x_name][0],end=data[x_name][-1])
    maxt, mint = max(np.nanmax(data['Temperature']), np.nanmax(data['Dew Point']))+1, min(np.nanmin(data['Temperature']),np.nanmin(data['Dew Point']))-1
    ydr = DataRange1d(start=mint,end=maxt)

    sv_plotcolour_temp = '#be3c3c'
    sv_plotcolour_dewpt = '#b65d5d'

    plot = figure(
        title = 'Temperature/Dew Point'+location,
        plot_width=width,
        plot_height=height,
        x_axis_type='datetime',
        x_range=xdr,
        y_range=ydr,
        toolbar_location=None,
        sizing_mode='stretch_both'
    )
    makeCirclePlot(plot, data, 'Temperature', sv_plotcolour_temp)
    temp_plot = makeLinePlot(plot, data, 'Temperature', sv_plotcolour_temp)
    plot.add_tools(HoverTool(
        renderers=[temp_plot],
        tooltips='Temperature @{Temperature} C at @Time{%H%MZ}',
        mode='vline', # use 'mouse' for only over points
        formatters={'@Time': 'datetime'},
        show_arrow=False,
    ))
    makeCirclePlot(plot, data, 'Dew Point', sv_plotcolour_dewpt)
    dewpt_plot = makeLinePlot(plot, data, 'Dew Point', sv_plotcolour_dewpt, line_alpha=0.5)
    plot.add_tools(HoverTool(
        renderers=[dewpt_plot],
        tooltips='Dew point @{Dew Point} C at @Time{%H%MZ}',
        mode='vline', # use 'mouse' for only over points
        formatters={'@Time': 'datetime'},
        show_arrow=False,
    ))

    plot.yaxis.axis_label = 'Temperature/Dew Point (C)'
    plot.add_layout(LinearAxis(axis_label='Temperature/Dew Point (C)'), 'right')

    setLook(plot)
    
    return components(plot)

def timeLineChartVisibility(data, details='', width=set_w, height=set_h):
    x_name = 'Time'

    if len(details['icao'])>0:
        location = ' at '+details['icao'].upper()
    else:
        location = ''
    
    xdr = DataRange1d(start=data[x_name][0],end=data[x_name][-1])
    ydr = DataRange1d(start=0,end=10000)

    sv_plotcolour_vis = 'white'

    plot = figure(
        title = 'Visibility/Weather'+location,
        plot_width=width,
        plot_height=height,
        x_axis_type='datetime',
        x_range=xdr,
        y_range=ydr,
        toolbar_location=None,
        sizing_mode='stretch_both'
    )
    colourstates = []
    for v in data['Visibility']:
        colourstates.append(applyVisColourState(v))
    data['colourstates']=colourstates
    makeCirclePlot(plot, data, 'Visibility', 'colourstates', size=18)
    vis_plot = makeLinePlot(plot, data, 'Visibility', sv_plotcolour_vis, line_alpha=0.2)
    plot.add_tools(HoverTool(
        renderers=[vis_plot],
        tooltips='@{Visibility}M at @Time{%H%MZ}<br>Weather: @{Weather}',
        mode='vline', # use 'mouse' for only over points
        formatters={'@Time': 'datetime'},
        show_arrow=False,
    ))

    plot.yaxis.axis_label = 'Visibility (M)'
    plot.add_layout(LinearAxis(axis_label='Visibility (M)'), 'right')
    plot.yaxis.major_label_overrides = {10000:'10K+'}

    setLook(plot)
    
    return components(plot)

def timeChartCloud(data, details='', width=set_w, height=set_h*2):
    x_name = 'Time'
    icao = details['icao']

    if len(icao)>0:
        location = ' at '+icao.upper()
    else:
        location = ''
    
    xdr = DataRange1d(start=data[x_name][0],end=data[x_name][-1])
    #ydr = DataRange1d(start=0,end=15000)
    tick_vals, tick_label_overrides = getHeightmapTicks(icao)
    ydr = DataRange1d(start=mapHeight(0, icao),end=mapHeight(int(tick_label_overrides[max(tick_vals)]), icao))

    sv_plotcolour_vis = 'white'

    plot = figure(
        title = 'Cloud base'+location,
        plot_width=width,
        plot_height=height,
        x_axis_type='datetime',
        x_range=xdr,
        y_range=ydr,
        toolbar_location=None,
        sizing_mode='stretch_both'
    )
    colourstates, alphas = [], []
    for b in data['Cloud Base']:
        colourstates.append(applyCloudColourState(b))
    data['colourstates']=colourstates
    for a in data['Cloud Amount']:
        if a in ['SCT', 'BKN', 'OVC']:
            alphas.append(0.6)
        else:
            alphas.append(0.2)
    data['alphas']=alphas
    cloud_plot = makeCirclePlot(plot, data, 'Cloud Base Adjusted', 'colourstates', size=15, alpha='alphas')
    
    plot.add_tools(HoverTool(
        renderers=[cloud_plot],
        tooltips='@{Cloud Amount} at @{Cloud Base}FT at @Time{%H%MZ}',
        mode='mouse', # use 'mouse' for only over points
        formatters={'@Time': 'datetime'},
        show_arrow=False,
    ))

    plot.yaxis.axis_label = 'Height (FT)'
    plot.add_layout(LinearAxis(axis_label='Height (FT)'), 'right')

    plot.yaxis.ticker = tick_vals
    plot.yaxis.major_label_overrides = tick_label_overrides

    setLook(plot)
    
    return components(plot)