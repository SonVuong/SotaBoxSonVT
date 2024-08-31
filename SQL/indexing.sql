-- Create an index on the Area column for quick lookups and grouping
CREATE INDEX idx_insurance_claims_area ON insurance_claims (Area);

-- Create an index on the VehBrand column for faster aggregation and joins
CREATE INDEX idx_insurance_claims_vehbrand ON insurance_claims (VehBrand);

-- Index on Density column to speed up queries involving min/max calculations
CREATE INDEX idx_insurance_claims_density ON insurance_claims (Density);

-- Create indexes on the exposure_summary table
CREATE INDEX idx_exposure_summary_area ON exposure_summary (Area);
CREATE INDEX idx_exposure_summary_vehbrand ON exposure_summary (VehBrand);

-- Create indexes on the density_summary table
CREATE INDEX idx_density_summary_area ON density_summary (Area);
