CREATE TABLE density_summary AS
SELECT 
    Area,
    MIN(Density) AS min_density,
    MAX(Density) AS max_density
FROM 
    insurance_data
GROUP BY 
    Area;
