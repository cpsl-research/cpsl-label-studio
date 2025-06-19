import json
import random
import os
import argparse


def split_coco_dataset(coco_json_path, output_dir, val_ratio=0.2, seed=42):
    with open(coco_json_path, 'r') as f:
        coco_data = json.load(f)

    images = coco_data['images']
    annotations = coco_data['annotations']
    categories = coco_data.get('categories', [])

    # Shuffle and split
    random.seed(seed)
    random.shuffle(images)

    num_val = int(len(images) * val_ratio)
    val_images = images[:num_val]
    train_images = images[num_val:]

    val_ids = set(img['id'] for img in val_images)
    train_ids = set(img['id'] for img in train_images)

    train_annotations = [ann for ann in annotations if ann['image_id'] in train_ids]
    val_annotations = [ann for ann in annotations if ann['image_id'] in val_ids]

    train_coco = {
        'images': train_images,
        'annotations': train_annotations,
        'categories': categories
    }

    val_coco = {
        'images': val_images,
        'annotations': val_annotations,
        'categories': categories
    }

    os.makedirs(output_dir, exist_ok=True)

    with open(os.path.join(output_dir, 'train.json'), 'w') as f:
        json.dump(train_coco, f)

    with open(os.path.join(output_dir, 'val.json'), 'w') as f:
        json.dump(val_coco, f)

    print(f"Split completed:\n- {len(train_images)} training images\n- {len(val_images)} validation images")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split a COCO dataset into training and validation sets.")
    parser.add_argument("--input", "-i", type=str, required=True, help="Path to the input COCO JSON file.")
    parser.add_argument("--output", "-o", type=str, default=".", help="Directory to save train.json and val.json.")
    parser.add_argument("--val_ratio", "-v", type=float, default=0.2, help="Validation split ratio (default: 0.2).")
    parser.add_argument("--seed", "-s", type=int, default=42, help="Random seed (default: 42).")

    args = parser.parse_args()

    split_coco_dataset(
        coco_json_path=args.input,
        output_dir=args.output,
        val_ratio=args.val_ratio,
        seed=args.seed
    )

