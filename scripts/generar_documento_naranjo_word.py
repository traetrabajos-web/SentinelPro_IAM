# -*- coding: utf-8 -*-
"""
Generador del Documento Word (.docx) Ejecutivo y Técnico:
Plan Maestro del Sistema Integral de Control de Acceso Físico, Asistencia y Aforo
para Recuperaciones Naranjo S.A.S. — Sede Cartagena de Indias.
"""
import os
import sys
import datetime
from docx import Document
from docx.shared import Pt, Cm, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DOCS_DIR = os.path.join(BASE_DIR, 'docs')
OUT_DOCX_ROOT = os.path.join(BASE_DIR, 'Plan_Sistema_Acceso_Recuperaciones_Naranjo_Cartagena.docx')
OUT_DOCX_DOCS = os.path.join(DOCS_DIR, 'Plan_Sistema_Acceso_Recuperaciones_Naranjo_Cartagena.docx')

# Paleta Corporativa Industrial / Recuperaciones Naranjo (Naranja Industrial, Azul Acero, Slate)
NARANJA_CORP = RGBColor(0xEA, 0x58, 0x0C)       # #EA580C
AZUL_ACERO = RGBColor(0x0F, 0x17, 0x2A)         # #0F172A
AZUL_MEDIO = RGBColor(0x1E, 0x40, 0xAF)         # #1E40AF
FONDO_TABLA_HEADER = RGBColor(0x1E, 0x29, 0x3B) # #1E293B
FONDO_FILA_ALT = RGBColor(0xF8, 0xFA, 0xFC)     # #F8FAFC
FONDO_CALLOUT = RGBColor(0xFF, 0xF7, 0xED)      # #FFF7ED (Naranja muy suave)
TEXTO_GRIS = RGBColor(0x33, 0x41, 0x55)         # #334155
TEXTO_MUTED = RGBColor(0x64, 0x74, 0x8B)        # #64748B
BLANCO = RGBColor(0xFF, 0xFF, 0xFF)

def set_cell_bg(cell, rgb: RGBColor):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    hex_color = '{:02X}{:02X}{:02X}'.format(rgb[0], rgb[1], rgb[2])
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)

def set_cell_borders(cell, color='CBD5E1', sz=4):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for side in ('top', 'left', 'bottom', 'right'):
        b = OxmlElement(f'w:{side}')
        b.set(qn('w:val'), 'single')
        b.set(qn('w:sz'), str(sz))
        b.set(qn('w:space'), '0')
        b.set(qn('w:color'), color)
        tcBorders.append(b)
    tcPr.append(tcBorders)

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in (('top', top), ('bottom', bottom), ('left', left), ('right', right)):
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def add_field(p, field_text):
    run = p.add_run()
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = field_text
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'separate')
    fldChar3 = OxmlElement('w:fldChar')
    fldChar3.set(qn('w:fldCharType'), 'end')
    r = run._r
    r.append(fldChar1)
    r.append(instrText)
    r.append(fldChar2)
    r.append(fldChar3)
    run.font.size = Pt(8.5)
    run.font.color.rgb = TEXTO_MUTED

def configure_header_footer(doc):
    for section in doc.sections:
        section.top_margin = Cm(2.2)
        section.bottom_margin = Cm(2.2)
        section.left_margin = Cm(2.3)
        section.right_margin = Cm(2.3)

        header = section.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("Recuperaciones Naranjo S.A.S. — Sistema de Control de Acceso, Asistencia y Portería (Cartagena)")
        hrun.font.size = Pt(8)
        hrun.font.color.rgb = TEXTO_MUTED

        footer = section.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r1 = fp.add_run("Recuperaciones Naranjo S.A.S.  |  Ingeniería de Software & Planta Industrial  |  Página ")
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = TEXTO_MUTED
        add_field(fp, "PAGE")
        r2 = fp.add_run(" de ")
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = TEXTO_MUTED
        add_field(fp, "NUMPAGES")

def add_hr(doc, color='EA580C', sz=12):
    p = doc.add_paragraph()
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), str(sz))
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), color)
    pBdr.append(bottom)
    pPr.append(pBdr)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(8)

def add_h1(doc, text):
    p = doc.add_heading(level=1)
    run = p.add_run(text)
    run.font.name = 'Segoe UI'
    run.font.size = Pt(15.5)
    run.font.bold = True
    run.font.color.rgb = AZUL_ACERO
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(4)
    add_hr(doc, 'EA580C', 14)

def add_h2(doc, text):
    p = doc.add_heading(level=2)
    run = p.add_run(text)
    run.font.name = 'Segoe UI'
    run.font.size = Pt(12)
    run.font.bold = True
    run.font.color.rgb = NARANJA_CORP
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)

def add_h3(doc, text):
    p = doc.add_heading(level=3)
    run = p.add_run(text)
    run.font.name = 'Segoe UI'
    run.font.size = Pt(10.5)
    run.font.bold = True
    run.font.color.rgb = AZUL_MEDIO
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)

def add_p(doc, text, bold_prefix=None):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        rb = p.add_run(bold_prefix)
        rb.font.name = 'Segoe UI'
        rb.font.size = Pt(9.5)
        rb.font.bold = True
        rb.font.color.rgb = AZUL_ACERO
    r = p.add_run(text)
    r.font.name = 'Segoe UI'
    r.font.size = Pt(9.5)
    r.font.color.rgb = TEXTO_GRIS
    return p

def add_bullet(doc, bold_lead, text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(3)
    rb = p.add_run(bold_lead)
    rb.font.name = 'Segoe UI'
    rb.font.size = Pt(9)
    rb.font.bold = True
    rb.font.color.rgb = AZUL_ACERO
    r = p.add_run(text)
    r.font.name = 'Segoe UI'
    r.font.size = Pt(9)
    r.font.color.rgb = TEXTO_GRIS

def add_callout(doc, title, text, border_color='EA580C', bg_color=FONDO_CALLOUT):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_bg(cell, bg_color)
    
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    
    left = OxmlElement('w:left')
    left.set(qn('w:val'), 'single')
    left.set(qn('w:sz'), '24')
    left.set(qn('w:space'), '0')
    left.set(qn('w:color'), border_color)
    tcBorders.append(left)
    
    for side in ('top', 'bottom', 'right'):
        b = OxmlElement(f'w:{side}')
        b.set(qn('w:val'), 'none')
        tcBorders.append(b)
    tcPr.append(tcBorders)
    set_cell_margins(cell, 90, 90, 140, 140)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    rt = p.add_run(f"📌 {title}\n")
    rt.font.name = 'Segoe UI'
    rt.font.size = Pt(9.5)
    rt.font.bold = True
    rt.font.color.rgb = AZUL_ACERO

    rc = p.add_run(text)
    rc.font.name = 'Segoe UI'
    rc.font.size = Pt(9)
    rc.font.color.rgb = TEXTO_GRIS

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_styled_table(doc, headers, rows):
    tbl = doc.add_table(rows=len(rows) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER

    hdr_cells = tbl.rows[0].cells
    for i, h_text in enumerate(headers):
        set_cell_bg(hdr_cells[i], FONDO_TABLA_HEADER)
        set_cell_borders(hdr_cells[i], '334155', 6)
        set_cell_margins(hdr_cells[i], 90, 90, 110, 110)
        p = hdr_cells[i].paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(str(h_text))
        run.font.name = 'Segoe UI'
        run.font.size = Pt(9)
        run.font.bold = True
        run.font.color.rgb = BLANCO

    for r_idx, row_data in enumerate(rows):
        row_cells = tbl.rows[r_idx + 1].cells
        bg = FONDO_FILA_ALT if r_idx % 2 == 1 else BLANCO
        for c_idx, val in enumerate(row_data):
            set_cell_bg(row_cells[c_idx], bg)
            set_cell_borders(row_cells[c_idx], 'CBD5E1', 4)
            set_cell_margins(row_cells[c_idx], 80, 80, 100, 100)
            p = row_cells[c_idx].paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            run = p.add_run(str(val))
            run.font.name = 'Segoe UI'
            run.font.size = Pt(8.5)
            if c_idx == 0:
                run.font.bold = True
                run.font.color.rgb = AZUL_ACERO
            else:
                run.font.color.rgb = TEXTO_GRIS

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def build_naranjo_document():
    doc = Document()
    configure_header_footer(doc)

    # PORTADA
    p_top = doc.add_paragraph()
    p_top.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_top.paragraph_format.space_before = Pt(36)
    r_badge = p_top.add_run("PLAN MAESTRO DE TRANSFORMACIÓN & INGENIERÍA DE SOFTWARE")
    r_badge.font.name = 'Segoe UI'
    r_badge.font.size = Pt(10)
    r_badge.font.bold = True
    r_badge.font.color.rgb = NARANJA_CORP

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(16)
    r_title = p_title.add_run("SISTEMA INTEGRAL DE CONTROL DE ACCESO, ASISTENCIA Y PORTERÍA INDUSTRIAL\nRECUPERACIONES NARANJO S.A.S.")
    r_title.font.name = 'Segoe UI'
    r_title.font.size = Pt(20)
    r_title.font.bold = True
    r_title.font.color.rgb = AZUL_ACERO

    add_hr(doc, 'EA580C', 20)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(6)
    p_sub.paragraph_format.space_after = Pt(20)
    r_sub = p_sub.add_run(
        "Sede Industrial Cartagena de Indias (Bolívar, Colombia) — Solución personalizada para el control ágil de ingreso "
        "y salida de operarios mediante Cédula de Ciudadanía en Pantalla Kiosco Táctil, Monitoreo en Vivo de Cuadrilla para Jefes "
        "de Patio, Pre-Liquidación Automática de Jornadas y Recargos según el Código Sustantivo del Trabajo de Colombia, "
        "Gestión de Visitantes/Contratistas y Modo Garita Offline-First."
    )
    r_sub.font.name = 'Segoe UI'
    r_sub.font.size = Pt(10)
    r_sub.font.color.rgb = TEXTO_GRIS

    add_styled_table(doc, ["Parámetro Institucional", "Detalle de Implementación"], [
        ["Empresa Beneficiaria", "Recuperaciones Naranjo S.A.S."],
        ["Ubicación de Operaciones", "Cartagena de Indias, Bolívar, Colombia (Zona Industrial)"],
        ["Rubro Operativo", "Reciclaje de Metales, Chatarrización, Desintegración Vehicular y Disposición Final"],
        ["Población Usuaria", "Operarios de Patio, Oxigenistas, Choferes de Grúa/Tractomula, Supervisores, Vigilancia y Personal Administrativo"],
        ["Mecanismo Principal de Fichaje", "Digitación de Cédula de Ciudadanía en Kiosco Táctil Industrial + Lector de Código de Barras / QR"],
        ["Lógica de Cálculo Laboral", "Legislación Laboral Colombiana (CST): Horas Ordinarias, Extras Diurnas (25%), Extras Nocturnas (75%), Recargos Nocturnos (35%) y Festivos"],
        ["Monitoreo para Jefes de Área", "Tablero Móvil y Web en Vivo (Presentes, Tardanzas, Ausentes, Horas trabajadas en el día)"],
        ["Continuidad de Servicio", "Arquitectura Garita Offline-First con base de datos local SQLite y respaldo de energía UPS"],
        ["Fecha de Formulación", datetime.date.today().strftime("%d de %B de %Y")]
    ])

    doc.add_page_break()

    # CAPÍTULO 1
    add_h1(doc, "1. Visión del Proyecto y Contexto Operativo en Cartagena")
    add_p(doc, 
        "Recuperaciones Naranjo S.A.S. es una empresa líder en la recuperación ambiental de metales ferrosos y no ferrosos, "
        "chatarrización pesada y desintegración vehicular en Cartagena de Indias. Las instalaciones de la planta industrial "
        "combinan el ingreso continuo de vehículos de carga pesada (tractomulas, camiones recolectores) con el flujo de "
        "personal operativo en turnos diurnos, mixtos y nocturnos. Implementar un sistema de control de acceso integral "
        "responde a tres necesidades críticas: exactitud en el control de asistencia para la nómina, supervisión en tiempo real "
        "por parte de los jefes de cuadrilla y cumplimiento estricto de los estándares de Seguridad y Salud en el Trabajo (SST/ARL)."
    )

    add_callout(doc, "Objetivo Central de la Solución", 
        "Garantizar que todo operario y colaborador que ingrese a las instalaciones de Recuperaciones Naranjo en Cartagena "
        "registre su entrada y salida en menos de 1 segundo mediante su Cédula de Ciudadanía en una pantalla táctil industrial, "
        "calculando al instante su puntualidad, informando en tiempo real al jefe de área sobre la disponibilidad de su equipo "
        "y suministrando al Administrador/Gestión Humana un consolidado exacto de horas extras y recargos para nómina.",
        border_color='EA580C'
    )

    # CAPÍTULO 2
    add_h1(doc, "2. El Kiosco de Garita: Experiencia del Trabajador con Cédula")
    add_p(doc, 
        "En la portería peatonal se ubicará una pantalla táctil industrial (All-in-One de 15 a 21 pulgadas) empotrada a la pared "
        "o instalada en tótem metálico. La interfaz estará diseñada con una estética de alto impacto y usabilidad intuitiva:"
    )

    add_h2(doc, "Flujo Paso a Paso de Marcación en Kiosco")
    add_bullet(doc, "1. Pantalla de Bienvenida con Teclado Numérico Gigante: ", 
        "Botones táctiles grandes (80x80 px) que permiten al operario marcar cómodamente su número de Cédula de Ciudadanía, incluso portando guantes de protección.")
    add_bullet(doc, "2. Opción de Lectura Automática (Escáner Código de Barras): ", 
        "El trabajador puede simplemente acercar la parte posterior de su cédula colombiana física (código de barras bidimensional PDF417) o el carnet corporativo al lector láser para un fichaje instantáneo en 300 ms sin necesidad de digitar.")
    add_bullet(doc, "3. Verificación Instantánea en el Backend: ", 
        "El sistema valida en microsegundos: a) Estado de la credencial (ACTIVA / SUSPENDIDA), b) Vigencia de ARL y examen médico periódico, c) Turno asignado y horario de inicio.")
    add_bullet(doc, "4. Pantalla de Confirmación con Foto y Datos: ", 
        "Muestra en pantalla la fotografía del colaborador, nombre completo, cargo (ej. 'Operario de Desintegración Vehicular'), área ('Patio de Chatarra'), hora exacta y estatus de puntualidad ('ENTRADA REGISTRADA — A TIEMPO' o 'TARDANZA DE 14 MINUTOS').")
    add_bullet(doc, "5. Retroalimentación Acústica de Alta Claridad: ", 
        "Un sonido agudo y claro confirma el acceso exitoso; un doble tono grave advierte si la persona tiene el ingreso suspendido o si intenta una marcación errónea.")
    add_bullet(doc, "6. Registro de Salida y Jornada Cumplida: ", 
        "Al finalizar el turno, el trabajador vuelve a digitar su cédula; el sistema detecta que se encuentra dentro de planta, registra la SALIDA y le muestra un resumen cordial: '¡Buen descanso, Roberto! Jornada cumplida: 8 horas 22 minutos'.")

    # CAPÍTULO 3
    add_h1(doc, "3. Portal del Jefe de Área / Supervisor de Patio en Tiempo Real")
    add_p(doc, 
        "Uno de los mayores dolores de cabeza en operaciones de patio es saber si la cuadrilla completa está disponible antes "
        "de iniciar labores críticas como el oxicorte, la operación de grúas o el despiece vehicular. El Jefe de Área contará "
        "con una vista exclusiva, accesible desde su teléfono celular, tablet o computador de oficina:"
    )

    add_styled_table(doc, ["Funcionalidad del Jefe", "Detalle Técnico y Operativo", "Beneficio para Recuperaciones Naranjo"], [
        ["Tablero 'Mi Cuadrilla en Vivo'", "Muestra en tiempo real: Trabajadores asignados al área, Total presentes en planta, Total ausentes y Tardanzas acumuladas.", "Permite reasignar labores o convocar relevos inmediatamente al inicio del turno."],
        ["Semáforo de Asistencia por Operario", "Verde: Presente y a tiempo. Amarillo: Llegó con tardanza (indica minutos). Rojo: Ausente sin justificar.", "Visibilidad visual instantánea del compromiso laboral del equipo de trabajo."],
        ["Alertas Tempranas en Celular", "Notificación push o WhatsApp si faltan cargos críticos (ej. Operador de Báscula o Chofer de Retroexcavadora) tras 15 min de iniciado el turno.", "Evita paradas operativas en patio por falta de personal clave."],
        ["Aprobación de Horas Extras en Campo", "El jefe puede autorizar desde su móvil la extensión de jornada de un operario cuando se requiere terminar una carga o corte urgente.", "Control estricto de horas extras, evitando pagos no justificados en nómina."],
        ["Historial de Asistencia y Puntualidad", "Consulta por trabajador de los últimos 30 días con gráficos de puntualidad, días laborados y tiempos promedio de estancia.", "Herramienta objetiva para evaluaciones de desempeño y bonificaciones."]
    ])

    # CAPÍTULO 4
    add_h1(doc, "4. Panel del Administrador General y Gestión Humana (Nómina)")
    add_p(doc, 
        "El Administrador General y el equipo de Gestión Humana poseen el control estratégico de la plataforma, "
        "con herramientas diseñadas para simplificar la gestión laboral y nómina bajo las leyes de Colombia:"
    )

    add_h2(doc, "Capacidades de Gestión y Nómina")
    add_bullet(doc, "1. Padrón Centralizado de Colaboradores: ", 
        "Ficha integral de cada trabajador con Cédula, Nombres, Cargo, Departamento (Patio de Chatarra, Desintegración, Mantenimiento, Báscula, Administración), EPS, ARL, Turno asignado y Foto.")
    add_bullet(doc, "2. Configuración Flexible de Turnos Industriales: ", 
        "Definición de turnos rotativos (Mañana 06:00-14:00, Tarde 14:00-22:00, Noche 22:00-06:00 o Administrativo 07:00-17:00 con 1 hora de almuerzo) y margen de tolerancia (ej. 10 minutos).")
    add_bullet(doc, "3. Motor de Pre-Liquidación según el Código Sustantivo del Trabajo (Colombia): ", 
        "Cálculo automático y desglosado para cada corte de nómina (quincenal o mensual): Horas Ordinarias, Horas Extras Diurnas (HED +25%), Horas Extras Nocturnas (HEN +75%), Recargo Nocturno (RN +35% de 21:00 a 06:00), y Horas Dominicales/Festivas ordinarias y con recargo.")
    add_bullet(doc, "4. Exportación Compatible con Softwares de Nómina en Colombia: ", 
        "Descarga en un clic de archivos Excel (.xlsx) y CSV formateados para importar en Siigo, World Office, Novasoft, Helisa o SAP.")
    add_bullet(doc, "5. Módulo de Novedades y Justificaciones: ", 
        "Registro y archivo de incapacidades médicas expedidas por la EPS, permisos remunerados/no remunerados, vacaciones y sanciones disciplinarias.")
    add_bullet(doc, "6. Bitácora de Auditoría Inmutable: ", 
        "Registro de cada acción administrativa (quién autorizó una excepción, quién modificó un turno o quién desbloqueó un acceso) con fecha, hora e IP.")

    # CAPÍTULO 5
    add_h1(doc, "5. Consola del Vigilante de Garita y Control de Visitantes")
    add_p(doc, 
        "El vigilante de turno en la portería de Recuperaciones Naranjo cuenta con una pantalla de monitoreo auxiliar para apoyar la seguridad física:"
    )
    add_styled_table(doc, ["Módulo de Garita", "Acción del Vigilante", "Impacto en Seguridad de Planta"], [
        ["Monitor Espejo de Marcaciones", "Al marcar un operario en el Kiosco, el monitor del vigilante muestra la foto oficial en grande para cotejo visual.", "Evita que un trabajador digite la cédula de otro compañero ausente."],
        ["Control de Visitantes y Proveedores", "Registro de transportistas de chatarra, clientes mayoristas, talleres o inspectores de tránsito con cédula y empresa de origen.", "Control de gafete temporal y asignación del anfitrión responsable dentro de planta."],
        ["Salida y Recuperación de Gafetes", "Fichaje obligatorio de la salida del visitante y liberación del gafete físico.", "Cero visitantes perdidos dentro de las instalaciones industriales."],
        ["Contador de Aforo en Vivo de Planta", "Muestra en tiempo real cuántas personas (operarios + administrativos + visitantes) se encuentran adentro.", "Vital para planes de evacuación de emergencia y visitas de Bomberos/Cardique."]
    ])

    # CAPÍTULO 6
    add_h1(doc, "6. Resiliencia Operativa: Garita Offline-First ante Cortes de Red")
    add_p(doc, 
        "En la zona industrial de Cartagena pueden presentarse fluctuaciones eléctricas o caídas temporales del enlace de fibra óptica. "
        "El sistema estará blindado bajo una arquitectura Offline-First:"
    )
    add_bullet(doc, "• Base de Datos Local en el Kiosco (SQLite): ", "El terminal de garita almacena localmente una réplica cifrada de las cédulas autorizadas y turnos.")
    add_bullet(doc, "• Marcación sin Interrupciones en Modo Offline: ", "Si se interrumpe la conexión con el servidor central, el Kiosco pasa automáticamente a 'Modo Local'. Los operarios siguen marcando cédula y el acceso se concede con normalidad.")
    add_bullet(doc, "• Sincronización Automática al Restaurarse la Red: ", "Cuando se reanuda el enlace, los registros encolados con su hora exacta se sincronizan hacia la base central sin intervención humana.")
    add_bullet(doc, "• Respaldo con UPS: ", "El Kiosco y la red de garita estarán respaldados por un sistema de alimentación ininterrumpida (UPS) de al menos 4 horas de autonomía.")

    # CAPÍTULO 7
    add_h1(doc, "7. Cronograma de Implementación Propuesto (4 Semanas)")
    add_styled_table(doc, ["Semana / Fase", "Hitos de Desarrollo e Implementación", "Entregables Tangibles"], [
        ["Semana 1: Identidad y Padrón Naranjo", "• Personalización de marca (logos, colores naranja/acero, textos Recuperaciones Naranjo Cartagena).\n• Carga del padrón inicial de trabajadores con cédulas colombianas.\n• Configuración de turnos de planta.", "Sistema parametrizado con los datos reales de Recuperaciones Naranjo."],
        ["Semana 2: Kiosco Táctil con Cédula", "• Desarrollo de la interfaz táctil con teclado numérico gigante.\n• Integración de sonidos de aprobación y alerta.\n• Algoritmo de cálculo de puntualidad y anti-passback en tiempo real.", "Kiosco táctil operativo para pruebas en portería."],
        ["Semana 3: Portal del Jefe y Nómina Colombia", "• Construcción del portal 'Mi Cuadrilla en Vivo' para supervisores de patio.\n• Motor de cálculo de horas extras diurnas, nocturnas y festivos colombianos.\n• Exportador a Excel para el departamento contable.", "Dashboard de supervisores y reportes de nómina activos."],
        ["Semana 4: Pruebas Piloto y Despliegue en Planta", "• Instalación del Kiosco en la garita de Cartagena.\n• Capacitación de 1 hora al personal de vigilancia.\n• Marcha blanca y salida a producción oficial.", "Planta de Cartagena operando con control de acceso sistematizado."]
    ])

    # CAPÍTULO 8
    add_h1(doc, "8. Conclusiones y Próximos Pasos")
    add_p(doc, 
        "La adaptación de SentinelPro IAM a la realidad operativa de Recuperaciones Naranjo S.A.S. en Cartagena de Indias "
        "transformará la gestión del talento humano y la seguridad de la planta. Se eliminarán los registros manuales en papel, "
        "se obtendrá precisión al minuto en el pago de jornadas y horas extras, y los directores de patio dispondrán de una "
        "herramienta tecnológica de primer nivel para dirigir sus cuadrillas. El sistema es escalable, modular y 100% propietario."
    )

    doc.save(OUT_DOCX_ROOT)
    doc.save(OUT_DOCX_DOCS)
    print(f"Documento Naranjo Word generado exitosamente en:\n1. {OUT_DOCX_ROOT}\n2. {OUT_DOCX_DOCS}")

if __name__ == '__main__':
    build_naranjo_document()
