-- Base de datos separada para la suite de tests.
-- Los tests NUNCA deben ejecutarse contra la base principal.
SELECT 'CREATE DATABASE ruta_utilities_test'
WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'ruta_utilities_test')\gexec
