from bokeh.models import HoverTool, DataRange1d, LinearAxis
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.models.callbacks import CustomJS

import numpy as np

set_w, set_h = 700, 100

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
        sizing_mode='scale_width'
    )
    sv_plotcolour = '#53f3ae'
    line_plot = plot.line(
        x='Time',
        y=y_name,
        source=data,
        line_color=sv_plotcolour,
        line_width=2, #in px
        line_alpha=0.8,
        line_join='bevel',
        line_cap='round',
        line_dash='solid',
    )
    tooltip_str = '@{'+y_name+'} '+units[2:-1]+' at @Time{%H%MZ}'
    plot.add_tools(HoverTool(
        renderers=[line_plot],
        tooltips=tooltip_str,
        mode='vline', # use 'mouse' for only over points
        formatters={'@Time': 'datetime'},
        show_arrow=False,
    ))
    plot.circle(
        x='Time',
        y=y_name,
        source=data,
        size=8,
        fill_color=sv_plotcolour,
        fill_alpha=0.5,
        hover_alpha=0.9,
        line_alpha=0,
        hover_line_alpha=0
    )
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

    sv_plotcolour_spd = '#58df58'
    sv_plotcolour_dir = '#eddf82'

    plot = figure(
        title = 'Wind'+location,
        plot_width=width,
        plot_height=height,
        x_axis_type='datetime',
        x_range=xdr,
        y_range=ydr,
        toolbar_location=None,
        sizing_mode='scale_width'
    )
    speed_plot = plot.line(
        x='Time',
        y='Wind Speed',
        source=data,
        line_color=sv_plotcolour_spd,
        line_width=2, #in px
        line_alpha=0.8,
        line_join='bevel',
        line_cap='round',
        line_dash='solid',
    )
    plot.add_tools(HoverTool(
        renderers=[speed_plot],
        tooltips='@{Wind Direction} @{Wind Speed}KT at @Time{%H%MZ}',
        mode='vline', # use 'mouse' for only over points
        formatters={'@Time': 'datetime'},
        show_arrow=False,
    ))
    plot.circle(
        x='Time',
        y='Wind Speed',
        source=data,
        size=8,
        fill_color=sv_plotcolour_spd,
        fill_alpha=0.5,
        hover_alpha=0.9,
        line_alpha=0,
        hover_line_alpha=0
    )
    gust_plot = plot.circle(
        x='Time',
        y='Wind Gust',
        source=data,
        size=14,
        fill_color=sv_plotcolour_spd,
        fill_alpha=0.5,
        hover_alpha=0.9,
        line_alpha=0,
        hover_line_alpha=0
    )
    plot.add_tools(HoverTool(
        renderers=[gust_plot],
        tooltips='Reported gust of @{Wind Gust}KT at @Time{%H%MZ}',
        mode='vline', # use 'mouse' for only over points
        formatters={'@Time': 'datetime'},
        show_arrow=False,
    ))
    plot.yaxis.axis_label = 'Wind speed/gust (KT)'

    setLook(plot)
    plot.yaxis.axis_line_color = sv_plotcolour_spd
    plot.yaxis.axis_label_text_color = sv_plotcolour_spd
    plot.yaxis.major_label_text_color = sv_plotcolour_spd
    plot.yaxis.major_tick_line_color = sv_plotcolour_spd

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

    plot.line(
        x='Time',
        y='Wind Direction',
        source=data,
        y_range_name='dir',
        line_color=sv_plotcolour_dir,
        line_width=2,
        line_alpha=0.8,
        line_join='bevel',
        line_cap='round',
        line_dash='solid',
    )

    
    return components(plot)