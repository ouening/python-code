import time

start = time.clock()
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import pandas as pd

posi=pd.read_excel("D:\\Files\\datasets\\2015Cities-CHINA.xlsx")
lat = np.array(posi["lat"][0:120])                        # 获取维度之维度值
lon = np.array(posi["lon"][0:120])                        # 获取经度值
pop = np.array(posi["pop"][0:120],dtype=float) 
size=(gdp/np.max(gdp))*100  


map = Basemap(llcrnrlon=80.33, 
              llcrnrlat=3.01, 
              urcrnrlon=138.16, 
              urcrnrlat=56.123,
             resolution='h', projection='cass', lat_0 = 42.5,lon_0=120)

map.readshapefile("D:\\GoogleDownload\\CHN_adm_shp\\CHN_adm1",'states',drawbounds=True)

map.etopo()

map.drawcoastlines()

x,y = map(lon[2],lat[2]) # 北京市坐标，经纬度坐标转换为该map的坐标
a,b = map(lon,lat)

map.scatter(a,b,s=size)

map.scatter(x,y,s=200,marker='*',facecolors='r',edgecolors='r')

end=time.clock()

print(end-start)

plt.show()

