'''
The code contains functions to compute the Gauss-Newton approximation.
References:
    https://en.wikipedia.org/wiki/Gauss%E2%80%93Newton_algorithm#Julia
'''
import numpy as np

# Make the residuals of the circles (equations we want to minimize).
def residuals_circle(amplitudes, centers, initial_values):
    x, y, k = initial_values
    residuals = []
    for i in range(len(centers)):
        a, b = centers[i]
        r = amplitudes[i]
        eq = np.sqrt( (x - a)**2 + (y - b)**2 ) - k * r
        residuals.append(eq)
    return np.array(residuals)

# Gets the Jacobian for the residuals
def jacobian_circle(amplitudes, centers, initial_values):
    x, y, k = initial_values
    jacobian = []
    for i in range(len(centers)):
        a, b = centers[i]
        r = amplitudes[i]
        si = np.sqrt( (x - a)**2 + (y - b)**2 )
        if np.isclose(si, 0):
            jac = [0, 0, -r]  # Assigning zero gradients to prevent division by zero
        else:
            jac = [ (x - a) / si, (y - b) / si, -r ]

        
        jacobian.append(jac)
    return np.array(jacobian)

# Compute the Gauss-Newton approximation.
# Parameters:
    # amplitudes = the list of amplitudes

    # centers = A list of the coordinates of each of the microphones
        # Example: centers = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
        # Note: The origin will be the center of the golf cart
        # Note: The indices should correpsond with those in the amplitude list
            # i.e) centers[0] is the center for the mic that picked up amplitude[0]

    # initial_values = [x, y, k] where
        # x = the initial guess for x-coordinate
        # y = the initial guess for y-coordinate
        # k = initial guess for radius scaling factor
        # Note: The initial guess for (x, y) should be 
        #       the center of the mic with the max amplitude, 
        #       since it's likely in that direction. The k can be 1. 
def gaussNewton(amplitudes, centers, initial_values, maxSteps=100, tol=1e-6):
    # Create a copy of the initial values to update over each iteration. 
    ivs = np.copy(initial_values).astype(float)
    for _ in range(maxSteps):
        # Get the Jacobian
        J = jacobian_circle(amplitudes, centers, ivs)
        # Get the residuals
        r = residuals_circle(amplitudes, centers, ivs)
        # Compute how much to change each of the values
        delta = -np.linalg.solve( J.T @ J, J.T @ r  )
        # Update the values
        ivs += delta
        # If less than our tolerance, break out and stop. 
        if (np.linalg.norm(delta) <= tol):
            break
    # Return the updated values after the loop. 
    return ivs

# Convert (x, y) cartesian coordinates into polar coordinates
def toPolarCoords(x, y):
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan(y/x)
    return (r, theta)





