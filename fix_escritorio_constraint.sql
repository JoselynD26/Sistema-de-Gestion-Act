-- Arreglar la constraint de escritorio para que apunte a sala_profesores
-- Primero eliminar la constraint existente
ALTER TABLE escritorio DROP CONSTRAINT IF EXISTS escritorio_sala_id_fkey;

-- Crear la nueva constraint apuntando a sala_profesores
ALTER TABLE escritorio ADD CONSTRAINT escritorio_sala_id_fkey 
FOREIGN KEY (sala_id) REFERENCES sala_profesores(id);