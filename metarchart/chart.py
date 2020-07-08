from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from .forms import SettingsForm

from .get_data import latestMetars, extract
from . import make_plot

bp = Blueprint('chart', __name__)

@bp.route('/', methods=('GET','POST'))
def index():
    form = SettingsForm()
    error = None
    if request.method == 'POST':
        if form.validate_on_submit():
            icao = form.icao.data.upper()
            time_window = int(form.time_window.data)
            vname = form.variable.data
        else:
            error = 'Valid parameters not recieved. Please check request details.'
        
        if error is None:
            metar_data = latestMetars(icao, time_window)
            name, units, values, times = extract(metar_data, vname)
            data={}
            data['Time'] = times
            data[name] = values

            details = {'icao':icao, 'name':name, 'units':units, 'time_window':time_window}

            if data[name]:
                script, div = make_plot.timeLineChart(data, "Time", name, details)
            else:
                error = 'No data retrieved. Please check request details.'

    if error != None or request.method != 'POST':
        script, div, details = '', '', {'icao':'???', 'name':'???', 'units':'???', 'time_window':'???'}
        pagetitle = 'Select ICAO, time window and variable.'
    else:
        pagetitle = details['name']+' at '+details['icao']+' over the last '+str(details['time_window'])+' hours'
    if error != None:
        flash(error)


    return render_template(
        'chart/index.html',
        pagetitle=pagetitle,
        form=form,
        details=details,
        the_div=div,
        the_script=script
    )