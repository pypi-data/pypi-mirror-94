# -*-coding:utf-8-*-
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np
from mpl_toolkits.axes_grid1.inset_locator import inset_axes

import sciPyFoam.readvtk as readvtk
# -------------------------------
import sciPyFoam.figure as scifig
# -------------------------------

def Read_VTK_POLYDATA(datapath,fieldName, name_fmt, coord2km=False, depthPositive=False, K2C=True):
    """Read VTK format results of cuttingPlane post-Processing.

    Parameters
    ----------
    datapath : string
        Path of the vtk files. (e.g. :code:`postProcessing/surfaces/864000`)
    fieldName : string
        Name of field. (e.g. :code:`T`)
    name_fmt : lambda
        lambda expression of the name format. (e.g. :code:`name_fmt=lambda  name : name + '_zNormal.vtk'`)
    coord2km : bool
        Convert coordinate from m to km, by default False
    depthPositive : bool
        Force depth coordinate value positive, by default False
    K2C : bool
        Convert unit of temperature from :math:`K` to :math:`^{\circ}C`, only used if :code:`fieldName=='T'`, by default True
    Returns
    -------
    x,y,z : array
        Coordinate arrays
    triangles : matplotlib.tri 
        Triangle mesh of matplotlib.tri object
    field : array 
        Field array (e.g. :code:`U`)
    """

    fname=datapath+'/'+name_fmt(fieldName)
    triangles,field=readvtk.readPolyData(fname,fieldName,coord2km, depthPositive, K2C)
    return triangles,field

def plotField(axis,triangles,field,levels=60,cmap='Spectral_r',fmt_cb='%.0f',figwidth=18, w_offset_cm=1.1):
    if(axis==None):
        figsize=scifig.figsize_cm(figwidth,x=triangles.x,y=triangles.y,w_offset_cm=w_offset_cm)
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