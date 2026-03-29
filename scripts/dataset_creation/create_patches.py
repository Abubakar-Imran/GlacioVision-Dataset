import os
import rasterio
from rasterio.windows import Window
import argparse

def create_patches(raw_dir, output_dir, patch_size=256, stride=None):
    stride = stride or patch_size // 2

    for glacier in os.listdir(raw_dir):
        for year in os.listdir(os.path.join(raw_dir, glacier)):

            base = os.path.join(raw_dir, glacier, year)

            img_path = os.path.join(base, "inputs", f"{year}_satellite.tif")
            mask_path = os.path.join(base, "labels", f"{year}_mask.tif")
            dem_path = os.path.join(base, "labels", f"{year}_dem.tif")
            climate_path = os.path.join(base, "inputs", f"{year}_climate.csv")

            save_dir = os.path.join(output_dir, glacier, year)

            dirs = {
                "img": os.path.join(save_dir, "inputs/image"),
                "mask": os.path.join(save_dir, "outputs/output_mask"),
                "dem": os.path.join(save_dir, "outputs/output_dem"),
                "climate": os.path.join(save_dir, "inputs/climate")
            }

            for d in dirs.values():
                os.makedirs(d, exist_ok=True)

            with rasterio.open(img_path) as img, \
                 rasterio.open(mask_path) as mask, \
                 rasterio.open(dem_path) as dem:

                for y in range(0, img.height - patch_size + 1, stride):
                    for x in range(0, img.width - patch_size + 1, stride):

                        win = Window(x, y, patch_size, patch_size)

                        patch_id = f"{year}_{y}_{x}"

                        meta = img.meta.copy()
                        meta.update(height=patch_size, width=patch_size)

                        with rasterio.open(os.path.join(dirs["img"], f"{patch_id}.tif"), "w", **meta) as dst:
                            dst.write(img.read(window=win))

                        with rasterio.open(os.path.join(dirs["mask"], f"{patch_id}.tif"), "w", **meta) as dst:
                            dst.write(mask.read(1, window=win), 1)

                        with rasterio.open(os.path.join(dirs["dem"], f"{patch_id}.tif"), "w", **meta) as dst:
                            dst.write(dem.read(1, window=win), 1)

                        # copy climate once
                        climate_out = os.path.join(dirs["climate"], f"{year}_climate.csv")
                        if not os.path.exists(climate_out):
                            import shutil
                            shutil.copy(climate_path, climate_out)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw_dir", required=True)
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--patch_size", type=int, default=256)

    args = parser.parse_args()
    create_patches(args.raw_dir, args.output_dir, args.patch_size)