# GlacioVision Dataset (2019–2024)

## Overview

This dataset provides a comprehensive, multi-modal collection of glacier-related data for four glaciers of Pakistan, which includes **Siachen**, **Baltoro**, **Batura**, and **Chiantar**, spanning the years **2019 to 2024**. It is designed to support research in **glaciology, remote sensing, climate science, and machine learning**, particularly for tasks such as glacier segmentation, elevation prediction, and temporal analysis.

The dataset integrates **satellite imagery, meteorological variables, and elevation data**, processed into both **raw geospatial formats** and **machine learning–ready patches**.

---

## 📦 Dataset Access
Download the dataset from Zenodo:

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19305311.svg)](https://doi.org/10.5281/zenodo.19305311)

---

## Key Features

* Multi-year coverage: **2019–2024**
* Multi-glacier dataset: **4 glaciers**
* Multi-modal inputs:

  * Satellite imagery (Sentinel-1 + Sentinel-2)
  * Climate variables
  * Elevation data 
* Pixel-aligned inputs and outputs
* Patch-based dataset for deep learning
* Fully reproducible pipeline

---

## Dataset Structure

```
GlacioVision-Dataset/
│
├── patches/              # ML-ready dataset (primary)
├── raw/                  # Full-resolution aligned data
├── inference/            # Inference-ready structure
│
├── pipeline/             # Data processing scripts
├── metadata/             # Dataset metadata and indexing
│
├── README.md
├── LICENSE
```

---

## 1. Patch-Based Dataset (Primary)

```
patches/{glacier}/{year}/
  ├── inputs/
  │     ├── image/              # Multi-band GeoTIFF patches
  │     ├── climate/            # Year-wise climate CSV
  │
  ├── outputs/
        ├── output_mask/        # Glacier segmentation mask
        ├── output_dem/         # Elevation patches
```

### Patch Specifications

* Patch size: **256 × 256 pixels**
* Overlap: **50% (stride = 128)**
* Naming convention:

  ```
  {year}_patch_{row}_{col}.tif
  ```
* All patches are **spatially aligned across modalities**

### Modalities

* **Image patches**: 10-band raster

  * Sentinel-2: B2, B3, B4, B8, B11, B12
  * Derived: NDSI
  * Sentinel-1: VV, VH
  * Elevation: Elevation band
* **Mask patches**: Binary glacier masks
* **DEM patches**: Continuous elevation values
* **Climate data**: Year-specific CSV (shared across patches)

---

## 2. Raw Dataset

```
raw/{glacier}/{year}/
  ├── inputs/
  │     ├── {year}_satellite_dem.tif
  │     ├── {year}_climate_input.csv
  │
  ├── labels/
        ├── {year}_dem_output.tif
        ├── {year}_glacier_mask.tif
```

This version preserves:

* Full spatial resolution
* Original alignment before patch extraction

---

## 3. Inference Dataset

```
inference/{glacier}/
  ├── Climate Data/
  ├── Satellite Data/
  ├── Output/
  ├── Predicted/
```

Used for:

* Model evaluation
* Real-world deployment scenarios

---

## Data Sources and Processing

### 1. Climate Data

* Source: CAMS Global Reanalysis (EAC4)
* Spatial selection: Glacier bounding box
* Temporal window:

  * **October (previous year) → September (current year)**

#### Variables Included

* Geopotential
* Relative humidity
* Vertical velocity
* Dewpoint temperature (2m)
* Temperature (2m)
* Mean sea level pressure
* Surface pressure
* Total column water vapor
* Snow albedo
* Snow depth

---

### 2. Satellite Data

#### Sentinel-2

* Bands: B2, B3, B4, B8, B11, B12
* Derived index: NDSI
* Cloud filtering: < 30%
* Temporal aggregation: Median composite (June–September)

#### Sentinel-1

* Polarizations: VV, VH
* Mode: IW
* Orbit: Ascending
* Temporal aggregation: Median composite

#### Output

* Combined into multi-band raster
* Spatial resolution: **25 meters**
* CRS: **EPSG:32643**

---

### 3. Elevation Data (DEM)

* Source: GEDI L2A data
* Processing steps:

  1. Extraction from HDF5 files
  2. Quality filtering:

     * Valid coordinates
     * Quality flags
     * Degradation filtering
  3. Conversion to CSV
  4. Interpolation (IDW) in QGIS software
* Output: Continuous elevation raster

---

### 4. Data Stacking

Satellite and elevation data are merged into a single raster:

* Total bands: **10**
* Band composition:

  * 6 Sentinel-2 bands
  * 1 NDSI
  * 2 Sentinel-1 bands
  * 1 Elevation band

All bands are:

* Reprojected
* Resampled
* Pixel-aligned

---

## Pipeline

The dataset is fully reproducible. Scripts are provided for:

* Climate data processing
* Satellite data extraction
* Elevation extraction and filtering
* Elevation interpolation
* Raster stacking
* Raw dataset construction
* Patch generation
* Inference dataset preparation

---

## Metadata

The `metadata/` directory includes:

* Dataset description
* Coordinate system information
* Patch index
* Variable definitions

---

## Usage

This dataset supports:

* Glacier segmentation
* Elevation prediction
* Multi-modal learning
* Time-series analysis
* Climate-glacier interaction studies

---

## Important Notes

* Climate data is **year-wise and shared across patches**
* All raster data is aligned to a common grid
* Missing or invalid values are filtered during preprocessing
* Elevation data is interpolated and may contain smoothing artifacts

---

## Limitations

* Elevation maps derived from interpolation (not direct measurement)
* Seasonal restriction in satellite data (June–September)
* Climate data is spatially aggregated over glacier extent

---

## License

This dataset is released under:


---

## Acknowledgments

* Copernicus Atmosphere Data Store (CAMS)
* Google Earth Engine
* NASA GEDI mission
* Open-source geospatial tools (QGIS, Rasterio, Pandas)

---
