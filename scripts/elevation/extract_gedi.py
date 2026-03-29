import h5py
import pandas as pd
import numpy as np
import glob
import os
import argparse

def extract_gedi(input_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    files = sorted(glob.glob(os.path.join(input_dir, "*.h5")))
    yearly_records = {}

    for f in files:
        filename = os.path.basename(f)

        try:
            year = int(filename[9:13])
            print(f"Processing {filename}")

            with h5py.File(f, "r") as h5f:
                beams = [b for b in h5f.keys() if b.startswith("BEAM")]

                for beam in beams:
                    try:
                        lat = h5f[f"{beam}/lat_highestreturn"][:]
                        lon = h5f[f"{beam}/lon_highestreturn"][:]
                        elev = h5f[f"{beam}/elev_highestreturn"][:]

                        qflag = h5f[f"{beam}/quality_flag"][:] if f"{beam}/quality_flag" in h5f else np.nan
                        dflag = h5f[f"{beam}/degrade_flag"][:] if f"{beam}/degrade_flag" in h5f else 0

                        valid = (
                            np.isfinite(lat) &
                            np.isfinite(lon) &
                            np.isfinite(elev) &
                            ((qflag == 1) | np.isnan(qflag)) &
                            (dflag == 0)
                        )

                        df = pd.DataFrame({
                            "latitude": lat[valid],
                            "longitude": lon[valid],
                            "elevation": elev[valid]
                        })

                        if year not in yearly_records:
                            yearly_records[year] = []
                        yearly_records[year].append(df)

                    except Exception as e:
                        print(f"Skipping beam: {beam} ({e})")

        except Exception as e:
            print(f"Skipping file: {filename} ({e})")

    for year, dfs in yearly_records.items():
        df_all = pd.concat(dfs, ignore_index=True)
        out_path = os.path.join(output_dir, f"GEDI_{year}.csv")
        df_all.to_csv(out_path, index=False)
        print(f"Saved: {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_dir", required=True)
    parser.add_argument("--output_dir", required=True)

    args = parser.parse_args()
    extract_gedi(args.input_dir, args.output_dir)