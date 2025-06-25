from argparse import ArgumentParser
import numpy as np
import cv2
import os
import glob


def main(args):

    # parameters
    n_corners_x = args.n_corners_x
    n_corners_y = args.n_corners_y
    show_preview = args.show_preview


    # termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # prepare object points
    objp = np.zeros((n_corners_x*n_corners_y,3), np.float32)
    objp[:,:2] = np.mgrid[0:n_corners_x, 0:n_corners_y].T.reshape(-1,2)

    # Arrays to store object points and image points from all the images.
    obj_points = [] # 3d point in real world space
    img_points = [] # 2d points in image plane.

    images = sorted(glob.glob(os.path.join(args.folder, "*" + args.extension)))
    print(f"Found {len(images)} images")

    # loop over the images
    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        print(f"Finding chessboard corners for image {fname}")
        ret, corners = cv2.findChessboardCorners(gray, (n_corners_x, n_corners_y), None)

        # If found, add object points, image points (after refining them)
        if ret == True:
            print("Found corners!")
            obj_points.append(objp)

            corners2 = cv2.cornerSubPix(gray,corners, (11,11), (-1,-1), criteria)
            img_points.append(corners2)

            # Draw and display the corners
            if show_preview:
                cv2.drawChessboardCorners(img, (n_corners_x, n_corners_y), corners2, ret)
                im_resized = cv2.resize(img, (900, 600))
                print("Showing image")
                cv2.imshow('img', im_resized)
                cv2.waitKey(1000)
        else:
            print(f"Did not find corners for image {fname}")


    # perform calibration
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(obj_points, img_points, gray.shape[::-1], None, None)

    # get the camera matrices
    img = cv2.imread(images[0])
    h,  w = img.shape[:2]
    camera_matrix, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w,h), 1, (w,h))

    # undistort
    dst = cv2.undistort(img, mtx, dist, None, camera_matrix)

    # crop the image
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    cv2.imwrite('undistorted.png', dst)

    print("Done with calibration...camera matrix is:")
    print(camera_matrix)

    # save the last calibration result
    with open("last_calibration.txt", "w") as f:
        cal_str = f"width: {w:d}\nheight: {h:d}\ndistortion: {list(dist)}\nintrinsics: {camera_matrix}"
        f.write(cal_str)

    cv2.destroyAllWindows()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--folder", type=str)
    parser.add_argument("--extension", type=str)
    parser.add_argument("--show_preview", action="store_true")
    parser.add_argument("--n_corners_x", type=int, default=10)
    parser.add_argument("--n_corners_y", type=int, default=7)
    args = parser.parse_args()
    main(args)