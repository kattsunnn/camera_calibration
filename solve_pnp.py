import cv2
import numpy as np

def solve_pnp(object_points, img_points, camera_matrix, dist_coeffs=None):
    if dist_coeffs is None:
        dist_coeffs = np.zeros((5,1))

    ret, rvec, tvec = cv2.solvePnP(object_points, img_points, camera_matrix, dist_coeffs)
    return ret, rvec, tvec

if __name__ == "__main__":

    import sys
    import img_utils.img_utils as iu

    object_points = np.array(   [[5.46, 23.745, 0],
                                [4.115, 23.745, 0],
                                [4.115, 6.375, 0],
                                [0, 6.375, 0],
                                [-4.115, 6.375, 0]], dtype=np.float32)

    img_points = np.array([[21, 241],
                             [143, 226],
                             [471, 302],
                             [659, 232],
                             [741, 203]], dtype=np.float32)

    camera_matrix = np.array([  [493.63, 0, 427.5],
                                [0, 529.13, 222],
                                [0, 0, 1]]
                                , dtype=np.float32)

    ret, rvec, tvec = solve_pnp(object_points, img_points, camera_matrix)

    print("Return value:", ret)
    print("Rotation Vector:\n", rvec)
    print("Translation Vector:\n", tvec)

    # object_points, img_points, rvec, tvec, camera_matrix, dist_coeffs がある場合
    projected_points, _ = cv2.projectPoints(object_points, rvec, tvec, camera_matrix, None)

    # projected_points は Nx1x2 の形なので、Nx2 に変換
    projected_points = projected_points.reshape(-1, 2)
    print("Projected Points:\n", projected_points)
    # 再投影誤差
    errors = np.linalg.norm(img_points - projected_points, axis=1)
    mean_error = np.mean(errors)

    print("Reprojection errors per point:", errors)
    print("Mean reprojection error:", mean_error)

    # print(855/np.tan(np.deg2rad(60)))
    # print(444/np.tan(np.deg2rad(40)))