
import matplotlib.pyplot as plt
import matplotlib.tri as tri
from vtk import *
from vtk.util import numpy_support as VN
import numpy as np
import copy

# only read mesh including mixtured mesh
def readPolyDataPolys(fname,fieldName='',coord2km=False, depthPositive=False, K2C=True, eval_patchIndex=None):
    coordRatio=1
    if(coord2km):
        coordRatio=1/1000
    reader = vtkPolyDataReader()
    reader.SetFileName(fname)
    reader.ReadAllVectorsOn()
    reader.ReadAllScalarsOn()
    reader.Update()
    #----polydata
    data = reader.GetOutput()
    numPolys=data.GetNumberOfPolys()
    #----field data
    field=data.GetPointData().GetArray(fieldName)
    # if point data of `fieldName` doesn't exist, try celldata
    if(field==None):
        # print(str('Point data of %s does not exist, try celldata'%(fieldName)))
        field=data.GetCellData().GetArray(fieldName)
    if(field!=None):
        field = VN.vtk_to_numpy(field)
    else:
        field=[]
    if((fieldName=='T') and (K2C) and (len(field)>0)):
        field=field-273.15
    #----coordinates
    x = np.zeros(data.GetNumberOfPoints())
    y = np.zeros(data.GetNumberOfPoints())
    z = np.zeros(data.GetNumberOfPoints())
    for i in range(data.GetNumberOfPoints()):
            x[i],y[i],z[i] = data.GetPoint(i)
    x=x*coordRatio
    y=y*coordRatio
    z=z*coordRatio
    index_points=np.array(range(0,len(x)))
    index_points_patch=index_points
    if(eval_patchIndex!=None):
        ind=(eval(eval_patchIndex))
        index_points_patch=index_points[ind]
    if(depthPositive):
        y=np.abs(y)
    #----polys
    numCells=data.GetNumberOfCells()
    polys=data.GetPolys()
    maxCellSize=polys.GetMaxCellSize()
    polys_list=[]
    for i in range(0, numCells):
        IDlist=vtkIdList()
        polys.GetNextCell(IDlist)
        numIDs=IDlist.GetNumberOfIds()
        IDs=np.zeros(numIDs,int)
        ptOnPatch=True
        for j in range(0,numIDs):
            IDs[j]=IDlist.GetId(j)
            if(IDs[j] not in index_points_patch):
                ptOnPatch=False
        if(ptOnPatch==False):
            continue
        polys_list.append(IDs)
    # check surface x,y,z
    xnew=x
    ynew=y
    znew=z
    # xmin=np.min(x[index_points_patch])
    # xmax=np.max(x[index_points_patch])
    # ymin=np.min(y[index_points_patch])
    # ymax=np.max(y[index_points_patch])
    # zmin=np.min(z[index_points_patch])
    # zmax=np.max(z[index_points_patch])
    # if(xmin==xmax): #y-z plane
    #     xnew=z
    #     ynew=y
    #     znew=x
    # elif(ymin==ymax): #x-z plane
    #     xnew=x
    #     ynew=z
    #     znew=y
    # elif(zmin==zmax): #x-y plane
    #     xnew=x
    #     ynew=y
    #     znew=z
    return polys_list, xnew, ynew, znew, field

def readPolyData(fname,fieldName,coord2km=False, depthPositive=False, K2C=True, eval_patchIndex=None):
    polys_list, xnew, ynew, znew, field=readPolyDataPolys(fname,fieldName,coord2km, depthPositive, K2C, eval_patchIndex)
    x=xnew
    y=ynew
    z=znew
    xmin=np.min(x)
    xmax=np.max(x)
    ymin=np.min(y)
    ymax=np.max(y)
    zmin=np.min(z)
    zmax=np.max(z)
    if(xmin==xmax): #y-z plane
        xnew=z
        ynew=y
        znew=x
    elif(ymin==ymax): #x-z plane
        xnew=x
        ynew=z
        znew=y
    elif(zmin==zmax): #x-y plane
        xnew=x
        ynew=y
        znew=z
    
    inds1=np.array([0, 1, 2])
    inds2=np.array([2, 3, 0])
    tris=[]
    for IDlist in polys_list:
        IDs=np.array(IDlist,int)
        tris.append((IDs[inds1]))
        if(len(IDs)==4):
            tris.append((IDs[inds2]))
        elif(len(IDs)>4):
            print("Currently only triangle and rectangle elements are supported, the maximum cell size in the mesh is", len(IDs))
    triangles=[]
    triangles = tri.Triangulation(xnew,ynew,np.array(tris))
    return triangles,field

def readPolyMesh(fname,coord2km=False, depthPositive=False, eval_patchIndex=None):
    K2C=False
    fieldName=''
    polys_list, xnew, ynew, znew, field=readPolyDataPolys(fname,fieldName,coord2km, depthPositive, K2C, eval_patchIndex)

    edges=getEdges_from_Polys(polys_list)
    return xnew,ynew, znew, edges

def getEdges_from_Polys(poly_list):
    import numpy_indexed as npi
    edges=[]
    for poly in poly_list:
        numPoints=len(poly)
        for i in range(0,numPoints-1):
            if(poly[i]<poly[i+1]):
                edges.append([poly[i], poly[i+1]])
            else:
                edges.append([poly[i+1], poly[i]])
        if(poly[numPoints-1] < poly[0]):
            edges.append([poly[numPoints-1], poly[0]])
        else:
            edges.append([poly[0], poly[numPoints-1]])
    
    edges=np.array(edges,int)
    # remove duplicate edges
    edges = npi.unique(edges)
    return edges