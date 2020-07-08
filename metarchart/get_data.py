import requests
from metar import Metar
import datetime
import re

def cleanOgi(input):
    p = map(lambda i: i.split(), input)
    output = []
    i = 0
    for l in p:
        temp = map(lambda s: s.strip('\\n'), l)
        output.append(' '.join(list(map(lambda t: t.strip('='), temp))[1:]))
        i = i+1
    return output

def latestMetars(icao, time_window=None):
    """Gets most recent METARs in time_window number of hours before current time.
    
    Scrapes ogimet to get the data.
    
    Returns a list of python-metar objects."""
    end = datetime.datetime.utcnow()
    if time_window == None:
        time_window = 12
    start = end - datetime.timedelta(hours=time_window)
    s = start.strftime('&ano=%Y&mes=%m&day=%d&hora=%H&min=%M')
    e = end.strftime('&anof=%Y&mesf=%m&dayf=%d&horaf=%H&minf=%M')
    urlstring = 'http://ogimet.com/display_metars2.php?lang=en&lugar='+str(icao)+'&tipo=ALL&ord=REV&nil=NO&fmt=txt'+s+e+'&send=send'
    response = requests.get(urlstring)
    if response is not None:
        page = response.text.replace('\n','')
        page = ' '.join(page.split())
        rex = '(METAR .*?=)'
        metars = re.findall(rex, str(page))
        metars = cleanOgi(metars)
        metar_objects = []
        for m in metars:
            metar_objects.append(Metar.Metar(m, strict=False))
        metar_objects.reverse()
    return metar_objects

def extract(object_list, v=None):
    """Converts a list of python-metar objects into a list of the given variable.
    
    Accepted variables: wspeed, wgust, wdir, temp, dewpt, qnh, vis.
    
    Returns variable name (str), units (str), data (list) and observation times (list)."""
    variable_list, times_list = [], []
    name = ''
    units = None
    for o in object_list:
        if v == 'wspeed':
            variable_list.append(o.wind_speed.value('KT'))
            name, units = 'Wind Speed', 'KT'
        elif v == 'wgust':
            if o.wind_gust:
                x = o.wind_gust.value('KT')
            else:
                x = None
            variable_list.append(x)
            name, units = 'Wind Gust', 'KT'
        elif v == 'wdir':
            variable_list.append(o.wind_dir.value())
            name, units = 'Wind Direction', ''
        elif v == 'temp':
            variable_list.append(o.temp.value('C'))
            name, units = 'Temperature', 'C'
        elif v == 'dewpt':
            variable_list.append(o.dewpt.value('C'))
            name, units = 'Dew Point', 'C'
        elif v == 'qnh':
            variable_list.append(o.press.value('MB'))
            name, units = 'QNH Pressure', 'hPa'
        elif v == 'vis':
            variable_list.append(o.vis.value('M'))
            name, units = 'Visibility', 'M'
        else:
            raise Exception('Valid variable not given. ("{}" was given)'.format(v))
        times_list.append(o.time)

    return name, units, variable_list, times_list
