from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from .get_data import latestMetars, extract
from . import make_plot

bp = Blueprint('chart', __name__)

@bp.route('/', methods=('GET','POST'))
def index():
    error = None
    if request.method == 'POST': # prefer POST parameters if available
        icao = request.form['icao']
        time_window = request.form['time_window']
    else: # otherwise try and use GET parameters
        icao = request.args.get('icao')
        if icao == None: # set default if no parameters available
            icao = 'EGVO'
            flash('Defaulted to location EGVO (parameter not given)') #DEBUG
        time_window = request.args.get('h')
        if time_window == None: # set default if no parameters available
            time_window = 12
            flash('Defaulted to latest '+str(time_window)+' hours (parameter not given)') #DEBUG
        else:
            time_window = int(time_window)

    if error is None:
        metar_data = latestMetars(icao, time_window)
        name, units, values, times = extract(metar_data, 'wspeed')
        data={}
        data['Time'] = times
        data[name] = values

        details = {'icao':icao, 'name':name, 'units':units, 'time_window':time_window}

        if data[name]:
            script, div = make_plot.timeLineChart(data, "Time", name, details)
        else:
            script, div = None, None
            error = 'No data retrieved. Please check request details.'
    
    if error != None:
        flash(error)

    return render_template(
        'chart/index.html',
        details=details,
        the_div=div,
        the_script=script
    )