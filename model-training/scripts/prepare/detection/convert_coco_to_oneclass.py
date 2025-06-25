import os
import json
import argparse
import numpy as np


def main(args):
    np.random.seed(args.seed)

    # load in the results json
    with open(os.path.join(args.root, args.input, "result.json"), "r") as f:
        result = json.load(f)
    result_out = {
        "train": {"images": [], "categories": [], "annotations": [], "info": []},
        "val":   {"images": [], "categories": [], "annotations": [], "info": []},
    }

    # get paths to images and id to filename map
    all_images = {
        img["id"]: os.path.join(args.root, args.input, img["file_name"]) for img in result["images"]
    }
    idx_to_id = {i: img["id"] for i, img in enumerate(result["images"])}

    # perform train-test-split on the GLOB files in order
    n_train = int(len(all_images) * args.pct_train)
    idx_train = np.random.choice(list(range(n_train)), size=n_train, replace=False)
    idx_val = list(set(range(len(all_images))).difference(set(idx_train)))
    idx_splits = {"train": idx_train, "val": idx_val}
    ids_splits = {
        "train": [idx_to_id[i] for i in idx_train],
        "val": [idx_to_id[i] for i in idx_val]
    }

    # split annotation information
    n_annos = 0
    n_anno_train = 0
    n_anno_val = 0
    for anno in result["annotations"]:
        # modify class of annotation to switch to oneclass
        anno["category_id"] = 0
        n_annos += 1

        # map annotations to the correct split
        if anno["image_id"] in ids_splits["train"]:
            result_out["train"]["annotations"].append(anno)
            n_anno_train += 1
        elif anno["image_id"] in ids_splits["val"]:
            result_out["val"]["annotations"].append(anno)
            n_anno_val += 1
        else:
            raise RuntimeError("Annotation unaccounted for")

    # split image information
    for split in ["train", "val"]:
        out_folder = os.path.join(args.root, args.output, split, "images")
        os.makedirs(out_folder, exist_ok=True)

        # process images for split
        for idx_img in idx_splits[split]:
            # link the files
            img_path = all_images[idx_to_id[idx_img]]
            dst = os.path.join(out_folder, img_path.split("/")[-1])
            if os.path.exists(dst):
                os.unlink(dst)
            os.symlink(img_path, dst)

            # update the metadata
            result_out[split]["images"].append(result["images"][idx_img])

        # set class categories -- only one category
        result_out[split]["categories"] = [{"id": 0, "name": "car"}]
        result_out[split]["info"] = result["info"]

        # save result info
        res_file = os.path.join(args.root, args.output, split, f"{split}.json")
        with open(res_file, "w") as f:
            json.dump(result_out[split], f)

    # print what we are about to do
    print(
        f"{len(all_images)} images, {n_annos} annotations found, split into:\n"
        f"    {len(idx_train)} train images with {n_anno_train} annotations\n"
        f"    {len(idx_val)} val images with {n_anno_val} annotations"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--seed', default=0, type=int)
    parser.add_argument('--root', default="/data/shared/rccars", type=str)
    parser.add_argument('--input', default="raw", type=str)
    parser.add_argument('--output', default="oneclass-detection", type=str)
    parser.add_argument('--pct_train', default=0.70, type=float)
    args = parser.parse_args()

    main(args)