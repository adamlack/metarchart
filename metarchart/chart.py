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
    time_window = int(request.args.get('h'))
    metar_data = latestMetars(icao, time_window)
    name, units, values, times = extract(metar_data, 'wgust')
    data={}
    data['Time'] = times
    data[name] = values

    script, div = make_plot.timeLineChart(data, "Time", name, units, icao)

    return render_template('chart/index.html', icao=icao, the_div=div, the_script=script)