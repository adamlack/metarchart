from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from .forms import VariableSettingsForm

from .get_data import latestMetars, extract
from . import make_plot

bp = Blueprint('singlevariable', __name__)

@bp.route('/singlevariable', methods=('GET','POST'))
def index():
    form = VariableSettingsForm()
    error = None
    if request.method == 'POST':
        if form.validate_on_submit():
            icao = form.icao.data.upper()
            time_window = int(form.time_window.data)
            vname = form.variable.data
        else:
            error = 'Valid parameters not received. Please check request details.'
        
        if error is None:
            metar_data = latestMetars(icao, time_window)
            if metar_data == 'ogi_limited':
                error = 'Data retrieval limited by ogimet. Please try again later.'
            else:
                name, units, values, times = extract(metar_data, vname)
                data={}
                data['Time'] = times
                details = {'icao':icao, 'name':name, 'units':units, 'time_window':time_window}
            
                if name == 'Cloud':
                    data['Cloud Base'], data['Cloud Amount'] = values['cloudbase'], values['cloudamount']
                    from .tools import mapHeight
                    data['Cloud Base Adjusted'] = [mapHeight(h, icao) for h in data['Cloud Base']]
                    if data['Cloud Base']:
                        script, div = make_plot.timeChartCloud(data, details)
                    else:
                        error = 'No data retrieved. Please check request details.'
                elif name == 'Visibility':
                    data[name] = values
                    d1, d2, data['Weather'], d3 = extract(metar_data, 'wx') # d1-3 dummy values
                    if data[name]:
                        script, div = make_plot.timeLineChartVisibility(data, details)
                    else:
                        error = 'No data retrieved. Please check request details.'
                elif name == 'Wind':
                    if values['speed']:
                        data['Wind Speed'], data['Wind Gust'], data['Wind Direction'] = values['speed'], values['gust'], values['direction']
                        script, div = make_plot.timeLineChartWind(data, details)
                    else:
                        error = 'No data retrieved. Please check request details.'
                else:
                    data[name] = values
                    
                    if data[name]:
                        script, div = make_plot.timeLineChart(data, name, details)
                    else:
                        error = 'No data retrieved. Please check request details.'

    if error != None or request.method != 'POST':
        script, div, details = '', '', {'icao':'???', 'name':'???', 'units':'???', 'time_window':'???'}
        pagetitle = 'Choose station ICAO, time window and variable.'
    else:
        pagetitle = details['name']+' at '+details['icao']+' (last '+str(details['time_window'])+' hours)'
    if error != None:
        flash(error)


    return render_template(
        'singlevariable/index.html',
        pagetitle=pagetitle,
        settings_visible=True,
        form=form,
        details=details,
        the_div=div,
        the_script=script,
    )