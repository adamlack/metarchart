from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from .forms import OverviewSettingsForm

from .get_data import latestMetars, extract
from . import make_plot

bp = Blueprint('overview', __name__)

@bp.route('/', methods=('GET','POST'))
def index():
    form = OverviewSettingsForm()
    error = None
    if request.method == 'POST':
        if form.validate_on_submit():
            icao = form.icao.data.upper()
            time_window = int(form.time_window.data)
        else:
            error = 'Valid parameters not received. Please check request details.'
        
        if error is None:
            metar_data = latestMetars(icao, time_window)
            if len(metar_data) > 0:
                scripts, divs = {}, {}

                name, units, values, times = extract(metar_data, 'wind')
                data = {}
                data['Time'] = times
                data['Wind Speed'], data['Wind Gust'], data['Wind Direction'] = values['speed'], values['gust'], values['direction']
                scripts['wind'], divs['wind'] = make_plot.timeLineChartWind(data, {'icao':icao, 'name':name, 'units':units, 'time_window':time_window})

                for x in ['temp','dewpt','qnh']:
                    data={}
                    name, units, data[name], data['Time'] = extract(metar_data, x)
                    scripts[name], divs[name] = make_plot.timeLineChart(data, name, {'icao':icao, 'name':name, 'units':units, 'time_window':time_window})
            else:
                error = 'No data retrieved. Please check request details.'

    if error != None or request.method != 'POST':
        scripts, divs, details = '', '', {'icao':'???', 'name':'???', 'units':'???', 'time_window':'???'}
        pagetitle = 'Select ICAO, time window and variable.'
    else:
        details = {'icao':icao, 'name':'overview', 'units':'', 'time_window':time_window}
        pagetitle = 'Overview for '+details['icao']+' over the last '+str(details['time_window'])+' hours'
    if error != None:
        flash(error)


    return render_template(
        'overview/index.html',
        pagetitle=pagetitle,
        settings_visible=True,
        form=form,
        details=details,
        the_divs=divs,
        the_scripts=scripts,
    )