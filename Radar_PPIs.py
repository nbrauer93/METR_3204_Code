#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb  2 21:21:09 2022
@author: noahbrauer
"""
#Import the librairies

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset, num2date, MFDataset
import netCDF4 as nc
import glob
import imageio
import os

#Load in the NetCDF files

files = glob.glob('*.nc')

#Let's parse the end of the file name, then sort to grab indices

times_parsed = []
times_string = []

for i in range(len(files)):  
    
    first_split = files[i].split("_")[2]
    second_split = first_split.split(".")[0]
    
    #Remove first zero from string:
        
    third_split = second_split[1:]
    times_parsed.append(third_split)
    
    times_used = third_split[0:3]
    times_string.append(times_used)
   

#Now sort times

times_ordered_index = np.argsort(times_parsed)    


times_ordered = [files[i] for i in times_ordered_index]




#%%


#order time

time_array = np.array(times_string)
time_array_sort = [time_array[i] for i in times_ordered_index]


    
#%%
#Open one file to retrieve lat-lon; You will need to modify this line.

file = 'KFTG_20220202_083500.nc'

nc = Dataset(file, 'r')

latitude = nc.variables['lat'][:]
longitude = nc.variables['lon'][:]


#Define a lat-lon grid for plotting purposes 
lat2,lon2 = np.meshgrid(latitude, longitude)


#Extract reflectivity (or any other vairables) from the list of files for your event:

for file in range(len(times_ordered)):
    
    data = Dataset(times_ordered[file], 'r')
    
    #Extract the reflectivity data
    zh = data.variables['Reflectivity'][:]
    
    #Mask out all values < 0
    zh[zh<0] = np.nan
    
    #Now plot
    plt.figure(figsize=(20,20))
    
    #Colorbar interval
    cmin = 0; cmax = 60; cint = 2; clevs = np.round(np.arange(cmin,cmax,cint),2)
    
    #Change your lat-lon domain to encompass your radar site:
    xlim = np.array([-106,-103.]); ylim = np.array([38,41])
   
    #Set up the projection for plotting
    m = Basemap(projection='cyl',lon_0=np.mean(xlim),lat_0=np.mean(ylim),llcrnrlat=ylim[0],urcrnrlat=ylim[1],llcrnrlon=xlim[0],urcrnrlon=xlim[1],resolution='i')
    m.drawstates(); m.drawcountries()
    m.drawcounties()
    
    #Plot your data here:
    cs = m.contourf(lon2,lat2,zh[0,:,:].T, clevs, cmap = 'turbo', extend = 'both')
    
    #If you want to have a watermark, this needs to be changed - off not, comment out. 
    x_loc = -103.75
    y_loc = 38.15
    label = '@NOAABrauer'
    plt.text(x_loc, y_loc, label, size = 24)
    
    #Plot the location of a major city for geographical reference - Change this depending on your location
    x = -104.99
    y = 39.74
    
    m.plot(x,y,'or', markerfacecolor= 'w', markersize = 14)
   
    #Add a colorbar
    cbar = plt.colorbar()
    cbar.ax.tick_params(labelsize = 26)
    cbar.set_label(label = '[dBZ]',size = 26)
        
    #Add a title - You will need to change this depending on your event   
    plt.title(r'KFTG 02/02 ' + time_array_sort[file] + ' UTC' + ' $0.5^{o} Z_{H}$', size = 40)
    plt.show()
    

