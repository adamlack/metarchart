from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from .get_data import latestMetars, extract
from . import make_plot

bp = Blueprint('chart', __name__)

@bp.route('/', methods=('GET','POST'))
def index():
    icao = request.args.get('icao')
    if icao == None:
        icao = 'EGVO'
    time_window = request.args.get('h')
    if time_window == None:
        time_window = 12
    else:
        time_window = int(time_window)
    metar_data = latestMetars(icao, time_window)
    name, units, values, times = extract(metar_data, 'wspeed')
    data={}
    data['Time'] = times
    data[name] = values

    script, div = make_plot.timeLineChart(data, "Time", name, units, icao)

    return render_template(
        'chart/index.html',
        details={'icao':icao, 'name':name, 'units':units, 'time_window':time_window},
        the_div=div,
        the_script=script
    )