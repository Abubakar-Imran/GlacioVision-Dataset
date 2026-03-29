import pandas as pd
import os
import argparse

COLUMNS = [
    "geopotential",
    "relative_humidity",
    "vertical_velocity",
    "dewpoint_2m_K",
    "temperature_2m_K",
    "mean_sea_level_pressure_Pa",
    "surface_pressure_Pa",
    "total_column_water_vapor",
    "snow_albedo",
    "snow_depth_m"
]

def extract_window(df, target_year):
    start = pd.Timestamp(target_year - 1, 10, 1)
    end = pd.Timestamp(target_year, 9, 30)
    return df[(df["time"] >= start) & (df["time"] <= end)]

def process_climate(input_csv, output_dir, start_year, end_year):
    df = pd.read_csv(input_csv)
    df["time"] = pd.to_datetime(df["time"])

    df["month"] = df["time"].dt.month
    df["year"] = df["time"].dt.year

    os.makedirs(output_dir, exist_ok=True)

    for yr in range(start_year, end_year + 1):
        subset = extract_window(df, yr)
        subset = subset[["year", "month"] + COLUMNS]

        out_path = os.path.join(output_dir, f"climate_input_{yr}.csv")
        subset.to_csv(out_path, index=False)
        print(f"Saved: {out_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_csv", required=True)
    parser.add_argument("--output_dir", required=True)
    parser.add_argument("--start_year", type=int, default=2019)
    parser.add_argument("--end_year", type=int, default=2024)

    args = parser.parse_args()
    process_climate(args.input_csv, args.output_dir, args.start_year, args.end_year)