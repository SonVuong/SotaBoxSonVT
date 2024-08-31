-- Create a new role for read-only access
CREATE ROLE readonly_user WITH LOGIN PASSWORD 'readonly';

-- Grant SELECT permissions to the readonly_user for all tables
GRANT SELECT ON TABLE insurance_data TO readonly_user;
GRANT SELECT ON TABLE exposure_summary TO readonly_user;
GRANT SELECT ON TABLE density_summary TO readonly_user;

-- Create a new role for write access
CREATE ROLE writeonly_user WITH LOGIN PASSWORD 'writeonly';

-- Grant INSERT, UPDATE permissions to the writeonly_user for all tables
GRANT INSERT, UPDATE ON TABLE insurance_data TO writeonly_user;
GRANT INSERT, UPDATE ON TABLE exposure_summary TO writeonly_user;
GRANT INSERT, UPDATE ON TABLE density_summary TO writeonly_user;

-- Create a new role for read-write access
CREATE ROLE readwrite_user WITH LOGIN PASSWORD 'readwrite';

-- Grant SELECT, INSERT, UPDATE, and DELETE permissions to the readwrite_user for all tables
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE insurance_data TO readwrite_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE exposure_summary TO readwrite_user;
GRANT SELECT, INSERT, UPDATE, DELETE ON TABLE density_summary TO readwrite_user;

-- Create the role with managing tables
CREATE ROLE table_manager WITH LOGIN PASSWORD 'tablemanager';

-- Grant Privilege on the Database
GRANT CREATE ON DATABASE your_database TO table_manager;
GRANT USAGE ON SCHEMA public TO table_manager;
GRANT CREATE ON SCHEMA public TO table_manager