BEGIN;

-- Create the table if it does not exist
CREATE TABLE IF NOT EXISTS exposure_summary (
    vehbrand VARCHAR(10),
    area VARCHAR(5),
    total_exposure DECIMAL(10, 2)
);

-- Calculate the sum of Exposure and insert the results into exposure_summary
INSERT INTO exposure_summary (vehbrand, area, total_exposure)
SELECT
    VehBrand,
    Area,
    SUM(Exposure) AS total_exposure
FROM
    insurance_claims
GROUP BY
    VehBrand, Area;

COMMIT;