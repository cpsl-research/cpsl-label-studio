import os
import json
import glob
import argparse
import numpy as np


def get_image_files(root, dir_name, pattern):
    patterns = [os.path.join(root, dir_name, pattern.upper()), os.path.join(root, dir_name, pattern.lower())]
    return [filename for p in patterns for filename in glob.glob(p)]


def main(args):
    np.random.seed(args.seed)

    # perform train-test-split
    all_images = get_image_files(args.root, os.path.join(args.input, "images"), "*.jpg")
    n_train = int(len(all_images) * args.pct_train)
    idx_train = np.random.choice(list(range(n_train)), size=n_train, replace=False)
    idx_val = list(set(range(len(all_images))).difference(set(idx_train)))
    train_images = [all_images[i] for i in idx_train]
    val_images = [all_images[i] for i in idx_val]
    img_dict = {"train": train_images, "val": val_images}
    idxs = {"train": idx_train, "val": idx_val}

    # load in the results json
    with open(os.path.join(args.root, args.input, "result.json"), "r") as f:
        result = json.load(f)
    result_out = {
        "train": {"images": [], "categories": [], "annotations": [], "info": []},
        "val":   {"images": [], "categories": [], "annotations": [], "info": []},
    }

    # split annotation information
    for anno in result["annotations"]:
        # modify class of annotation to switch to oneclass
        anno["category_id"] = 0

        # account for annotation
        if anno["image_id"] in idxs["train"]:
            result_out["train"]["annotations"].append(anno)
        elif anno["image_id"] in idxs["val"]:
            result_out["val"]["annotations"].append(anno)
        else:
            raise RuntimeError("Annotation unaccounted for")

    # split image information
    for split in ["train", "val"]:
        out_folder = os.path.join(args.root, args.output, split, "images")
        os.makedirs(out_folder, exist_ok=True)
        # process images for split
        for idx, img in enumerate(img_dict[split]):
            # link the files
            dst = os.path.join(out_folder, img.split("/")[-1])
            if os.path.exists(dst):
                os.unlink(dst)
            os.symlink(img, dst)

            # update the entries in the result file
            idx_image = idxs[split][idx]
            image_metadata = result["images"][idx_image]
            assert image_metadata["id"] == idx_image
            result_out[split]["images"].append(image_metadata)

        # set class categories -- only one category
        result_out[split]["categories"] = [{"id": 0, "name": "car"}]
        result_out[split]["info"] = result["info"]

        # save result info
        res_file = os.path.join(args.root, args.output, split, f"{split}.json")
        with open(res_file, "w") as f:
            json.dump(result_out[split], f)

    # print what we are about to do
    print(f"{len(all_images)} images found -- split into {len(train_images)} train, {len(val_images)} val")

    #
    # TODO: print out the number of bounding boxes (annotations) in each set
    #
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', default=0, type=int)
    parser.add_argument('--root', default="/data/shared/rccars", type=str)
    parser.add_argument('--input', default="raw", type=str)
    parser.add_argument('--output', default="oneclass-detection", type=str)
    parser.add_argument('--pct_train', default=0.70, type=float)
    args = parser.parse_args()

    main(args)