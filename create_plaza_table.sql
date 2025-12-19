-- Crear tabla plaza
CREATE TABLE IF NOT EXISTS plaza (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    sede_id INTEGER NOT NULL REFERENCES sede(id),
    croquis_url TEXT
);

-- Agregar plaza_id a sala_profesores
ALTER TABLE sala_profesores ADD COLUMN IF NOT EXISTS plaza_id INTEGER REFERENCES plaza(id);

-- Insertar plazas por defecto para cada sede
INSERT INTO plaza (nombre, sede_id) 
SELECT 'Piso 1', id FROM sede 
WHERE NOT EXISTS (SELECT 1 FROM plaza WHERE nombre = 'Piso 1' AND sede_id = sede.id);

INSERT INTO plaza (nombre, sede_id) 
SELECT 'Piso 2', id FROM sede 
WHERE NOT EXISTS (SELECT 1 FROM plaza WHERE nombre = 'Piso 2' AND sede_id = sede.id);