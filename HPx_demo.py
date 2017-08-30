'''
Interactive Dynamic Hyperparameters Demo

Author: Matt Shaffer matt@discovermatt.com
Website: discovermatt.com

visualization based on this iPython notebook by Andrej Karpathy:
https://github.com/karpathy/randomfun/blob/master/es.ipynb

'''
import os, sys, time
import numpy as np
import cv2
import matplotlib.pyplot as plt
import keyboard
import platform as _platform

# local modules
from console_logging import *
from hyperparams import *
from settings import hyperparams


'''
1. Initialization
'''
# create hyperparameters object
HPx = Hyperparams(hyperparams)

# np.random.seed(3) # (optional) set random seed for replicating results
plot_filename = 'evo' + str(time.time()) + '.png' # filename to save output
eps = 1e-8 # epsilon value for numerical convenience
cap = cv2.VideoCapture(None) # cv2 object
state_dim = 400 # dimension of x by y simulated space
plot_size1, plot_size2 = 10, 10 # Size of simulated demo

# Initialize Gaussian data
def initialize_data():
    X,Y = np.meshgrid(np.linspace(-1,1,state_dim),np.linspace(-1,1,state_dim))
    mux,muy,sigma=  0.3,-0.3,4
    G1 = np.exp(-((X-mux)**2+(Y-muy)**2)/2.0*sigma**2)
    mux,muy,sigma=-0.3,0.3,2
    G2 = np.exp(-((X-mux)**2+(Y-muy)**2)/2.0*sigma**2)
    mux,muy,sigma=0.6,0.6,2
    G3 = np.exp(-((X-mux)**2+(Y-muy)**2)/2.0*sigma**2)
    mux,muy,sigma=-0.4,-0.2,3
    G4 = np.exp(-((X-mux)**2+(Y-muy)**2)/2.0*sigma**2)
    G = G1 + G2 - G3 - G4
    return G

# Define random starting coordinates for optimization
# Add sigma so that population that initializes stays in bounds
def init_start_coord(state_dim, sigma):
    # fixed initialization
    # w = np.array([0.80*state_dim,0.75*state_dim])
    # random initialization
    w = np.array(np.random.randint(1+sigma, (state_dim-1)-sigma, size=2).astype(np.float))
    return w

# draw the history of optimization as a white line
def init_path():
    prevx, prevy = [], []
    line1, = plt.plot(prevx, prevy, 'wo-', markersize=2, alpha=0.8)
    return line1, prevx, prevy


# plotting parameters
plt.rcParams['image.cmap'] = 'gray'
plt.rcParams['image.interpolation'] = 'nearest'
G = initialize_data()
fig,ax = plt.subplots()
fig = plt.figure(figsize=(plot_size1, plot_size2))
canvas = fig.canvas
w = init_start_coord(state_dim, HPx.sigma['value'])
line1, prevx, prevy = init_path()

# Printing initialization
last_time = time.time()
print_line = None

# (optional) Countdown timer
countdown(10)

ii = 0
while ii < HPx.epochs['value']:
    ii += 1

    # send the captured keypress events to a fn that uses them to change params
    HPx = hyperstate(HPx)

    # print current values of hyperparameters + additional message if changed
    print_line = print_iter(ii, HPx)
    print(print_line, end='\n')

    plot1 = plt.imshow(G, vmin=-1, vmax=1, cmap='jet')

    # draw a population of samples
    noise = np.random.randn(HPx.population_size['value'], 2)

    wp = np.expand_dims(w, 0) + HPx.sigma['value']*noise

    # if we've drifted out of bounds, reinitialize population
    if not np.array_equal(wp.clip(0+eps, state_dim-eps),wp):
        print('out of bounds:: reinitialize')
        w = init_start_coord(state_dim, HPx.sigma['value'])
        wp = np.expand_dims(w, 0) + HPx.sigma['value']*noise
        line1, prevx, prevy = init_path()

    # draw the population
    x,y = zip(*wp)
    points1 = plt.scatter(x,y,4,'#003333', edgecolors='face', alpha=0.2)
    # draw the current parameter vector in white
    points1 = plt.scatter([w[0]],[w[1]],10,'w', edgecolors='face', alpha=0.7)


    # draw estimated gradient as white arrow
    R = np.array([G[int(wi[1].clip(0, state_dim-1)), int(wi[0].clip(0, state_dim-1))] for wi in wp])
    R -= R.mean()
    R /= R.std() # standardize the rewards to be N(0,1) gaussian
    g = np.dot(R, noise)
    u = HPx.alpha['value'] * g

    if u.clip(0+eps, state_dim-eps).all() == u.all():
        arrow1 = plt.arrow(w[0], w[1], u[0], u[1], head_width=2, head_length=2, fc='w', ec='w', alpha=0.9)
    else:
        print('out of bounds u detected')
        print(u)
    axis1 = plt.axis('off')
    hx_string1 = 'training steps: ' + str(HPx.epochs['value']) + '  learning rate: ' + str(HPx.alpha['value'])
    hx_string2 = 'sigma: ' + str(HPx.sigma['value']) + '  pop size: ' + str(HPx.population_size['value'])
    title1 = plt.title('\n\niteration {}, reward {:.2f} \n{}\n{}\n{}'.format(ii+1, G[int(w[0]), int(w[1])], hx_string1, hx_string2, HPx.message))

    # draw the history of optimization as a white line
    prevx.append(w[0])
    prevy.append(w[1])
    if len(prevx) > 0:
        line1.set_data(prevx, prevy)

    # move position relative to u
    w += u
    plt.axis('tight')

    # redraw the canvas
    canvas.draw()

    # convert canvas to image
    img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8,
            sep='')
    img  = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))

    # img is rgb, convert to opencv's default bgr
    img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)

    cv2.imshow("plot",img)
    ret, _ = cap.read()

    # if this is removed, plots won't animate in real time
    k = cv2.waitKey(33) & 0xFF
    if k == 27:
        break

    time.sleep(2)

# Uncomment the following line to save plots
#plt.savefig(plot_filename,bbox_inches='tight',pad_inches=0,dpi=200)
