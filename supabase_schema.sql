-- Script para crear el schema completo en Supabase
-- Ejecutar en el SQL Editor de Supabase

-- Crear tipos ENUM
CREATE TYPE regimen_enum AS ENUM ('LOES', 'Codigo de trabajo');
CREATE TYPE observacion_enum AS ENUM ('Medio tiempo', 'Tiempo completo');

-- Tabla sede
CREATE TABLE sede (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    ubicacion VARCHAR NOT NULL
);

-- Tabla usuario
CREATE TABLE usuario (
    id SERIAL PRIMARY KEY,
    nombres VARCHAR,
    apellidos VARCHAR,
    correo VARCHAR(100) UNIQUE NOT NULL,
    contrasena VARCHAR(100) NOT NULL,
    rol VARCHAR(50) NOT NULL,
    id_docente INTEGER
);

-- Tabla docente
CREATE TABLE docente (
    id SERIAL PRIMARY KEY,
    cedula VARCHAR UNIQUE NOT NULL,
    correo VARCHAR NOT NULL,
    apellidos VARCHAR NOT NULL,
    nombres VARCHAR NOT NULL,
    regimen regimen_enum NOT NULL,
    observacion observacion_enum NOT NULL,
    sede_id INTEGER NOT NULL REFERENCES sede(id)
);

-- Tabla carrera
CREATE TABLE carrera (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    codigo VARCHAR(20) UNIQUE NOT NULL
);

-- Tabla materia
CREATE TABLE materia (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    codigo VARCHAR(20) UNIQUE NOT NULL
);

-- Tabla sala
CREATE TABLE sala (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    capacidad INTEGER NOT NULL,
    sede_id INTEGER NOT NULL REFERENCES sede(id)
);

-- Tabla aula
CREATE TABLE aula (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    capacidad INTEGER NOT NULL,
    sede_id INTEGER NOT NULL REFERENCES sede(id)
);

-- Tabla escritorio
CREATE TABLE escritorio (
    id SERIAL PRIMARY KEY,
    numero VARCHAR(50) NOT NULL,
    sala_id INTEGER NOT NULL REFERENCES sala(id),
    docente_id INTEGER REFERENCES docente(id)
);

-- Tabla curso
CREATE TABLE curso (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    nivel VARCHAR(50) NOT NULL,
    paralelo VARCHAR(10) NOT NULL,
    carrera_id INTEGER NOT NULL REFERENCES carrera(id),
    sede_id INTEGER NOT NULL REFERENCES sede(id)
);

-- Tabla horario
CREATE TABLE horario (
    id SERIAL PRIMARY KEY,
    dia VARCHAR(20) NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    materia_id INTEGER NOT NULL REFERENCES materia(id),
    docente_id INTEGER NOT NULL REFERENCES docente(id),
    aula_id INTEGER NOT NULL REFERENCES aula(id),
    curso_id INTEGER NOT NULL REFERENCES curso(id),
    sede_id INTEGER NOT NULL REFERENCES sede(id)
);

-- Tabla reserva
CREATE TABLE reserva (
    id SERIAL PRIMARY KEY,
    fecha DATE NOT NULL,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    motivo VARCHAR NOT NULL,
    estado VARCHAR(20) DEFAULT 'pendiente',
    docente_id INTEGER NOT NULL REFERENCES docente(id),
    aula_id INTEGER NOT NULL REFERENCES aula(id)
);

-- Tablas de relaciones many-to-many
CREATE TABLE carrera_sede (
    carrera_id INTEGER REFERENCES carrera(id),
    sede_id INTEGER REFERENCES sede(id),
    PRIMARY KEY (carrera_id, sede_id)
);

CREATE TABLE docente_materia (
    docente_id INTEGER REFERENCES docente(id),
    materia_id INTEGER REFERENCES materia(id),
    PRIMARY KEY (docente_id, materia_id)
);

CREATE TABLE docente_carrera (
    docente_id INTEGER REFERENCES docente(id),
    carrera_id INTEGER REFERENCES carrera(id),
    PRIMARY KEY (docente_id, carrera_id)
);

CREATE TABLE sede_materia (
    sede_id INTEGER REFERENCES sede(id),
    materia_id INTEGER REFERENCES materia(id),
    PRIMARY KEY (sede_id, materia_id)
);

CREATE TABLE materia_carrera (
    materia_id INTEGER REFERENCES materia(id),
    carrera_id INTEGER REFERENCES carrera(id),
    PRIMARY KEY (materia_id, carrera_id)
);

-- Índices para mejorar rendimiento
CREATE INDEX idx_usuario_correo ON usuario(correo);
CREATE INDEX idx_docente_cedula ON docente(cedula);
CREATE INDEX idx_horario_fecha ON horario(dia);
CREATE INDEX idx_reserva_fecha ON reserva(fecha);

-- Insertar datos iniciales
INSERT INTO sede (nombre, ubicacion) VALUES 
('Sede Principal', 'Quito Centro'),
('Sede Norte', 'Quito Norte');

-- Comentarios para documentación
COMMENT ON TABLE usuario IS 'Tabla de usuarios del sistema (admin, docente)';
COMMENT ON TABLE docente IS 'Información de docentes';
COMMENT ON TABLE sede IS 'Sedes del instituto';
COMMENT ON TABLE horario IS 'Horarios de clases';
COMMENT ON TABLE reserva IS 'Reservas de aulas';