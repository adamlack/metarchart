import datetime

# Set colours to use for applying colour states on cloud and visibility
cstate = {'blue':'#3070f0','white':'white','green':'#2ba141','yellow':'yellow','amber':'#ffa436','red':'red','other':'pink',}

def applyVisColourState(v):
    if v>7999:
        c=cstate['blue']
    elif v>4999:
        c=cstate['white']
    elif v>3699:
        c=cstate['green']
    elif v>1599:
        c=cstate['yellow']
    elif v>799:
        c=cstate['amber']
    elif v>=0:
        c=cstate['red']
    else:
        c=cstate['other']
    return c

def applyCloudColourState(b):
    if b>2499:
        c=cstate['blue']
    elif b>1499:
        c=cstate['white']
    elif b>699:
        c=cstate['green']
    elif b>299:
        c=cstate['yellow']
    elif b>199:
        c=cstate['amber']
    elif b>=0:
        c=cstate['red']
    else:
        c=cstate['other']
    return c

def heightMap(icao=None):
    """Map of coordinates for simulating the Met Office Visio cross
    section height scale for a particular station"""
    if icao != None:
        maps = {}
        # maps['icao'] = [[<<pixel height of each section on x-sect ("up to top...")>>],[<<Tops of each section in FT>>]]
        maps['egvo'] = [[132,77,99,150,122,75,999],[500,1000,2000,5000,10000,15000,999999],15000]
        maps['egvo_gliding'] = [[87,49,80,69,61,34,999],[1000,2000,5000,10000,18000,25000,999999],25000]
        maps['egub'] = [[132,77,99,150,122,75,999],[500,1000,2000,5000,10000,15000,999999],15000]
        maps['egxc'] = [[42,35,42,33,43,60,96,102,105,64,44,999],[200,400,700,1000,1500,2500,5000,10000,20000,30000,40000,999999],40000]
        maps['egxw'] = [[73,46,57,100,79,70,61,33,999],[500,1000,2000,5000,10000,18000,30000,40000,999999],40000]
        maps['egxt'] = [[150,93,123,191,159,97,44,999],[500,1000,2000,5000,10000,15000,20000,999999],20000]
        maps['egom'] = [[129,81,101,161,134,119,64,68,999],[500,1000,2000,5000,10000,18000,25000,35000,999999],35000]
        maps['egyp'] = [[62,50,69,135,125,115,58,72,61,36,71,999],[500,1000,2000,5000,10000,18000,24000,34000,45000,53000,70000,999999],70000]
        maps['egow'] = [[163,103,128,205,171,104,46,999],[500,1000,2000,5000,10000,15000,18000,999999],18000]
        maps['egwc'] = [[151,95,125,202,170,176,999],[500,1000,2000,5000,10000,18000,999999],18000]
        maps['egvp'] = [[153,95,119,189,160,140,999],[500,1000,2000,5000,10000,18000,999999],18000]
        maps['egwu'] = [[173,101,128,84,111,162,97,999],[500,1000,2000,3000,5000,10000,15000,999999],15000]

        return maps[icao.lower()][0], maps[icao.lower()][1], maps[icao.lower()][2]
    else:
        return None

def wintertimeCheck(now):
    wintertime = False
    if now.month in [11,12,1,2,3]:
        wintertime = True
    if now.month == 10 and now.day > 24:
        tempdate = datetime.datetime(now.year, 10, 31)
        change_date = 99
        for i in range(7):
            tempdate = tempdate - datetime.timedelta(days=1)
            if tempdate.weekday() == 6:
                change_date = tempdate.day
        if now.day >= change_date:
            wintertime = True
    if now.month == 3 and now.day > 24:
        tempdate = datetime.datetime(now.year, 3, 31)
        change_date = 99
        for i in range(7):
            tempdate = tempdate - datetime.timedelta(days=1)
            if tempdate.weekday() == 6:
                change_date = tempdate.day
        if now.day >= change_date:
            wintertime = False
    return now.strftime('%d%m%Y'), wintertime
    
if __name__ == '__main__':   
    from datetime import datetime as dt

    print(str(wintertimeCheck(dt(2019,10,27)))+' should be TRUE')
    print(str(wintertimeCheck(dt(2019,10,31)))+' should be TRUE')
    print(str(wintertimeCheck(dt(2019,11,1)))+' should be TRUE')
    print(str(wintertimeCheck(dt(2020,3,12)))+' should be TRUE')
    print(str(wintertimeCheck(dt(2020,3,20)))+' should be TRUE')
    print(str(wintertimeCheck(dt(2020,3,27)))+' should be TRUE')
    print(str(wintertimeCheck(dt(2020,3,28)))+' should be TRUE')
    print(str(wintertimeCheck(dt(2020,10,25)))+' should be TRUE')
    print(str(wintertimeCheck(dt(2020,10,26)))+' should be TRUE')
    print('\n')
    print(str(wintertimeCheck(dt(2020,3,29)))+' should be FALSE')
    print(str(wintertimeCheck(dt(2020,3,30)))+' should be FALSE')
    print(str(wintertimeCheck(dt(2020,7,20)))+' should be FALSE')
    print(str(wintertimeCheck(dt(2020,10,23)))+' should be FALSE')
    print(str(wintertimeCheck(dt(2020,10,24)))+' should be FALSE')
    print(str(wintertimeCheck(dt(2019,10,15)))+' should be FALSE')
    print(str(wintertimeCheck(dt(2019,10,25)))+' should be FALSE')
    print(str(wintertimeCheck(dt(2019,10,26)))+' should be FALSE')