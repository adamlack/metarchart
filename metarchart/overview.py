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
            if metar_data == 'ogi_limited':
                error = 'Data retrieval limited by ogimet. Please try again later.'
            elif len(metar_data) > 0:
                scripts, divs = {}, {}

                from .tools import mapHeight
                data = {}
                name, units, values, data['Time'] = extract(metar_data, 'cloud')
                data['Cloud Base'], data['Cloud Amount'] = values['cloudbase'], values['cloudamount']
                data['Cloud Base Adjusted'] = [mapHeight(h, icao) for h in data['Cloud Base']]
                scripts['cloudbase'], divs['cloudbase'] = make_plot.timeChartCloud(data, {'icao':icao, 'name':name, 'units':units, 'time_window':time_window})

                data = {}
                name, units, values, data['Time'] = extract(metar_data, 'wind')
                data['Wind Speed'], data['Wind Gust'], data['Wind Direction'] = values['speed'], values['gust'], values['direction']
                scripts['wind'], divs['wind'] = make_plot.timeLineChartWind(data, {'icao':icao, 'name':name, 'units':units, 'time_window':time_window})

                data = {}
                name, units, data['Temperature'], data['Time'] = extract(metar_data, 'temp')
                data['Dew Point'] = extract(metar_data, 'dewpt')[2]
                scripts['tempdewpt'], divs['tempdewpt'] = make_plot.timeLineChartTempDewpt(data, {'icao':icao, 'name':'Temperature/Dew Point', 'units':units, 'time_window':time_window})

                data = {}
                name, units, data['Visibility'], data['Time'] = extract(metar_data, 'vis')
                d1, d2, data['Weather'], d3 = extract(metar_data, 'wx') # d1-3 dummy values
                scripts['visibility'], divs['visibility'] = make_plot.timeLineChartVisibility(data, {'icao':icao, 'name':'Visibility', 'units':units, 'time_window':time_window})

                for x in ['qnh']:
                    data={}
                    name, units, data[name], data['Time'] = extract(metar_data, x)
                    scripts[name], divs[name] = make_plot.timeLineChart(data, name, {'icao':icao, 'name':name, 'units':units, 'time_window':time_window})
            else:
                error = 'No data retrieved. Please check request details.'

    if error != None or request.method != 'POST':
        scripts, divs, details = '', '', {'icao':'???', 'name':'???', 'units':'???', 'time_window':'???'}
        pagetitle = 'Choose station ICAO and time window.'
    else:
        details = {'icao':icao, 'name':'overview', 'units':'', 'time_window':time_window}
        pagetitle = details['icao']+' overview for the last '+str(details['time_window'])+' hours'
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