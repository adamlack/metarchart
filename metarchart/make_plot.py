from bokeh.models import HoverTool, DataRange1d
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models.sources import ColumnDataSource
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.models.callbacks import CustomJS

def timeLineChart(data, x_name, y_name, details='', width=600, height=150):
    source = ColumnDataSource(data)

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

    sv_plotcolour = '#5afaad'
    plot.line(
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
    plot.yaxis.axis_label = y_name+units

    # Style variables "sv"
    sv_maincolour = '#888888'
    sv_boldcolour = '#bbbbbb'
    sv_font = 'arial'

    plot.xgrid.visible = False
    plot.grid.grid_line_color = sv_maincolour
    plot.grid.grid_line_alpha = 0.2

    plot.axis.axis_line_width = 1
    plot.axis.axis_line_color = sv_maincolour
    plot.axis.major_tick_line_color = sv_maincolour
    plot.axis.minor_tick_line_color = None
    plot.axis.major_label_text_color = sv_maincolour
    plot.axis.axis_label_text_color = sv_maincolour

    tooltip_str = '@{'+y_name+'} '+units[2:-1]+' at @Time{%H%MZ}'
    plot.add_tools(HoverTool(
        tooltips=tooltip_str,
        mode='vline', # use 'mouse' for only over points
        formatters={'@Time': 'datetime'},
        show_arrow=False,
    ))
    #tooltip css styled manually with .bk-tooltip

    plot.title.text_color = sv_boldcolour
    plot.title.text_font = sv_font
    plot.title.text_font_style = 'bold'

    plot.background_fill_color = "black"
    plot.background_fill_alpha = 0.2

    plot.border_fill_alpha = 0
    plot.outline_line_alpha = 0
    
    return components(plot)