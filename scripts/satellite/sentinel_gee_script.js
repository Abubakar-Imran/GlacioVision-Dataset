// Load the glacier shapefile and set map center
var shapefile = ee.FeatureCollection('projects/assets/Glacier_Shape');

// Safely extract geometry from the first feature
var aoi = ee.Feature(shapefile.first()).geometry();

// Visualize and center
Map.centerObject(aoi, 11);
Map.addLayer(shapefile.style({color: 'cyan', fillColor: '00000000', width: 2}), {}, 'Glacier Boundary');


// Loop over each year from 2018 to 2024
var startYear = 2018;
var endYear = 2024;

for (var year = startYear; year <= endYear; year++) {
  var startDate = ee.Date.fromYMD(year, 6, 1);
  var endDate = ee.Date.fromYMD(year, 9, 30);
  
  // Sentinel-2 preprocessing
  var s2 = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
    .filterBounds(aoi)
    .filterDate(startDate, endDate)
    .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 30))
    .map(function(img){ return img.clip(aoi); });
    
  var s2_median = s2.median();
  var ndsi = s2_median.normalizedDifference(['B3', 'B11']).rename('NDSI');
  var s2_resampled = s2_median.select(['B2','B3','B4','B8','B11','B12']);
  var s2_with_ndsi = s2_resampled.addBands(ndsi);

  // Sentinel-1 preprocessing
  var s1 = ee.ImageCollection('COPERNICUS/S1_GRD')
    .filterBounds(aoi)
    .filterDate(startDate, endDate)
    .filter(ee.Filter.eq('instrumentMode', 'IW'))
    .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))
    .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))
    .filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'))
    .map(function(img){ return img.clip(aoi); });

  var s1_median = s1.median().select(['VV', 'VH']);

  // Stack all bands
  var stacked = s2_with_ndsi.addBands(s1_median).toFloat();

  // Export to Google Drive
  Export.image.toDrive({
    image: stacked,
    description: 'Glacier_' + year,
    folder: 'Satellite Data', 
    fileNamePrefix: 'glacier_' + year,
    region: aoi,
    scale: 25,
    crs: 'EPSG:32643',
    maxPixels: 1e13
  });
}