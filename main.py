import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
from matplotlib.patches import Arc
from matplotlib.lines import Line2D

def rotation_matrix(theta):
        return np.array([
                [np.cos(theta), -np.sin(theta)],
                [np.sin(theta), np.cos(theta)]
        ])

dirxy = np.array([[1, 0], [0, 1], [-1, 0], [0,-1]], dtype=float)
coords = np.array([[0, 0], [1, 0], [1, 1], [0, 1]], dtype=float) 

def update_coords_base_on_dir():
    global coords
    for i in range(1,4):
        coords[i] = coords[i - 1] + dirxy[i - 1] 

# generating our vectors to form a square shape:
def create_vectors(vector_list, zrd = 2, alp = 1, c = 'black'):
    for i in range(4):
        x, y = coords[i]
        dx, dy = dirxy[i]
        vector_list.append(plt.quiver(x, y, dx, dy, angles='xy', scale_units='xy', scale=1, units='xy', alpha=alp, zorder=zrd, color = c))

vectors = []
create_vectors(vectors, 2)
static_vectors = []
create_vectors(static_vectors, 1, 0.6, c='red')

def update_directions(theta):
    global dirxy
    dirxy = np.dot(dirxy, rotation_matrix(theta))    

def rotate(theta = 0):
    update_directions(theta)
    update_coords_base_on_dir()

    for index, vector in enumerate(vectors):
        new_X, new_Y, = coords[index]
        dx, dy = dirxy[index]
        vector.set_offsets(np.column_stack((new_X, new_Y)))
        vector.set_UVC(dx, dy)

plt.xlim(-2, 2)
plt.ylim(-2, 2)
plt.axhline(0, color='gray', alpha=0.6, zorder=0, linestyle='dashed')
plt.axvline(0, color='gray', alpha=0.6, zorder=0, linestyle='dashed')
plt.gca().set_aspect('equal', adjustable='box')  # Set aspect ratio to equal

# color lines for legend (used as labels)
line1 = Line2D([0], [0], color='blue', lw=2, label='Rotation Path') 
line2 = Line2D([0], [0], color='black', lw=2, label='Square after Rotation')      
line3 = Line2D([0], [0], color='red', lw=2, label='Initial Square')   

plt.legend(handles=[line1, line2, line3])

arc_ax = plt.gca()  # Use the current axis for the arc
arc = Arc((0, 0), 1, 1, theta1=0, theta2=0, color='blue', linewidth=2, label='Rotation Arc')
arc_ax.add_patch(arc)  # Add the arc to axis


ax_slider = plt.axes([0.2, 0.02, 0.65, 0.03], facecolor='lightgoldenrodyellow')
slider = Slider(ax_slider, 'Rotation Angle (radians)', 0, np.pi * 2, valinit=0)

prev_angle = 0  # Store the previous angle of the slider

def update(val):
    val *= -1

    global prev_angle
    angle_diff = val - prev_angle  # Calculate the angle difference
    
    rotate(angle_diff)
    
    prev_angle = val  # Update the previous angle

    arc.theta2= np.rad2deg(-val)  # This updates the angle
    plt.draw()
    
slider.on_changed(update)

plt.show()