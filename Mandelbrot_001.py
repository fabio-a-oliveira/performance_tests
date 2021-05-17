# =============================================================================
# Imports
# =============================================================================

import numpy as np
import matplotlib.pyplot as plt
import time
from os import mkdir, listdir
from os.path import join

# =============================================================================
# iterate_fc()
# =============================================================================

def iterate_fc(c = 0,
               initial_z = 0,
               max_iter = 1000):
    """
    Checks for how many iteractive applications of fc = z**2 + c does the value of
    fc remain bounded (< 2)
    
    Arguments:
        c -- complex constant
        initial_z -- initial value of z (defaults to 0)
        max_iter -- number of iterations to check boundedness for
        
    Return:
        iters -- max_iter or number of iterations after which the value of fc is > 2
        fc -- list of values of fc after applying the function iteractively
    """
    
    iters = 0
    z = initial_z
    fc = [z]
    
    while iters <= max_iter:
        if abs(z) > 2:
            return iters, fc
        else:
            z = z * z + c
            fc.append(z)
            iters += 1
            
    return max_iter, fc

# =============================================================================
# make_coordinates()
# =============================================================================

def make_coordinates(x_range = (-1,1),
                     y_range = (-1,1),
                     x_steps = 100,
                     y_steps = 100):
    """
    Makes list of complex coordinates
    
    Arguments:
        x_range/y_range -- tuples with min/max x/y values
        x_steps/y_steps -- number of steps between min/max x/y values
        
    Return:
        zs -- list of complex coordinates        
    """
    
    x0, x1 = x_range[0], x_range[1]
    y0, y1 = y_range[0], y_range[1]
    xs, ys, zs = [], [], []
    
    for step in range(x_steps):
        xs.append(x0 + step * (x1-x0) / (x_steps-1))
        
    for step in range(y_steps):
        ys.append(y0 + step * (y1-y0) / (y_steps-1))
    
    for y in ys:
        for x in xs:
            zs.append(complex(x, y))
    
    return zs
        
# =============================================================================
# make_set()
# =============================================================================

def make_set(x_range = (-1,1),
             y_range = (-1,1),
             x_steps = 100,
             y_steps = 100,
             max_iter = 1000):
    """
    Runs iteractive algorithm at each point of a complex dominium to check if function remains
    bounded within max_iter iterations

    Arguments:
        x_range/y_range -- tuple with lowest/highest values of x/y
        x_steps/y_steps -- number of steps in the x/y direction
        max_iter -- max number of iterations to verify if z > 2
        
    Return:
        cs -- list of complex coordinates
        iters -- number of iterations until z>2 or max_iter
    """

    cs = make_coordinates(x_range, y_range, x_steps, y_steps)
    iters = []
    
    for c in cs:
        num_iters, _ = iterate_fc(c = c, initial_z = 0, max_iter = max_iter)
        iters.append(num_iters)
    
    return cs, iters

# =============================================================================
# save_figure()
# =============================================================================

def save_figure(cs, iters, x_steps=100, y_steps=100, fname = None, **kwargs):
    """
    Saves figure from results of make_set() method
    
    Arguments:
        cs -- list of complex coordinates
        iters -- number of iterations of fc until fc > 2
        x_steps/y_steps -- number of steps in the x and y directions
        fname -- file name (if None, will use timestamp)
        **kwargs -- passed to matplotlib.pyplot.imsave
    
    Returns:
        None
    """
    
    if fname == None:
        if 'images' not in listdir():
            mkdir('images')
        fname = join('images', time.strftime('Mandelbrot_001___%Y-%m-%d___%H-%M-%S.png'))
    
    arr = np.array(iters).reshape((y_steps, x_steps))
    plt.imsave(fname = fname, arr = arr, origin = 'lower', **kwargs)
    
    return None

# =============================================================================
# make_figure()
# =============================================================================

def make_figure(x_range = (-3,1),
                y_range = (-1.125,1.125),
                x_steps = 1920,
                y_steps = 1080,
                max_iter = 100,
                fname = None,
                cmap = 'hot',
                **kwargs):
    """
    Calculates number of iterations at each point and saves figure
    
    Arguments:
        x_range/y_range -- tuple with lowest/highest values of x/y
        x_steps/y_steps -- number of steps in the x/y direction
        max_iter -- max number of iterations to verify if z > 2
        fname -- file name (if None, will use timestamp)
        **kwargs -- passed to matplotlib.pyplot.imsave
        
    Returns:
        None
    """
    
    cs, iters = make_set(x_range, y_range, x_steps, y_steps, max_iter)
    save_figure(cs, iters, x_steps, y_steps, cmap = cmap)
    
    return None