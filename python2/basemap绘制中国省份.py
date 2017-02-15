

#-*- coding: utf-8 -*-
import time

start = time.clock()
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap 
from matplotlib.patches import Polygon

fig = plt.figure()
ax1 = fig.add_axes([0.1,0.1,0.8,0.8])

bmap = Basemap(llcrnrlon=87.33, 
              llcrnrlat=3.01, 
              urcrnrlon=138.16, 
              urcrnrlat=53.123,
            projection='lcc',lat_1=33,lat_2=45,lon_0=120, ax=ax1,resolution='l')
            
# bmap = Basemap(llcrnrlon=80.33, 
#               llcrnrlat=3.01, 
#               urcrnrlon=138.16, 
#               urcrnrlat=56.123,
#              resolution='h', projection='cass', lat_0 = 42.5,lon_0=120)
#              
             
shp_info = bmap.readshapefile("D:\\GoogleDownload\\CHN_adm_shp\\CHN_adm1",'states',drawbounds=False)

for info, shp in zip(bmap.states_info, bmap.states):
    proid = info['NAME_1']
    if proid == 'Guangdong':
        poly = Polygon(shp,facecolor='g',edgecolor='b', lw=0.8)
        ax1.add_patch(poly)
    
bmap.drawcoastlines()
#bmap.drawcountries()
bmap.drawparallels(np.arange(3,55,10),labels=[1,0,0,0])
bmap.drawmeridians(np.arange(80,140,10),labels=[0,0,0,1])
plt.title('Province')
plt.show()
plt.savefig('d:\\fig_province.png', dpi=100, bbox_inches='tight')
plt.clf()
plt.close()
end=time.clock()

print(end-start)
