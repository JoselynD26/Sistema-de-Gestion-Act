-- Crear usuario administrador en Supabase
-- Ejecutar en el SQL Editor de Supabase

INSERT INTO usuario (nombres, apellidos, correo, contrasena, rol) 
VALUES (
    'Raul', 
    'Hidalgo', 
    'hidalgo11141@gmail.com', 
    '$2b$12$LQv3c1yqBwlFFzpeNweMcOElwibpBuS4LsANjH.P6VtjKFiQBdHSS', -- admin123 hasheado
    'admin'
);

-- Verificar que se creó correctamente
SELECT id, nombres, apellidos, correo, rol FROM usuario WHERE correo = 'hidalgo11141@gmail.com';