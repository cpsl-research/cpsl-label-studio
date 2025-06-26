import argparse
import json
import os
import numpy as np
from glob import glob
import cv2


def main(args):
    # load in the results json
    with open(os.path.join(args.root, args.input, "result.json"), "r") as f:
        result = json.load(f)

    # package up the label information
    anns_by_files = {}
    for result_vid in result:
        labels_objs_frames = []
        for ann in result_vid["annotations"][0]["result"]:
            # package up the label information per frame
            label = {
                ann_seq["frame"]: {
                    "frame": ann_seq["frame"],
                    "time": ann_seq["time"],
                    "track_id": ann["id"],
                    "category_id": ann["value"]["labels"][0],  # assumes only one label
                    "bbox": [
                        ann_seq["x"],
                        ann_seq["y"],
                        ann_seq["x"] + ann_seq["width"],
                        ann_seq["y"] + ann_seq["height"],
                    ],
                    "rotation": ann_seq["rotation"],
                }
                for ann_seq in ann["value"]["sequence"]
            }
            labels_objs_frames.append(label)
        anns_by_files[result_vid["file_upload"]] = labels_objs_frames
    breakpoint()

    # set output directory
    output_dir = os.path.join(args.root, ("multiclass" if args.multiclass else "oneclass") + "-" + args.output)
    print("Saving scenes to", output_dir)     

    # loop over the videos and split them into individual frames
    videos = sorted(glob(os.path.join(args.root, args.input, "videos", "*.mp4")))
    for video in videos:
        # check if we have ground truth label for this video
        idx_gt = np.argwhere([res["file_upload"] in video for res in result])
        if len(idx_gt) == 0:
            print(f"No ground truth for {video}")
            found_gt = False
        else:
            idx_gt = idx_gt[0][0]
            print(f"Found ground truth for {video}")
            found_gt = True

        # build up the labels per object
        if found_gt:
            pass

        # make directory for the scenes
        scene_name = "scene-" + (os.path.basename(video).split(".")[0]).split("_")[-1]
        scene_images_dir = os.path.join(output_dir, scene_name, "images")
        scene_labels_dir = os.path.join(output_dir, scene_name, "labels")
        os.makedirs(scene_images_dir, exist_ok=True)
        os.makedirs(scene_labels_dir, exist_ok=True)

        # load in the video
        cap = cv2.VideoCapture(video)
        frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        fps = cap.get(cv2.CAP_PROP_FPS)
        print(f"Scene {scene_name} has {frame_count} frames at {fps} fps")
        
        # loop over the frames and save them
        for i in range(frame_count):
            # read in the frame
            ret, frame = cap.read()
            if not ret:
                break
            
            # save the frame
            cv2.imwrite(os.path.join(scene_images_dir, f"{i:06d}.jpg"), frame)

            # save the label                
            # save the labels
            # with open(os.path.join(scene_labels_dir, f"{i:06d}.json"), "w") as f:
            #     json.dump(labels_frame, f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', default="/data/shared/rccars", type=str)
    parser.add_argument('--input', default="raw-tracking", type=str)
    parser.add_argument('--output', default="tracking-2025", type=str)
    parser.add_argument('--multiclass', default=False, action="store_true")
    parser.add_argument('--pct_train', default=0.70, type=float)
    args = parser.parse_args()

    main(args)