# -*-coding:utf-8-*-
# Read vtk data generated from the command of `foamToVTK`

import numpy as np
import matplotlib.pyplot as plt
import sciPyFoam.readvtk as readvtk
import sciPyFoam.figure as scifig
from colored import fg, bg, attr
C_GREEN = fg('green')
C_RED = fg('red')
C_BLUE = fg('blue')
C_DEFAULT = attr('reset')
import os
# read 2D case boundary coordinates (x,y) and field values
def readPatch_2D(caseDir, patchs, time, fieldNames,name_fmt=lambda  patch,time : str('%s_%s.vtk'% (patch,time)),coord2km=False, depthPositive=False, K2C=True, eval_patchIndex=None, sort_xy='x'):
    def readPatch_2D_singleField(caseDir, patchs, time, fieldName,name_fmt,coord2km, depthPositive, K2C, eval_patchIndex, sort_xy):
        x=[]
        y=[]
        field=[]
        if(type(patchs)==type(['a','b'])):
            for i in range(0,len(patchs)):
                patch=patchs[i]
                fname=caseDir+'/VTK/'+patch+'/'+name_fmt(patch,time)
                if(not os.path.exists(fname)):
                    cmd=str('foamToVTK -case %s -noInternal -useTimeName -time %s')% (caseDir,time)
                    print('You can use command to convert foam to vtk: '+C_GREEN+cmd+C_DEFAULT)
                    raise Exception(C_RED+str('File do not exist: "%s" '%(fname))+C_DEFAULT)
                polys_list, xnew, ynew, znew, fieldnew=readvtk.readPolyDataPolys(fname,fieldName,coord2km, depthPositive, K2C, eval_patchIndex)
                z_unique=np.unique(znew)
                if(len(z_unique)!=2):
                    raise Exception(C_RED+str('Patch "%s" is not a non-empty 2D boundary patch in %s'%(patch,caseDir))+C_DEFAULT)
                ind_bc=(znew==z_unique[0])
                shape_field=fieldnew.shape
                if(i==0):
                    x=xnew[ind_bc]
                    y=ynew[ind_bc]
                    field=fieldnew[ind_bc]
                else:
                    x=np.append(x,xnew[ind_bc])
                    y=np.append(y,ynew[ind_bc])
                    if(len(shape_field)==1):  #e.g. T, p
                        field=np.append(field,fieldnew[ind_bc])
                    else:  # e.g. U, heatFlux
                        field=np.vstack((field,fieldnew[ind_bc]))
        else:
            patch=patchs
            fname=caseDir+'/VTK/'+patch+'/'+name_fmt(patch,time)
            if(not os.path.exists(fname)):
                cmd=str('foamToVTK -case %s -noInternal -useTimeName -time %s')% (caseDir,time)
                print('You can use command to convert foam to vtk: '+C_GREEN+cmd+C_DEFAULT)
                raise Exception(C_RED+str('File do not exist: "%s" '%(fname))+C_DEFAULT)
            polys_list, xnew, ynew, znew, fieldnew=readvtk.readPolyDataPolys(fname,fieldName,coord2km, depthPositive, K2C, eval_patchIndex)
            z_unique=np.unique(znew)
            if(len(z_unique)!=2):
                raise Exception(C_RED+str('Patch "%s" is not a non-empty 2D boundary patch in %s'%(patch,caseDir))+C_DEFAULT)
            ind_bc=(znew==z_unique[0])
            x=xnew[ind_bc]
            y=ynew[ind_bc]
            field=fieldnew[ind_bc]
        x=np.array(x)
        y=np.array(y)
        field=np.array(field)
        # sort
        if(sort_xy=='x'):
            ind=np.argsort(x)
            x=x[ind]
            y=y[ind]
            field=field[ind]
        elif(sort_xy=='y'):
            ind=np.argsort(y)
            x=x[ind]
            y=y[ind]
            field=field[ind]
        return x,y,field
    if(type(fieldNames)==type(['a','b'])):
        fields={}
        x=[]
        y=[]
        for fieldName in fieldNames:
            x,y,field=readPatch_2D_singleField(caseDir, patchs, time, fieldName,name_fmt,coord2km, depthPositive, K2C, eval_patchIndex, sort_xy)
            fields[fieldName]=field
        return x,y,fields 
    else:
        fieldName=fieldNames
        x,y,field=readPatch_2D_singleField(caseDir, patchs, time, fieldName,name_fmt,coord2km, depthPositive, K2C, eval_patchIndex, sort_xy)
        return x,y,field
def readPatch(caseDir, patch, time, fieldName,name_fmt=lambda  patch,time : str('%s_%s.vtk'% (patch,time)),coord2km=False, depthPositive=False, K2C=True, eval_patchIndex=None):
    
    fname=caseDir+'/VTK/'+patch+'/'+name_fmt(patch,time)
    triangles,field=readvtk.readPolyData(fname,fieldName,coord2km, depthPositive, K2C, eval_patchIndex)
    return triangles,field

def readPatchMesh(caseDir, patch, time,name_fmt=lambda  patch, time : str('%s_%s.vtk'% (patch,time)),coord2km=False, depthPositive=False, eval_patchIndex=None):
    
    fname=caseDir+'/VTK/'+patch+'/'+name_fmt(patch,time)
    x,y, z,edges=readvtk.readPolyMesh(fname,coord2km, depthPositive, eval_patchIndex)
    
    return x,y, z, edges