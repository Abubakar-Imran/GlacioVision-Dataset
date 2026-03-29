import os
import shutil
import argparse

def create_inference(base_dir, output_dir, glaciers, years):
    for glacier in glaciers:
        dest_root = os.path.join(output_dir, glacier)

        dirs = {
            "climate": os.path.join(dest_root, "climate"),
            "satellite": os.path.join(dest_root, "satellite"),
            "output": os.path.join(dest_root, "output")
        }

        for d in dirs.values():
            os.makedirs(d, exist_ok=True)

        for year in years:
            try:
                shutil.copy(
                    f"{base_dir}/climate/{glacier}/climate_input_{year}.csv",
                    f"{dirs['climate']}/{year}.csv"
                )
                shutil.copy(
                    f"{base_dir}/stacked/{glacier}/{year}.tif",
                    f"{dirs['satellite']}/{year}.tif"
                )
                shutil.copy(
                    f"{base_dir}/dem/{glacier}/{year}.tif",
                    f"{dirs['output']}/{year}_dem.tif"
                )
                shutil.copy(
                    f"{base_dir}/mask/{glacier}/{year}.tif",
                    f"{dirs['output']}/{year}_mask.tif"
                )
            except FileNotFoundError as e:
                print(f"Missing: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--base_dir", required=True)
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--glaciers", nargs="+", required=True)
    parser.add_argument("--years", nargs="+", type=int, required=True)

    args = parser.parse_args()
    create_inference(args.base_dir, args.output_dir, args.glaciers, args.years)