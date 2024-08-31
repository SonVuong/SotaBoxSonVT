-- Create a new role for read-only access
CREATE ROLE readonly_user WITH LOGIN PASSWORD 'readonly';

-- Grant SELECT permissions to the readonly_user for all tables
GRANT SELECT ON TABLE insurance_claims TO readonly_user;
GRANT SELECT ON TABLE exposure_summary TO readonly_user;
GRANT SELECT ON TABLE density_summary TO readonly_user;

-- Create a new role for read-write access
CREATE ROLE readwrite_user WITH LOGIN PASSWORD 'readwrite';

-- Grant SELECT, INSERT, UPDATE, and DELETE permissions to the readwrite_user for all tables
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE insurance_claims TO readwrite_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE exposure_summary TO readwrite_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE density_summary TO readwrite_user;
