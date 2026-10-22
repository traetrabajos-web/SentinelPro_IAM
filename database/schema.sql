-- ============================================================================
-- BASE DE DATOS COMPLETA: SENTINELPRO ACCESS & IAM (v2.5)
-- Sistema Empresarial de Control de Acceso Físico en Portería (Trabajadores),
-- Gestión de Garita (Rol Vigilante), Asistencia y Seguridad Granular IAM
-- ============================================================================
-- Compatible al 100% con: MySQL 5.7+, MySQL 8.0+, MariaDB, phpMyAdmin, 
-- DBeaver, Navicat, MySQL Workbench y consolas CLI.
--
-- INSTRUCCIONES DE IMPORTACIÓN RÁPIDA:
-- 1. Abre phpMyAdmin, MySQL Workbench o tu gestor de base de datos favorito.
-- 2. Dirígete a la pestaña "Importar" (o abre una ventana de consulta SQL).
-- 3. Selecciona este archivo "schema.sql" y pulsa "Ejecutar" (Go / Run).
-- 4. El script creará automáticamente la base de datos `sentinelpro_iam`,
--    todas sus 13 tablas relacionales con claves foráneas, restricciones,
--    índices de rendimiento y todos los datos iniciales pre-cargados (seeds).
-- ============================================================================

CREATE DATABASE IF NOT EXISTS `sentinelpro_iam` 
DEFAULT CHARACTER SET utf8mb4 
COLLATE utf8mb4_unicode_ci;

USE `sentinelpro_iam`;

-- Desactivar temporalmente revisión de claves foráneas para importación limpia
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------------------------------------------------------
-- LIMPIEZA DE TABLAS PREVIAS (SI EXISTEN)
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS `audit_logs`;
DROP TABLE IF EXISTS `sesiones_activas`;
DROP TABLE IF EXISTS `usuario_permisos_individuales`;
DROP TABLE IF EXISTS `usuarios`;
DROP TABLE IF EXISTS `roles_sistema`;
DROP TABLE IF EXISTS `permisos_catalogo`;
DROP TABLE IF EXISTS `incidencias_acceso`;
DROP TABLE IF EXISTS `visitantes`;
DROP TABLE IF EXISTS `registros_acceso`;
DROP TABLE IF EXISTS `trabajadores`;
DROP TABLE IF EXISTS `zonas_acceso`;
DROP TABLE IF EXISTS `turnos_laborales`;
DROP TABLE IF EXISTS `configuracion_empresa`;

-- ============================================================================
-- 1. TABLA: configuracion_empresa
-- ============================================================================
CREATE TABLE `configuracion_empresa` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `nombre_empresa` VARCHAR(150) NOT NULL,
  `nit_ruc` VARCHAR(50) NOT NULL,
  `rubro_empresa` VARCHAR(150) DEFAULT NULL,
  `slogan_corporativo` TEXT DEFAULT NULL,
  `direccion` VARCHAR(255) DEFAULT NULL,
  `telefono_central` VARCHAR(50) DEFAULT NULL,
  `email_seguridad` VARCHAR(120) DEFAULT NULL,
  `color_primario` VARCHAR(20) DEFAULT '#1e40af',
  `color_secundario` VARCHAR(20) DEFAULT '#0f172a',
  `tolerancia_tardanza_min` INT DEFAULT 10,
  `aforo_maximo_planta` INT DEFAULT 150
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 2. TABLA: turnos_laborales
-- ============================================================================
CREATE TABLE `turnos_laborales` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `codigo` VARCHAR(50) NOT NULL UNIQUE,
  `nombre` VARCHAR(100) NOT NULL,
  `hora_entrada` TIME NOT NULL,
  `hora_salida` TIME NOT NULL,
  `tolerancia_minutos` INT DEFAULT 10,
  `activo` TINYINT(1) DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 3. TABLA: zonas_acceso (PUERTAS FÍSICAS Y PUNTOS DE CONTROL)
-- ============================================================================
CREATE TABLE `zonas_acceso` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `codigo` VARCHAR(50) NOT NULL UNIQUE,
  `nombre` VARCHAR(120) NOT NULL,
  `tipo` VARCHAR(50) NOT NULL, -- PEATONAL, VEHICULAR, PLANTA_INDUSTRIAL, ALTA_SEGURIDAD
  `nivel_seguridad` VARCHAR(80) NOT NULL,
  `ubicacion` VARCHAR(150) DEFAULT NULL,
  `estado` VARCHAR(30) DEFAULT 'OPERATIVA',
  `requiere_autorizacion_especial` TINYINT(1) DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 4. TABLA: trabajadores (PADRÓN DE EMPLEADOS DE LA EMPRESA)
-- ============================================================================
CREATE TABLE `trabajadores` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `codigo_credencial` VARCHAR(50) NOT NULL UNIQUE,
  `documento` VARCHAR(50) NOT NULL UNIQUE,
  `nombre_completo` VARCHAR(150) NOT NULL,
  `cargo` VARCHAR(100) NOT NULL,
  `departamento` VARCHAR(100) NOT NULL,
  `telefono` VARCHAR(50) DEFAULT NULL,
  `email` VARCHAR(120) DEFAULT NULL,
  `turno_id` INT DEFAULT NULL,
  `zonas_autorizadas` TEXT DEFAULT NULL, -- JSON con IDs de puertas permitidas ej: [1,2,3]
  `placa_vehiculo` VARCHAR(30) DEFAULT NULL,
  `estado` VARCHAR(30) DEFAULT 'ACTIVO', -- ACTIVO, SUSPENDIDO, VACACIONES
  `ubicacion_actual` VARCHAR(30) DEFAULT 'FUERA_PLANTA', -- DENTRO_PLANTA, FUERA_PLANTA
  `ultima_puerta_id` INT DEFAULT NULL,
  `ultima_entrada` VARCHAR(60) DEFAULT NULL,
  CONSTRAINT `fk_trabajador_turno` FOREIGN KEY (`turno_id`) REFERENCES `turnos_laborales` (`id`) ON DELETE SET NULL,
  CONSTRAINT `fk_trabajador_puerta` FOREIGN KEY (`ultima_puerta_id`) REFERENCES `zonas_acceso` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX `idx_trabajadores_doc` ON `trabajadores` (`documento`);
CREATE INDEX `idx_trabajadores_cred` ON `trabajadores` (`codigo_credencial`);
CREATE INDEX `idx_trabajadores_estado` ON `trabajadores` (`estado`);
CREATE INDEX `idx_trabajadores_ubicacion` ON `trabajadores` (`ubicacion_actual`);

-- ============================================================================
-- 5. TABLA: registros_acceso (ASISTENCIA, ENTRADAS Y SALIDAS FÍSICAS)
-- ============================================================================
CREATE TABLE `registros_acceso` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `codigo_movimiento` VARCHAR(60) NOT NULL UNIQUE,
  `trabajador_id` INT NOT NULL,
  `codigo_credencial` VARCHAR(50) NOT NULL,
  `documento` VARCHAR(50) NOT NULL,
  `trabajador_nombre` VARCHAR(150) NOT NULL,
  `departamento` VARCHAR(100) DEFAULT NULL,
  `zona_id` INT DEFAULT NULL,
  `zona_nombre` VARCHAR(120) DEFAULT NULL,
  `fecha` DATE NOT NULL,
  `hora_entrada` VARCHAR(10) NOT NULL,
  `hora_salida` VARCHAR(10) DEFAULT NULL,
  `estado_asistencia` VARCHAR(30) DEFAULT 'PUNTUAL', -- PUNTUAL, TARDANZA
  `estado_ciclo` VARCHAR(30) DEFAULT 'EN_PLANTA', -- EN_PLANTA, FINALIZADO
  `minutos_trabajados` INT DEFAULT NULL,
  `horas_formateadas` VARCHAR(50) DEFAULT NULL,
  `metodo_identificacion` VARCHAR(50) DEFAULT 'TARJETA_RFID', -- TARJETA_RFID, DOCUMENTO_DNI, TERMINAL_KIOSCO_PIN
  `registrado_por_email` VARCHAR(120) DEFAULT NULL,
  `registrado_por_nombre` VARCHAR(150) DEFAULT NULL,
  `observacion` TEXT DEFAULT NULL,
  CONSTRAINT `fk_registro_trabajador` FOREIGN KEY (`trabajador_id`) REFERENCES `trabajadores` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_registro_zona` FOREIGN KEY (`zona_id`) REFERENCES `zonas_acceso` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX `idx_registros_fecha` ON `registros_acceso` (`fecha`);
CREATE INDEX `idx_registros_trabajador` ON `registros_acceso` (`trabajador_id`);
CREATE INDEX `idx_registros_ciclo` ON `registros_acceso` (`estado_ciclo`);

-- ============================================================================
-- 6. TABLA: visitantes (CONTROL DE VISITAS, PROVEEDORES Y CONTRATISTAS)
-- ============================================================================
CREATE TABLE `visitantes` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `gafete` VARCHAR(50) NOT NULL UNIQUE,
  `documento` VARCHAR(50) NOT NULL,
  `nombre_completo` VARCHAR(150) NOT NULL,
  `empresa_origen` VARCHAR(150) NOT NULL,
  `anfitrion_visitado` VARCHAR(150) NOT NULL,
  `zona_autorizada` VARCHAR(150) DEFAULT NULL,
  `motivo` TEXT DEFAULT NULL,
  `fecha` DATE NOT NULL,
  `hora_entrada` VARCHAR(10) NOT NULL,
  `hora_salida` VARCHAR(10) DEFAULT NULL,
  `estado` VARCHAR(30) DEFAULT 'EN_PLANTA', -- EN_PLANTA, SALIDA_REGISTRADA
  `registrado_por` VARCHAR(150) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX `idx_visitantes_estado` ON `visitantes` (`estado`);
CREATE INDEX `idx_visitantes_fecha` ON `visitantes` (`fecha`);

-- ============================================================================
-- 7. TABLA: incidencias_acceso (ALERTAS DE ACCESO FÍSICO DENEGADO)
-- ============================================================================
CREATE TABLE `incidencias_acceso` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `fecha_hora` VARCHAR(60) NOT NULL,
  `trabajador_nombre` VARCHAR(150) DEFAULT NULL,
  `documento` VARCHAR(50) DEFAULT NULL,
  `zona_nombre` VARCHAR(120) DEFAULT NULL,
  `tipo_alerta` VARCHAR(60) NOT NULL, -- CREDENCIAL_SUSPENDIDA, ZONA_NO_AUTORIZADA, FUERA_DE_TURNO
  `severidad` VARCHAR(30) DEFAULT 'ALTA', -- ALTA, MEDIA, BAJA
  `detalle` TEXT DEFAULT NULL,
  `estado_resolucion` VARCHAR(30) DEFAULT 'PENDIENTE', -- PENDIENTE, RESUELTA
  `registrado_por` VARCHAR(150) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX `idx_incidencias_estado` ON `incidencias_acceso` (`estado_resolucion`);

-- ============================================================================
-- 8. TABLA: permisos_catalogo (18 PERMISOS GRANULARES)
-- ============================================================================
CREATE TABLE `permisos_catalogo` (
  `codigo` VARCHAR(60) PRIMARY KEY,
  `modulo` VARCHAR(80) NOT NULL,
  `nombre` VARCHAR(120) NOT NULL,
  `descripcion` TEXT DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 9. TABLA: roles_sistema (4 ROLES BASE)
-- ============================================================================
CREATE TABLE `roles_sistema` (
  `codigo` VARCHAR(50) PRIMARY KEY,
  `nombre` VARCHAR(100) NOT NULL,
  `descripcion` TEXT DEFAULT NULL,
  `color_badge` VARCHAR(20) DEFAULT '#4f46e5',
  `permisos_base` TEXT DEFAULT NULL -- JSON con lista de códigos de permisos
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 10. TABLA: usuarios (CUENTAS DE OPERACIÓN DEL SISTEMA)
-- ============================================================================
CREATE TABLE `usuarios` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `nombre_completo` VARCHAR(150) NOT NULL,
  `email` VARCHAR(120) NOT NULL UNIQUE,
  `password_hash` VARCHAR(255) NOT NULL, -- Formato scrypt$salt$hash
  `rol` VARCHAR(50) NOT NULL,
  `cargo` VARCHAR(120) DEFAULT NULL,
  `max_sesiones_simultaneas` INT DEFAULT 1,
  `politica_concurrencia` VARCHAR(40) DEFAULT 'RECHAZAR_NUEVA',
  `activo` TINYINT(1) DEFAULT 1,
  `creado_en` VARCHAR(60) NOT NULL,
  CONSTRAINT `fk_usuario_rol` FOREIGN KEY (`rol`) REFERENCES `roles_sistema` (`codigo`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX `idx_usuarios_email` ON `usuarios` (`email`);

-- ============================================================================
-- 11. TABLA: usuario_permisos_individuales (OVERRIDES ALLOW / DENY)
-- ============================================================================
CREATE TABLE `usuario_permisos_individuales` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `usuario_id` INT NOT NULL,
  `permiso_codigo` VARCHAR(60) NOT NULL,
  `modo_override` VARCHAR(15) NOT NULL, -- ALLOW, DENY
  `actualizado_en` VARCHAR(60) DEFAULT NULL,
  UNIQUE KEY `uk_usuario_permiso` (`usuario_id`, `permiso_codigo`),
  CONSTRAINT `fk_override_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_override_permiso` FOREIGN KEY (`permiso_codigo`) REFERENCES `permisos_catalogo` (`codigo`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- ============================================================================
-- 12. TABLA: sesiones_activas (CONTROL DE SESIÓN Y TOKENS HMAC)
-- ============================================================================
CREATE TABLE `sesiones_activas` (
  `session_id` VARCHAR(64) PRIMARY KEY,
  `usuario_id` INT NOT NULL,
  `usuario_nombre` VARCHAR(150) DEFAULT NULL,
  `usuario_email` VARCHAR(120) DEFAULT NULL,
  `rol` VARCHAR(50) DEFAULT NULL,
  `ip` VARCHAR(60) DEFAULT NULL,
  `dispositivo` VARCHAR(150) DEFAULT NULL,
  `creada_en` VARCHAR(60) NOT NULL,
  `ultima_actividad` VARCHAR(60) NOT NULL,
  `expira_en` BIGINT NOT NULL,
  `activa` TINYINT(1) DEFAULT 1,
  CONSTRAINT `fk_sesion_usuario` FOREIGN KEY (`usuario_id`) REFERENCES `usuarios` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX `idx_sesiones_usuario` ON `sesiones_activas` (`usuario_id`);
CREATE INDEX `idx_sesiones_activa` ON `sesiones_activas` (`activa`);

-- ============================================================================
-- 13. TABLA: audit_logs (BITÁCORA INMUTABLE DE SEGURIDAD)
-- ============================================================================
CREATE TABLE `audit_logs` (
  `id` INT AUTO_INCREMENT PRIMARY KEY,
  `fecha_hora` VARCHAR(60) NOT NULL,
  `usuario_id` INT DEFAULT NULL,
  `usuario_email` VARCHAR(120) NOT NULL,
  `rol` VARCHAR(50) DEFAULT NULL,
  `evento` VARCHAR(80) NOT NULL,
  `modulo` VARCHAR(80) DEFAULT NULL,
  `permiso_evaluado` VARCHAR(60) DEFAULT NULL,
  `resultado` VARCHAR(30) DEFAULT 'EXITO', -- EXITO, DENEGADO, ALERTA
  `ip` VARCHAR(60) DEFAULT NULL,
  `detalle` TEXT DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE INDEX `idx_audit_fecha` ON `audit_logs` (`fecha_hora`);
CREATE INDEX `idx_audit_evento` ON `audit_logs` (`evento`);

-- ============================================================================
-- INSERCIÓN DE DATOS INICIALES (SEEDS Y USUARIOS CON CLAVES CIFRADAS)
-- ============================================================================

-- 1. Inserción de Configuración Corporativa
INSERT INTO `configuracion_empresa` 
(`id`, `nombre_empresa`, `nit_ruc`, `rubro_empresa`, `slogan_corporativo`, `direccion`, `telefono_central`, `email_seguridad`, `color_primario`, `color_secundario`, `tolerancia_tardanza_min`, `aforo_maximo_planta`) 
VALUES 
(1, 'Grupo Industrial & Logístico Titan S.A.', '901.452.889-1', 'Planta Industrial, Almacén y Oficinas Corporativas', 'Control de Acceso Físico en Portería, Asistencia de Trabajadores en Tiempo Real y Seguridad IAM por Roles', 'Parque Industrial Norte Km 14 — Complejo Empresarial B-12', '+57 300 912 4500', 'seguridad@grupotitan.com', '#1e40af', '#0f172a', 10, 150);

-- 2. Inserción de Turnos Laborales
INSERT INTO `turnos_laborales` (`id`, `codigo`, `nombre`, `hora_entrada`, `hora_salida`, `tolerancia_minutos`, `activo`) VALUES
(1, 'TURNO-MANANA', 'Turno Mañana (Planta y Oficinas)', '08:00:00', '17:00:00', 10, 1),
(2, 'TURNO-TARDE', 'Turno Tarde (Operaciones y Logística)', '14:00:00', '22:00:00', 10, 1),
(3, 'TURNO-NOCHE', 'Turno Nocturno (Seguridad y Mantenimiento)', '22:00:00', '06:00:00', 15, 1);

-- 3. Inserción de Zonas y Puertas Físicas
INSERT INTO `zonas_acceso` (`id`, `codigo`, `nombre`, `tipo`, `nivel_seguridad`, `ubicacion`, `estado`, `requiere_autorizacion_especial`) VALUES
(1, 'PUERTA-01', 'Portería Principal Peatonal (Torniquete Norte)', 'PEATONAL', 'NIVEL 1 — GENERAL', 'Entrada Principal Calle 100', 'OPERATIVA', 0),
(2, 'PUERTA-02', 'Garita de Acceso Vehicular y Muelle de Carga', 'VEHICULAR', 'NIVEL 2 — OPERATIVO', 'Acceso Sur — Patio de Maniobras', 'OPERATIVA', 0),
(3, 'PUERTA-03', 'Planta de Producción y Almacén de Materiales', 'PLANTA_INDUSTRIAL', 'NIVEL 3 — RESTRINGIDO', 'Nave Central — Sector B', 'OPERATIVA', 1),
(4, 'PUERTA-04', 'Bóveda de Servidores y DataCenter TI', 'ALTA_SEGURIDAD', 'NIVEL 4 — CRÍTICO BIOMÉTRICO', 'Piso 3 — Núcleo Blindado TI', 'OPERATIVA', 1);

-- 4. Inserción de Trabajadores
INSERT INTO `trabajadores` (`id`, `codigo_credencial`, `documento`, `nombre_completo`, `cargo`, `departamento`, `telefono`, `email`, `turno_id`, `zonas_autorizadas`, `placa_vehiculo`, `estado`, `ubicacion_actual`, `ultima_puerta_id`, `ultima_entrada`) VALUES
(1, 'EMP-001', '72849102', 'Javier Morales Castro', 'Jefe de Planta y Mantenimiento', 'Operaciones y Planta', '3004128890', 'jmorales@empresa.com', 1, '[1,2,3]', 'KLM-482', 'ACTIVO', 'DENTRO_PLANTA', 1, '2026-10-22 07:52'),
(2, 'EMP-002', '45918273', 'Daniela Ríos Salgado', 'Ingeniera de Infraestructura y Redes', 'Tecnología (TI)', '3115902341', 'drios@empresa.com', 1, '[1,2,3,4]', 'BGT-901', 'ACTIVO', 'DENTRO_PLANTA', 4, '2026-10-22 07:58'),
(3, 'EMP-003', '80192834', 'Andrés Felipe Pineda', 'Operador de Montacargas y Despacho', 'Logística y Almacén', '3158891203', 'apineda@empresa.com', 1, '[1,2,3]', 'MTR-119', 'ACTIVO', 'DENTRO_PLANTA', 2, '2026-10-22 08:19'),
(4, 'EMP-004', '52839104', 'Camila Torres Villalba', 'Analista Contable y Tesorería', 'Administración y Finanzas', '3017745612', 'ctorres@empresa.com', 1, '[1]', '', 'ACTIVO', 'FUERA_PLANTA', 1, '2026-10-22 07:55'),
(5, 'EMP-005', '10928374', 'Héctor Julio Ramírez', 'Técnico Electromecánico Senior', 'Operaciones y Planta', '3209918273', 'hramirez@empresa.com', 1, '[1,2,3]', 'ZXC-330', 'ACTIVO', 'FUERA_PLANTA', 1, '2026-10-21 07:56'),
(6, 'EMP-006', '39182736', 'Paola Andrea Vega', 'Coordinadora de Calidad e ISO', 'Calidad y Seguridad Industrial', '3146629182', 'pvega@empresa.com', 1, '[1,3]', '', 'ACTIVO', 'FUERA_PLANTA', 1, '2026-10-21 08:02'),
(7, 'EMP-007', '91827364', 'Miguel Ángel Duarte', 'Supervisor de Despachos Nocturnos', 'Logística y Almacén', '3183349012', 'mduarte@empresa.com', 2, '[1,2,3]', 'QWE-712', 'ACTIVO', 'FUERA_PLANTA', 2, '2026-10-21 13:55'),
(8, 'EMP-008', '66778899', 'Esteban Salazar (Credencial Suspendida)', 'Auxiliar Externo de Bodega', 'Logística y Almacén', '3001192837', 'esalazar@empresa.com', 1, '[1]', '', 'SUSPENDIDO', 'FUERA_PLANTA', 1, '2026-10-21 08:00');

-- 5. Inserción de Registros de Acceso y Asistencia
INSERT INTO `registros_acceso` (`id`, `codigo_movimiento`, `trabajador_id`, `codigo_credencial`, `documento`, `trabajador_nombre`, `departamento`, `zona_id`, `zona_nombre`, `fecha`, `hora_entrada`, `hora_salida`, `estado_asistencia`, `estado_ciclo`, `minutos_trabajados`, `horas_formateadas`, `metodo_identificacion`, `registrado_por_email`, `registrado_por_nombre`, `observacion`) VALUES
(1, 'ACC-1001', 1, 'EMP-001', '72849102', 'Javier Morales Castro', 'Operaciones y Planta', 1, 'Portería Principal Peatonal (Torniquete Norte)', '2026-10-22', '07:52', NULL, 'PUNTUAL', 'EN_PLANTA', NULL, 'En curso (En planta)', 'TARJETA_RFID', 'vigilante@sentinelpro.com', 'Sgto. Roberto Vargas', 'Ingreso normal con EPP verificado en portería.'),
(2, 'ACC-1002', 2, 'EMP-002', '45918273', 'Daniela Ríos Salgado', 'Tecnología (TI)', 4, 'Bóveda de Servidores y DataCenter TI', '2026-10-22', '07:58', NULL, 'PUNTUAL', 'EN_PLANTA', NULL, 'En curso (En planta)', 'BIOMETRICO_QR', 'vigilante@sentinelpro.com', 'Sgto. Roberto Vargas', 'Acceso autorizado a DataCenter para mantenimiento preventivo.'),
(3, 'ACC-1003', 3, 'EMP-003', '80192834', 'Andrés Felipe Pineda', 'Logística y Almacén', 2, 'Garita de Acceso Vehicular y Muelle de Carga', '2026-10-22', '08:19', NULL, 'TARDANZA', 'EN_PLANTA', NULL, 'En curso (En planta)', 'DOCUMENTO_DNI', 'vigilante@sentinelpro.com', 'Sgto. Roberto Vargas', 'Ingreso con 19 min de retraso respecto al Turno Mañana (08:00).'),
(4, 'ACC-1004', 4, 'EMP-004', '52839104', 'Camila Torres Villalba', 'Administración y Finanzas', 1, 'Portería Principal Peatonal (Torniquete Norte)', '2026-10-22', '07:55', '16:40', 'PUNTUAL', 'FINALIZADO', 525, '8h 45m', 'TARJETA_RFID', 'vigilante@sentinelpro.com', 'Sgto. Roberto Vargas', 'Jornada completada con salida registrada en portería.'),
(5, 'ACC-1000', 5, 'EMP-005', '10928374', 'Héctor Julio Ramírez', 'Operaciones y Planta', 3, 'Planta de Producción y Almacén de Materiales', '2026-10-21', '07:56', '17:08', 'PUNTUAL', 'FINALIZADO', 552, '9h 12m', 'TARJETA_RFID', 'vigilante@sentinelpro.com', 'Sgto. Roberto Vargas', 'Jornada completa sin novedades.');

-- 6. Inserción de Visitantes
INSERT INTO `visitantes` (`id`, `gafete`, `documento`, `nombre_completo`, `empresa_origen`, `anfitrion_visitado`, `zona_autorizada`, `motivo`, `fecha`, `hora_entrada`, `hora_salida`, `estado`, `registrado_por`) VALUES
(1, 'VIS-01', '1020394857', 'Ing. Fernando Lozano', 'Siemens Automatización Industrial', 'Javier Morales Castro (Jefe de Planta)', 'Planta de Producción y Almacén de Materiales', 'Calibración de tableros eléctricos en Nave B', '2026-10-22', '09:15', NULL, 'EN_PLANTA', 'Sgto. Roberto Vargas'),
(2, 'VIS-02', '79445112', 'Marta Lucía Benítez', 'DHL Express Corporativo', 'Camila Torres Villalba (Administración)', 'Portería Principal Peatonal (Torniquete Norte)', 'Entrega de documentación legal certificada', '2026-10-22', '10:05', '10:32', 'SALIDA_REGISTRADA', 'Sgto. Roberto Vargas');

-- 7. Inserción de Incidencias de Acceso Denegado
INSERT INTO `incidencias_acceso` (`id`, `fecha_hora`, `trabajador_nombre`, `documento`, `zona_nombre`, `tipo_alerta`, `severidad`, `detalle`, `estado_resolucion`, `registrado_por`) VALUES
(1, '2026-10-22 08:25', 'Esteban Salazar (EMP-008)', '66778899', 'Portería Principal Peatonal (Torniquete Norte)', 'CREDENCIAL_SUSPENDIDA', 'ALTA', 'Intento de ingreso rechazado en portería: el trabajador se encuentra con estado SUSPENDIDO por RR.HH.', 'PENDIENTE', 'Sgto. Roberto Vargas'),
(2, '2026-10-22 09:40', 'Andrés Felipe Pineda (EMP-003)', '80192834', 'Bóveda de Servidores y DataCenter TI', 'ZONA_NO_AUTORIZADA', 'MEDIA', 'Intento de apertura en Puerta DataCenter TI denegado: la credencial EMP-003 solo tiene autorizadas las Zonas [1, 2, 3].', 'RESUELTA', 'Sistema Biométrico / Garita');

-- 8. Inserción de Permisos del Catálogo
INSERT INTO `permisos_catalogo` (`codigo`, `modulo`, `nombre`, `descripcion`) VALUES
('dashboard:ver', 'Dashboard & Aforo', 'Ver Dashboard y Aforo en Planta', 'Permite visualizar KPIs en vivo, personal actualmente dentro de la empresa, entradas/salidas del día y alertas.'),
('porteria:ver', 'Consola de Portería', 'Abrir Consola de Portería y Garita', 'Permite visualizar el monitor de acceso peatonal/vehicular y el personal actualmente en planta.'),
('porteria:registrar', 'Consola de Portería', 'Registrar Entrada y Salida de Trabajadores', 'Permite al Vigilante u operador fichar el ingreso (Check-In) y salida (Check-Out) de trabajadores por DNI/Credencial.'),
('asistencia:ver', 'Historial Asistencia', 'Consultar Historial de Entradas y Salidas', 'Permite consultar registros históricos de asistencia, puntualidad, tardanzas y horas trabajadas.'),
('asistencia:exportar', 'Historial Asistencia', 'Exportar Reportes de Asistencia (CSV)', 'Permite descargar reportes consolidados de marcaciones, horas laboradas y tardanzas para nómina.'),
('trabajadores:ver', 'Trabajadores (RR.HH.)', 'Consultar Directorio de Trabajadores', 'Permite ver la ficha de los trabajadores, su documento, cargo, departamento, turno y estado de autorización.'),
('trabajadores:crear', 'Trabajadores (RR.HH.)', 'Registrar Nuevos Trabajadores', 'Permite dar de alta nuevos trabajadores en el padrón y emitir su código de credencial (EMP-XXX).'),
('trabajadores:editar', 'Trabajadores (RR.HH.)', 'Editar Trabajadores, Turnos y Zonas', 'Permite modificar el turno asignado, zonas autorizadas o suspender/activar el acceso de un trabajador.'),
('visitantes:ver', 'Control Visitantes', 'Consultar Visitantes y Contratistas', 'Permite visualizar los visitantes externos activos en la empresa y el historial de visitas.'),
('visitantes:registrar', 'Control Visitantes', 'Registrar Entrada/Salida de Visitantes', 'Permite registrar el ingreso de un visitante en garita, asignarle gafete temporal y marcar su salida.'),
('zonas:ver', 'Zonas y Turnos', 'Ver Puertas de Acceso y Turnos', 'Permite consultar los puntos de control (puertas/torniquetes), niveles de seguridad y horarios de turnos.'),
('zonas:editar', 'Zonas y Turnos', 'Administrar Puertas y Turnos Laborales', 'Permite crear o modificar puntos de acceso físico, niveles de restricción y horarios de turnos.'),
('incidencias:ver', 'Alertas de Acceso', 'Ver Alertas de Accesos Denegados', 'Permite consultar intentos de ingreso rechazados (trabajador suspendido, zona no autorizada, doble entrada).'),
('incidencias:resolver', 'Alertas de Acceso', 'Justificar o Resolver Incidencias', 'Permite autorizar excepciones o registrar observaciones sobre incidentes de acceso en planta.'),
('seguridad:ver', 'Seguridad IAM', 'Ver Usuarios, Sesiones y Bitácora IAM', 'Permite auditar usuarios del sistema, matriz de permisos efectivos, sesiones activas y logs de seguridad.'),
('seguridad:administrar', 'Seguridad IAM', 'Administrar Usuarios y Permisos Individuales', 'Permite crear usuarios, asignar roles, conceder/revocar permisos individuales (ALLOW/DENY) y cerrar sesiones.'),
('configuracion:ver', 'Configuración Empresa', 'Ver Configuración de la Empresa', 'Permite consultar los datos institucionales, políticas de tolerancia y reglas de control de acceso.'),
('configuracion:editar', 'Configuración Empresa', 'Modificar Configuración Corporativa', 'Permite actualizar los parámetros generales de la empresa, sedes y reglas operativas.');

-- 9. Inserción de Roles Base
INSERT INTO `roles_sistema` (`codigo`, `nombre`, `descripcion`, `color_badge`, `permisos_base`) VALUES
('SUPER_ADMIN', 'Super Administrador General', 'Control absoluto de la plataforma: Planta, Portería, RR.HH., Zonas, Configuración y Administración de Seguridad IAM.', '#4f46e5', '["dashboard:ver","porteria:ver","porteria:registrar","asistencia:ver","asistencia:exportar","trabajadores:ver","trabajadores:crear","trabajadores:editar","visitantes:ver","visitantes:registrar","zonas:ver","zonas:editar","incidencias:ver","incidencias:resolver","seguridad:ver","seguridad:administrar","configuracion:ver","configuracion:editar"]'),
('VIGILANTE_PORTERIA', 'Vigilante / Oficial de Portería', 'Encargado de garita y puntos de acceso: registra entradas y salidas de trabajadores, controla visitantes y verifica credenciales.', '#0284c7', '["porteria:ver","porteria:registrar","visitantes:ver","visitantes:registrar","trabajadores:ver","zonas:ver","incidencias:ver"]'),
('SUPERVISOR_RRHH', 'Supervisor de RR.HH. y Asistencia', 'Gestiona el padrón de trabajadores, asignación de turnos, zonas autorizadas, justificación de tardanzas y reportes de asistencia.', '#059669', '["dashboard:ver","porteria:ver","asistencia:ver","asistencia:exportar","trabajadores:ver","trabajadores:crear","trabajadores:editar","visitantes:ver","zonas:ver","zonas:editar","incidencias:ver","incidencias:resolver","configuracion:ver"]'),
('AUDITOR_SEGURIDAD', 'Auditor de Seguridad e Inspector', 'Acceso de supervisión e inspección en modo solo lectura sobre planta, historial de accesos, incidencias y bitácora IAM.', '#d97706', '["dashboard:ver","porteria:ver","asistencia:ver","asistencia:exportar","trabajadores:ver","visitantes:ver","zonas:ver","incidencias:ver","seguridad:ver","configuracion:ver"]');

-- 10. Inserción de Usuarios del Sistema (Contraseñas Cifradas con scrypt)
-- Credenciales predeterminadas para pruebas:
-- admin@sentinelpro.com     / admin123  (Super Administrador)
-- vigilante@sentinelpro.com / vigi123   (Vigilante de Garita)
-- rrhh@sentinelpro.com      / rrhh123   (Supervisor de RR.HH.)
-- auditor@sentinelpro.com   / audit123  (Auditor de Seguridad)
INSERT INTO `usuarios` (`id`, `nombre_completo`, `email`, `password_hash`, `rol`, `cargo`, `max_sesiones_simultaneas`, `politica_concurrencia`, `activo`, `creado_en`) VALUES
(1, 'Ing. Carlos Mendoza (Director de Seguridad y TI)', 'admin@sentinelpro.com', 'scrypt$2ec3ebee0827d1c574fc4f8d4d17ec30$62c06431745c449a8ec999d7ac3565d989ee32899ef75dbf3fe8e29937373e142db3efbf92a76cd19470e767853f6fedd57daf4c7f684af9c72c55b3ce3d4d9b', 'SUPER_ADMIN', 'Director General de Seguridad e IAM', 2, 'RECHAZAR_NUEVA', 1, '2026-10-22 15:00:00'),
(2, 'Sgto. Roberto Vargas (Vigilante Portería Principal)', 'vigilante@sentinelpro.com', 'scrypt$9ff586f30da294cbf6f7b490f388b84e$804f1c30896d47142cf72d8d0b42459e1c0ba9916f2466bfe0bcc4d2a31e870d541d59ac86af3b655155f796d2cbd5d3055ba3497e9f1f7f309009973a8221a7', 'VIGILANTE_PORTERIA', 'Oficial de Seguridad y Control de Garita', 1, 'RECHAZAR_NUEVA', 1, '2026-10-22 15:00:00'),
(3, 'Lic. Laura Gómez (Jefa de RR.HH. y Control de Personal)', 'rrhh@sentinelpro.com', 'scrypt$d2d57e3db4866027dff047b9871dc3a4$e7fc3d487f372c77378cd3002c9f047238f672198d27cb596ae1cb9cb41bf4de5a80eea97216b3fc0186430658a9352d0ef17c24fa31f5f8af0ffc66367f2e1d', 'SUPERVISOR_RRHH', 'Supervisora de Recursos Humanos y Turnos', 1, 'RECHAZAR_NUEVA', 1, '2026-10-22 15:00:00'),
(4, 'Ing. Sofía Herrera (Auditora Interna de Seguridad)', 'auditor@sentinelpro.com', 'scrypt$f1e0fc9ee264e81e831d8b0da1d27521$5148fd47d3ec7300328c3934335e776b099a1448565344798aba692557de531170f2e8464bf565c2dd10cddc97a6a5339133a43e18a8b7e19a5bda10f7e48b55', 'AUDITOR_SEGURIDAD', 'Inspectora de Cumplimiento y Auditoría IAM', 1, 'RECHAZAR_NUEVA', 1, '2026-10-22 15:00:00');

-- 11. Inserción de Permisos Individuales (ALLOW / DENY Overrides)
-- El Vigilante titular tiene un permiso individual ALLOW para consultar y exportar asistencia del día
INSERT INTO `usuario_permisos_individuales` (`usuario_id`, `permiso_codigo`, `modo_override`, `actualizado_en`) VALUES
(2, 'asistencia:ver', 'ALLOW', '2026-10-22 15:00:00'),
(2, 'asistencia:exportar', 'ALLOW', '2026-10-22 15:00:00');

-- 12. Inserción de Auditoría Inicial
INSERT INTO `audit_logs` (`id`, `fecha_hora`, `usuario_id`, `usuario_email`, `rol`, `evento`, `modulo`, `permiso_evaluado`, `resultado`, `ip`, `detalle`) VALUES
(1, '2026-10-22 15:00:00', 1, 'admin@sentinelpro.com', 'SUPER_ADMIN', 'INICIALIZACION_SISTEMA_IAM', 'seguridad', 'seguridad:administrar', 'EXITO', '127.0.0.1', 'Motor SentinelPro IAM iniciado con 4 roles (incluyendo VIGILANTE_PORTERIA), 18 permisos granulares y control de entrada/salida de trabajadores.'),
(2, '2026-10-22 15:00:00', 1, 'admin@sentinelpro.com', 'SUPER_ADMIN', 'CAMBIO_PERMISOS_USUARIO', 'seguridad', 'seguridad:administrar', 'EXITO', '127.0.0.1', 'Se otorgó permiso individual ALLOW [asistencia:ver] a vigilante@sentinelpro.com (Sgto. Roberto Vargas).');

-- Reactivar revisión de claves foráneas
SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================================
-- FIN DEL SCRIPT SQL — BASE DE DATOS `sentinelpro_iam` LISTA Y OPERATIVA
-- ============================================================================
