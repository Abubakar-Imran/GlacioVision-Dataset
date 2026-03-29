import rasterio
import numpy as np
import argparse
import os
from rasterio.warp import reproject, Resampling

def match_raster(ref_path, src_path):
    with rasterio.open(ref_path) as ref:
        profile = ref.profile
        shape = (ref.height, ref.width)
        transform = ref.transform
        crs = ref.crs

    with rasterio.open(src_path) as src:
        data = np.empty((src.count, *shape), dtype=src.dtypes[0])

        for i in range(src.count):
            reproject(
                source=src.read(i+1),
                destination=data[i],
                src_transform=src.transform,
                src_crs=src.crs,
                dst_transform=transform,
                dst_crs=crs,
                resampling=Resampling.bilinear
            )

    return data, profile

def stack_rasters(sentinel_path, dem_path, output_path):
    with rasterio.open(sentinel_path) as s:
        s_data = s.read()
        profile = s.profile

    dem_data, _ = match_raster(sentinel_path, dem_path)

    stacked = np.concatenate([s_data, dem_data], axis=0)

    profile.update(count=stacked.shape[0], compress="lzw")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with rasterio.open(output_path, "w", **profile) as dst:
        for i in range(stacked.shape[0]):
            dst.write(stacked[i], i+1)

    print(f"Saved: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--sentinel", required=True)
    parser.add_argument("--dem", required=True)
    parser.add_argument("--output", required=True)

    args = parser.parse_args()
    stack_rasters(args.sentinel, args.dem, args.output)