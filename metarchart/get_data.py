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
    
    Accepted variables: cloudbase, wspeed, wgust, wdir, temp, dewpt, qnh, vis.

    Can also use wind, which returns a dict of speed, gust and direction.
    
    Returns variable name (str), units (str), data (list) and observation times (list)."""
    variable_list, times_list = [], []
    name = ''
    units = None

    if v == 'wind':
        variable_list = {'speed':[],'gust':[],'direction':[]}
        speed_extraction = extract(object_list, v='wspeed')
        variable_list['speed'], times_list = speed_extraction[2], speed_extraction[3]
        variable_list['gust'] = extract(object_list, v='wgust')[2]
        variable_list['direction'] = extract(object_list, v='wdir')[2]
        name, units = 'Wind', ''
    else:
        for o in object_list:
            if v == 'cloudbase':
                if o.sky: #cover, height, cloud
                    for layer in o.sky:
                        if layer[1]:
                            variable_list.append(layer[1].value('FT'))
                            times_list.append(o.time)
                else:
                    variable_list.append(float('nan'))
                    times_list.append(o.time)
                name, units = 'Cloud Base', 'FT'
            else:
                if v == 'wspeed':
                    if o.wind_speed:
                        x = o.wind_speed.value('KT')
                    else:
                        x = float('nan')
                    name, units = 'Wind Speed', 'KT'
                elif v == 'wgust':
                    if o.wind_gust:
                        x = o.wind_gust.value('KT')
                    else:
                        x = float('nan')
                    name, units = 'Wind Gust', 'KT'
                elif v == 'wdir':
                    if o.wind_dir:
                        x = o.wind_dir.value()
                    else:
                        x = float('nan')
                    name, units = 'Wind Direction', ''
                elif v == 'temp':
                    x = o.temp.value('C')
                    name, units = 'Temperature', 'C'
                elif v == 'dewpt':
                    x = o.dewpt.value('C')
                    name, units = 'Dew Point', 'C'
                elif v == 'qnh':
                    x = o.press.value('MB')
                    name, units = 'QNH Pressure', 'hPa'
                elif v == 'vis':
                    if o.vis:
                        if o.vis.value('M') == 10000:
                            x = 9999
                        else:
                            x = o.vis.value('M')
                    else:
                        x = float('nan')
                    name, units = 'Visibility', 'M'
                else:
                    raise Exception('Valid variable not given. ("{}" was given)'.format(v))
                variable_list.append(x)
                times_list.append(o.time)

    return name, units, variable_list, times_list