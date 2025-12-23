-- Ver estructura de la tabla usuario
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default,
    character_maximum_length
FROM information_schema.columns 
WHERE table_name = 'usuario' 
ORDER BY ordinal_position;

-- Ver todos los datos de la tabla usuario
SELECT * FROM usuario;