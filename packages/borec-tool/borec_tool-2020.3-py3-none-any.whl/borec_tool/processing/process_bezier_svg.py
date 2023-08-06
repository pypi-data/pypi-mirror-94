import numpy as np
from svgpathtools import svg2paths
from pkg_resources import resource_filename

def svg_to_function(filename, x_range=[0,1], y_range=[0,1], num_points = 10000):
    paths, attributes = svg2paths(resource_filename('borec_tool.resources',filename))
    path = paths[0]

    n = num_points  # number of points segments to get

    pts = []
    for i in range(0,n+1):
        f = float(i)/float(n)  # will go from 0.0 to 1.0
        complex_point = path.point(f)  # point(x) is method on svg.path to return point x * 100  percent along path
        pts.append((complex_point.real, complex_point.imag))

    graph_path = np.asarray(pts)
    graph_max = np.max(graph_path[:,1])
    graph_path[:,1] = graph_max-graph_path[:,1]
    
    #map x range
    np.min(graph_path[:,0])
    graph_path[:,0] = graph_path[:,0]-np.min(graph_path[:,0])
    np.max(graph_path[:,0])
    graph_path[:,0] = x_range[0]+(x_range[1]-x_range[0])*(graph_path[:,0]/np.max(graph_path[:,0]))

    #map y range
    np.min(graph_path[:,1])
    graph_path[:,1] = graph_path[:,1]-np.min(graph_path[:,1])
    np.max(graph_path[:,1])
    graph_path[:,1] =y_range[0]+(y_range[1]-y_range[0])*(graph_path[:,1]/np.max(graph_path[:,1]))

    #approximate function f(x) -> y of the path
    def f(x):
        return graph_path[np.argmin(abs(graph_path[:,0]-x)),1]

    return f