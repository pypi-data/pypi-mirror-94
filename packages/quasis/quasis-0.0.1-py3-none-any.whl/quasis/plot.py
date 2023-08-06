import plotly.express       as pe 
import plotly.graph_objects as go
import csv

def plot(functions, x1, x2, marker_mode, size, logX, logY):
    lines = list()

    for f in functions:
        lineX = list()
        lineY = list()
        for x in range(x1, x2):
            lineX.append(x)
            lineY.append(f(x))
        lines.append([lineX, lineY])
    
    fig = go.Figure()

    for line in lines:
        fig.add_trace(go.Line(x=line[0],y=line[1],mode=marker_mode))
    
    fig.update_traces(marker_size=size)

    if logX:
        fig.update_xaxes(type="log")
    if logY:
        fig.update_yaxes(type="log") 

    return fig

def plot_hn(dataPath, functions, x1, x2, logX, logY, marker_mode, size):

    if not (x1 >= 0 and x1 <= 1201126):
        raise ValueError('X1 needs to be in the range [0-1201126]')
    if not (x2 >= 0 and x2 <= 1201126):
        raise ValueError('X2 needs to be in the range [0-1201126]')

    if x1 > x2:
        raise ValueError("X2 needs to higher than X1")



    mainX = list()
    mainY = list()

    with open(dataPath, "r") as file:
        reader = csv.reader(file)
        next(reader)
        for i in range(x1):
            next(reader)
        
        i = 0
        for x, y in reader:
            if i >= (x2 - x1):
                break
            mainX.append(int(x))
            mainY.append(float(y))
            i += 1

    lines = list()

    for f in functions:
        lineX = list()
        lineY = list()
        for x in range(x1, x2):
            lineX.append(x)
            lineY.append(f(x))
        lines.append([lineX, lineY])
    
    fig = pe.scatter(x=mainX,y=mainY,log_x=logX,log_y=logY)

    for line in lines:
        fig.add_trace(go.Line(x=line[0],y=line[1],mode=marker_mode))
    
    fig.update_traces(marker_size=size)

    return fig

def plot_sn(dataPath, functions, x1, x2, logX, logY, marker_mode, size):

    if not (x1 >= 0 and x1 <= 100000):
        raise ValueError('X1 needs to be in the range [0-100000]')
    if not (x2 >= 0 and x2 <= 100000):
        raise ValueError('X2 needs to be in the range [0-100000]')

    if x1 > x2:
        raise ValueError("X2 needs to higher than X1")



    mainX = list()
    mainY = list()

    with open(dataPath, "r") as file:
        reader = csv.reader(file)
        next(reader)
        for i in range(x1):
            next(reader)
        
        i = 0
        for x, y in reader:
            if i >= (x2 - x1):
                break
            mainX.append(int(x))
            mainY.append(float(y))
            i += 1

    lines = list()

    for f in functions:
        lineX = list()
        lineY = list()
        for x in range(x1, x2):
            lineX.append(x)
            lineY.append(f(x))
        lines.append([lineX, lineY])
    
    fig = pe.scatter(x=mainX,y=mainY,log_x=logX,log_y=logY)

    for line in lines:
        fig.add_trace(go.scatter.Line(x=line[0],y=line[1],mode=marker_mode))
    
    fig.update_traces(marker_size=size)

    return fig