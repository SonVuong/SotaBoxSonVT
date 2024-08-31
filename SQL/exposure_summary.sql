CREATE TABLE exposure_summary AS
SELECT 
    VehBrand,
    Area,
    SUM(Exposure) AS total_exposure
FROM 
    insurance_data
GROUP BY 
    VehBrand, 
    Area;
