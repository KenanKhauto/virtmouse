from math import sqrt
from filterpy.kalman import KalmanFilter
import numpy as np

# Clamping function to prevent mouse from going to screen corners
def clamp(x, min_value, max_value):
    return max(min_value, min(x, max_value))

def distance(p1, p2):
    return sqrt((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

def kalman_filter(current_x, current_y):
    # Initialize Kalman Filter for 2D hand position (x, y)
    kf = KalmanFilter(dim_x=4, dim_z=2)
    kf.x = np.array([0., 0., 0., 0.])  # initial state (x, y, x_velocity, y_velocity)
    kf.F = np.array([[1., 0., 1., 0.],
                    [0., 1., 0., 1.],
                    [0., 0., 1., 0.],
                    [0., 0., 0., 1.]])  # state transition matrix
    kf.H = np.array([[1., 0., 0., 0.],
                    [0., 1., 0., 0.]])  # measurement function
    kf.P *= 1000.  # covariance matrix
    kf.R = np.array([[5., 0.],
                    [0., 5.]])  # measurement noise

    # In each frame, update the Kalman filter
    current_measurement = np.array([current_x, current_y])
    kf.predict()
    kf.update(current_measurement)

    # Get the filtered position
    smoothed_x, smoothed_y = kf.x[:2]

    return smoothed_x, smoothed_y