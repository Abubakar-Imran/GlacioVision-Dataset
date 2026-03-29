import os
import shutil
import argparse

def create_raw(base_dir, output_dir, glaciers, years):
    for glacier in glaciers:
        for year in years:
            dest_inputs = os.path.join(output_dir, glacier, str(year), "inputs")
            dest_labels = os.path.join(output_dir, glacier, str(year), "labels")

            os.makedirs(dest_inputs, exist_ok=True)
            os.makedirs(dest_labels, exist_ok=True)

            files = {
                "climate": f"{base_dir}/climate/{glacier}/climate_input_{year}.csv",
                "stacked": f"{base_dir}/stacked/{glacier}/{year}.tif",
                "dem": f"{base_dir}/dem/{glacier}/{year}.tif",
                "mask": f"{base_dir}/mask/{glacier}/{year}.tif"
            }

            shutil.copy(files["climate"], os.path.join(dest_inputs, f"{year}_climate.csv"))
            shutil.copy(files["stacked"], os.path.join(dest_inputs, f"{year}_satellite.tif"))
            shutil.copy(files["dem"], os.path.join(dest_labels, f"{year}_dem.tif"))
            shutil.copy(files["mask"], os.path.join(dest_labels, f"{year}_mask.tif"))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base_dir", required=True)
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--glaciers", nargs="+", required=True)
    parser.add_argument("--years", nargs="+", type=int, required=True)

    args = parser.parse_args()
    create_raw(args.base_dir, args.output_dir, args.glaciers, args.years)