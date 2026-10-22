/**
 * Semillas de Datos Empresariales para SentinelPro IAM
 * Sistema de Control de Acceso Físico de Trabajadores (Entradas/Salidas en Portería),
 * Visitantes, Zonas y Control de Acceso Digital Basado en Roles y Permisos Individuales.
 */

const {
    CATALOGO_PERMISOS,
    ROLES_SISTEMA,
    hashPassword
} = require('./security');

function getTodayStr(offsetDays = 0) {
    const d = new Date();
    d.setDate(d.getDate() + offsetDays);
    const yyyy = d.getFullYear();
    const mm = String(d.getMonth() + 1).padStart(2, '0');
    const dd = String(d.getDate()).padStart(2, '0');
    return `${yyyy}-${mm}-${dd}`;
}

function buildSecuritySeeds() {
    const nowIso = new Date().toISOString();
    return {
        permisos_catalogo: CATALOGO_PERMISOS,
        roles_sistema: ROLES_SISTEMA,
        usuarios: [
            {
                id: 1,
                nombre_completo: 'Ing. Carlos Mendoza (Director de Seguridad y TI)',
                email: 'admin@sentinelpro.com',
                password_hash: hashPassword('admin123'),
                rol: 'SUPER_ADMIN',
                cargo: 'Director General de Seguridad e IAM',
                max_sesiones_simultaneas: 2,
                politica_concurrencia: 'RECHAZAR_NUEVA',
                activo: true,
                permisos_individuales: {},
                creado_en: nowIso
            },
            {
                id: 2,
                nombre_completo: 'Sgto. Roberto Vargas (Vigilante Portería Principal)',
                email: 'vigilante@sentinelpro.com',
                password_hash: hashPassword('vigi123'),
                rol: 'VIGILANTE_PORTERIA',
                cargo: 'Oficial de Seguridad y Control de Garita',
                max_sesiones_simultaneas: 1,
                politica_concurrencia: 'RECHAZAR_NUEVA',
                activo: true,
                // Ejemplo real de Permiso Individual ALLOW otorgado al Vigilante titular:
                // Además de su rol de garita, puede consultar el historial de asistencia del día
                permisos_individuales: {
                    'asistencia:ver': 'ALLOW'
                },
                creado_en: nowIso
            },
            {
                id: 3,
                nombre_completo: 'Lic. Laura Gómez (Jefa de RR.HH. y Control de Personal)',
                email: 'rrhh@sentinelpro.com',
                password_hash: hashPassword('rrhh123'),
                rol: 'SUPERVISOR_RRHH',
                cargo: 'Supervisora de Recursos Humanos y Turnos',
                max_sesiones_simultaneas: 1,
                politica_concurrencia: 'RECHAZAR_NUEVA',
                activo: true,
                permisos_individuales: {},
                creado_en: nowIso
            },
            {
                id: 4,
                nombre_completo: 'Ing. Sofía Herrera (Auditora Interna de Seguridad)',
                email: 'auditor@sentinelpro.com',
                password_hash: hashPassword('audit123'),
                rol: 'AUDITOR_SEGURIDAD',
                cargo: 'Inspectora de Cumplimiento y Auditoría IAM',
                max_sesiones_simultaneas: 1,
                politica_concurrencia: 'RECHAZAR_NUEVA',
                activo: true,
                permisos_individuales: {},
                creado_en: nowIso
            }
        ],
        sesiones_activas: [],
        audit_logs: [
            {
                id: 1,
                fecha_hora: nowIso,
                usuario_id: 1,
                usuario_email: 'admin@sentinelpro.com',
                rol: 'SUPER_ADMIN',
                evento: 'INICIALIZACION_SISTEMA_IAM',
                modulo: 'seguridad',
                permiso_evaluado: 'seguridad:administrar',
                resultado: 'EXITO',
                ip: '127.0.0.1',
                detalle: 'Motor SentinelPro IAM iniciado con 4 roles (incluyendo VIGILANTE_PORTERIA), 18 permisos granulares y control de entrada/salida de trabajadores.'
            },
            {
                id: 2,
                fecha_hora: nowIso,
                usuario_id: 1,
                usuario_email: 'admin@sentinelpro.com',
                rol: 'SUPER_ADMIN',
                evento: 'CAMBIO_PERMISOS_USUARIO',
                modulo: 'seguridad',
                permiso_evaluado: 'seguridad:administrar',
                resultado: 'EXITO',
                ip: '127.0.0.1',
                detalle: 'Se otorgó permiso individual ALLOW [asistencia:ver] a vigilante@sentinelpro.com (Sgto. Roberto Vargas).'
            }
        ]
    };
}

function buildEnterpriseAccessDb(presetType = 'industrial') {
    const today = getTodayStr(0);
    const yesterday = getTodayStr(-1);
    const sec = buildSecuritySeeds();

    const presetConfigs = {
        industrial: {
            nombre_empresa: 'Grupo Industrial & Logístico Titan S.A.',
            nit_ruc: '901.452.889-1',
            rubro_empresa: 'Planta Industrial, Almacén y Oficinas Corporativas',
            slogan_corporativo: 'Control de Acceso Físico en Portería, Asistencia de Trabajadores en Tiempo Real y Seguridad IAM por Roles',
            direccion: 'Parque Industrial Norte Km 14 — Complejo Empresarial B-12',
            telefono_central: '+57 300 912 4500',
            email_seguridad: 'seguridad@grupotitan.com',
            color_primario: '#1e40af',
            color_secundario: '#0f172a',
            tolerancia_tardanza_min: 10,
            aforo_maximo_planta: 150
        },
        corporativo: {
            nombre_empresa: 'Torre Financiera & Tecnológica Nexus',
            nit_ruc: '900.812.334-9',
            rubro_empresa: 'Centro Corporativo de Tecnología y DataCenter',
            slogan_corporativo: 'Gestión Inteligente de Torniquetes, Credenciales RFID, Visitantes y Permisos Individuales',
            direccion: 'Av. Empresarial 850, Torre A — Distrito Financiero',
            telefono_central: '+57 310 445 8890',
            email_seguridad: 'controlacceso@nexustower.com',
            color_primario: '#4f46e5',
            color_secundario: '#1e1b4b',
            tolerancia_tardanza_min: 10,
            aforo_maximo_planta: 250
        },
        clinica: {
            nombre_empresa: 'Complejo Hospitalario San Rafael',
            nit_ruc: '890.112.900-4',
            rubro_empresa: 'Infraestructura Hospitalaria, Laboratorios y Áreas Críticas',
            slogan_corporativo: 'Control de Ingreso de Personal Médico, Guardias, Farmacia y Áreas Restringidas',
            direccion: 'Av. de la Salud 420 — Campus Médico Central',
            telefono_central: '+57 315 778 2100',
            email_seguridad: 'porteria@hospitalrafael.org',
            color_primario: '#0284c7',
            color_secundario: '#0c4a6e',
            tolerancia_tardanza_min: 5,
            aforo_maximo_planta: 300
        }
    };

    const cfg = presetConfigs[presetType] || presetConfigs.industrial;

    return {
        preset_activo: presetType,
        ...sec,
        configuracion_empresa: {
            id: 1,
            ...cfg
        },
        turnos_laborales: [
            {
                id: 1,
                codigo: 'TURNO-MANANA',
                nombre: 'Turno Mañana (Planta y Oficinas)',
                hora_entrada: '08:00',
                hora_salida: '17:00',
                tolerancia_minutos: 10,
                activo: true
            },
            {
                id: 2,
                codigo: 'TURNO-TARDE',
                nombre: 'Turno Tarde (Operaciones y Logística)',
                hora_entrada: '14:00',
                hora_salida: '22:00',
                tolerancia_minutos: 10,
                activo: true
            },
            {
                id: 3,
                codigo: 'TURNO-NOCHE',
                nombre: 'Turno Nocturno (Seguridad y Mantenimiento)',
                hora_entrada: '22:00',
                hora_salida: '06:00',
                tolerancia_minutos: 15,
                activo: true
            }
        ],
        zonas_acceso: [
            {
                id: 1,
                codigo: 'PUERTA-01',
                nombre: 'Portería Principal Peatonal (Torniquete Norte)',
                tipo: 'PEATONAL',
                nivel_seguridad: 'NIVEL 1 — GENERAL',
                ubicacion: 'Entrada Principal Calle 100',
                estado: 'OPERATIVA',
                requiere_autorizacion_especial: false
            },
            {
                id: 2,
                codigo: 'PUERTA-02',
                nombre: 'Garita de Acceso Vehicular y Muelle de Carga',
                tipo: 'VEHICULAR',
                nivel_seguridad: 'NIVEL 2 — OPERATIVO',
                ubicacion: 'Acceso Sur — Patio de Maniobras',
                estado: 'OPERATIVA',
                requiere_autorizacion_especial: false
            },
            {
                id: 3,
                codigo: 'PUERTA-03',
                nombre: 'Planta de Producción y Almacén de Materiales',
                tipo: 'PLANTA_INDUSTRIAL',
                nivel_seguridad: 'NIVEL 3 — RESTRINGIDO',
                ubicacion: 'Nave Central — Sector B',
                estado: 'OPERATIVA',
                requiere_autorizacion_especial: true
            },
            {
                id: 4,
                codigo: 'PUERTA-04',
                nombre: 'Bóveda de Servidores y DataCenter TI',
                tipo: 'ALTA_SEGURIDAD',
                nivel_seguridad: 'NIVEL 4 — CRÍTICO BIOMÉTRICO',
                ubicacion: 'Piso 3 — Núcleo Blindado TI',
                estado: 'OPERATIVA',
                requiere_autorizacion_especial: true
            }
        ],
        trabajadores: [
            {
                id: 1,
                codigo_credencial: 'EMP-001',
                documento: '72849102',
                nombre_completo: 'Javier Morales Castro',
                cargo: 'Jefe de Planta y Mantenimiento',
                departamento: 'Operaciones y Planta',
                telefono: '3004128890',
                email: 'jmorales@empresa.com',
                turno_id: 1,
                zonas_autorizadas: [1, 2, 3],
                placa_vehiculo: 'KLM-482',
                estado: 'ACTIVO', // ACTIVO | SUSPENDIDO | VACACIONES
                ubicacion_actual: 'DENTRO_PLANTA', // DENTRO_PLANTA | FUERA_PLANTA
                ultima_puerta_id: 1,
                ultima_entrada: `${today} 07:52`
            },
            {
                id: 2,
                codigo_credencial: 'EMP-002',
                documento: '45918273',
                nombre_completo: 'Daniela Ríos Salgado',
                cargo: 'Ingeniera de Infraestructura y Redes',
                departamento: 'Tecnología (TI)',
                telefono: '3115902341',
                email: 'drios@empresa.com',
                turno_id: 1,
                zonas_autorizadas: [1, 2, 3, 4],
                placa_vehiculo: 'BGT-901',
                estado: 'ACTIVO',
                ubicacion_actual: 'DENTRO_PLANTA',
                ultima_puerta_id: 4,
                ultima_entrada: `${today} 07:58`
            },
            {
                id: 3,
                codigo_credencial: 'EMP-003',
                documento: '80192834',
                nombre_completo: 'Andrés Felipe Pineda',
                cargo: 'Operador de Montacargas y Despacho',
                departamento: 'Logística y Almacén',
                telefono: '3158891203',
                email: 'apineda@empresa.com',
                turno_id: 1,
                zonas_autorizadas: [1, 2, 3],
                placa_vehiculo: 'MTR-119',
                estado: 'ACTIVO',
                ubicacion_actual: 'DENTRO_PLANTA',
                ultima_puerta_id: 2,
                ultima_entrada: `${today} 08:19`
            },
            {
                id: 4,
                codigo_credencial: 'EMP-004',
                documento: '52839104',
                nombre_completo: 'Camila Torres Villalba',
                cargo: 'Analista Contable y Tesorería',
                departamento: 'Administración y Finanzas',
                telefono: '3017745612',
                email: 'ctorres@empresa.com',
                turno_id: 1,
                zonas_autorizadas: [1],
                placa_vehiculo: '',
                estado: 'ACTIVO',
                ubicacion_actual: 'FUERA_PLANTA',
                ultima_puerta_id: 1,
                ultima_entrada: `${today} 07:55`
            },
            {
                id: 5,
                codigo_credencial: 'EMP-005',
                documento: '10928374',
                nombre_completo: 'Héctor Julio Ramírez',
                cargo: 'Técnico Electromecánico Senior',
                departamento: 'Operaciones y Planta',
                telefono: '3209918273',
                email: 'hramirez@empresa.com',
                turno_id: 1,
                zonas_autorizadas: [1, 2, 3],
                placa_vehiculo: 'ZXC-330',
                estado: 'ACTIVO',
                ubicacion_actual: 'FUERA_PLANTA',
                ultima_puerta_id: 1,
                ultima_entrada: `${yesterday} 07:56`
            },
            {
                id: 6,
                codigo_credencial: 'EMP-006',
                documento: '39182736',
                nombre_completo: 'Paola Andrea Vega',
                cargo: 'Coordinadora de Calidad e ISO',
                departamento: 'Calidad y Seguridad Industrial',
                telefono: '3146629182',
                email: 'pvega@empresa.com',
                turno_id: 1,
                zonas_autorizadas: [1, 3],
                placa_vehiculo: '',
                estado: 'ACTIVO',
                ubicacion_actual: 'FUERA_PLANTA',
                ultima_puerta_id: 1,
                ultima_entrada: `${yesterday} 08:02`
            },
            {
                id: 7,
                codigo_credencial: 'EMP-007',
                documento: '91827364',
                nombre_completo: 'Miguel Ángel Duarte',
                cargo: 'Supervisor de Despachos Nocturnos',
                departamento: 'Logística y Almacén',
                telefono: '3183349012',
                email: 'mduarte@empresa.com',
                turno_id: 2,
                zonas_autorizadas: [1, 2, 3],
                placa_vehiculo: 'QWE-712',
                estado: 'ACTIVO',
                ubicacion_actual: 'FUERA_PLANTA',
                ultima_puerta_id: 2,
                ultima_entrada: `${yesterday} 13:55`
            },
            {
                id: 8,
                codigo_credencial: 'EMP-008',
                documento: '66778899',
                nombre_completo: 'Esteban Salazar (Credencial Suspendida)',
                cargo: 'Auxiliar Externo de Bodega',
                departamento: 'Logística y Almacén',
                telefono: '3001192837',
                email: 'esalazar@empresa.com',
                turno_id: 1,
                zonas_autorizadas: [1],
                placa_vehiculo: '',
                estado: 'SUSPENDIDO',
                ubicacion_actual: 'FUERA_PLANTA',
                ultima_puerta_id: 1,
                ultima_entrada: `${yesterday} 08:00`
            }
        ],
        registros_acceso: [
            {
                id: 1,
                codigo_movimiento: 'ACC-1001',
                trabajador_id: 1,
                codigo_credencial: 'EMP-001',
                documento: '72849102',
                trabajador_nombre: 'Javier Morales Castro',
                departamento: 'Operaciones y Planta',
                zona_id: 1,
                zona_nombre: 'Portería Principal Peatonal (Torniquete Norte)',
                fecha: today,
                hora_entrada: '07:52',
                hora_salida: null,
                estado_asistencia: 'PUNTUAL', // PUNTUAL | TARDANZA
                estado_ciclo: 'EN_PLANTA', // EN_PLANTA | FINALIZADO
                minutos_trabajados: null,
                horas_formateadas: 'En curso (En planta)',
                metodo_identificacion: 'TARJETA_RFID',
                registrado_por_email: 'vigilante@sentinelpro.com',
                registrado_por_nombre: 'Sgto. Roberto Vargas',
                observacion: 'Ingreso normal con EPP verificado en portería.'
            },
            {
                id: 2,
                codigo_movimiento: 'ACC-1002',
                trabajador_id: 2,
                codigo_credencial: 'EMP-002',
                documento: '45918273',
                trabajador_nombre: 'Daniela Ríos Salgado',
                departamento: 'Tecnología (TI)',
                zona_id: 4,
                zona_nombre: 'Bóveda de Servidores y DataCenter TI',
                fecha: today,
                hora_entrada: '07:58',
                hora_salida: null,
                estado_asistencia: 'PUNTUAL',
                estado_ciclo: 'EN_PLANTA',
                minutos_trabajados: null,
                horas_formateadas: 'En curso (En planta)',
                metodo_identificacion: 'BIOMETRICO_QR',
                registrado_por_email: 'vigilante@sentinelpro.com',
                registrado_por_nombre: 'Sgto. Roberto Vargas',
                observacion: 'Acceso autorizado a DataCenter para mantenimiento preventivo.'
            },
            {
                id: 3,
                codigo_movimiento: 'ACC-1003',
                trabajador_id: 3,
                codigo_credencial: 'EMP-003',
                documento: '80192834',
                trabajador_nombre: 'Andrés Felipe Pineda',
                departamento: 'Logística y Almacén',
                zona_id: 2,
                zona_nombre: 'Garita de Acceso Vehicular y Muelle de Carga',
                fecha: today,
                hora_entrada: '08:19',
                hora_salida: null,
                estado_asistencia: 'TARDANZA',
                estado_ciclo: 'EN_PLANTA',
                minutos_trabajados: null,
                horas_formateadas: 'En curso (En planta)',
                metodo_identificacion: 'DOCUMENTO_DNI',
                registrado_por_email: 'vigilante@sentinelpro.com',
                registrado_por_nombre: 'Sgto. Roberto Vargas',
                observacion: 'Ingreso con 19 min de retraso respecto al Turno Mañana (08:00).'
            },
            {
                id: 4,
                codigo_movimiento: 'ACC-1004',
                trabajador_id: 4,
                codigo_credencial: 'EMP-004',
                documento: '52839104',
                trabajador_nombre: 'Camila Torres Villalba',
                departamento: 'Administración y Finanzas',
                zona_id: 1,
                zona_nombre: 'Portería Principal Peatonal (Torniquete Norte)',
                fecha: today,
                hora_entrada: '07:55',
                hora_salida: '16:40',
                estado_asistencia: 'PUNTUAL',
                estado_ciclo: 'FINALIZADO',
                minutos_trabajados: 525,
                horas_formateadas: '8h 45m',
                metodo_identificacion: 'TARJETA_RFID',
                registrado_por_email: 'vigilante@sentinelpro.com',
                registrado_por_nombre: 'Sgto. Roberto Vargas',
                observacion: 'Jornada completada con salida registrada en portería.'
            },
            {
                id: 5,
                codigo_movimiento: 'ACC-1000',
                trabajador_id: 5,
                codigo_credencial: 'EMP-005',
                documento: '10928374',
                trabajador_nombre: 'Héctor Julio Ramírez',
                departamento: 'Operaciones y Planta',
                zona_id: 3,
                zona_nombre: 'Planta de Producción y Almacén de Materiales',
                fecha: yesterday,
                hora_entrada: '07:56',
                hora_salida: '17:08',
                estado_asistencia: 'PUNTUAL',
                estado_ciclo: 'FINALIZADO',
                minutos_trabajados: 552,
                horas_formateadas: '9h 12m',
                metodo_identificacion: 'TARJETA_RFID',
                registrado_por_email: 'vigilante@sentinelpro.com',
                registrado_por_nombre: 'Sgto. Roberto Vargas',
                observacion: 'Jornada completa sin novedades.'
            }
        ],
        visitantes: [
            {
                id: 1,
                gafete: 'VIS-01',
                documento: '1020394857',
                nombre_completo: 'Ing. Fernando Lozano',
                empresa_origen: 'Siemens Automatización Industrial',
                anfitrion_visitado: 'Javier Morales Castro (Jefe de Planta)',
                zona_autorizada: 'Planta de Producción y Almacén de Materiales',
                motivo: 'Calibración de tableros eléctricos en Nave B',
                fecha: today,
                hora_entrada: '09:15',
                hora_salida: null,
                estado: 'EN_PLANTA', // EN_PLANTA | SALIDA_REGISTRADA
                registrado_por: 'Sgto. Roberto Vargas'
            },
            {
                id: 2,
                gafete: 'VIS-02',
                documento: '79445112',
                nombre_completo: 'Marta Lucía Benítez',
                empresa_origen: 'DHL Express Corporativo',
                anfitrion_visitado: 'Camila Torres Villalba (Administración)',
                zona_autorizada: 'Portería Principal Peatonal (Torniquete Norte)',
                motivo: 'Entrega de documentación legal certificada',
                fecha: today,
                hora_entrada: '10:05',
                hora_salida: '10:32',
                estado: 'SALIDA_REGISTRADA',
                registrado_por: 'Sgto. Roberto Vargas'
            }
        ],
        incidencias_acceso: [
            {
                id: 1,
                fecha_hora: `${today} 08:25`,
                trabajador_nombre: 'Esteban Salazar (EMP-008)',
                documento: '66778899',
                zona_nombre: 'Portería Principal Peatonal (Torniquete Norte)',
                tipo_alerta: 'CREDENCIAL_SUSPENDIDA',
                severidad: 'ALTA',
                detalle: 'Intento de ingreso rechazado en portería: el trabajador se encuentra con estado SUSPENDIDO por RR.HH.',
                estado_resolucion: 'PENDIENTE',
                registrado_por: 'Sgto. Roberto Vargas'
            },
            {
                id: 2,
                fecha_hora: `${today} 09:40`,
                trabajador_nombre: 'Andrés Felipe Pineda (EMP-003)',
                documento: '80192834',
                zona_nombre: 'Bóveda de Servidores y DataCenter TI',
                tipo_alerta: 'ZONA_NO_AUTORIZADA',
                severidad: 'MEDIA',
                detalle: 'Intento de apertura en Puerta DataCenter TI denegado: la credencial EMP-003 solo tiene autorizadas las Zonas [1, 2, 3].',
                estado_resolucion: 'RESUELTA',
                registrado_por: 'Sistema Biométrico / Garita'
            }
        ]
    };
}

const PRESETS = {
    industrial: () => buildEnterpriseAccessDb('industrial'),
    corporativo: () => buildEnterpriseAccessDb('corporativo'),
    clinica: () => buildEnterpriseAccessDb('clinica')
};

module.exports = { PRESETS, getTodayStr, buildEnterpriseAccessDb };
