# -*- coding: utf-8 -*-
"""
Generador de Diagramas Profesionales en Alta Resolución (.PNG) para:
SentinelPro Access & IAM — Sistema Empresarial de Control de Acceso Físico en Portería,
Registro de Entrada/Salida de Trabajadores, Rol Vigilante y Autorización Granular Digital (RBAC + Overrides).
"""
import os
import math
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = os.path.join(os.path.dirname(__file__), '..', 'docs', 'diagramas_png')
os.makedirs(OUT_DIR, exist_ok=True)

def get_font(size=18, bold=False):
    candidates = [
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
        r"C:\Windows\Fonts\calibrib.ttf" if bold else r"C:\Windows\Fonts\calibri.ttf"
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                pass
    return ImageFont.load_default()

def create_canvas(title, subtitle, width=2000, height=1250):
    img = Image.new('RGB', (width, height), (248, 250, 252))
    draw = ImageDraw.Draw(img)

    # Banner superior institucional
    draw.rectangle([0, 0, width, 110], fill=(15, 23, 42))
    draw.rectangle([0, 106, width, 112], fill=(79, 70, 229))

    f_title = get_font(30, bold=True)
    f_sub = get_font(18, bold=False)
    draw.text((40, 22), title, fill=(255, 255, 255), font=f_title)
    draw.text((40, 66), subtitle, fill=(148, 163, 184), font=f_sub)

    # Pie de diagrama
    draw.rectangle([0, height - 42, width, height], fill=(226, 232, 240))
    f_foot = get_font(15, bold=False)
    draw.text(
        (40, height - 32),
        "SentinelPro Access & IAM — Control de Acceso de Trabajadores, Portería y Seguridad Granular (RBAC + ALLOW/DENY)",
        fill=(71, 85, 105),
        font=f_foot
    )
    return img, draw

def draw_box(draw, box, title, lines=None, header_bg=(30, 58, 95), body_bg=(255, 255, 255), border=(79, 70, 229), radius=12):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle([x1 + 4, y1 + 4, x2 + 4, y2 + 4], radius=radius, fill=(203, 213, 225))
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=body_bg, outline=border, width=3)

    if lines:
        h_bar = 44
        draw.rounded_rectangle([x1, y1, x2, y1 + h_bar], radius=radius, fill=header_bg)
        draw.rectangle([x1, y1 + h_bar - 10, x2, y1 + h_bar], fill=header_bg)
        f_h = get_font(18, bold=True)
        draw.text((x1 + 16, y1 + 10), title, fill=(255, 255, 255), font=f_h)

        f_b = get_font(15, bold=False)
        curr_y = y1 + h_bar + 12
        for line in lines:
            draw.text((x1 + 16, curr_y), line, fill=(30, 41, 59), font=f_b)
            curr_y += 24
    else:
        f_h = get_font(18, bold=True)
        draw.text((x1 + 18, y1 + (y2 - y1) // 2 - 12), title, fill=(15, 23, 42), font=f_h)

def draw_arrow(draw, p1, p2, label="", color=(39, 110, 168), width=3):
    x1, y1 = p1
    x2, y2 = p2
    draw.line([x1, y1, x2, y2], fill=color, width=width)
    angle = math.atan2(y2 - y1, x2 - x1)
    arrow_len = 14
    a1 = angle + math.pi * 0.82
    a2 = angle - math.pi * 0.82
    p_a1 = (x2 + arrow_len * math.cos(a1), y2 + arrow_len * math.sin(a1))
    p_a2 = (x2 + arrow_len * math.cos(a2), y2 + arrow_len * math.sin(a2))
    draw.polygon([(x2, y2), p_a1, p_a2], fill=color)

    if label:
        mx, my = (x1 + x2) // 2, (y1 + y2) // 2
        f_l = get_font(13, bold=True)
        tw = len(label) * 7 + 14
        draw.rounded_rectangle([mx - tw // 2, my - 13, mx + tw // 2, my + 11], radius=6, fill=(255, 255, 255), outline=color, width=1)
        draw.text((mx - tw // 2 + 7, my - 10), label, fill=(15, 23, 42), font=f_l)

# =============================================================================
# DIAGRAMA 01: CASOS DE USO GENERAL Y ROLES OPERATIVOS
# =============================================================================
def diag_01_casos_de_uso():
    img, draw = create_canvas(
        "DIAGRAMA 01: CASOS DE USO GENERAL Y ACTORES DE CONTROL DE ACCESO",
        "Interacción entre Trabajadores, Vigilante de Garita, Supervisor RR.HH. y Administrador IAM"
    )

    # Actores (Izquierda)
    draw_box(draw, (60, 160, 420, 310), "👤 Trabajador de Planta", [
        "• Fichar Entrada en Terminal Kiosco",
        "• Fichar Salida al terminar jornada",
        "• Consultar estado de su credencial",
        "• Identificación con DNI o Tarjeta RFID"
    ], header_bg=(2, 132, 199))

    draw_box(draw, (60, 370, 420, 560), "👮 Vigilante / Oficial Garita", [
        "• Operar Consola de Portería en vivo",
        "• Registrar In/Out manual o escáner",
        "• Controlar ingreso de visitantes y gafetes",
        "• Verificar EPP y placas de vehículos",
        "• Recibir alertas de credenciales suspendidas"
    ], header_bg=(30, 64, 175))

    draw_box(draw, (60, 630, 420, 830), "👩‍💼 Supervisor RR.HH.", [
        "• Administrar padrón de trabajadores",
        "• Asignar turnos y tolerancia horaria",
        "• Autorizar puertas/zonas por empleado",
        "• Consultar y exportar asistencia (CSV)",
        "• Justificar tardanzas e incidencias"
    ], header_bg=(5, 150, 105))

    draw_box(draw, (60, 900, 420, 1100), "👨‍💼 Super Administrador IAM", [
        "• Gestión total de usuarios del sistema",
        "• Asignar Roles Base (RBAC)",
        "• Configurar excepciones ALLOW / DENY",
        "• Revocar sesiones activas remotas",
        "• Inspeccionar bitácora de auditoría"
    ], header_bg=(79, 70, 229))

    # Casos de Uso del Núcleo (Centro / Derecha)
    draw_box(draw, (560, 180, 1150, 330), "CU-01: Registro de Entrada / Salida (Check-In/Out)", [
        "• Valida si el trabajador está ACTIVO (rechaza suspendidos)",
        "• Valida si tiene permiso para la Puerta/Zona seleccionada",
        "• Detecta intentos de doble entrada o salida sin entrada",
        "• Calcula puntualidad vs tardanza según turno laboral",
        "• Computa horas y minutos exactos al registrar salida"
    ], header_bg=(15, 23, 42))

    draw_box(draw, (560, 390, 1150, 540), "CU-02: Control de Visitantes y Contratistas", [
        "• Registro de ingreso con documento y empresa de origen",
        "• Vinculación con anfitrión interno responsable",
        "• Asignación y liberación de Gafete temporal (VIS-XX)",
        "• Monitoreo de tiempo de permanencia en planta"
    ], header_bg=(15, 23, 42))

    draw_box(draw, (560, 600, 1150, 750), "CU-03: Zonificación y Puntos de Control Físico", [
        "• Configuración de torniquetes peatonales y vehiculares",
        "• Restricción de áreas críticas (Bóveda DataCenter, Almacén)",
        "• Detección automática de violaciones de zona"
    ], header_bg=(15, 23, 42))

    draw_box(draw, (560, 810, 1150, 960), "CU-04: Motor de Autorización Híbrida (IAM)", [
        "• Evaluación de 18 permisos del tipo modulo:operacion",
        "• Precedencia jerárquica: DENY > ALLOW > ROL_BASE",
        "• Verificación en Backend mediante authorizeAction()",
        "• Respuestas HTTP 401 (No autenticado) y 403 (Forbidden)"
    ], header_bg=(15, 23, 42))

    draw_box(draw, (560, 1020, 1150, 1170), "CU-05: Control de Concurrencia y Auditoría", [
        "• Límite configurable de sesiones simultáneas por usuario",
        "• Detección de colisiones de sesión con HTTP 409",
        "• Registro inmutable de cada evento en audit_logs"
    ], header_bg=(15, 23, 42))

    # Conexiones
    draw_arrow(draw, (420, 235), (560, 240), "Ficha en Garita", color=(2, 132, 199))
    draw_arrow(draw, (420, 450), (560, 270), "Opera Portería", color=(30, 64, 175))
    draw_arrow(draw, (420, 480), (560, 450), "Registra Visitas", color=(30, 64, 175))
    draw_arrow(draw, (420, 710), (560, 290), "Supervisa Asistencia", color=(5, 150, 105))
    draw_arrow(draw, (420, 750), (560, 660), "Define Zonas/Turnos", color=(5, 150, 105))
    draw_arrow(draw, (420, 980), (560, 880), "Administra IAM", color=(79, 70, 229))
    draw_arrow(draw, (420, 1020), (560, 1080), "Audita Sesiones", color=(79, 70, 229))

    # Panel lateral de Seguridad
    draw_box(draw, (1230, 280, 1920, 1050), "🛡️ PRINCIPIOS DE SEGURIDAD GARANTIZADOS", [
        "1. SEGURIDAD EN BACKEND OBLIGATORIA:",
        "   El servidor rechaza peticiones no autorizadas (401 / 403)",
        "   incluso si se manipula o burla la interfaz web.",
        "",
        "2. CONTROL DE SESIONES SIMULTÁNEAS:",
        "   Impide el uso compartido descontrolado de contraseñas",
        "   bloqueando sesiones excedentes (409 MAX_SESSIONS).",
        "",
        "3. PERMISOS INDIVIDUALES EN CALIENTE:",
        "   Permite a un Vigilante consultar reportes (ALLOW)",
        "   o revocar a un supervisor una función (DENY)",
        "   sin crear decenas de roles artificiales.",
        "",
        "4. AUDITORÍA INMUTABLE EN TIEMPO REAL:",
        "   Cada ingreso físico, login o cambio de permisos",
        "   queda estampado con usuario, IP y timestamp ISO."
    ], header_bg=(79, 70, 229), body_bg=(248, 250, 252))

    img.save(os.path.join(OUT_DIR, "01_Diagrama_Casos_De_Uso_General.png"), quality=95)

# =============================================================================
# DIAGRAMA 02: ARQUITECTURA EN CAPAS Y GATEKEEPER
# =============================================================================
def diag_02_arquitectura():
    img, draw = create_canvas(
        "DIAGRAMA 02: ARQUITECTURA DEL SISTEMA EN 4 CAPAS Y COMPUERTA DE SEGURIDAD",
        "Desacoplamiento entre Kiosco/Portería, Middleware de Seguridad, Lógica de Negocio y Persistencia"
    )

    # Capa 1: Presentación
    draw_box(draw, (80, 160, 1920, 320), "CAPA 1: PRESENTACIÓN (FRONTEND SPA & TERMINAL KIOSCO)", [
        "• Terminal Kiosco de Marcación Rápida (Entrada/Salida para trabajadores por DNI o Código RFID)",
        "• Consola de Garita del Vigilante (Operación rápida, búsqueda en tiempo real, validación visual de credenciales)",
        "• Panel Administrativo (Dashboard de Aforo, Historial de Asistencia, Padrón RR.HH., Visitantes, Zonas, Auditoría)",
        "• Módulo IAM Reactivo: Matriz dinámica de 18 permisos, Monitor de Sesiones Activas y Simulador 403 en Servidor"
    ], header_bg=(30, 41, 59))

    # Flecha 1 -> 2
    draw_arrow(draw, (1000, 320), (1000, 380), "Peticiones HTTP/REST (JSON + Bearer Token HMAC)", color=(79, 70, 229))

    # Capa 2: Gatekeeper & Seguridad IAM
    draw_box(draw, (80, 380, 1920, 600), "CAPA 2: COMPUERTA DE SEGURIDAD, AUTENTICACIÓN Y AUTORIZACIÓN (IAM GATEKEEPER)", [
        "• Validador Criptográfico de Contraseñas: scrypt con sal aleatoria de 16 bytes y timingSafeEqual()",
        "• Verificador de Tokens Firmados: HMAC-SHA256 con tiempo de vida (TTL) y validación en sesiones_activas",
        "• Gestor de Concurrencia de Sesiones: Aplica límite individual max_sesiones_simultaneas (409 Conflict)",
        "• Motor Híbrido de Permisos: Evalúa precedencia DENY > ALLOW > ROL_BASE sobre los 18 permisos",
        "• Middleware authorizeAction(): Retorna HTTP 401 si no hay sesión o HTTP 403 si falta el permiso específico"
    ], header_bg=(79, 70, 229), body_bg=(238, 242, 255))

    # Flechas 2 -> 3
    draw_arrow(draw, (1000, 600), (1000, 660), "Acceso Autorizado al Contexto de Negocio", color=(22, 101, 52))

    # Capa 3: Servicios de Negocio
    draw_box(draw, (80, 660, 1920, 890), "CAPA 3: SERVICIOS DE NEGOCIO Y CONTROL OPERATIVO (BACKEND API)", [
        "• Servicio de Portería (processWorkerAccessMovement): Valida estado activo, autorización de puerta y previene doble entrada",
        "• Servicio de Asistencia y Turnos: Compara hora de entrada vs turno + tolerancia (Puntual/Tardanza) y computa horas trabajadas",
        "• Servicio de Zonas y Puntos de Control: Aplica políticas de acceso a puertas peatonales, vehiculares y áreas de alta seguridad",
        "• Servicio de Visitantes: Registro de ingresos externos, asignación de gafete temporal y liberación al fichar salida",
        "• Servicio de Seguridad IAM: Altas/bajas de usuarios, asignación de roles base y configuración de overrides individuales"
    ], header_bg=(30, 64, 175))

    # Flecha 3 -> 4
    draw_arrow(draw, (1000, 890), (1000, 950), "Operaciones Transaccionales ACID / Lectura y Escritura", color=(71, 85, 105))

    # Capa 4: Persistencia
    draw_box(draw, (80, 950, 1920, 1170), "CAPA 4: PERSISTENCIA Y REGISTRO INMUTABLE (DATA STORAGE LAYER)", [
        "• Tablas Operativas: trabajadores, registros_acceso, visitantes, zonas_acceso, turnos_laborales, incidencias_acceso",
        "• Tablas de Seguridad IAM: usuarios, roles, permisos, usuario_permisos_individuales, sesiones_activas",
        "• Bitácora Inmutable: audit_logs (registro detallado de cada login, acceso concedido, bloqueo 403 y cambio de permisos)",
        "• Soporte Dual: Motor JSON Transaccional en memoria/disco con compatibilidad completa para SQL Relacional (schema.sql)"
    ], header_bg=(15, 23, 42))

    img.save(os.path.join(OUT_DIR, "02_Diagrama_Arquitectura_Capas_RBAC.png"), quality=95)

# =============================================================================
# DIAGRAMA 03: MODELO ENTIDAD-RELACIÓN (ERD)
# =============================================================================
def diag_03_erd():
    img, draw = create_canvas(
        "DIAGRAMA 03: MODELO ENTIDAD-RELACIÓN (ERD) — ESQUEMA RELACIONAL COMPLETO",
        "Estructura de Datos para Control Físico de Asistencia, Garita y Seguridad Digital IAM"
    )

    # Dominio Físico y Operativo (Izquierda / Centro)
    draw_box(draw, (60, 160, 480, 480), "TRABAJADORES", [
        "PK  id  (INTEGER)",
        "    codigo_credencial  (VARCHAR UNIQUE)",
        "    documento  (VARCHAR UNIQUE)",
        "    nombre_completo  (VARCHAR)",
        "    cargo  (VARCHAR)",
        "    departamento  (VARCHAR)",
        "FK  turno_id  (INTEGER -> turnos)",
        "    zonas_autorizadas  (JSON / ARRAY)",
        "    placa_vehiculo  (VARCHAR NULL)",
        "    estado  (ACTIVO, SUSPENDIDO)",
        "    ubicacion_actual  (DENTRO/FUERA)"
    ], header_bg=(2, 132, 199))

    draw_box(draw, (560, 160, 1020, 520), "REGISTROS_ACCESO", [
        "PK  id  (INTEGER)",
        "    codigo_movimiento  (VARCHAR UNIQUE)",
        "FK  trabajador_id  (INTEGER -> trabajadores)",
        "FK  zona_id  (INTEGER -> zonas_acceso)",
        "    fecha  (DATE)",
        "    hora_entrada  (TIME)",
        "    hora_salida  (TIME NULL)",
        "    estado_asistencia  (PUNTUAL, TARDANZA)",
        "    estado_ciclo  (EN_PLANTA, FINALIZADO)",
        "    minutos_trabajados  (INTEGER)",
        "    metodo_identificacion  (VARCHAR)",
        "    registrado_por_email  (VARCHAR)"
    ], header_bg=(22, 101, 52))

    draw_box(draw, (60, 540, 480, 790), "ZONAS_ACCESO (PUERTAS)", [
        "PK  id  (INTEGER)",
        "    codigo  (VARCHAR UNIQUE)",
        "    nombre  (VARCHAR)",
        "    tipo  (PEATONAL, VEHICULAR)",
        "    nivel_seguridad  (VARCHAR)",
        "    ubicacion  (VARCHAR)",
        "    estado  (OPERATIVA, CERRADA)"
    ], header_bg=(15, 23, 42))

    draw_box(draw, (60, 840, 480, 1110), "TURNOS_LABORALES", [
        "PK  id  (INTEGER)",
        "    codigo  (VARCHAR UNIQUE)",
        "    nombre  (VARCHAR)",
        "    hora_entrada  (TIME)",
        "    hora_salida  (TIME)",
        "    tolerancia_minutos  (INTEGER)",
        "    activo  (BOOLEAN)"
    ], header_bg=(15, 23, 42))

    draw_box(draw, (560, 570, 1020, 840), "VISITANTES", [
        "PK  id  (INTEGER)",
        "    gafete  (VARCHAR UNIQUE)",
        "    documento  (VARCHAR)",
        "    nombre_completo  (VARCHAR)",
        "    empresa_origen  (VARCHAR)",
        "    anfitrion_visitado  (VARCHAR)",
        "    hora_entrada  (TIME)",
        "    hora_salida  (TIME NULL)",
        "    estado  (EN_PLANTA, SALIDA)"
    ], header_bg=(217, 119, 6))

    draw_box(draw, (560, 880, 1020, 1140), "INCIDENCIAS_ACCESO", [
        "PK  id  (INTEGER)",
        "    fecha_hora  (TIMESTAMP)",
        "    trabajador_nombre  (VARCHAR)",
        "    documento  (VARCHAR)",
        "    zona_nombre  (VARCHAR)",
        "    tipo_alerta  (SUSPENDIDO, NO_ZONA)",
        "    severidad  (ALTA, MEDIA)",
        "    estado_resolucion  (PENDIENTE, RESUELTA)"
    ], header_bg=(220, 38, 38))

    # Dominio de Seguridad Digital e Identidad IAM (Derecha)
    draw_box(draw, (1100, 160, 1520, 480), "USUARIOS_SISTEMA", [
        "PK  id  (INTEGER)",
        "    nombre_completo  (VARCHAR)",
        "    email  (VARCHAR UNIQUE)",
        "    password_hash  (scrypt$salt$hash)",
        "FK  rol  (VARCHAR -> roles_sistema)",
        "    cargo  (VARCHAR)",
        "    max_sesiones_simultaneas  (INTEGER)",
        "    politica_concurrencia  (VARCHAR)",
        "    activo  (BOOLEAN)"
    ], header_bg=(79, 70, 229))

    draw_box(draw, (1580, 160, 1940, 420), "ROLES_SISTEMA", [
        "PK  codigo  (VARCHAR)",
        "    nombre  (VARCHAR)",
        "    descripcion  (TEXT)",
        "    color_badge  (VARCHAR)",
        "    permisos_base  (JSON ARRAY)"
    ], header_bg=(79, 70, 229))

    draw_box(draw, (1100, 530, 1520, 770), "PERMISOS_INDIVIDUALES", [
        "PK  id  (INTEGER)",
        "FK  usuario_id  (INTEGER -> usuarios)",
        "FK  permiso_codigo  (VARCHAR -> permisos)",
        "    modo_override  (ALLOW, DENY)",
        "    actualizado_en  (TIMESTAMP)"
    ], header_bg=(147, 51, 234))

    draw_box(draw, (1580, 470, 1940, 750), "PERMISOS_CATALOGO", [
        "PK  codigo  (VARCHAR)",
        "    modulo  (VARCHAR)",
        "    nombre  (VARCHAR)",
        "    descripcion  (TEXT)"
    ], header_bg=(79, 70, 229))

    draw_box(draw, (1100, 820, 1520, 1140), "SESIONES_ACTIVAS", [
        "PK  session_id  (UUID v4)",
        "FK  usuario_id  (INTEGER -> usuarios)",
        "    ip  (VARCHAR)",
        "    dispositivo  (VARCHAR)",
        "    creada_en  (TIMESTAMP)",
        "    expira_en  (BIGINT EPOCH)",
        "    activa  (BOOLEAN)"
    ], header_bg=(30, 41, 59))

    draw_box(draw, (1580, 800, 1940, 1140), "AUDIT_LOGS", [
        "PK  id  (INTEGER)",
        "    fecha_hora  (TIMESTAMP)",
        "    usuario_email  (VARCHAR)",
        "    rol  (VARCHAR)",
        "    evento  (VARCHAR)",
        "    modulo  (VARCHAR)",
        "    resultado  (EXITO, DENEGADO)",
        "    detalle  (TEXT)"
    ], header_bg=(15, 23, 42))

    # Relaciones
    draw_arrow(draw, (480, 250), (560, 250), "1:N (Historial)", color=(22, 101, 52))
    draw_arrow(draw, (480, 650), (560, 320), "1:N (Puerta)", color=(15, 23, 42))
    draw_arrow(draw, (270, 840), (270, 480), "1:N (Turno)", color=(15, 23, 42))
    draw_arrow(draw, (1520, 250), (1580, 250), "Hereda", color=(79, 70, 229))
    draw_arrow(draw, (1310, 480), (1310, 530), "1:N (Overrides)", color=(147, 51, 234))
    draw_arrow(draw, (1310, 770), (1310, 820), "1:N (Tokens)", color=(30, 41, 59))

    img.save(os.path.join(OUT_DIR, "03_Diagrama_Entidad_Relacion_ERD.png"), quality=95)

# =============================================================================
# DIAGRAMA 04: CLASES UML DEL DOMINIO
# =============================================================================
def diag_04_clases():
    img, draw = create_canvas(
        "DIAGRAMA 04: DIAGRAMA DE CLASES UML DEL DOMINIO Y CONTROL DE ACCESO",
        "Entidades del Sistema, Servicios de Negocio y Motor Criptográfico IAM"
    )

    draw_box(draw, (80, 160, 500, 500), "Trabajador", [
        "- id: int",
        "- codigo_credencial: string",
        "- documento: string",
        "- nombre_completo: string",
        "- cargo: string",
        "- departamento: string",
        "- turno_id: int",
        "- zonas_autorizadas: int[]",
        "- estado: EstadoTrabajador",
        "- ubicacion_actual: Ubicacion",
        "+ estaHabilitado(): bool",
        "+ tieneAccesoAZona(zonaId): bool"
    ], header_bg=(2, 132, 199))

    draw_box(draw, (560, 160, 1020, 500), "RegistroAcceso", [
        "- id: int",
        "- codigo_movimiento: string",
        "- trabajador_id: int",
        "- zona_id: int",
        "- fecha: Date",
        "- hora_entrada: Time",
        "- hora_salida: Time",
        "- estado_asistencia: EstadoAsist",
        "- estado_ciclo: EstadoCiclo",
        "- minutos_trabajados: int",
        "+ computarJornada(horaSalida): int",
        "+ evaluarTardanza(turno): string"
    ], header_bg=(22, 101, 52))

    draw_box(draw, (1080, 160, 1540, 500), "UsuarioIAM", [
        "- id: int",
        "- nombre_completo: string",
        "- email: string",
        "- password_hash: string",
        "- rol_base: string",
        "- max_sesiones: int",
        "- politica_concurrencia: string",
        "- activo: bool",
        "- overrides: Map<string, string>",
        "+ verificarCredenciales(pass): bool",
        "+ resolverPermisosEfectivos(): Map"
    ], header_bg=(79, 70, 229))

    draw_box(draw, (1600, 160, 1940, 500), "SesionActiva", [
        "- session_id: UUID",
        "- usuario_id: int",
        "- ip: string",
        "- creada_en: DateTime",
        "- expira_en: long",
        "- activa: bool",
        "+ haExpirado(): bool",
        "+ invalidar(): void"
    ], header_bg=(30, 41, 59))

    # Capa de Servicios
    draw_box(draw, (80, 580, 680, 880), "WorkerAccessService", [
        "+ processWorkerAccessMovement(params): Result",
        "+ validarPuntualidad(entrada, turno): string",
        "+ registrarEntrada(trabajador, zona): Registro",
        "+ registrarSalida(trabajador, zona): Registro",
        "+ generarAlerta(trabajador, motivo): Incidencia"
    ], header_bg=(30, 64, 175))

    draw_box(draw, (740, 580, 1340, 880), "SecurityEngine & Gatekeeper", [
        "+ hashPassword(plain, salt): string",
        "+ verifyPassword(plain, hash): bool",
        "+ createSignedToken(payload): string",
        "+ verifySignedToken(token): object",
        "+ resolveEffectivePermissions(user, roles): Result",
        "+ authenticateRequest(req, db): AuthContext",
        "+ authorizeAction(req, res, db, perm): AuthContext"
    ], header_bg=(79, 70, 229))

    draw_box(draw, (1400, 580, 1940, 880), "AuditService", [
        "+ recordAuditLog(db, entry): LogItem",
        "+ registrarLoginExitoso(user, ip): void",
        "+ registrarBloqueo403(user, perm): void",
        "+ registrarConflicto409(user, max): void",
        "+ purgarLogsAntiguos(): void"
    ], header_bg=(15, 23, 42))

    # Relaciones entre Clases
    draw_arrow(draw, (500, 300), (560, 300), "1 a N", color=(22, 101, 52))
    draw_arrow(draw, (1540, 300), (1600, 300), "1 a N", color=(79, 70, 229))
    draw_arrow(draw, (380, 580), (380, 500), "Gestiona", color=(30, 64, 175))
    draw_arrow(draw, (1040, 580), (1200, 500), "Evalúa Permisos", color=(79, 70, 229))
    draw_arrow(draw, (1670, 580), (1670, 500), "Audita Sesión", color=(15, 23, 42))

    img.save(os.path.join(OUT_DIR, "04_Diagrama_Clases_Dominio_Seguridad.png"), quality=95)

# =============================================================================
# DIAGRAMA 05: SECUENCIA DE LOGIN Y SESIONES SIMULTÁNEAS (409)
# =============================================================================
def diag_05_secuencia_login():
    img, draw = create_canvas(
        "DIAGRAMA 05: SECUENCIA — LOGIN CRIPTOGRÁFICO Y CONTROL DE CONCURRENCIA (409)",
        "Verificación de Hash scrypt, Detección de Límite de Sesiones y Emisión de Token HMAC"
    )

    # Columnas / Lifelines
    col_x = [120, 500, 950, 1400, 1800]
    col_names = ["Vigilante / Admin", "Frontend Web", "Auth Controller", "Security Engine", "Base de Datos"]

    for i, name in enumerate(col_names):
        draw_box(draw, (col_x[i] - 100, 160, col_x[i] + 100, 220), name, header_bg=(30, 41, 59))
        draw.line([col_x[i], 220, col_x[i], 1180], fill=(203, 213, 225), width=2)

    # Pasos
    y = 260
    draw_arrow(draw, (col_x[0], y), (col_x[1], y), "1. Ingresa credenciales (email, password)", color=(30, 64, 175))
    y += 70
    draw_arrow(draw, (col_x[1], y), (col_x[2], y), "2. POST /api/auth/login", color=(30, 64, 175))
    y += 70
    draw_arrow(draw, (col_x[2], y), (col_x[4], y), "3. Busca usuario por email", color=(71, 85, 105))
    y += 70
    draw_arrow(draw, (col_x[4], y), (col_x[2], y), "4. Retorna usuario y password_hash (scrypt)", color=(71, 85, 105))
    y += 70
    draw_arrow(draw, (col_x[2], y), (col_x[3], y), "5. verifyPassword(password, storedHash)", color=(79, 70, 229))
    y += 70
    draw_arrow(draw, (col_x[3], y), (col_x[2], y), "6. timingSafeEqual() -> OK", color=(22, 101, 52))
    y += 80

    # Condición de Sesión Simultánea
    draw_box(draw, (col_x[2] - 180, y, col_x[2] + 180, y + 60), "¿Sesiones Activas >= max_sesiones?", header_bg=(217, 119, 6))
    y += 90

    # Rama 409
    draw_arrow(draw, (col_x[2], y), (col_x[1], y), "7a. [Sin force_replace] HTTP 409 MAX_SESSIONS_REACHED", color=(220, 38, 38))
    y += 50
    draw_arrow(draw, (col_x[1], y), (col_x[0], y), "Alerta: 'Límite alcanzado. ¿Cerrar sesión previa?'", color=(220, 38, 38))
    y += 80

    # Rama Reemplazo
    draw_arrow(draw, (col_x[0], y), (col_x[1], y), "8. Usuario confirma: force_replace = true", color=(22, 101, 52))
    y += 60
    draw_arrow(draw, (col_x[1], y), (col_x[2], y), "9. Reintenta login con force_replace", color=(22, 101, 52))
    y += 60
    draw_arrow(draw, (col_x[2], y), (col_x[4], y), "10. Invalida sesión anterior (activa = false)", color=(71, 85, 105))
    y += 60
    draw_arrow(draw, (col_x[2], y), (col_x[3], y), "11. createSignedToken(sid, uid, rol, exp)", color=(79, 70, 229))
    y += 60
    draw_arrow(draw, (col_x[2], y), (col_x[1], y), "12. HTTP 200 OK + Token HMAC + Permisos Efectivos", color=(22, 101, 52))

    img.save(os.path.join(OUT_DIR, "05_Diagrama_Secuencia_Autenticacion_Sesion.png"), quality=95)

# =============================================================================
# DIAGRAMA 06: SECUENCIA DE AUTORIZACIÓN EN BACKEND (403 VS 200)
# =============================================================================
def diag_06_secuencia_autorizacion():
    img, draw = create_canvas(
        "DIAGRAMA 06: SECUENCIA — EVALUACIÓN DE PERMISOS EN SERVIDOR (403 VS 200)",
        "Protección en Backend, Bloqueo de Acceso no Autorizado y Efecto de Permiso Individual ALLOW"
    )

    col_x = [140, 550, 1050, 1550, 1850]
    col_names = ["Vigilante Portería", "Frontend SPA", "Gatekeeper Middleware", "Lógica de Negocio", "Audit Logs"]

    for i, name in enumerate(col_names):
        draw_box(draw, (col_x[i] - 110, 160, col_x[i] + 110, 220), name, header_bg=(30, 41, 59))
        draw.line([col_x[i], 220, col_x[i], 1180], fill=(203, 213, 225), width=2)

    y = 260
    draw_arrow(draw, (col_x[0], y), (col_x[1], y), "1. Intenta modificar turno de trabajador (RR.HH.)", color=(30, 64, 175))
    y += 70
    draw_arrow(draw, (col_x[1], y), (col_x[2], y), "2. PUT /api/admin/trabajadores/1 (Bearer Token)", color=(30, 64, 175))
    y += 70
    draw_arrow(draw, (col_x[2], y), (col_x[2], y + 40), "3. Evalúa authorizeAction('trabajadores:editar')", color=(79, 70, 229))
    y += 70
    draw_arrow(draw, (col_x[2], y), (col_x[4], y), "4. Registra ACCESO_DENEGADO_403 en auditoría", color=(220, 38, 38))
    y += 70
    draw_arrow(draw, (col_x[2], y), (col_x[1], y), "5. HTTP 403 Forbidden: 'Carece de permiso [trabajadores:editar]'", color=(220, 38, 38))
    y += 70
    draw_arrow(draw, (col_x[1], y), (col_x[0], y), "Muestra Alerta Roja: Operación rechazada por el servidor", color=(220, 38, 38))
    y += 100

    # Concesión de permiso individual ALLOW
    draw_box(draw, (col_x[1] - 80, y, col_x[3] + 80, y + 55), "El Administrador otorga en caliente ALLOW en 'asistencia:ver' al Vigilante", header_bg=(22, 101, 52))
    y += 90

    draw_arrow(draw, (col_x[0], y), (col_x[1], y), "6. Vigilante consulta Historial de Asistencia del día", color=(22, 101, 52))
    y += 70
    draw_arrow(draw, (col_x[1], y), (col_x[2], y), "7. GET /api/admin/dashboard (requiere asistencia:ver)", color=(22, 101, 52))
    y += 70
    draw_arrow(draw, (col_x[2], y), (col_x[2], y + 40), "8. Overrides individual ALLOW detectado -> Permiso Efectivo = TRUE", color=(22, 101, 52))
    y += 70
    draw_arrow(draw, (col_x[2], y), (col_x[3], y), "9. Ejecuta controlador y consulta registros de hoy", color=(30, 64, 175))
    y += 70
    draw_arrow(draw, (col_x[3], y), (col_x[1], y), "10. HTTP 200 OK + Lista de marcaciones", color=(22, 101, 52))

    img.save(os.path.join(OUT_DIR, "06_Diagrama_Secuencia_Autorizacion_Backend.png"), quality=95)

# =============================================================================
# DIAGRAMA 07: ACTIVIDADES — FLUJO DE CONTROL DE ACCESO EN PORTERÍA
# =============================================================================
def diag_07_actividades():
    img, draw = create_canvas(
        "DIAGRAMA 07: ACTIVIDADES — FLUJO OPERATIVO DE MARCACIÓN EN PORTERÍA",
        "Algoritmo de Validación de Credencial, Verificación de Zona, Horario y Apertura de Puerta"
    )

    y = 150
    draw_box(draw, (850, y, 1150, y + 60), "Inicio: Pasa Tarjeta / Digita DNI", header_bg=(30, 41, 59))
    draw_arrow(draw, (1000, y + 60), (1000, y + 110), "", color=(71, 85, 105))
    y += 110

    draw_box(draw, (800, y, 1200, y + 60), "¿Existe en Padrón de Trabajadores?", header_bg=(30, 64, 175))
    draw_arrow(draw, (800, y + 30), (500, y + 30), "No", color=(220, 38, 38))
    draw_box(draw, (220, y, 500, y + 60), "Alerta: No Encontrado (404)", header_bg=(220, 38, 38))
    draw_arrow(draw, (1000, y + 60), (1000, y + 110), "Sí", color=(22, 101, 52))
    y += 110

    draw_box(draw, (800, y, 1200, y + 60), "¿Estado es ACTIVO?", header_bg=(30, 64, 175))
    draw_arrow(draw, (800, y + 30), (500, y + 30), "Suspendido", color=(220, 38, 38))
    draw_box(draw, (150, y - 10, 500, y + 70), "Rechazo 403: Genera Incidencia Falsa", header_bg=(220, 38, 38))
    draw_arrow(draw, (1000, y + 60), (1000, y + 110), "Sí", color=(22, 101, 52))
    y += 110

    draw_box(draw, (750, y, 1250, y + 60), "¿Tiene Autorización en esta Puerta/Zona?", header_bg=(30, 64, 175))
    draw_arrow(draw, (750, y + 30), (500, y + 30), "No Permitida", color=(220, 38, 38))
    draw_box(draw, (150, y - 10, 500, y + 70), "Rechazo 403: Zona no Autorizada", header_bg=(220, 38, 38))
    draw_arrow(draw, (1000, y + 60), (1000, y + 110), "Sí", color=(22, 101, 52))
    y += 110

    draw_box(draw, (820, y, 1180, y + 60), "¿Es ENTRADA o SALIDA?", header_bg=(79, 70, 229))
    draw_arrow(draw, (820, y + 30), (600, y + 100), "ENTRADA", color=(22, 101, 52))
    draw_arrow(draw, (1180, y + 30), (1400, y + 100), "SALIDA", color=(217, 119, 6))

    # Rama ENTRADA (Izquierda)
    draw_box(draw, (400, y + 100, 800, y + 210), "Procesar Entrada (Check-In)", [
        "• Valida que no esté ya dentro de planta",
        "• Compara hora vs turno + tolerancia",
        "• Determina: PUNTUAL o TARDANZA",
        "• Estado = DENTRO_PLANTA"
    ], header_bg=(22, 101, 52))

    # Rama SALIDA (Derecha)
    draw_box(draw, (1200, y + 100, 1600, y + 210), "Procesar Salida (Check-Out)", [
        "• Valida que tenga entrada abierta",
        "• Calcula horas y minutos laborados",
        "• Cierra ciclo de asistencia (FINALIZADO)",
        "• Estado = FUERA_PLANTA"
    ], header_bg=(217, 119, 6))

    y += 260
    draw_arrow(draw, (600, y - 50), (900, y + 20), "OK", color=(22, 101, 52))
    draw_arrow(draw, (1400, y - 50), (1100, y + 20), "OK", color=(217, 119, 6))

    draw_box(draw, (750, y + 20, 1250, y + 100), "Guarda Registro + Desbloquea Torniquete / Puerta", [
        "• Actualiza Aforo de Planta en Vivo",
        "• Notifica en la Consola del Vigilante"
    ], header_bg=(15, 23, 42))

    img.save(os.path.join(OUT_DIR, "07_Diagrama_Actividades_Flujo_Control_Acceso.png"), quality=95)

# =============================================================================
# DIAGRAMA 08: MÁQUINAS DE ESTADOS — SESIÓN DIGITAL Y PRESENCIA DE TRABAJADOR
# =============================================================================
def diag_08_estados():
    img, draw = create_canvas(
        "DIAGRAMA 08: MÁQUINAS DE ESTADOS — CICLO DE SESIÓN IAM Y PRESENCIA FÍSICA",
        "Transiciones de Sesiones de Usuario y Ciclo de Asistencia del Personal en la Empresa"
    )

    # Máquina 1: Sesión IAM (Izquierda)
    draw_box(draw, (80, 150, 950, 220), "MÁQUINA DE ESTADOS 1: SESIÓN DIGITAL DEL USUARIO (IAM)", header_bg=(79, 70, 229))

    draw_box(draw, (120, 280, 360, 360), "ESTADO: INACTIVA", ["• Sin sesión", "• Credenciales requeridas"], header_bg=(71, 85, 105))
    draw_arrow(draw, (360, 320), (550, 320), "Login correcto (scrypt)", color=(22, 101, 52))

    draw_box(draw, (550, 280, 850, 420), "ESTADO: SESIÓN_ACTIVA", [
        "• Token HMAC válido en memoria",
        "• Registrada en sesiones_activas",
        "• Permisos efectivos activos"
    ], header_bg=(22, 101, 52))

    draw_arrow(draw, (700, 420), (700, 560), "Supera max_sesiones (409)", color=(217, 119, 6))

    draw_box(draw, (550, 560, 850, 680), "ESTADO: CONFLICTO_409", [
        "• Bloqueo por concurrencia",
        "• Requiere force_replace = true"
    ], header_bg=(217, 119, 6))

    draw_arrow(draw, (700, 680), (700, 780), "Cierre / Revocación", color=(220, 38, 38))

    draw_box(draw, (550, 780, 850, 900), "ESTADO: REVOCADA / EXPIRADA", [
        "• Sesión cerrada por Administrador",
        "• Token inválido en Backend (401)"
    ], header_bg=(220, 38, 38))

    draw_arrow(draw, (550, 840), (240, 840), "", color=(71, 85, 105))
    draw_arrow(draw, (240, 840), (240, 360), "Regresa a Login", color=(71, 85, 105))

    # Máquina 2: Presencia Física del Trabajador (Derecha)
    draw_box(draw, (1050, 150, 1920, 220), "MÁQUINA DE ESTADOS 2: PRESENCIA FÍSICA Y ASISTENCIA", header_bg=(2, 132, 199))

    draw_box(draw, (1100, 280, 1400, 380), "ESTADO: FUERA_DE_PLANTA", [
        "• Trabajador fuera de la empresa",
        "• Sin jornada activa abierta"
    ], header_bg=(71, 85, 105))

    draw_arrow(draw, (1400, 330), (1550, 330), "Marca Entrada (Garita)", color=(22, 101, 52))

    draw_box(draw, (1550, 280, 1880, 460), "ESTADO: DENTRO_DE_PLANTA", [
        "• Credencial activa en aforo",
        "• Asistencia: Puntual / Tardanza",
        "• Jornada laboral en curso",
        "• Puerta registrada"
    ], header_bg=(22, 101, 52))

    draw_arrow(draw, (1715, 460), (1715, 620), "Marca Salida en Puerta", color=(217, 119, 6))

    draw_box(draw, (1550, 620, 1880, 780), "ESTADO: SALIDA_REGISTRADA", [
        "• Horas trabajadas calculadas",
        "• Ciclo cerrado (FINALIZADO)",
        "• Actualiza contador de aforo"
    ], header_bg=(217, 119, 6))

    draw_arrow(draw, (1550, 700), (1250, 700), "", color=(71, 85, 105))
    draw_arrow(draw, (1250, 700), (1250, 380), "Listo para nueva jornada", color=(71, 85, 105))

    img.save(os.path.join(OUT_DIR, "08_Diagrama_Estados_Sesion_Y_Citas.png"), quality=95)

def main():
    print("Iniciando generación de los 8 diagramas profesionales PNG...")
    diag_01_casos_de_uso()
    diag_02_arquitectura()
    diag_03_erd()
    diag_04_clases()
    diag_05_secuencia_login()
    diag_06_secuencia_autorizacion()
    diag_07_actividades()
    diag_08_estados()
    print("Los 8 diagramas han sido generados exitosamente en:", OUT_DIR)

if __name__ == '__main__':
    main()
