# Data Generation Pipeline

## Overview

This document describes the complete pipeline used to construct the glacier dataset, including data acquisition, preprocessing, and final dataset generation. The pipeline integrates multi-source data, including climate reanalysis, satellite imagery, and elevation measurements, to produce a structured dataset suitable for machine learning and geospatial analysis.

The workflow consists of the following major stages:

1. Climate data acquisition and processing
2. Satellite imagery generation (Sentinel-1 and Sentinel-2)
3. Elevation data extraction and interpolation
4. Multi-source raster stacking
5. Dataset structuring (raw, patches, inference)

---

## 1. Climate Data Acquisition and Processing

### Source

Climate data is obtained from the Copernicus Atmosphere Data Store (ADS):

* Dataset: CAMS Global Reanalysis (EAC4)
* URL: https://ads.atmosphere.copernicus.eu/datasets/cams-global-reanalysis-eac4

### Procedure

1. Select variables such as:

   * geopotential
   * temperature (2m)
   * dewpoint temperature
   * relative humidity
   * surface pressure
   * total column water vapor
   * snow depth and albedo

2. Define spatial extent using glacier bounding box coordinates.

3. Select temporal range (2018–2024 to support hydrological year splitting).

4. Download data as CSV.

### Processing

The downloaded data is processed into hydrological years using:

```
scripts/climate/process_climate.py
```

Hydrological year definition:

* Start: October 1 (previous year)
* End: September 30 (target year)

### Output

```
climate/{glacier}/climate_input_{year}.csv
```

---

## 2. Satellite Data Acquisition (Sentinel-1 & Sentinel-2)

### Source

Satellite imagery is obtained using Google Earth Engine (GEE):

* Sentinel-2 Surface Reflectance
* Sentinel-1 Ground Range Detected (GRD)

### Script

```
scripts/satellite/sentinel_gee_script.js
```

### Processing Steps

For each glacier and year:

1. Define Area of Interest (AOI) using glacier shapefile
2. Filter by date range (June–September)
3. Apply cloud filtering (<30%) for Sentinel-2
4. Compute median composite

### Derived Bands

* Sentinel-2 bands: B2, B3, B4, B8, B11, B12
* Normalized Difference Snow Index (NDSI)
* Sentinel-1 bands: VV, VH

### Output

Multi-band GeoTIFF per year:

```
Satellite Data/{glacier}/{glacier}_{year}.tif
```

---

## 3. Elevation Data Processing (GEDI)

### Source

Elevation data is obtained from NASA GEDI:

* Dataset: GEDI L2A Elevation and Height Metrics
* Format: `.h5`

### Extraction

Raw GEDI files are processed using:

```
scripts/elevation/extract_gedi.py
```

### Processing Steps

1. Extract:

   * latitude
   * longitude
   * elevation (highest return)

2. Apply filtering:

   * valid coordinates
   * quality flag filtering
   * removal of degraded signals

3. Aggregate data per year

### Output

```
GEDI_{year}.csv
```

---

## 4. Elevation Interpolation

### Tool

Interpolation is performed using QGIS.

### Steps

1. Load CSV as point layer
2. Reproject to target CRS (e.g., EPSG:32643)
3. Remove outliers
4. Apply IDW interpolation

### Output

Continuous elevation raster:

```
Elevation/{glacier}/{year}.tif
```

---

## 5. Raster Stacking

Satellite and elevation data are combined into a unified multi-band raster.

### Script

```
scripts/preprocessing/stack_rasters.py
```

### Process

1. Align elevation raster to satellite grid
2. Resample elevation using bilinear interpolation
3. Stack bands:

* Sentinel-2 (6 bands)
* NDSI (1 band)
* Sentinel-1 (2 bands)
* Elevation (1 band)

### Output

```
stacked/{glacier}/{year}.tif
```

---

## 6. Raw Dataset Creation

The dataset is organized into a structured format for downstream processing.

### Script

```
scripts/dataset_creation/create_raw_dataset.py
```

### Structure

```
raw/{glacier}/{year}/
    inputs/
        {year}_climate.csv
        {year}_satellite.tif
    labels/
        {year}_dem.tif
        {year}_mask.tif
```

---

## 7. Patch Generation

To support machine learning workflows, raster data is divided into patches.

### Script

```
scripts/dataset_creation/create_patches.py
```

### Parameters

* Patch size: 256 × 256
* Overlap: 50% (stride = 128)

### Output Structure

```
patches/{glacier}/{year}/
    inputs/
        image/
        climate/
    outputs/
        output_mask/
        output_dem/
```

Each patch includes:

* multi-band raster input
* corresponding glacier mask
* elevation target
* associated climate data

---

## 8. Inference Dataset Creation

A simplified dataset format is created for inference and evaluation.

### Script

```
scripts/dataset_creation/create_inference_dataset.py
```

### Structure

```
inference/{glacier}/
    climate/
    satellite/
    output/
```

---

## Reproducibility

All steps in this pipeline can be reproduced using the scripts provided in the `scripts/` directory. Users are expected to:

1. Download raw data from the original sources
2. Execute scripts in the order described above
3. Use consistent coordinate reference systems and spatial resolutions

---

## Notes

* Temporal consistency is maintained using hydrological years
* Spatial alignment is enforced during raster stacking
* Quality filtering is applied to ensure reliability of elevation data
* Patch generation enables scalable machine learning workflows

---

## Citation

If you use this dataset or pipeline, please cite the associated Zenodo record:

https://doi.org/10.5281/zenodo.19305311
