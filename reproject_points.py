import cv2

R = np.array([
    [1,2,3],
    [4,5,6],
    [7,8,9],
])

R_vec = cv2.Rodrigues(R.T)
R = cv.Rodrigues(R_vec)
# def reproject_points(img, intrinsics, world_point, R: np.array, t):
    
    