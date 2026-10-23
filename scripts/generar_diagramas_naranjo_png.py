# -*- coding: utf-8 -*-
"""
Generador de Diagramas Oficiales en Alta Resolución (.PNG) para:
Recuperaciones Naranjo S.A.S. — Sistema de Control de Acceso, Asistencia y Portería Industrial (Cartagena)
Genera 8 diagramas técnicos profesionales con la paleta institucional (Naranja Industrial #EA580C y Azul Acero #0F172A).
"""
import os
import math
from PIL import Image, ImageDraw, ImageFont

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
OUT_DIR = os.path.join(BASE_DIR, 'docs', 'diagramas_naranjo_png')
os.makedirs(OUT_DIR, exist_ok=True)

# Paleta Corporativa Recuperaciones Naranjo
NARANJA_CORP = (234, 88, 12)       # #EA580C
AZUL_ACERO = (15, 23, 42)          # #0F172A
AZUL_MEDIO = (30, 64, 175)         # #1E40AF
SLATE_HEADER = (30, 41, 59)        # #1E293B
FONDO_CANVAS = (248, 250, 252)     # #F8FAFC
BLANCO = (255, 255, 255)
VERDE_EXITO = (16, 185, 129)       # #10B981
ROJO_ALERTA = (239, 68, 68)        # #EF4444
AMBAR_TARDANZA = (245, 158, 11)    # #F59E0B
GRIS_TEXTO = (51, 65, 85)          # #334155
GRIS_BORDE = (203, 213, 225)       # #CBD5E1

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
    img = Image.new('RGB', (width, height), FONDO_CANVAS)
    draw = ImageDraw.Draw(img)

    # Banner superior institucional
    draw.rectangle([0, 0, width, 110], fill=AZUL_ACERO)
    draw.rectangle([0, 106, width, 112], fill=NARANJA_CORP)

    f_title = get_font(28, bold=True)
    f_sub = get_font(17, bold=False)
    draw.text((40, 20), title, fill=BLANCO, font=f_title)
    draw.text((40, 66), subtitle, fill=(203, 213, 225), font=f_sub)

    # Badge Naranjo
    draw.rounded_rectangle([width - 340, 28, width - 40, 82], radius=8, fill=NARANJA_CORP)
    f_badge = get_font(16, bold=True)
    draw.text((width - 325, 42), "RECUPERACIONES NARANJO", fill=BLANCO, font=f_badge)

    # Pie de diagrama
    draw.rectangle([0, height - 42, width, height], fill=(226, 232, 240))
    f_foot = get_font(15, bold=False)
    draw.text(
        (40, height - 32),
        "Recuperaciones Naranjo S.A.S. — Sistema de Control de Acceso, Asistencia 42h (L-V) y Patio (Cartagena de Indias)",
        fill=(71, 85, 105),
        font=f_foot
    )
    return img, draw

def draw_box(draw, box, title, lines=None, header_bg=SLATE_HEADER, body_bg=BLANCO, border=NARANJA_CORP, radius=10):
    x1, y1, x2, y2 = box
    draw.rounded_rectangle([x1 + 4, y1 + 4, x2 + 4, y2 + 4], radius=radius, fill=(203, 213, 225))
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=body_bg, outline=border, width=3)

    if lines is not None:
        h_bar = 42
        draw.rounded_rectangle([x1, y1, x2, y1 + h_bar], radius=radius, fill=header_bg)
        draw.rectangle([x1, y1 + h_bar - 10, x2, y1 + h_bar], fill=header_bg)

        f_head = get_font(16, bold=True)
        draw.text((x1 + 16, y1 + 10), title, fill=BLANCO, font=f_head)

        f_body = get_font(14, bold=False)
        curr_y = y1 + h_bar + 12
        for line in lines:
            draw.text((x1 + 16, curr_y), line, fill=GRIS_TEXTO, font=f_body)
            curr_y += 24
    else:
        f_mid = get_font(16, bold=True)
        draw.text((x1 + 14, y1 + 14), title, fill=GRIS_TEXTO, font=f_mid)

def draw_arrow(draw, start, end, label=None, color=NARANJA_CORP, width=3):
    x1, y1 = start
    x2, y2 = end
    draw.line([x1, y1, x2, y2], fill=color, width=width)

    angle = math.atan2(y2 - y1, x2 - x1)
    arrow_len = 16
    arrow_angle = math.pi / 6

    px1 = x2 - arrow_len * math.cos(angle - arrow_angle)
    py1 = y2 - arrow_len * math.sin(angle - arrow_angle)
    px2 = x2 - arrow_len * math.cos(angle + arrow_angle)
    py2 = y2 - arrow_len * math.sin(angle + arrow_angle)

    draw.polygon([(x2, y2), (px1, py1), (px2, py2)], fill=color)

    if label:
        mx = (x1 + x2) / 2
        my = (y1 + y2) / 2 - 18
        f_lbl = get_font(13, bold=True)
        draw.text((mx + 6, my), label, fill=color, font=f_lbl)

def draw_actor(draw, x, y, label):
    r = 22
    draw.ellipse([x - r, y - r, x + r, y + r], fill=BLANCO, outline=AZUL_ACERO, width=3)
    draw.line([x, y + r, x, y + r + 38], fill=AZUL_ACERO, width=3)
    draw.line([x - 24, y + r + 14, x + 24, y + r + 14], fill=AZUL_ACERO, width=3)
    draw.line([x, y + r + 38, x - 20, y + r + 75], fill=AZUL_ACERO, width=3)
    draw.line([x, y + r + 38, x + 20, y + r + 75], fill=AZUL_ACERO, width=3)

    f_act = get_font(15, bold=True)
    bbox = f_act.getbbox(label)
    w_text = bbox[2] - bbox[0]
    draw.text((x - w_text // 2, y + r + 82), label, fill=AZUL_ACERO, font=f_act)

# =============================================================================
# 1. DIAGRAMA DE CASOS DE USO GENERAL
# =============================================================================
def generate_diagram_01():
    img, draw = create_canvas(
        "Diagrama 01: Casos de Uso del Sistema de Control de Acceso y Asistencia",
        "Interacción entre Operario de Patio, Conductor, Vigilante, Jefe de Patio y Administrador (Recuperaciones Naranjo)"
    )

    draw_actor(draw, 140, 280, "👷 Operario de Patio")
    draw_actor(draw, 140, 680, "🚛 Conductor / Proveedor")
    draw_actor(draw, 1860, 260, "🛡️ Vigilante Garita")
    draw_actor(draw, 1860, 600, "📱 Jefe de Patio")
    draw_actor(draw, 1860, 940, "💼 Admin / RR.HH.")

    # Límite del sistema
    draw.rounded_rectangle([320, 140, 1680, 1170], radius=16, fill=(255, 255, 255), outline=SLATE_HEADER, width=3)
    f_sys = get_font(20, bold=True)
    draw.text((360, 160), "SISTEMA INTEGRAL SENTINELPRO NARANJO (CARTAGENA)", fill=AZUL_ACERO, font=f_sys)

    cases = [
        ([380, 230, 800, 310], "CU-01: Digitar Cédula en Kiosco (Entrada/Salida)", (140, 310)),
        ([380, 340, 800, 420], "CU-02: Escanear Cédula / Carnet con Código de Barras", (140, 320)),
        ([380, 450, 800, 530], "CU-03: Validar Tolerancia y Horario Oficial (Lunes a Viernes 42h)", None),
        ([380, 560, 800, 640], "CU-04: Control Anti-Passback (Bloqueo de Doble Entrada)", None),
        ([380, 670, 800, 750], "CU-05: Fichar Ingreso de Camión de Chatarra / Báscula", (140, 700)),
        ([380, 780, 800, 860], "CU-06: Asignar Gafete Temporal a Visitante/Taller", (140, 710)),

        ([940, 230, 1500, 310], "CU-07: Monitorear Cuadrilla en Vivo (Presentes / Ausentes / Tardanzas)", (1860, 620)),
        ([940, 340, 1500, 420], "CU-08: Autorizar Jornada en Sábados, Domingos o Festivos (Patio)", (1860, 630)),
        ([940, 450, 1500, 530], "CU-09: Recibir Alerta de Ausencia en Puesto Crítico (Oxicorte/Báscula)", (1860, 640)),
        ([940, 560, 1500, 640], "CU-10: Supervisar Monitor Espejo de Garita y Foto en Grande", (1860, 280)),
        ([940, 670, 1500, 750], "CU-11: Controlar Aforo Global de Planta en Vivo (SST/ARL)", (1860, 290)),
        ([940, 780, 1500, 860], "CU-12: Liquidar Horas Semanales (42h L-V + Extras + Recargo Nocturno)", (1860, 960)),
        ([940, 890, 1500, 970], "CU-13: Exportar Pre-Nómina a Excel (Siigo / World Office)", (1860, 970)),
        ([940, 1000, 1500, 1080], "CU-14: Administrar Padrón de Cédulas y Permisos Especiales", (1860, 980))
    ]

    f_cu = get_font(14, bold=True)
    for box, title, actor_conn in cases:
        x1, y1, x2, y2 = box
        draw.ellipse([x1, y1, x2, y2], fill=(254, 243, 199), outline=NARANJA_CORP, width=2)
        # Centrar texto
        bbox = f_cu.getbbox(title)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        draw.text((cx - tw // 2, cy - th // 2), title, fill=AZUL_ACERO, font=f_cu)

        if actor_conn:
            draw.line([actor_conn[0], actor_conn[1], x1 if actor_conn[0] < x1 else x2, cy], fill=(148, 163, 184), width=2)

    path = os.path.join(OUT_DIR, "01_Casos_De_Uso_Recuperaciones_Naranjo.png")
    img.save(path, quality=95)
    print(f"Generado: {path}")

# =============================================================================
# 2. DIAGRAMA DE ARQUITECTURA EN CAPAS Y MOTOR DE LIQUIDACIÓN 42H
# =============================================================================
def generate_diagram_02():
    img, draw = create_canvas(
        "Diagrama 02: Arquitectura en Capas y Motor de Liquidación Horaria (42h L-V)",
        "Estructura Tecnológica de SentinelPro IAM adaptada para la Planta de Recuperaciones Naranjo (Cartagena)"
    )

    layers = [
        ("1. CAPA DE INTERFACES INDUSTRIALES (FRONTEND / EDGE)", 140, [
            ("Kiosco Táctil Garita", ["• Teclado numérico gigante para Cédula", "• Lector láser código de barras PDF417", "• Sonidos feedback Web Audio API", "• Interfaz responsive 15-21\" full-screen"], (60, 200, 480, 360)),
            ("Monitor Espejo Vigilante", ["• Foto en grande del operario", "• Cotejo visual instantáneo", "• Control de visitantes y gafetes", "• Aforo de planta en vivo"], (540, 200, 960, 360)),
            ("Portal Móvil Jefe de Patio", ["• Tablero 'Mi Cuadrilla en Vivo'", "• Semáforo verde/amarillo/rojo", "• Alertas push puestos críticos", "• Aprobación extras Sáb/Dom"], (1020, 200, 1440, 360)),
            ("Panel Admin & Nómina", ["• Gestión de padrón de cédulas", "• Parametrización de turnos L-V", "• Exportador Siigo / World Office", "• Bitácora inmutable de auditoría"], (1500, 200, 1940, 360))
        ]),
        ("2. CAPA DE LÓGICA DE NEGOCIO Y MOTOR LABORAL (BACKEND NODE.JS)", 420, [
            ("Motor de Validación Acceso", ["• Comprueba Cédula ACTIVA/SUSPENDIDA", "• Control Anti-Passback estricto", "• Comparador horario oficial L-V", "• Tolerancia 10 min de gracia"], (60, 480, 520, 640)),
            ("Motor de Jornadas y Nómina (42h)", ["• Lunes: 8:00 a 16:30 (1.5h almuerzo = 7.0h)", "• Mar/Vie: 7:30 a 17:00 (1h almuerzo = 8.5h)", "• Mié/Jue: 7:30 a 17:30 (1h almuerzo = 9.0h)", "• Total L-V = 42h ordinarias semanales"], (580, 480, 1060, 640)),
            ("Motor de Patio (Sáb/Dom/Festivos)", ["• Detecta trabajo extraordinario en patio", "• Horas Extras Diurnas (HED +25%)", "• Horas Extras Nocturnas (HEN +75%)", "• Recargo Dominical/Festivo (+75%/100%)"], (1120, 480, 1560, 640)),
            ("Servicio Cuadrilla en Tiempo Real", ["• Eventos SSE / WebSockets a celular", "• Notificación de ausencias a 15 min", "• Sincronización continua de aforo", "• Registro inmutable en audit_logs"], (1620, 480, 1940, 640))
        ]),
        ("3. CAPA DE PERSISTENCIA, RESILIENCIA Y SEGURIDAD", 700, [
            ("Base de Datos Relacional Central", ["• PostgreSQL 16 / Tablas Naranjo", "• Partición de marcaciones por mes", "• Historial de auditoría inmutable", "• Transacciones ACID protegidas"], (60, 760, 660, 920)),
            ("Garita Offline-First (SQLite)", ["• Padrón de cédulas en caché local", "• Marcación continua ante cortes de fibra", "• Cola transaccional de sincronización", "• Autonomía total con respaldo UPS"], (720, 760, 1320, 920)),
            ("Criptografía e Identidad IAM", ["• Contraseñas scrypt (salt 16 bytes)", "• Tokens HMAC-SHA256 con TTL", "• Matriz RBAC + Overrides individuales", "• Comparación timingSafeEqual"], (1380, 760, 1940, 920))
        ])
    ]

    for title, y_top, boxes in layers:
        draw.rounded_rectangle([40, y_top, 1960, y_top + 260], radius=12, fill=(241, 245, 249), outline=SLATE_HEADER, width=2)
        f_lay = get_font(17, bold=True)
        draw.text((60, y_top + 12), title, fill=NARANJA_CORP, font=f_lay)

        for b_title, b_lines, coords in boxes:
            draw_box(draw, coords, b_title, b_lines, header_bg=AZUL_ACERO, border=NARANJA_CORP)

    # Flechas intercapas
    draw_arrow(draw, (270, 360), (270, 480), "Cédula", color=AZUL_MEDIO)
    draw_arrow(draw, (820, 360), (820, 480), "Foto / Aforo", color=AZUL_MEDIO)
    draw_arrow(draw, (1280, 480), (1280, 360), "SSE Cuadrilla", color=VERDE_EXITO)
    draw_arrow(draw, (820, 640), (820, 760), "Sync Offline", color=NARANJA_CORP)
    draw_arrow(draw, (360, 640), (360, 760), "Commit SQL", color=AZUL_ACERO)

    path = os.path.join(OUT_DIR, "02_Arquitectura_Capas_Y_Motor_42Horas.png")
    img.save(path, quality=95)
    print(f"Generado: {path}")

# =============================================================================
# 3. DIAGRAMA DE SECUENCIA - FICHAJE EN KIOSCO CON CÉDULA
# =============================================================================
def generate_diagram_03():
    img, draw = create_canvas(
        "Diagrama 03: Secuencia — Fichaje en Kiosco Táctil con Cédula de Ciudadanía",
        "Validación de Horario Oficial Naranjo (Lunes a Viernes), Tolerancia, Anti-Passback y Notificación a Jefe de Patio"
    )

    lifelines = [
        ("👷 Operario", 160),
        ("🖥️ Kiosco Táctil", 500),
        ("🛡️ Backend SentinelPro", 880),
        ("📊 Base de Datos", 1240),
        ("🛡️ Monitor Vigilante", 1560),
        ("📱 Celular Jefe Patio", 1840)
    ]

    f_life = get_font(15, bold=True)
    for title, x in lifelines:
        draw.rounded_rectangle([x - 90, 140, x + 90, 190], radius=8, fill=AZUL_ACERO)
        bbox = f_life.getbbox(title)
        tw = bbox[2] - bbox[0]
        draw.text((x - tw // 2, 152), title, fill=BLANCO, font=f_life)
        draw.line([x, 190, x, 1160], fill=(203, 213, 225), width=2)

    events = [
        ((160, 240), (500, 240), "1. Digita Cédula de Ciudadanía en Pantalla", NARANJA_CORP),
        ((500, 290), (880, 290), "2. POST /api/public/kiosco/marcar {cedula, movimiento}", AZUL_MEDIO),
        ((880, 340), (1240, 340), "3. SELECT trabajador, turno_dia, ultimo_movimiento", AZUL_ACERO),
        ((1240, 390), (880, 390), "4. Retorna {activo: true, turno_hoy, ubicacion: FUERA}", AZUL_ACERO),
        ((880, 450), (880, 500), "5. Valida Anti-Passback (¿Está fuera? OK)", SLATE_HEADER),
        ((880, 550), (880, 600), "6. Compara hora vs horario oficial Naranjo (tolerancia 10m)", SLATE_HEADER),
        ((880, 660), (1240, 660), "7. INSERT INTO registros_acceso {hora, puntualidad}", AZUL_ACERO),
        ((880, 720), (500, 720), "8. HTTP 200 OK: {nombre, cargo, 'PUNTUAL', foto}", VERDE_EXITO),
        ((500, 780), (160, 780), "9. Pantalla Verde + Sonido Beep Aprobación + Muestra Foto", VERDE_EXITO),
        ((880, 850), (1560, 850), "10. WS / SSE: Actualiza monitor garita con foto grande", NARANJA_CORP),
        ((880, 920), (1840, 920), "11. WS / SSE: Cuadrilla patio (Carlos Pérez: PRESENTE)", VERDE_EXITO),
        ((160, 1020), (500, 1020), "12. Al salir: Digita Cédula -> Calcula horas laboradas turno", AZUL_MEDIO),
        ((500, 1080), (160, 1080), "13. Pantalla Azul: '¡Buen descanso! Jornada cumplida: 8h 30m'", AZUL_MEDIO)
    ]

    for start, end, label, col in events:
        if start[0] == end[0]: # Auto-llamada
            x = start[0]
            y1 = start[1]
            y2 = end[1]
            draw.line([x, y1, x + 40, y1], fill=col, width=2)
            draw.line([x + 40, y1, x + 40, y2], fill=col, width=2)
            draw_arrow(draw, (x + 40, y2), (x, y2), None, color=col, width=2)
            f_l = get_font(13, bold=True)
            draw.text((x + 48, y1 + 6), label, fill=col, font=f_l)
        else:
            draw_arrow(draw, start, end, label, color=col, width=2)

    path = os.path.join(OUT_DIR, "03_Secuencia_Fichaje_Kiosco_Cedula.png")
    img.save(path, quality=95)
    print(f"Generado: {path}")

# =============================================================================
# 4. DIAGRAMA DE SECUENCIA - MONITOREO CUADRILLA JEFE DE PATIO
# =============================================================================
def generate_diagram_04():
    img, draw = create_canvas(
        "Diagrama 04: Secuencia — Monitoreo de Cuadrilla y Alertas de Puestos Críticos",
        "Control Operativo en Vivo para el Jefe de Patio / Supervisor en Planta (Recuperaciones Naranjo)"
    )

    lifelines = [
        ("📱 Jefe de Patio (Móvil)", 220),
        ("🌐 Web App Cuadrilla", 640),
        ("⚙️ Motor SentinelPro", 1100),
        ("⏰ Cron Alertas (15m)", 1500),
        ("💬 Alertas WhatsApp/Push", 1820)
    ]

    f_life = get_font(15, bold=True)
    for title, x in lifelines:
        draw.rounded_rectangle([x - 110, 140, x + 110, 190], radius=8, fill=AZUL_ACERO)
        bbox = f_life.getbbox(title)
        tw = bbox[2] - bbox[0]
        draw.text((x - tw // 2, 152), title, fill=BLANCO, font=f_life)
        draw.line([x, 190, x, 1160], fill=(203, 213, 225), width=2)

    events = [
        ((220, 240), (640, 240), "1. Abre portal 'Mi Cuadrilla en Vivo' desde celular", NARANJA_CORP),
        ((640, 290), (1100, 290), "2. GET /api/jefe/cuadrilla/en-vivo (Área: Patio de Metales)", AZUL_MEDIO),
        ((1100, 350), (640, 350), "3. Retorna {total: 25, presentes: 22, tardanzas: 3, ausentes: 0}", AZUL_ACERO),
        ((640, 410), (220, 410), "4. Renderiza semáforo visual de asistencia de operarios", VERDE_EXITO),
        ((1500, 500), (1100, 500), "5. Disparo de verificación: Hora inicio + 15 min (7:45 AM / 8:15 AM)", SLATE_HEADER),
        ((1100, 570), (1100, 620), "6. Revisa puestos críticos: ¿Llegó Operario de Grúa y Oxicorte?", ROJO_ALERTA),
        ((1100, 680), (1820, 680), "7. Detecta falta de Oxigenista -> Dispara alerta inmediata", ROJO_ALERTA),
        ((1820, 740), (220, 740), "8. Notificación en celular: '¡ALERTA! Falta Operario Oxicorte'", ROJO_ALERTA),
        ((220, 820), (640, 820), "9. Jefe reasigna operario de relevo o llama al colaborador", NARANJA_CORP),
        ((220, 920), (640, 920), "10. Autoriza jornada extraordinaria Sábado para terminar cargue", AZUL_MEDIO),
        ((640, 980), (1100, 980), "11. POST /api/jefe/autorizar-extra {operario_id, fecha, motivo}", AZUL_MEDIO),
        ((1100, 1040), (220, 1040), "12. Confirmación: Hora extra aprobada y registrada para nómina", VERDE_EXITO)
    ]

    for start, end, label, col in events:
        if start[0] == end[0]:
            x = start[0]
            y1 = start[1]
            y2 = end[1]
            draw.line([x, y1, x + 40, y1], fill=col, width=2)
            draw.line([x + 40, y1, x + 40, y2], fill=col, width=2)
            draw_arrow(draw, (x + 40, y2), (x, y2), None, color=col, width=2)
            f_l = get_font(13, bold=True)
            draw.text((x + 48, y1 + 6), label, fill=col, font=f_l)
        else:
            draw_arrow(draw, start, end, label, color=col, width=2)

    path = os.path.join(OUT_DIR, "04_Secuencia_Monitoreo_Cuadrilla_Jefe_Patio.png")
    img.save(path, quality=95)
    print(f"Generado: {path}")

# =============================================================================
# 5. DIAGRAMA DE FLUJO / ACTIVIDADES - LIQUIDACIÓN JORNADAS Y HORAS EXTRAS
# =============================================================================
def generate_diagram_05():
    img, draw = create_canvas(
        "Diagrama 05: Flujo de Actividades — Liquidación de Jornadas 42h y Recargos de Patio",
        "Reglas de Negocio Oficiales: Lunes a Viernes 42h + Sábados, Domingos y Festivos (Recuperaciones Naranjo)"
    )

    steps = [
        ("INICIO: Marcación de Entrada con Cédula", 1000, 160, AZUL_ACERO),
        ("¿Día de la Semana?", 1000, 270, SLATE_HEADER),
        ("LUNES (8:00 AM a 4:30 PM)\nAlmuerzo 12:00 a 1:30 PM (1.5h)\nTotal: 7.0 horas ordinarias", 500, 420, AZUL_MEDIO),
        ("MARTES A VIERNES\n7:30 AM a 5:00 / 5:30 PM (Alm 1h)\nTotal: 8.5h a 9.0h ordinarias", 1000, 420, AZUL_MEDIO),
        ("SÁBADO / DOMINGO / FESTIVO\n(Personal Operativo de Patio)", 1540, 420, NARANJA_CORP),
        ("Verifica Tolerancia (10 min de gracia)\nSi llega después: Calcula Tardanza en Minutos", 750, 600, AMBAR_TARDANZA),
        ("¿Cuenta con Autorización de Jefe de Patio?\n(Solo Patio labora fines de semana)", 1540, 600, SLATE_HEADER),
        ("Marcación de SALIDA al Terminar Turno\nCálculo de Horas Netas Laboradas", 1000, 770, AZUL_ACERO),
        ("Acumulador Semanal: Suma Horas Lunes a Viernes\nObjetivo: 42 Horas Semanales (Ley 2101 / CST)", 750, 930, VERDE_EXITO),
        ("Liquidación Especial de Patio:\n• Sábado: Horas Extras Diurnas (+25%)\n• Dom/Fest: Recargo Dominical (+75%/100%)", 1540, 930, NARANJA_CORP),
        ("CONSOLIDACIÓN Y EXPORTACIÓN A EXCEL / NÓMINA (SIIGO / SAP)", 1000, 1100, AZUL_ACERO)
    ]

    f_box = get_font(13, bold=True)
    for title, cx, cy, col in steps:
        lines = title.split('\n')
        h = 32 + len(lines) * 22
        w = 380
        x1 = cx - w // 2
        y1 = cy - h // 2
        x2 = cx + w // 2
        y2 = cy + h // 2

        draw.rounded_rectangle([x1 + 3, y1 + 3, x2 + 3, y2 + 3], radius=10, fill=(203, 213, 225))
        draw.rounded_rectangle([x1, y1, x2, y2], radius=10, fill=col)

        curr_y = y1 + 14
        for l in lines:
            bbox = f_box.getbbox(l)
            tw = bbox[2] - bbox[0]
            draw.text((cx - tw // 2, curr_y), l, fill=BLANCO, font=f_box)
            curr_y += 22

    # Conexiones
    draw_arrow(draw, (1000, 205), (1000, 235), color=SLATE_HEADER)
    draw_arrow(draw, (1000, 310), (500, 370), "Lunes", color=AZUL_MEDIO)
    draw_arrow(draw, (1000, 310), (1000, 370), "Mar-Vie", color=AZUL_MEDIO)
    draw_arrow(draw, (1000, 310), (1540, 370), "Fin Semana", color=NARANJA_CORP)

    draw_arrow(draw, (500, 480), (750, 550), color=SLATE_HEADER)
    draw_arrow(draw, (1000, 480), (750, 550), color=SLATE_HEADER)
    draw_arrow(draw, (1540, 480), (1540, 550), color=NARANJA_CORP)

    draw_arrow(draw, (750, 660), (1000, 720), color=AZUL_ACERO)
    draw_arrow(draw, (1540, 660), (1000, 720), "Autorizado", color=VERDE_EXITO)

    draw_arrow(draw, (1000, 830), (750, 870), "L-V", color=VERDE_EXITO)
    draw_arrow(draw, (1000, 830), (1540, 870), "Extra Patio", color=NARANJA_CORP)

    draw_arrow(draw, (750, 1000), (1000, 1060), color=AZUL_ACERO)
    draw_arrow(draw, (1540, 1000), (1000, 1060), color=AZUL_ACERO)

    path = os.path.join(OUT_DIR, "05_Flujo_Liquidacion_Jornadas_Y_Horas_Extras.png")
    img.save(path, quality=95)
    print(f"Generado: {path}")

# =============================================================================
# 6. DIAGRAMA DE MÁQUINA DE ESTADOS DEL TRABAJADOR
# =============================================================================
def generate_diagram_06():
    img, draw = create_canvas(
        "Diagrama 06: Máquina de Estados — Ciclo de Turno del Colaborador en Planta",
        "Transiciones desde Fuera de Planta, Entrada (Puntual/Tardanza), Almuerzo, Salida y Suspensión SST (Recuperaciones Naranjo)"
    )

    states = [
        ("FUERA_DE_PLANTA\n(Estado Inicial)", 300, 300, AZUL_ACERO),
        ("MARCANDO_EN_KIOSCO\n(Digitando Cédula)", 800, 300, SLATE_HEADER),
        ("EN_PLANTA_PUNTUAL\n(Marcó dentro de tolerancia)", 1350, 220, VERDE_EXITO),
        ("EN_PLANTA_TARDANZA\n(Marcó con minutos de retraso)", 1350, 420, AMBAR_TARDANZA),
        ("EN_ALMUERZO\n(Lunes 12-1:30 / Mar-Vie 12-1)", 1350, 680, AZUL_MEDIO),
        ("JORNADA_CUMPLIDA\n(Tiempo diario completado)", 800, 680, VERDE_EXITO),
        ("ACCESO_SUSPENDIDO\n(Vencimiento ARL / Disciplinario)", 300, 680, ROJO_ALERTA),
        ("JORNADA_EXTRA_PATIO\n(Sábado / Domingo con Autorización)", 800, 980, NARANJA_CORP)
    ]

    f_st = get_font(14, bold=True)
    for title, cx, cy, col in states:
        lines = title.split('\n')
        h = 36 + len(lines) * 22
        w = 340
        x1 = cx - w // 2
        y1 = cy - h // 2
        x2 = cx + w // 2
        y2 = cy + h // 2

        draw.rounded_rectangle([x1 + 3, y1 + 3, x2 + 3, y2 + 3], radius=14, fill=(203, 213, 225))
        draw.rounded_rectangle([x1, y1, x2, y2], radius=14, fill=col, outline=AZUL_ACERO, width=2)

        curr_y = y1 + 16
        for l in lines:
            bbox = f_st.getbbox(l)
            tw = bbox[2] - bbox[0]
            draw.text((cx - tw // 2, curr_y), l, fill=BLANCO, font=f_st)
            curr_y += 22

    # Transiciones
    draw_arrow(draw, (470, 300), (630, 300), "Digita Cédula", NARANJA_CORP)
    draw_arrow(draw, (970, 280), (1180, 220), "Hora <= Tolerancia", VERDE_EXITO)
    draw_arrow(draw, (970, 320), (1180, 420), "Hora > Tolerancia", AMBAR_TARDANZA)
    draw_arrow(draw, (800, 360), (300, 610), "Credencial Suspendida", ROJO_ALERTA)

    draw_arrow(draw, (1350, 300), (1350, 610), "Llega hora almuerzo", AZUL_MEDIO)
    draw_arrow(draw, (1350, 480), (1350, 610), "Llega hora almuerzo", AZUL_MEDIO)
    draw_arrow(draw, (1180, 680), (970, 680), "Retorna de almuerzo", AZUL_MEDIO)
    draw_arrow(draw, (800, 610), (800, 360), "Marcación Salida", AZUL_ACERO)
    draw_arrow(draw, (630, 680), (300, 380), "Salida validada -> FUERA", AZUL_ACERO)

    draw_arrow(draw, (800, 750), (800, 910), "Trabajo Extraordinario Sáb/Dom", NARANJA_CORP)
    draw_arrow(draw, (630, 980), (300, 380), "Salida Fin de Semana", NARANJA_CORP)

    path = os.path.join(OUT_DIR, "06_Estados_Trabajador_Y_Ciclo_Turno.png")
    img.save(path, quality=95)
    print(f"Generado: {path}")

# =============================================================================
# 7. DIAGRAMA ENTIDAD-RELACIÓN (ERD) MODELO DE DATOS NARANJO
# =============================================================================
def generate_diagram_07():
    img, draw = create_canvas(
        "Diagrama 07: Modelo Entidad-Relación (ERD) — Base de Datos Recuperaciones Naranjo",
        "Estructura Relacional para Padrón, Horarios 42h (L-V), Marcaciones de Kiosco, Aprobaciones de Patio y Nómina"
    )

    tables = [
        ("trabajadores", [
            "PK  id : INT AUTO_INCREMENT",
            "    cedula : VARCHAR(20) UNIQUE NOT NULL",
            "    nombres : VARCHAR(100) NOT NULL",
            "    apellidos : VARCHAR(100) NOT NULL",
            "FK  cargo_id : INT NOT NULL",
            "FK  area_id : INT NOT NULL",
            "    tipo_personal : ENUM('PATIO', 'ADMIN')",
            "    estado_autorizacion : ENUM('ACTIVO','SUSP')",
            "    arl_vigente : BOOLEAN DEFAULT TRUE",
            "    foto_url : VARCHAR(255)",
            "    ubicacion_actual : ENUM('DENTRO','FUERA')",
            "    created_at : TIMESTAMP"
        ], (60, 160, 460, 520)),

        ("horarios_semana_naranjo", [
            "PK  id : INT AUTO_INCREMENT",
            "    dia_semana : ENUM('LUN','MAR','MIE','JUE','VIE','SAB','DOM')",
            "    hora_entrada : TIME NOT NULL",
            "    hora_inicio_almuerzo : TIME NOT NULL",
            "    hora_fin_almuerzo : TIME NOT NULL",
            "    hora_salida : TIME NOT NULL",
            "    horas_ordinarias : DECIMAL(4,2) NOT NULL",
            "    aplica_administracion : BOOLEAN DEFAULT TRUE",
            "    tolerancia_minutos : INT DEFAULT 10"
        ], (520, 160, 980, 480)),

        ("marcaciones_kiosco", [
            "PK  id : BIGINT AUTO_INCREMENT",
            "FK  trabajador_id : INT NOT NULL",
            "    tipo_movimiento : ENUM('ENTRADA','SALIDA')",
            "    fecha_hora : TIMESTAMP NOT NULL",
            "    minutos_tardanza : INT DEFAULT 0",
            "    es_puntual : BOOLEAN DEFAULT TRUE",
            "    origen : ENUM('KIOSCO_TACTIL','ESCANER_BARRAS','MANUAL')",
            "    modo_offline : BOOLEAN DEFAULT FALSE",
            "    dispositivo_id : VARCHAR(50)"
        ], (1040, 160, 1500, 480)),

        ("jornadas_liquidadas", [
            "PK  id : BIGINT AUTO_INCREMENT",
            "FK  trabajador_id : INT NOT NULL",
            "    fecha : DATE NOT NULL",
            "    hora_entrada_real : TIMESTAMP",
            "    hora_salida_real : TIMESTAMP",
            "    horas_ordinarias : DECIMAL(4,2)",
            "    horas_extras_diurnas_hed : DECIMAL(4,2)",
            "    horas_extras_nocturnas_hen : DECIMAL(4,2)",
            "    recargo_nocturno_rn : DECIMAL(4,2)",
            "    horas_dominical_festivo : DECIMAL(4,2)",
            "    estado_cierre : ENUM('PRELIQUIDADO','CERRADO')"
        ], (1560, 160, 1940, 520)),

        ("areas_planta_naranjo", [
            "PK  id : INT AUTO_INCREMENT",
            "    codigo : VARCHAR(30) UNIQUE",
            "    nombre : VARCHAR(100)",
            "    descripcion : TEXT",
            "    nivel_riesgo_arl : INT (1-5)",
            "    aforo_maximo : INT"
        ], (60, 600, 460, 840)),

        ("cargos_operativos", [
            "PK  id : INT AUTO_INCREMENT",
            "    nombre : VARCHAR(100)",
            "    categoria : ENUM('OPERATIVO_PATIO','SUPERVISION','ADMIN')",
            "    es_puesto_critico : BOOLEAN DEFAULT FALSE"
        ], (520, 600, 980, 820)),

        ("autorizaciones_extras_patio", [
            "PK  id : INT AUTO_INCREMENT",
            "FK  trabajador_id : INT NOT NULL",
            "FK  jefe_autorizador_id : INT NOT NULL",
            "    fecha_extra : DATE NOT NULL",
            "    dia : ENUM('SABADO','DOMINGO','FESTIVO')",
            "    motivo_justificacion : TEXT",
            "    horas_aprobadas : DECIMAL(4,2)",
            "    created_at : TIMESTAMP"
        ], (1040, 600, 1500, 860)),

        ("visitantes_camiones_chatarra", [
            "PK  id : INT AUTO_INCREMENT",
            "    cedula_conductor : VARCHAR(20)",
            "    nombre_completo : VARCHAR(120)",
            "    empresa_origen : VARCHAR(120)",
            "    placa_camion : VARCHAR(10)",
            "    gafete_asignado : VARCHAR(20)",
            "    hora_ingreso : TIMESTAMP",
            "    hora_salida : TIMESTAMP",
            "    estado : ENUM('DENTRO','SALIDA_REGISTRADA')"
        ], (1560, 600, 1940, 900))
    ]

    for title, lines, box in tables:
        draw_box(draw, box, title, lines, header_bg=AZUL_ACERO, border=NARANJA_CORP)

    # Relaciones
    draw_arrow(draw, (460, 280), (520, 280), "1:N", color=AZUL_MEDIO)
    draw_arrow(draw, (460, 360), (1040, 360), "1:N", color=AZUL_MEDIO)
    draw_arrow(draw, (460, 440), (1560, 440), "1:N", color=AZUL_MEDIO)
    draw_arrow(draw, (260, 520), (260, 600), "FK area", color=NARANJA_CORP)
    draw_arrow(draw, (460, 700), (520, 700), "FK cargo", color=NARANJA_CORP)
    draw_arrow(draw, (1270, 480), (1270, 600), "FK extra", color=VERDE_EXITO)

    path = os.path.join(OUT_DIR, "07_Modelo_Entidad_Relacion_ERD_Naranjo.png")
    img.save(path, quality=95)
    print(f"Generado: {path}")

# =============================================================================
# 8. DIAGRAMA DE DESPLIEGUE HARDWARE Y RED EN PLANTA CARTAGENA
# =============================================================================
def generate_diagram_08():
    img, draw = create_canvas(
        "Diagrama 08: Despliegue Físico de Hardware y Red — Planta Recuperaciones Naranjo",
        "Distribución de Garita Peatonal, Garita Báscula, Patio de Chatarrización y Servidor Central (Cartagena)"
    )

    zones = [
        ("ZONA 1: PORTERÍA PEATONAL (ACCESO PRINCIPAL)", (60, 150, 640, 680), [
            ("Tótem Kiosco Táctil Industrial", ["• Pantalla táctil All-in-One 19\"", "• Teclado táctil gigante para Cédula", "• Escáner láser código de barras PDF417", "• Carcasa antivandálica acero inoxidable"], (80, 220, 620, 380)),
            ("Respaldo Energético y Conectividad", ["• UPS Online 2 KVA (4h autonomía)", "• Switch PoE Industrial Gigabit", "• Alarma acústica y estroboscópica verde/roja", "• Cámara IP de seguridad cotejo facial"], (80, 430, 620, 650))
        ]),

        ("ZONA 2: GARITA VEHICULAR / BÁSCULA", (700, 150, 1280, 680), [
            ("Consola de Garita (Vigilante)", ["• PC de escritorio con monitor de 24\"", "• Monitor espejo en tiempo real de marcaciones", "• Registro de camiones, placas y gafetes", "• Visualizador de aforo de planta en vivo"], (720, 220, 1260, 380)),
            ("Control de Báscula y Barrera", ["• Interfaz con báscula de pesaje chatarra", "• Talanquera vehicular automatizada", "• Lector UHF de largo alcance (Tags camión)", "• Cámaras LPR lectura automática de placas"], (720, 430, 1260, 650))
        ]),

        ("ZONA 3: SERVIDOR LOCAL Y NUBE EMPRESARIAL", (1340, 150, 1940, 680), [
            ("Servidor On-Premise / Edge", ["• Mini Servidor industrial en rack garita", "• Node.js Backend SentinelPro IAM", "• SQLite de réplica para Modo Offline", "• Agente de sincronización en ráfaga"], (1360, 220, 1920, 380)),
            ("Nube Central y Base de Datos", ["• Servidor PostgreSQL 16 Primario", "• Copias de seguridad automáticas en la nube", "• API REST para integración con Siigo/SAP", "• Acceso HTTPS seguro con certificado SSL"], (1360, 430, 1920, 650))
        ]),

        ("ZONA 4: PATIO DE RECICLAJE Y OFICINAS ADMINISTRATIVAS", (60, 740, 1940, 1160), [
            ("Patio de Chatarra y Desintegración", ["• WiFi Industrial de largo alcance", "• Tablets Android rugerizadas para Jefes de Patio", "• Supervisión de cuadrillas en vivo a pie de máquina", "• Autorización de horas extras directamente en campo"], (80, 810, 660, 1120)),
            ("Taller de Oxicorte y Mantenimiento", ["• Botonera de parada de emergencia enlazada", "• Verificación de certificación SST antes de acceso", "• Sensor de aforo en área de alto riesgo", "• Registro de ingreso de personal de contratistas"], (720, 810, 1300, 1120)),
            ("Oficinas Administrativas y Gestión Humana", ["• PCs de administración y gerencia general", "• Generación y descarga de nómina quincenal en Excel", "• Matriz de control de ausentismo y tardanzas", "• Auditoría de seguridad y gestión de novedades"], (1360, 810, 1920, 1120))
        ])
    ]

    for title, coords, inner_boxes in zones:
        draw.rounded_rectangle([coords[0], coords[1], coords[2], coords[3]], radius=14, fill=(241, 245, 249), outline=SLATE_HEADER, width=2)
        f_z = get_font(16, bold=True)
        draw.text((coords[0] + 20, coords[1] + 16), title, fill=NARANJA_CORP, font=f_z)

        for b_title, b_lines, b_box in inner_boxes:
            draw_box(draw, b_box, b_title, b_lines, header_bg=AZUL_ACERO, border=NARANJA_CORP)

    # Conexiones de red
    draw_arrow(draw, (620, 300), (720, 300), "Red Local Ethernet", color=AZUL_MEDIO)
    draw_arrow(draw, (1260, 300), (1360, 300), "Fibra Óptica / LAN", color=AZUL_MEDIO)
    draw_arrow(draw, (1640, 380), (1640, 430), "Sincronización Cloud", color=VERDE_EXITO)
    draw_arrow(draw, (1000, 680), (1000, 810), "WiFi Industrial 5GHz", color=NARANJA_CORP)

    path = os.path.join(OUT_DIR, "08_Despliegue_Hardware_Red_Planta_Cartagena.png")
    img.save(path, quality=95)
    print(f"Generado: {path}")

def generate_all():
    print("Iniciando generación de los 8 diagramas oficiales para Recuperaciones Naranjo...")
    generate_diagram_01()
    generate_diagram_02()
    generate_diagram_03()
    generate_diagram_04()
    generate_diagram_05()
    generate_diagram_06()
    generate_diagram_07()
    generate_diagram_08()
    print("¡Todos los 8 diagramas han sido generados exitosamente!")

if __name__ == '__main__':
    generate_all()
