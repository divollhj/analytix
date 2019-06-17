# -*- coding: utf-8 -*-
"""
Created on Fri May 31 12:46:02 2019

@author: DivollHJ
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)),'Importerator'))
import Importerator
RELATIVE_LIB_PATH = Importerator.RELATIVE_LIB_PATH
        
if __name__ == '__main__':
    if os.name == 'posix':
        try:
            from subprocess import check_output
            with open('/dev/tty') as tty:
                h,w = map(int,check_output(['stty','size'],stdin==tty).split())
        except:
            w = 140
    else:
        w = 140
    NOTES = '*' * w
    NOTES+=\
"""
usage: Plotteratory.py <dir 1> <dir N> <file 1> <file N> <options>

option: -nt <##>
            Number of threads
            
        --max-threads Thread all jobs
"""
    NOTES += '*' * w
    if len(sys.argv) == 1:
        print(NOTES)
        sys.exit(0)
    else:
        Importerator.loadDepends('Plotterator')
#        exports, tup = Importerator.buildDepends('Plotterator')
#        for line in exports.splitlines():
#            try:
#                exec line in globals(), globals()
#                print(line)
#            except:
#                print('{} did not work.'.format(line))
        
print globals(), '\n\nbreak\n\n'
globals().update(Importerator.returnGlobals())
print globals()
#tits.makeAndPrintArray()
intermediary.deeperNdeeper()
"""IMPORTERATOR        
import glob
import cPickle
import numpy as np
from copy import deepcopy
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
from matplotlib.lines import Line2D
from matplotlib import table
from mpl_toolkits.mplot3d import Axes3D
from multiprocessing import cpu_count, Pool
import cartopy.crs as ccrs
from cartopy import config
from cartopy.io.shapereader import Reader
import cartopy.feature as cfeature
IMPORTERATOR_FROM_REPO
import intermediary
"""
if 'ccrs' in dir():
    CfgDir = config['repo_data_dir']
    lenCfgDir = len(CfgDir)+1
    resolution ='10m'
    shapefiles_cultural_path = os.path.join(config['repo_data_dir'],
                                            'shapefiles',
                                            'natural_earth',
                                            resolution+'_cultural')
    ADMIN0_COUNTRIES_NAME    = glob.glob(os.path.join(shapefiles_cultural_path, 'ne_'+resolution+'_admin_0_countries*.shp'))[0]

#if not hasattr(sys,'frozen'):
#    RELATIVE_LIB_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
##    sys.path.extend([_ for _ in glob.glob(os.path.join(RELATIVE_LIB_PATH,'*')) if os.path.isdir(_)])
#else:
#    RELATIVE_LIB_PATH = os.path.dirname(sys.eexecutable)
    
STYLE_SHEET = os.path.join(RELATIVE_LIB_PATH,'gobat','ota_presentation.mplstyle')
ESI_STYLE_SHEET = os.path.join(RELATIVE_LIB_PATH,'gobat','esi_presentation.mplstyle')
plt.style.use(STYLE_SHEET)
exclude_list = ['x','y','z','fmt','plottype','bins','height','width','left','bottom','align']
special_cmds = ['twinx','twiny','get_legend']
figTitleFD = {
            'family':'sans',
            'color':'black',
            'fontweight':'bold',
            'fontsize':'24',
            'size':'24',
            'weight':'bold'
            }
figAxisFD = {
            'family':'sans',
            'color':'black',
            'weight':'bold',
            'size':'20'
            }
figTitleFDSmall = {
            'family':'sans',
            'color':'black',
            'weight':'bold',
            'size':'16'
            }
figClassFD = {
            'family':'sans',
            'color':'red',
            'weight':'bold',
            'size':'18'
            }

def general_format_coord(current,other=None,llabel='',rlabel=''):
    def format_coord(x,y):
        display_coord = current.transData.transform((x,y))
        rlabel = current.get_ylabel()
        if other:
            llabel = other.get_ylabel()
            inv = other.transData.inverted()
            ax_coord = inv.transform(display_coord)
            coords = [tuple(ax_coord)+(llabel,),(x,y,rlabel)]
            fcoords = ['{}: ({:.3f}, {:.3f})'.format(l,tx,ty) for tx,ty,l in coords]
            return ('{:<40}{}{:>}'.format(fcoords[0],space,fcoords[1]))
        else:
            return ('{:<40}'.format('{}: ({:.3f}, {:.3f})'.format(rlabel,x,y)))
    return format_coord

ann_list = []

def on_pick(event):
    try:
        line = event.artist
        xdata = line.get_xdata()
        ydata = line.get_ydata()
        ind = event.ind
        ax = line.axes
        ann = ax.annotate(line.get_label(),(xdata[ind[0]],ydata[ind[0]]))
        ann_list.append(ann)
        line.figure.canvas.draw()
    except:
        pass
    
def on_release(event):
    for ann in ann_list:
        ann.remove()
        ann_list.remove(ann)
    event.canvas.draw()
    
def PNGerator(flist,**kwargs):
    nthreads = kwargs.pop('nthreads',1)
    if (nthreads > 1 and nthreads > cpu_count()) or nthreads < 1:
        nthreads = cpu_count()
    if isinstance(flist,str):
        flist = [flist]
    if isinstance(flist,list):
        if nthreads > 1:
            pool = Pool(nthreads)
        for fname in flist:
            if os.path.isfile(fname) and os.path.splitext(fname)[1] == '.pklplt':
                if nthreads > 1:
                    pool.apply_async(pngthread,args=(fname,))
                else:
                    pngthread(fname)
        if nthreads > 1:
            pool.close()
            pool.join()
    else:
        print('Invalid input.  Provide single file name string or list of filename strings.')
        
def pngthread(fname):
    pltr = Plotter()
    pltr.retrievePlot(fname)
    pltr.createPlot(fname,SAVEPNG=True,SAVEPKL=False)
    
class Plotter(object):
    """
    Plotter class allows for storing data, specifications and commands
    for matplotlib to generate plots. Current plot types supported:
        line plot
        scatter plot
        3d scatter plot
        pie chart
        stack plot
        histogram
        cartopy map plot
        bar plot
        horizontal bar plot
    The figure is built using a GridSpec.  Calls to add_suplot initiate each
    subplot using the starting row, col as a reference and allowing for a
    rowspan, colspan to span multiple grid squares.  Plot, scatter, pie, 
    scatter3d, hist, stackplot, bar, barh calls add data to the plot.
    
    Data is stored as follows:
        fig - a dictionary of figure params, as well as any commands to be
              executed against the figure at generation.
        sub - a dictionary containing subplots information indexed by a 
              2-tuple of row, col; if an axis is twinned or a colorbar is
              added, it will be a 3-tuple starting with the reference
              row, col then an index
        sub[key]['lines'] - contains each set of data to be added to the
              subplot, lines have a type to indicate which call to make
              to matplotlib subplot
        lines - pointers to all the line object for all the plots, so 
              they can be programmatically separated from the subplot
        cbs - colorbar instances to be used in subplots
    """
    def __init__(self,**kwargs):
        """
        Initiates figure with some commonly used defaults.  Use kwargs
        to override.
        """
        self.fig = {'commands':[]}
        self.sub = {}
        self.lines = []
        self.cbs = []
        esistyle = kwargs.pop('esistyle',False)
        if esistyle:
            self.fig['stylesheet'] = os.path.basename(ESI_STYLE_SHEET)
        else:
            self.fig['stylesheet'] = os.path.basename(STYLE_SHEET)
        plt.style.use(os.path.join(RELATIVE_LIB_PATH,'gobat',os.path.basename(self.fig['stylesheet'])))
        self.fig['title'] = kwargs.pop('title','')
        self.fig['figsize'] = kwargs.pop('figsize',plt.rcParams['figure.figsize'])
        self.fig['classification'] = kwargs.pop('classy','SECRET//NOFORN')
        self.fig['facecolor'] = kwargs.pop('facecolor',plt.rcParams['figure.facecolor'])
        self.fig['picker'] = kwargs.pop('picker',False)
        self.fig['customlegend'] = None
        
    def initAxes(self,axid,rowspan,colspan,threeD=False,colorbar={},combinelegend=False,mapplot=False,mapproj='PlateCarree()',table=None):
        """
        Initiates each axes in the sub dictionary, requires reference starting
        ax id, and a row and column span
        """
        self.sub[axid] = {'commands':[],
                          'lines':[],
                          'patches':[],
                          'features':[],
                          'rowspan':rowspan,
                          'colspan':colspan,
                          '3d':threeD,
                          'colorbar':colorbar,
                          'combinelegend':combinelegend,
                          'mapplot':mapplot,
                          'mapproj':mapproj,
                          'mapimg':None,
                          'table':table,
                          'customlegend':None}
        
    def buildExecString(self,command):
        """
        Given a command dictionary as follows:
            'cmd' - the matplotlib function as a string
            'args' - list of arguments to be ged into the function
            'kwargs' - dictionary of kwargs to be fed into function
                       can be two levels deep, which should support
                       most matplotlib function calls
        Returns the function built to be executed using exec() or eval(),
        calling object is added separately to provide flexibility
        """
        execString = command['cmd']+"("
        if command['args']:
            execString += ",".join(map(str,[self.multiDims(arg,[])
                                            for arg in command['args']]))
        if command['kwargs']:
            if command['args']:
                execString += ","
            execString += self.buildKwargs(command['kwargs'])
            execString = execString[:-1]
        execString += ")"
        return execString.replace('transform=','transform=ccrs.')
    
    def buildKwargs(self,kwargs):
        execString = ''
        for key in kwargs:
            if key == 'transform':
                execString += key+"="+kwargs[key].strip('\'')
            elif isinstance(kwargs[key],dict):
                execString += key+"=dict("+",".join([k+"="+str(self.multiDims(kwargs[key][k],[]))
                                                        for k in kwargs[key]])+")"
            elif isinstance(kwargs[key],str) or isinstance(kwargs[key],unicode):
                execString += key+"="+str(kwargs[key])
            else:
                execString += key+"="+str(self.multiDims(kwargs[key],[]))
            execString += ","
        return execString
    
    def multiDims(self,arr,newlist):
        if isinstance(arr,np.ndarray):
            if arr.ndim > 2:
                for nextarr in arr:
                    newlist.append([])
                    self.multiDims(nextarr,newlist[-1])
            elif arr.ndim == 2:
                for nextarr in arr:
                    newlist.append(list(nextarr))
            else:
                newlist = list(arr)
            return newlist
        else:
            return arr
        
    def createPlot(self,fname,**kwargs):
        try:
            if self.lines:
                pass
        except:
            self.lines = []
            for rowcol in self.sub:
                for line in self.sub['lines']:
                    self.lines.append(line)
        try:
            if self.cbs:
                pass
        except:
            self.cbs = []
        SAVEPNG = kwargs.pop('SAVEPNG',True)
        SAVEPKL = kwargs.pop('SAVEPKL',True)
        SHOW = kwargs.pop('SHOW',False)
        PERSIST = kwargs.pop('PERSIST',False)
        SAVEONLY = kwargs.pop('SAVEONLY',False)
        if SAVEONLY:
            self.savePkl(fname)
            return
        plt.style.use(os.path.join(RELATIVE_LIB_PATH,'gobat',os.path.basename(self.fig['stylesheet'])))
        fig = plt.figure(facecolor=self.fig['facecolor'],
                         figsize=self.fig['figsize'])
        global space
        space = ' '*(int(self.fig['figsize'][0])*15)
        numrows = 1
        numcols = 1
        for rowcol in self.sub:
            if len(rowcol) == 2:
                if rowcol[0]+self.sub[rowcol]['rowspan'] > numrows:
                    numrows = rowcol[0]+self.sub[rowcol]['rowspan']
                if rowcol[1]+self.sub[rowcol]['colspan'] > numcols:
                    numcols = rowcol[1]+self.sub[rowcol]['colspan']
        gs = gridspec.GridSpec(numrows,numcols,figure=fig)
        setformat = False
        rowcols = self.sub.keys()
        rowcols.sort()
        for rowcol in rowcols:
            if len(rowcol) == 2:
                cm = {None:None}
                othAx = {}
                if self.sub[rowcol]['3d']:
                    thisax = fig.add_subplot(gs[rowcol[0]:rowcol[0]+self.sub[rowcol]['rowspan'],
                                                rowcol[1]:rowcol[1]+self.sub[rowcol]['colspan']],
                                             projection='3d')
                elif 'mapplot' in self.sub[rowcol] and self.sub[rowcol]['mapplot']:
                    thisax = fig.add_subplot(gs[rowcol[0]:rowcol[0]+self.sub[rowcol]['rowspan'],
                                                rowcol[1]:rowcol[1]+self.sub[rowcol]['colspan']],
                                             projection=eval('ccrs.{}'.format(self.sub[rowcol]['mapproj']),{"ccrs":ccrs}))
                    lonScale = None
                    if 'central_longitude' in self.sub[rowcol]['mapproj']:
                        cloc = self.sub[rowcol]['mapproj'].find('central_longitude')+len('central_longitude')+1
                        loc = self.sub[rowcol]['mapproj'].find(',',cloc)
                        if loc > -1:
                            lonScale = 1.-(float(self.sub[rowcol]['mapproj'][cloc:loc])/360.)
                        else:
                            loc = self.sub[rowcol]['mapproj'].find(')',cloc)
                            if loc > -1:
                                lonScale = 1.-(float(self.sub[rowcol]['mapproj'][cloc:loc])/360.)
                else:
                    thisax = fig.add_subplot(gs[rowcol[0]:rowcol[0]+self.sub[rowcol]['rowspan'],
                                                rowcol[1]:rowcol[1]+self.sub[rowcol]['colspan']])
                for t in self.sub:
                    if len(t) == 3 and t[:2] == rowcol:
                        for command in self.sub[t]['commands']:
                            if command['cmd'].startswith('twin'):
                                execString = "thisax."+self.buildExecString(command)
                                othAx[t] = eval(execString,{},{"thisax":thisax})
                cbs = [(rc,self.sub[rc]['colorbar']['colorbarname']) for rc in rowcols
                           if len(rc) == 3 and rc[:2] == rowcol and self.sub[rc]['colorbar']]
                for rc,cb in cbs:
                    cm[cb] = plt.cm.get_cmap(cb)
                for line in deepcopy(self.sub[rowcol]['lines']):
                    if 'cmap' in line and line['cmap']:
                        line['cmap'] = plt.cm.get_cmap(line['cmap'])
                    if 'transform' in line:
                        line['transform'] = eval('ccrs.{}'.format(line['transform']),{"ccrs":ccrs})
                    sc = self.plotCall(thisax,line)
                    if line['plottype'] == 'plot':
                        setformat = True
                if self.sub[rowcol]['commands']:
                    for command in self.sub[rowcol]['commands']:
                        if not(command['cmd'].startswith('get_legend')) and not(command['cmd'] == 'legend'):
                            execString = "thisax."+self.buildExecString(command)
                            exec(execString,{"ccrs":ccrs},{"thisax":thisax})
                    if 'patches' in self.sub[rowcol] and self.sub[rowcol]['patches']:
                        for patch in self.sub[rowcol]['patches']:
                            execString ="thisax.add_patch(mpatches.{})".format(self.buildExecString(patch))
                            exec(execString,{"ccrs":ccrs,"mpatches":mpatches},{"thisax":thisax})
                for t in self.sub:
                    if len(t) == 3 and t[:2] == rowcol and not self.sub[t]['colorbar']:
                        for line in deepcopy(self.sub[t]['lines']):
                            if 'cmap' in line and line['cmap']:
                                line['cmap'] = plt.cm.get_cmap(line['cmap'])
                            if 'transform' in line:
                                line['transform'] = eval('ccrs.{}'.format(line['transform']),{"ccrs":ccrs})
                            sc = self.plotCall(othAx[t],line)
                            if line['plottype'] == 'plot':
                                setformat ==True
                        if self.sub[t]['commands']:
                            for command in self.sub[t]['commands']:
                                if command['cmd'] not in special_cmds and not([scmd for scmd in special_cmds if command['cmd'].startswith(scmd)]):
                                    execString = "othAx[t]."+self.buildExecString(command)
                                    exec(execString,{"ccrs":ccrs},{"othAx":othAx,"t":t})
                        if 'patches' in self.sub[t] and self.sub[t]['patches']:
                            for patch in self.sub[t]['patches']:
                                execString ="othAx[t].add_patch(mpatches.{})".format(self.buildExecString(patch))
                                exec(execString,{"ccrs":ccrs,"mpatches":mpatches},{"othAx":othAx,"t":t})
                        if setformat:
                            othAx[t].format_coord = general_format_coord(othAx[t],thisax)
                        lng = othAx[t].get_legend()
                        if lng:
                            if self.sub[t]['commands']:
                                for command in self.sub[t]['commands']:
                                    if command['cmd'].startswith('get_legend'):
                                        execString = "othAx[t]."+self.buildExecString(command)
                                        exec(execString,{"ccrs":ccrs},{"othAx":othAx,"t":t})
                            lng.draggable()
                h = []
                l = []
                if 'combinelegend' in self.sub[rowcol] and self.sub[rowcol]['combinelegend']:
                    h, l = thisax.get_legend_handles_labels()
                    for t in othAx:
                        h1,l1 = othAx[t].get_legend_handles_labels()
                        h += h1
                        l += l1
                if 'customlegend' in self.sub[rowcol] and self.sub[rowcol]['customlegend']:
                    h, l = self.sub[rowcol]['customlegend']
                    h = [eval('Line2D(hndl[0],hndl[1],{})'.format(self.buildKwargs(hndl[2])[:-1]),{'Line2D':Line2D},{'hndl':hndl})
                            for hndl in h]
                if self.sub[rowcol]['commands']:
                    for command in self.sub[rowcol]['commands']:
                        if command['cmd'] == 'legend':
                            if h:
                                execString = "thisax.legend(h,l,"+self.buildExecString(command)[7:]
                                exec(execString,{"ccrs":ccrs},{"thisax":thisax,"h":h,"l":l})
                            else:
                                execString = "thisax."+self.buildExecString(command)
                                exec(execString,{"ccrs":ccrs},{"thisax":thisax})
                lng = thisax.get_legend()
                if lng:
                    if self.sub[rowcol]['commands']:
                        for command in self.sub[rowcol]['commands']:
                            if command['cmd'].startswith('get_legend'):
                                execString = "thisax."+self.buildExecString(command)
                                exec(execString,{"ccrs":ccrs},{"thisax":thisax})
                    lng.draggable()
                for rc,cb in cbs:
                    thiscb = fig.colorbar(sc)
                    thiscb.set_label(self.sub[rc]['colorbar']['label'])
                if 'mapplot' in self.sub[rowcol] and self.sub[rowcol]['mapplot'] and self.sub[rowcol]['mapimg']:
                    EARTH_IMG = plt.imread(os.path.join(RELATIVE_LIB_PATH,'data',self.sub[rowcol]['mapimg']))
                    #EARTH_IMG = EARTH_IMG[::-1]
                    if lonScale:
                        thisax.set_global()
                        #EARTH_IMG = np.roll(EARTH_IMG,int(lonScale*np.size(EARTH_IMG,1)),axis=1)
                    thisax.imshow(EARTH_IMG,
                                        origin='upper',
                                        transform=ccrs.PlateCarree(),
                                        extent=[-180,180,-90,90])
                    #j.set_data(EARTH_IMG)
                if 'mapplot' in self.sub[rowcol] and self.sub[rowcol]['features']:
                    for feature in self.sub[rowcol]['features']:
                        featOfStrength = cfeature.ShapelyFeature(Reader(os.path.join(CfgDir,feature['fname'])).geometries(),
                                                                 eval('ccrs.{}'.format(feature['transform']),{"ccrs":ccrs}),
                                                                 **feature['kwargs'])
                        thisax.add_feature(featOfStrength)
                if 'table' in self.sub[rowcol] and self.sub[rowcol]['table']:
                    execString = "(thisax,"+self.buildExecString(self.sub[rowcol]['table']['command'])[1:]
                    the_table = eval('table.table'+execString,{"table":table},{"thisax":thisax})
                    if 'cellParams' in self.sub[rowcol]['table'] and (self.sub[rowcol]['table']['cellParams']['cellFontSize'] or
                                                                      self.sub[rowcol]['table']['cellParams']['cellHeight']):
                        prop=the_table.properties()
                        cells = prop['child_artists']
                        for cell in cells:
                            if self.sub[rowcol]['table']['cellParams']['cellFontSize']:
                                cell.set_fontsize(self.sub[rowcol]['table']['cellParams']['cellFontSize'])
                                cell.set_height(cell.get_height() * self.sub[rowcol]['table']['cellParams']['cellHeight']) 
                if setformat:
                    thisax.format_coord = general_format_coord(thisax)
        gotTitle = False
        figlng = None
        figh = []
        figl = []
        if 'customlegend' in self.fig and self.fig['customlegend']:
            figh, figl = self.sub[rowcol]['customlegend']
            figh = [eval('Line2D(hndl[0],hndl[1],{})'.format(self.buildKwargs(hndl[2])[:-1]),{'Line2D':Line2D},{'hndl':hndl})
                    for hndl in figh]
        if self.fig['commands']:
            for command in self.fig['commands']:
                if not(command['cmd'].startswith('get_legend')) and not(command['cmd'] == 'legend'):
                    if 'title' in command['cmd']:
                        gotTitle = True
                    execString = "fig."+self.buildExecString(command)
                    exec(execString,{"ccrs":ccrs},{"fig":fig})
            for command in self.fig['commands']:
                if command['cmd'] == 'legend':
                    if h:
                        execString = "fig.legend(figh,figl,"+self.buildExecString(command)[7:]
                        figlng = eval(execString,{"ccrs":ccrs},{"fig":fig,"figh":figh,"figl":figl})
                    else:
                        execString = "fig."+self.buildExecString(command)
                        figlng = eval(execString,{"ccrs":ccrs},{"fig":fig})
        if figlng:
            if self.fig['commands']:
                for command in self.fig['commands']:
                    if command['cmd'].startswith('get_legend'):
                        execString = "fig."+self.buildExecString(command)
                        exec(execString,{"ccrs":ccrs},{"fig":fig})
            figlng.draggable()
        if not gotTitle and self.fig['title']:
            fig.suptitle(self.fig['title'])
        fig.text(.03,.97,self.fig['classification'],fontdict=figClassFD,ha='left',color='r')
        fig.text(.97,.03,self.fig['classification'],fontdict=figClassFD,ha='right',color='r')
        if self.fig['picker']:
            fig.canvas.mpl_connect('pick_event',on_pick)
            fig.canvas.mpl_connect('button_release_event',on_release)
        if PERSIST:
            plt.show()
        else:
            if SAVEPNG:
                fig.savefig(os.path.splitext(fname)[0]+'.png',facecolor=self.fig['facecolor'],format='png')
            if SAVEPKL:
                self.savePkl(fname)
            if SHOW:
                plt.show()
            plt.close(fig)
            
    def savePkl(self,fname):
        try:
            if self.lines:
                pass
        except:
            self.lines = []
            for rowcol in self.sub:
                for line in self.sub['lines']:
                    self.lines.append(line)
        try:
            if self.cbs:
                pass
        except:
            self.cbs = []
        cPickle.dump({'fig':self.fig,'sub':self.sub,'lines':self.lines,'cbs':self.cbs},
                     file(os.path.splitext(fname)[0]+'.pklplt','wb'),
                     cPickle.HIGHEST_PROTOCOL)
        
    def plotCall(self,ax,line):
        if line['plottype'] == 'plot':
            sc = ax.plot(line['x'],line['y'],line['fmt'],
                         **{k:line[k] for k in line
                            if k not in exclude_list})
        elif line['plottype'] == 'scatter':
            sc = ax.scatter(line['x'],line['y'],
                         **{k:line[k] for k in line
                            if k not in exclude_list})
        elif line['plottype'] == 'pie':
            sc = ax.pie(line['x'],
                         **{k:line[k] for k in line
                            if k not in exclude_list})
        elif line['plottype'] == 'scatter3d':
            sc = ax.scatter(line['x'],line['y'],line['z'],
                         **{k:line[k] for k in line
                            if k not in exclude_list})
        elif line['plottype'] == 'stackplot':
            sc = ax.stackplot(line['x'],line['y'],
                         **{k:line[k] for k in line
                            if k not in exclude_list})
        elif line['plottype'] == 'hist':
            sc = ax.hist(line['x'],line['bins'],
                         **{k:line[k] for k in line
                            if k not in exclude_list})
        elif line['plottype'] == 'bar':
            sc = ax.bar(line['x'],line['height'],width=line['width'],bottom=line['bottom'],align=line['align'],
                         **{k:line[k] for k in line
                            if k not in exclude_list})
        elif line['plottype'] == 'barh':
            sc = ax.barh(line['x'],line['width'],height=line['height'],left=line['left'],align=line['align'],
                         **{k:line[k] for k in line
                            if k not in exclude_list})
        return sc
    
    def add_subplot(self,axid=(0,0),rowspan=1,colspan=1,threeD=False,combinelegend=False,mapplot=False,mapproj='PlateCarree()'):
        if axid not in self.sub:
            self.initAxes(axid,rowspan,colspan,threeD,{},combinelegend,mapplot,mapproj)
            return axid
        else:
            print('Axes location already initiated')
            return []
        
    def plot(self,x,y,fmt='',axid=(0,0),**kwargs):
        # Attempt to set the reference to the correct axis,
        # return with message if invalid
        # axid not required, will default to single subplot
        if axid in self.sub:
            self.sub[axid]['lines'].append({})
            self.lines.append(self.sub[axid]['lines'][-1])
        else:
            print('Invalid axis reference')
            return
        # last entry in axis lines is a blank dictionary
        self.sub[axid]['lines'][-1]['plottype'] = 'plot'
        self.sub[axid]['lines'][-1]['x'] = x
        self.sub[axid]['lines'][-1]['y'] = y
        self.sub[axid]['lines'][-1]['fmt'] = fmt
        self.sub[axid]['lines'][-1].update(kwargs)

    def scatter(self,x,y,axid=(0,0),**kwargs):
        # Attempt to set the reference to the correct axis,
        # return with message if invalid
        # axid not required, will default to single subplot
        if axid in self.sub:
            self.sub[axid]['lines'].append({})
            self.lines.append(self.sub[axid]['lines'][-1])
        else:
            print('Invalid axis reference')
            return
        # last entry in axis lines is a blank dictionary
        self.sub[axid]['lines'][-1]['plottype'] = 'scatter'
        self.sub[axid]['lines'][-1]['x'] = x
        self.sub[axid]['lines'][-1]['y'] = y
        self.sub[axid]['lines'][-1].update(kwargs)

    def scatter3d(self,x,y,z,axid=(0,0),**kwargs):
        # Attempt to set the reference to the correct axis,
        # return with message if invalid
        # axid not required, will default to single subplot
        if axid in self.sub:
            self.sub[axid]['lines'].append({})
            self.lines.append(self.sub[axid]['lines'][-1])
        else:
            print('Invalid axis reference')
            return
        # last entry in axis lines is a blank dictionary
        self.sub[axid]['lines'][-1]['plottype'] = 'scatter3d'
        self.sub[axid]['lines'][-1]['x'] = x
        self.sub[axid]['lines'][-1]['y'] = y
        self.sub[axid]['lines'][-1]['z'] = z
        self.sub[axid]['lines'][-1].update(kwargs)

    def pie(self,sizes,fmt='',axid=(0,0),**kwargs):
        # Attempt to set the reference to the correct axis,
        # return with message if invalid
        # axid not required, will default to single subplot
        if axid in self.sub:
            self.sub[axid]['lines'].append({})
            self.lines.append(self.sub[axid]['lines'][-1])
        else:
            print('Invalid axis reference')
            return
        # last entry in axis lines is a blank dictionary
        self.sub[axid]['lines'][-1]['plottype'] = 'pie'
        self.sub[axid]['lines'][-1]['x'] = sizes
        self.sub[axid]['lines'][-1].update(kwargs)

    def stackplot(self,x,y,axid=(0,0),**kwargs):
        # Attempt to set the reference to the correct axis,
        # return with message if invalid
        # axid not required, will default to single subplot
        if axid in self.sub:
            self.sub[axid]['lines'].append({})
            self.lines.append(self.sub[axid]['lines'][-1])
        else:
            print('Invalid axis reference')
            return
        # last entry in axis lines is a blank dictionary
        self.sub[axid]['lines'][-1]['plottype'] = 'stackplot'
        self.sub[axid]['lines'][-1]['x'] = x
        self.sub[axid]['lines'][-1]['y'] = y
        self.sub[axid]['lines'][-1].update(kwargs)

    def hist(self,x,bins,axid=(0,0),**kwargs):
        # Attempt to set the reference to the correct axis,
        # return with message if invalid
        # axid not required, will default to single subplot
        if axid in self.sub:
            self.sub[axid]['lines'].append({})
            self.lines.append(self.sub[axid]['lines'][-1])
        else:
            print('Invalid axis reference')
            return
        # last entry in axis lines is a blank dictionary
        self.sub[axid]['lines'][-1]['plottype'] = 'hist'
        self.sub[axid]['lines'][-1]['x'] = x
        self.sub[axid]['lines'][-1]['bins'] = bins
        self.sub[axid]['lines'][-1].update(kwargs)

    def bar(self,x,height,axid=(0,0),width=0.8,bottom=None,align='center',**kwargs):
        # Attempt to set the reference to the correct axis,
        # return with message if invalid
        # axid not required, will default to single subplot
        if axid in self.sub:
            self.sub[axid]['lines'].append({})
            self.lines.append(self.sub[axid]['lines'][-1])
        else:
            print('Invalid axis reference')
            return
        # last entry in axis lines is a blank dictionary
        self.sub[axid]['lines'][-1]['plottype'] = 'bar'
        self.sub[axid]['lines'][-1]['x'] = x
        self.sub[axid]['lines'][-1]['height'] = height
        self.sub[axid]['lines'][-1]['width'] = width
        self.sub[axid]['lines'][-1]['bottom'] = bottom
        self.sub[axid]['lines'][-1]['align'] = align
        self.sub[axid]['lines'][-1].update(kwargs)

    def barh(self,x,width,axid=(0,0),height=0.8,left=None,align='center',**kwargs):
        # Attempt to set the reference to the correct axis,
        # return with message if invalid
        # axid not required, will default to single subplot
        if axid in self.sub:
            self.sub[axid]['lines'].append({})
            self.lines.append(self.sub[axid]['lines'][-1])
        else:
            print('Invalid axis reference')
            return
        # last entry in axis lines is a blank dictionary
        self.sub[axid]['lines'][-1]['plottype'] = 'barh'
        self.sub[axid]['lines'][-1]['x'] = x
        self.sub[axid]['lines'][-1]['width'] = width
        self.sub[axid]['lines'][-1]['height'] = height
        self.sub[axid]['lines'][-1]['left'] = left
        self.sub[axid]['lines'][-1]['align'] = align
        self.sub[axid]['lines'][-1].update(kwargs)

    def add_colorbar(self,axid=(0,0),colorbarname='jet',label=''):
        if axid in self.sub:
            cnt = 0
            for t in self.sub:
                if len(t) == 3 and t[:2] == axid:
                    cnt+=1
            newref = axid+(cnt,)
            self.initAxes(newref,1,1,False,{'colorbarname':colorbarname,
                                            'label':label})
            return newref
        else:
            print('Invalid axis reference.')
            
    def twin(self,axid=(0,0),axis='x',**kwargs):
        if axid in self.sub:
            cnt = 0
            for t in self.sub:
                if len(t) == 3 and t[:2] == axid:
                    cnt+=1
            newref = axid+(cnt,)
            self.initAxes(newref,1,1)
            self.parseCommand(newref,'twin{}'.format(axis),[kwargs])
            return newref
        else:
            print('Invalid axis reference.')
            return []
        
    def add_map(self,filename,axid=(0,0),**kwargs):
        if not os.path.isfile(os.path.join(RELATIVE_LIB_PATH,'data',filename)):
            print('{} not in ./src/data'.format(filename))
        elif axid not in self.sub:
            print('Invalid axis reference.')
        elif not self.sub[axid]['mapplot']:
            print('Subplot is not a Map Plot.')
        else:
            self.sub[axid]['mapimg'] = filename
            
    def add_patch(self,obj,cmd,cargs):
        if obj != 'fig' and not (isinstance(obj,tuple) and obj in self.sub):
            print('Unrecognized reference object.')
            return
        if not isinstance(cmd,str) or not isinstance(cargs,list):
            print(obj,cmd,cargs)
            print('Invalid input to parseCommand.')
            return
        # OK now do stuff
        if obj == 'fig':
            thisthing = self.fig
        else:
            thisthing = self.sub[obj]
        thisthing['patches'].append({'cmd':cmd,'args':[],'kwargs':{}})
        for carg in cargs:
            if isinstance(carg,list):
                for car in carg:
                    if isinstance(car,str) or isinstance(car,unicode):
                        thisthing['patches'][-1]['args'].append("'''"+car+"'''")
                    else:
                        thisthing['patches'][-1]['args'].append(car)
            elif isinstance(carg,dict):
                for car in carg:
                    if isinstance(carg[car],dict):
                        thisthing['patches'][-1]['kwargs'][car] = {}
                        for k in carg[car]:
                            if isinstance(carg[car][k],str) or isinstance(car,unicode):
                                thisthing['patches'][-1]['kwargs'][car][k] = "'''"+carg[car][k]+"'''"
                            else:
                                thisthing['patches'][-1]['kwargs'][car][k] = carg[car][k]
                    else:
                        if isinstance(carg[car],str) or isinstance(carg[car],unicode):
                            thisthing['patches'][-1]['kwargs'][car] = "'''"+carg[car]+"'''"
                        else:
                            thisthing['patches'][-1]['kwargs'][car] = carg[car]
                            
    def add_feature(self,filename,transform,axid=(0,0),**kwargs):
        if not os.path.isfile(os.path.join(CfgDir,filename[lenCfgDir:])):
            print('{} not in cartopy config dir.'.format(filename))
        elif axid not in self.sub:
            print('Invalid axis reference.')
        elif not self.sub[axid]['mapplot']:
            print('Subplot is not a Map Plot.')
        else:
            self.sub[axid]['features'].append({'fname':filename[lenCfgDir:],'transform':transform,'kwargs':kwargs})
            
    def add_table(self,axid,
                  cellText=None, cellColours=None,
                  cellLoc='right', colWidths=None,
                  rowLabels=None, rowColours=None, rowLoc='left',
                  colLabels=None, colColours=None, colLoc='center',
                  loc='bottom', bbox=None, edges='closed', 
                  cellFontSize=None,cellHeight=None,
                  kwargs={}):
        if not (isinstance(axid,tuple) and axid in self.sub):
            print('Unrecognized reference object.')
            return
        # OK now do stuff
        self.sub[axid]['table'] = {'ax':axid,'command':{'cmd':'','args':[cellText,cellColours,
                                                                         "'''"+cellLoc+"'''",colWidths,
                                                                         rowLabels,rowColours,"'''"+rowLoc+"'''",
                                                                         colLabels,colColours,"'''"+colLoc+"'''",
                                                                         "'''"+loc+"'''",bbox,"'''"+edges+"'''"],
                                                                'kwargs':kwargs},
                                   'cellParams':{'cellFontSize':cellFontSize,
                                                 'cellHeight':cellHeight}}

    def add_customlegend(self,obj,handles,labels,**kwargs):
        if obj != 'fig' and not (isinstance(obj,tuple) and obj in self.sub):
            print('Unrecognized reference object.')
            return
        if not isinstance(handles,list) or not isinstance(labels,list) or len(handles) != len(labels):
            print(obj,handles,labels)
            print('Invalid input to parseCommand.')
            return
        # OK now do stuff        
        if obj == 'fig':
            thisthing = self.fig
        else:
            thisthing = self.sub[obj]
        newhandles = []
        for a,b,c in handles:
            newc = {}
            for k in c:
                if isinstance(c[k],dict):
                    newc[k] = {}
                    for k1 in c[k]:
                        if isinstance(c[k][k1],str) or isinstance(c[k][k1],unicode):
                            newc[k][k1] = "'''"+c[k][k1]+"'''"
                        else:
                            newc[k][k1] = c[k][k1]
                elif isinstance(c[k],str) or isinstance(c[k],unicode):
                    newc[k] = "'''"+c[k]+"'''"
                else:
                    newc[k] = c[k]
            newhandles.append((a,b,newc))
        thisthing['customlegend'] = (newhandles,labels)
        self.parseCommand(obj,'legend',[kwargs])
            
    def retrievePlot(self,fname):
        if os.path.isfile(fname):
            tempDict = cPickle.load(file(fname,'rb'))
            if 'fig' in tempDict and 'sub' in tempDict:
                self.fig = deepcopy(tempDict['fig'])
                self.sub = deepcopy(tempDict['sub'])
                if 'lines' in tempDict:
                    self.lines = deepcopy(tempDict['lines'])
                if 'cbs' in tempDict:
                    self.cbs = deepcopy(tempDict['cbs'])
            else:
                print('Invalid file.')
        else:
            print('Invalid file.')
            
    def parseCommand(self,obj,cmd,cargs):
        if obj != 'fig' and not (isinstance(obj,tuple) and obj in self.sub):
            print('Unrecognized reference object.')
            return
        if not isinstance(cmd,str) or not isinstance(cargs,list):
            print(obj,cmd,cargs)
            print('Invalid input to parseCommand.')
            return
        # OK now do stuff
        if obj == 'fig':
            thisthing = self.fig
        else:
            thisthing = self.sub[obj]
        thisthing['commands'].append({'cmd':cmd,'args':[],'kwargs':{}})
        for carg in cargs:
            if isinstance(carg,list):
                for car in carg:
                    if isinstance(car,str) or isinstance(car,unicode):
                        thisthing['commands'][-1]['args'].append("'''"+car+"'''")
                    else:
                        thisthing['commands'][-1]['args'].append(car)
            elif isinstance(carg,dict):
                for car in carg:
                    if isinstance(carg[car],dict):
                        thisthing['commands'][-1]['kwargs'][car] = {}
                        for k in carg[car]:
                            if isinstance(carg[car][k],str) or isinstance(carg[car][k],unicode):
                                thisthing['commands'][-1]['kwargs'][car][k] = "'''"+carg[car][k]+"'''"
                            else:
                                thisthing['commands'][-1]['kwargs'][car][k] = carg[car][k]
                    else:
                        if isinstance(carg[car],str) or isinstance(car,unicode):
                            thisthing['commands'][-1]['kwargs'][car] = "'''"+carg[car]+"'''"
                        else:
                            thisthing['commands'][-1]['kwargs'][car] = carg[car]
                            
    def reparseCommand(self,obj,cmd,cargs):
        if obj!= 'fig' and not (isinstance(obj,tuple) and obj in self.sub):
            print('Unrecognized reference object.')
            return
        if not isinstance(cmd,str) or not isinstance(cargs,list):
            print(obj,cmd,cargs)
            print('Invalid input to parseCommand.')
            return
        
        return
        # For now, don't do stuff
        # OK now do stuff
        if obj == 'fig':
            thisthing = self.fig
        else:
            thisthing = self.sub[obj]
        thisthing['commands'] = [c for c in thisthing['commands']
                                    if c['cmd'] != cmd]
        self.parseCommand(obj,cmd,cargs)
        
#    def getAxisInfo(self,axid=(0,0)):
#        if not (isinstance(axid,tuple) and axid in self.sub):
#            print('Unrecognized reference object.')
#            return
#        axinfo = {'labels':{'x':'',
#                            'y':'',
#                            'z':''},
#                  'backgroundcolor':plt.rcParams['axes.facecolor'],
#                  'colorbarnames':[self.sub[cb]['colorbar']['colorbarname'] for cb in self.sub
#                                       if len(cb) == 3 and cb[:2] == axid and self.sub[cb]['colorbar']],
#                  'lines':[]}
#        for command in self.sub[axid]['commands']:
#            for axl in ('x','y','z'):
#                if command['cmd'] == 'set_{}label'.format(axl):
#                    axinfo[axl] = command['args'][0]
#            if command['cmd'] == 'set_facecolor':
#                axinfo['backgroundcolor'] = command['args'][0] # Assuming this, may be wrong, not a likely case
#        for line in deepcopy(self.sub[axid]['lines']):
#            axinfo['lines'].append({})
#            loopdict = {'markersize':[5,'ms'],
#                        'linewidth':[1,'lw'],
#                        'label':'',
#                        'color':['','c'],
#                        'marker':'',
#                        'symbolcode':'',
#                        'cmap':''}
#            for kwname in loopdict:
#                if isinstance(loopdict[kwname],list):
#                    if kkwname in line:
#                        axinfo['lines'][-1][kwname] = line[kwname]
#                    axinfo['lines'][-1][kwname] = line.pop(loopdict[kwname][1],loopdict[kwname][0])
#                else:
#                    axinfo['lines'][-1][kwname] = line.pop(kwname,loopdict[kwname])
#        return axinfo
        
if __name__ == '__main__':
    if True:
        pltr = Plotter(combinelegend=True)
        pltr.add_subplot()
        x = np.random.randint(0,100,20)
        y = np.random.randint(0,100,20)
        pltr.scatter(x,y,label='FML')
        pltr.parseCommand((0,0),'legend',[[]])
        ax1 = pltr.add_subplot((1,0))
        pltr.scatter(y,x,axid=ax1,label='FYL')
#        pltr.parseCommand(ax1,'legend',[[]])
#        pltr.parseCommand(ax1,'legend',[dict(loc='best')])
        l = ['FudgeMyLife']
        h = [([0],[0],dict(markerfacecolor='red',marker='d',color='w'))]
        pltr.add_customlegend(ax1,h,l,loc='best')
        ax2 = pltr.add_subplot((2,0))
        pltr.scatter(y,y,ax2,label='fudge dragon')
        
#        pltr.add_colorbar(colorbarname='bone',label='FML')
        pltr.parseCommand(ax2,'legend',[[]])
        pltr.parseCommand('fig','legend',[dict(prop=dict(size=6),loc='best',ncol=4)])
        pltr.createPlot('test.png',PERSIST=True)
    if False:
        jobs = []
        add = jobs.append
        ext = jobs.extend
        maxThreads = False
        nthreads = 1
        dashOp = False
        for i in xrange(1,len(sys.argv)):
            if dashOp:
                dashOp = False
                continue
            if sys.argv[i] == '--max-threads':
                maxThreads = True
                nthreads = cpu_count()
            elif sys.argv[i] == '-nt':
                dashOp = True
                maxThreads = True
                try:
                    nthreads = int(sys.argv[i+1])
                except:
                    print(NOTES)
                    sys.exit(1)
            elif os.path.isfile(os.path.realpath(sys.argv[i])):
                add(os.path.realpath(sys.argv[i]))
            elif os.path.isdir(os.path.realpath(sys.argv[i])):
                ext(glob.glob(os.path.join(os.path.realpath(sys.argv[i]),'*.pklplt')))
        if jobs:
            PNGerator(jobs,nthreads=nthreads)
        else:
            print(NOTES)
    if False:
        """
        Demo of scatter plot with varying marker colors and sizes.
        """
        import numpy as np
        import matplotlib.pyplot as plt
        import matplotlib.cbook as cbook
        
        datafile = cbook.get_sample_data('/home/jacob/anaconda2/pkgs/matplotlib-1.5.1-np110py27_0/lib/python2.7/site-packages/matplotlib/mpl-data/sample_data/goog.npy')
        try:
            price_data = np.load(datafile, encoding='bytes').view(np.recarray)
        except TypeError:
            price_data = np.load(datafile).view(np.recarray)
        price_data = price_data[-250:] # get the most recent 250 trading days
        
        delta1 = np.diff(price_data.adj_close)/price_data.adj_close[:-1]
        
        # Marker size in units of points^2
        volume = (15 * price_data.volume[:-2] / price_data.volume[0])**2
        close = 0.003 * price_data.close[:-2] / 0.003 * price_data.open[:-2]
        pltr = Plotter(ncols=2)
        pltr.add_subplot((0,0))
        pltr.scatter(delta1[:-1],delta1[1:],c=close,s=volume,alpha=0.5)
        pltr.parseCommand((0,0),'set_xlabel',[[r'$\Delta_i$'],dict(fontsize=15)])
        pltr.parseCommand((0,0),'set_ylabel',[[r'$\Delta_{i+1}$'],dict(fontsize=15)])
        pltr.parseCommand((0,0),'set_title',[['Volume and percent change']])
        pltr.parseCommand((0,0),'grid',[[True]])
        pltr.parseCommand('fig','tight_layout',[])
        """
        Basic Pie Chart
        """
        labels = 'Frogs','Hogs','Dogs','Logs'
        sizes = [15, 30, 45, 10]
        explode = (0, 0.1, 0, 0)
        pltr.add_subplot((0,1))
        pltr.pie(sizes,(0,1),explode=explode,labels=labels,autopct='%1.1f%%',
                 shadow=True,startangle=90)
        pltr.parseCommand((0,1),'axis',[['equal']])
        pltr.createPlot('',SAVEPNG=False,SAVEPKL=False,SHOW=True)
    if False:
        """
        Grid Spec Example
        """
        import numpy as np
        pltr = Plotter()
        pltr.parseCommand('fig','tight_layout',[])
        pltr.add_subplot((0,0),1,2)
        pltr.plot(np.arange(0,1e6,1000),np.arange(0,1e6,1000),'',(0,0))
        pltr.parseCommand((0,0),'set_ylabel',[['YLabel0']])
        pltr.parseCommand((0,0),'set_xlabel',[['XLabel0']])
        for i in range(2):
            pltr.add_subplot((1,i))
            pltr.parseCommand((1,i),'set_ylabel',[['YLabel1 %d'%i]])
            pltr.parseCommand((1,i),'set_xlabel',[['XLabel1 %d'%i]])
        pltr.createPlot('',SAVEPNG=False,SAVEPKL=False,SHOW=True)
    if False:
        pltr = Plotter()
        pltr.add_subplot((0,0),1,3)
        pltr.add_subplot((1,0),1,2)
        pltr.add_subplot((1,2),2,1)
        pltr.add_subplot((2,0))
        pltr.add_subplot((2,1))
        pltr.parseCommand((0,0),'set_xlabel',[['GridSpec']])
        pltr.parseCommand('fig','tight_layout',[])
        pltr.createPlot('',SAVEPNG=False,SAVEPKL=False,SHOW=True)
    if False:
        ny_lon, ny_lat = -75., 43.
        delhi_lon, delhi_lat = 77.23, 28.61
        mapimg = 'bluemarble_8192x4096.png'
        pltr = Plotter()
        ax = pltr.add_subplot(mapplot=True)
        pltr.add_map(mapimg)
        pltr.add_feature(ADMIN0_COUNTRIES_NAME, 'PlateCarree()', facecolor='none', color='grey', alpha=0.7)
        pltr.add_patch(ax, 'Ellipse', [dict(xy=[-70,40],height = 10., width = 10., color='red', alpha = 0.3, \
                                            transform = 'PlateCarree()')])
        pltr.plot([ny_lon,dehli_lon],[ny_lat,delhi_lat],axid=ax,
                  color='blue',lw=2,marker='o',
                  transform='Geodetic()')
        pltr.plot([ny_lon,dehli_lon],[ny_lat,delhi_lat],axid=ax,
                  color='gray',ls='--',
                  transform='PlateCarree()')
        pltr.parseCommand(ax,'text',[[ny_lon-3,ny_lat-12,'New York'],
                                     dict(ha='right',transform='Geodetic()')])
        pltr.parseCommand(ax,'text',[[delhi_lon+3,delhi_lat-12,'New York'],
                                     dict(ha='left',transform='Geodetic()')])
        pltr.createPlot('test.png',SAVEONLY=True)
    if False:
        """
        ==========
        Table Demo
        ==========
        
        Demo of table function to display a table within a plot.
        """
        OPTION = 3
        # 1 - origninal
        # 2 - stack overflow fix
        # 3 - hammy's cell stuff that is more kitti
        import numpy as np
        import matplotlib.pyplot as plt
        
        
        data = [[ 66386, 174296,  75131, 577908,  32015],
                [ 58230, 381139,  78045,  99308, 160454],
                [ 89135,  80552, 152558, 497981, 603535],
                [ 78415,  81858, 150656, 193263,  69638],
                [139361, 331509, 343164, 781380,  52269]]
        
        columns = ('Freeze', 'Wind', 'Flood', 'Quake', 'Hail')
        rows = ['%d year' % x for x in (100, 50, 20, 10, 5)]
        
        values = np.arange(0, 2500, 500)
        value_increment = 1000
        
        # Get some pastel shades for the colors
        colors = plt.cm.BuPu(np.linspace(0, 0.5, len(rows)))
        n_rows = len(data)
        
        index = np.arange(len(columns)) + 0.3
        bar_width = 0.4
        
        # Initialize the vertical-offset for the stacked bar chart.
        y_offset = np.zeros(len(columns))
        
        pltr = Plotter()
        ax = pltr.add_subplot()
        # Plot bars and create text labels for the table
        cell_text = []
        for row in range(n_rows):
            pltr.bar(index, data[row], ax, bar_width, bottom=y_offset, color=colors[row])
#            plt.bar(index, data[row], bar_width, bottom=y_offset, color=colors[row])
            y_offset = y_offset + data[row]
            cell_text.append(['%1.1f' % (x / 1000.0) for x in y_offset])
        # Reverse colors and text labels to display the last value at the top.
        colors = colors[::-1]
        cell_text.reverse()
        
        # Add a table at the bottom of the axes
#        if OPTION == 1 or OPTION == 3:
        print cell_text
        pltr.add_table(ax,cellText=cell_text,
                              rowLabels=rows,
                              rowColours=colors,
                              colLabels=columns,
                              loc='bottom',
                              colLoc='center',
                              rowLoc='center',
                              cellFontSize=10,
                              cellHeight=1.4)
#            the_table = plt.table(cellText=cell_text,
#                                  rowLabels=rows,
#                                  rowColours=colors,
#                                  colLabels=columns,
#                                  loc='bottom',
#                                  colLoc='center',
#                                  rowLoc='center')
#        elif OPTION == 2:
#            the_table = plt.table(cellText=cell_text,
#                                  rowLabels=rows,
#                                  rowColours=colors,
#                                  colLabels=columns,
#                                  loc='bottom',
#                                  colLoc='center',
#                                  rowLoc='center',
#                                  bbox=[0, -0.3, 1, 0.275])
        
#        if False:
#            prop=the_table.properties()
#            cells = prop['child_artists']
#            for cell in cells:
#                if OPTION != 3:
#                    continue
#                cell.set_fontsize(10)
#                #cell.set_facecolor('red')
#                # this works if you leave off the bbox from the original call
#                cell.set_height(cell.get_height() * 1.4)
#                # don't seem to work
#                #cell['height'] =1
#                #cell.set_height(1)
#                #cell.set_visible(False)
        
        # Adjust layout to make room for the table:
#        if OPTION == 1:
#            plt.subplots_adjust(left=0.2, bottom=0.2)
#        elif OPTION == 2:
#            plt.subplots_adjust(left=0.2, bottom=0.2)
#        elif OPTION == 3:
        pltr.parseCommand('fig','subplots_adjust',[dict(left=0.2, bottom=0.35, right=0.95)])
#            plt.subplots_adjust(left=0.2, bottom=0.25, right=0.95)
        
        pltr.parseCommand(ax,'set_ylabel',[["Loss in ${0}'s".format(value_increment)]])
#        plt.ylabel("Loss in ${0}'s".format(value_increment))
        pltr.parseCommand(ax,'set_yticks',[[values * value_increment, ['%d' % val for val in values]]])
#        plt.yticks(values * value_increment, ['%d' % val for val in values])
        pltr.parseCommand(ax,'set_xticks',[[[]]])
#        plt.xticks([])
        pltr.parseCommand(ax,'set_title',[['Loss by Disaster']])
#        plt.title('Loss by Disaster')
        pltr.createPlot('',SAVEPNG=False,SAVEPKL=False,SHOW=True)
        
#        plt.show()        
