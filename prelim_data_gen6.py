import numpy as np
from scipy.spatial import distance
import matplotlib.pyplot as plt
import itertools
import os
import random
import pandas

np.random.seed(42)
nx = 7
ny = 7
nz = 1
nP = 1
num_quads = 25
max_combo = 3
min_combo = 3

quad_combos = []
for L in range(min_combo, max_combo+1):
    for subset in itertools.combinations(range(0,num_quads),L):
        quad_combos.append(list(subset))
print(quad_combos)

x_j = np.linspace(0, 50, nx)
y_j = np.linspace(0, 50, ny)
z_j = np.linspace(0, 0, nz)
P_j = np.linspace(100, 100, nP)

xx_j, yy_j = np.meshgrid(x_j, y_j)

temp_xx_j = xx_j.reshape((np.prod(xx_j.shape),))
temp_yy_j = yy_j.reshape((np.prod(yy_j.shape),))

temp_jam_coords = zip(temp_xx_j, temp_yy_j)
print(temp_jam_coords)
jammer_combos = []

for L in range(min_combo, max_combo+1):
    for subset in itertools.combinations(temp_jam_coords,L):
        jammer_combos.append(subset)
max_jammer_combo = len(jammer_combos)

FREQ = 1575.42
GT = 1.
GR = 1.
PT = 100.
C = 299792458.
WAVELENGTH = C/(FREQ*1000000.)

nx_sensor = 5.
ny_sensor = 5.
nz_sensor = 1.

x_sensor = np.linspace(-5, 55, nx_sensor)
y_sensor = np.linspace(-5, 55, ny_sensor)
z_sensor = np.linspace(15, 15, nz_sensor)

xx, yy, zz = np.meshgrid(x_sensor, y_sensor, z_sensor)

xx = xx.reshape((np.prod(xx.shape),))
yy = yy.reshape((np.prod(yy.shape),))
zz = zz.reshape((np.prod(zz.shape),))

sensor_coords = zip(xx, yy, zz)


def determine_quadrant(x_pos,y_pos):
    if (0 <= x_pos <= 10 and 0 <= y_pos <= 10):
        temp_quadrant = 0
    if (10 < x_pos <= 20 and 0 <= y_pos <= 10):
        temp_quadrant = 1
    if (0 <= x_pos <= 10 and 10 < y_pos <= 20):
        temp_quadrant = 2
    if (10 < x_pos <= 20 and 10 < y_pos <= 20):
        temp_quadrant = 3
    if (0 <= x_pos <= 10 and 20 < y_pos <= 30):
        temp_quadrant = 4
    if (10 < x_pos <= 20 and 20 < y_pos <= 30):
        temp_quadrant = 5
    if (0 <= x_pos <= 10 and 30 < y_pos <= 40):
        temp_quadrant = 6
    if (10 < x_pos <= 20 and 30 < y_pos <= 40):
        temp_quadrant = 7
    if (0 <= x_pos <= 10 and 40 < y_pos <= 50):
        temp_quadrant = 8
    if (10 < x_pos <= 20 and 40 < y_pos <= 50):
        temp_quadrant = 9

    if (20 < x_pos <= 30 and 0 <= y_pos <= 10):
        temp_quadrant = 10
    if (30 < x_pos <= 40 and 0 <= y_pos <= 10):
        temp_quadrant = 11
    if (20 < x_pos <= 30 and 10 < y_pos <= 20):
        temp_quadrant = 12
    if (30 < x_pos <= 40 and 10 < y_pos <= 20):
        temp_quadrant = 13
    if (20 < x_pos <= 30 and 20 < y_pos <= 30):
        temp_quadrant = 14
    if (30 < x_pos <= 40 and 20 < y_pos <= 30):
        temp_quadrant = 15
    if (20 < x_pos <= 30 and 30 < y_pos <= 40):
        temp_quadrant = 16
    if (30 < x_pos <= 40 and 30 < y_pos <= 40):
        temp_quadrant = 17
    if (20 < x_pos <= 30 and 40 < y_pos <= 50):
        temp_quadrant = 18
    if (30 < x_pos <= 40 and 40 < y_pos <= 50):
        temp_quadrant = 19

    if (40 < x_pos <= 50 and 0 <= y_pos <= 10):
        temp_quadrant = 20
    if (40 < x_pos <= 50 and 10 < y_pos <= 20):
        temp_quadrant = 21
    if (40 < x_pos <= 50 and 20 < y_pos <= 30):
        temp_quadrant = 22
    if (40 < x_pos <= 50 and 30 < y_pos <= 40):
        temp_quadrant = 23
    if (40 < x_pos <= 50 and 40 < y_pos <= 50):
        temp_quadrant = 24
    return temp_quadrant

PR = dict([])
jam_test = {'data':[], 'target':[], 'jam_coords':[], 'sensor_coords':sensor_coords}

num_combo = len(jammer_combos)
for i, combo in enumerate(jammer_combos):
    temp_PR_list = [0]*len(sensor_coords)
    temp_quad_list = []
    for jammer in combo:
        x = jammer[0]
        y = jammer[1]
        z = z_j
        temp_R = [distance.euclidean((x,y,z_j),sensor) for sensor in sensor_coords]
        temp_PR = [PT*GT*GR*WAVELENGTH**2/(4*np.pi * R)**2 for R in temp_R]
        temp_PR_list = [a + b for a,b in zip(temp_PR_list,temp_PR)]
        temp_quadrant = determine_quadrant(x,y)
        temp_quad_list.append(temp_quadrant)
    if len(temp_quad_list) == len(set(temp_quad_list)):
        temp_quad_list = sorted(set(temp_quad_list))
        target_quad_combo = quad_combos.index(temp_quad_list)
        jam_test['data'].append(temp_PR_list)
        jam_test['target'].append(target_quad_combo)
        jam_test['jam_coords'].append(combo)
    print float(i)/float(num_combo)

jam_test['data'] = np.array(jam_test['data'])
jam_test['target'] = np.array(jam_test['target'])
jam_test['jam_coords'] = np.array(jam_test['jam_coords'])
jam_test['sensor_coords'] = np.array(jam_test['sensor_coords'])

np.save('test_data.npy', jam_test)
print(jam_test['target'])
plt.scatter(xx_j,yy_j)
plt.scatter(jam_test['sensor_coords'][:,0],jam_test['sensor_coords'][:,1], color='r', marker='x')

for x_line in range(0,50,10):
    for y_line in range(0,50,10):
        plt.plot([x_line, x_line], [y_line, y_line+10], 'k-', lw=2)
        plt.plot([x_line, x_line+10], [y_line+10, y_line+10], 'k-', lw=2)

plt.show()

plt.hist(jam_test['target'])
plt.show()

fig, axes = plt.subplots(2, 5)
# use global min / max to ensure all weights are shown on the same scale
flat_list = [item for sublist in jam_test['data'] for item in sublist]
vmin, vmax = min(flat_list), max(flat_list)
print vmin,vmax
i_temp = 0
for i_jammer, ax in zip(jam_test['data'], axes.ravel()):
    ax.matshow(i_jammer.reshape(nx_sensor, ny_sensor), cmap=plt.cm.gray, vmin=.5 * vmin,
               vmax=.5 * vmax)
    ax.scatter(1, 1)
    ax.set_xticks(())
    ax.set_yticks(())
    i_temp= i_temp+1

plt.show()