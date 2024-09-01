BEGIN;

-- Create the table if it does not exist
CREATE TABLE IF NOT EXISTS density_summary (
    area VARCHAR(5),
    min_density INT,
    max_density INT
);

-- Calculate the minimum and maximum Density and insert the results into density_summary
INSERT INTO density_summary (area, min_density, max_density)
SELECT
    Area,
    MIN(Density) AS min_density,
    MAX(Density) AS max_density
FROM
    insurance_claims
GROUP BY
    Area;

COMMIT;