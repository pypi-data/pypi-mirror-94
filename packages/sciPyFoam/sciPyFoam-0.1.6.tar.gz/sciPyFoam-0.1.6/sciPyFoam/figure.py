import numpy as np
import os 
import matplotlib.pyplot as plt 
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

def figsize_cm(w_cm, h_cm=0,x=[],y=[],w_offset_cm=0.0):
    """Get figure size in unit cm. 
    Calculate figure height according to data aspect if :code:`x,y` are given.

    Parameters
    ----------
    w_cm : float
        Figure width in unit cm.
    h_cm : float, optional
        Figure height in unit cm, by default 0
    x : array, optional
        Data x array, by default []
    y : array, optional
        Data y array, by default []
    xoffset_cm : float, optional
        Figure width adjust offset in unit cm, by default 0

    Returns
    -------
    (x,y) : shape
        Calculated figure width and height.
    """
    cm2inch=1/2.54
    w=w_cm*cm2inch
    h=h_cm*cm2inch
    if(h_cm<=0):
        h=w/16*9
    if((len(x)>0) & (len(y)>0)):
        length_x=np.max(x)-np.min(x)
        length_y=np.max(y)-np.min(y)
        xyRatio=length_y/length_x
        h=w*xyRatio
    w=w+w_offset_cm*cm2inch

    return (w,h)

def usePaperStyle(mpl, fontsize=9):
    mpl.rcParams['axes.titlesize']  = fontsize
    mpl.rcParams['axes.labelsize']  = fontsize
    mpl.rcParams['xtick.labelsize'] = fontsize
    mpl.rcParams['ytick.labelsize'] = fontsize
    mpl.rcParams['legend.fontsize'] = fontsize
    mpl.rcParams['axes.titlesize']  = fontsize
    mpl.rcParams['axes.titlesize']  = fontsize

def tricontourf(axis,triangles,field,levels=60,cmap='Spectral_r',fmt_cb='%.0f',figwidth=12):
    if(axis==None):
        figsize=figsize_cm(figwidth,x=triangles.x,y=triangles.y,w_offset_cm=1.1)
        fig=plt.figure(figsize=figsize)
        axis=plt.gca()
    ax=axis
    vmin=np.min(field)
    vmax=np.max(field)
    CSf=ax.tricontourf(triangles, field,levels=levels, cmap=cmap,vmin=vmin,vmax=vmax)
    ax.axis('scaled')
    # axis
    ax.set_ylim(np.max(triangles.y),np.min(triangles.y))
    # colorbar
    ax_cb=axis.inset_axes([1.01, 0, 0.03, 1], transform=axis.transAxes)
    ax=ax_cb
    cb = plt.colorbar(CSf, cax = ax_cb,format=fmt_cb)  
    cb.set_label('Field')
    return axis, ax_cb, CSf, cb,vmin,vmax
def tripcolor(axis,triangles,field,levels=60,cmap='Spectral_r',fmt_cb='%.0f',figwidth=12,w_offset_cm=1.1):
    if(axis==None):
        figsize=figsize_cm(figwidth,x=triangles.x,y=triangles.y,w_offset_cm=w_offset_cm)
        fig=plt.figure(figsize=figsize)
        axis=plt.gca()
    ax=axis
    vmin=np.min(field)
    vmax=np.max(field)
    CSf=ax.tripcolor(triangles, field, shading='gouraud',cmap=cmap)
    ax.axis('scaled')
    # axis
    ax.set_ylim(np.max(triangles.y),np.min(triangles.y))
    # colorbar
    ax_cb=axis.inset_axes([1.01, 0, 0.03, 1], transform=axis.transAxes)
    ax=ax_cb
    cb = plt.colorbar(CSf, cax = ax_cb,format=fmt_cb)  
    cb.set_label('Field')
    return axis, ax_cb, CSf, cb,vmin,vmax
# polyplot is based on triplot, polyplot(ax, x, y, edges, **kwargs)
def polyplot(ax, *args, figwidth=12,w_offset_cm=1.1, **kwargs):
    import matplotlib.axes
    
    x=args[0]
    y=args[1]
    edges=args[2]
    kw = kwargs.copy()
    tri_lines_x = np.insert(x[edges], 2, np.nan, axis=1)
    tri_lines_y = np.insert(y[edges], 2, np.nan, axis=1)
    tri_lines = ax.plot(tri_lines_x.ravel(), tri_lines_y.ravel(),
                        **kwargs)
    # # # Draw markers separately.
    # marker=None
    # if('marker' in kw.keys()):
    #     marker = kw['marker']
    # kw_markers = {
    #     **kw,
    #     'linestyle': 'None',  # No line to draw.
    #     'label': 'None'
    # }
    # if marker not in [None, 'None', '', ' ']:
    #     tri_markers = ax.plot(x, y, **kw_markers)
    # else:
    #     tri_markers = ax.plot([], [], **kw_markers)

    # return tri_lines + tri_markers
    return tri_lines