# -----------------------------------------------------------------------------
# Copyright (c) 2015, Nicolas P. Rougier. All Rights Reserved.
# Distributed under the (new) BSD License. See LICENSE.txt for more info.
# -----------------------------------------------------------------------------
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# No toolbar
matplotlib.rcParams['toolbar'] = 'None'

# New figure with white background
fig = plt.figure(figsize=(6,6), facecolor='white')

# New axis over the whole figureand a 1:1 aspect ratio
# ax = fig.add_axes([0,0,1,1], frameon=False, aspect=1)
ax = fig.add_axes([0.005,0.005,0.990,0.990], frameon=True, aspect=1)

# Number of ring
n = 50
size_min = 50
size_max = 50*50
          
# Ring position ，圆环位置，范围在[0,1]之间
P = np.random.uniform(0,1,(n,2))

# Ring colors环的颜色
C = np.ones((n,4)) * (0,1,0,1)

#C = np.ones((n,3)) * (1,0,1)
# Alpha color channel goes from 0 (transparent) to 1 (opaque)
# 透明度，数值在[0,1]之间
C[:,2] = np.linspace(0,1,n)

# Ring sizes环的大小，范围在[50,2500]
S = np.linspace(size_min, size_max, n)

# Scatter plot
# 散点图绘制
scat = ax.scatter(P[:,0], P[:,1], s=S, lw = 0.5,
                  edgecolors = C, facecolors='None')

# Ensure limits are [0,1] and remove ticks
#保证x,y的范围在[0,1]之间,移除坐标轴标记
ax.set_xlim(0,1), ax.set_xticks([])
ax.set_ylim(0,1), ax.set_yticks([])


def update(frame):
    global P, C, S

    # Every ring is made more transparent每个环变得更透明
    C[:,3] = np.maximum(0, C[:,3] - 1.0/n)

    # Each ring is made larger每个环都比原来的大
    S += (size_max - size_min) / n

    # Reset ring specific ring (relative to frame number)
    i = frame % 50   
    P[i] = np.random.uniform(0,1,2) # P[i] = P[i,:],同时改变了x,y两个位置的值
    S[i] = size_min #从最小的形状开始
    C[i,3] = 1      #设置透明度为1 

    # Update scatter object
    # 更新scatter绘图对象的属性，例如edgecolors,sizes,offsets等
    scat.set_edgecolors(C)
    scat.set_sizes(S)
    scat.set_offsets(P)
    return scat,

animation = FuncAnimation(fig, update, interval=70)
# animation.save('../figures/rain.gif', writer='imagemagick', fps=30, dpi=72)
plt.show()

