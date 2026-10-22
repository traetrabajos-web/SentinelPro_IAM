# 🛡️ SentinelPro Access & IAM — Suite Empresarial de Control de Acceso Físico y Gestión de Identidades

> **Sistema Empresarial Integral:** Control de acceso físico en portería y garita, registro de entradas y salidas de trabajadores mediante DNI / Tarjetas RFID (`EMP-XXX`), terminal Kiosco de autoservicio, cálculo automático de jornadas y tardanzas, control de visitantes con asignación de gafetes temporales, zonificación de áreas físicas y **motor de autorización híbrido** (RBAC + Permisos Individuales `ALLOW` / `DENY` con precedencia estricta en Backend).

---

## ⚡ Cómo Iniciar el Sistema en 1 Clic

1. Haz doble clic sobre [`iniciar-sistema.bat`](./iniciar-sistema.bat) (o ejecuta en consola `node server/server.js`).
2. Se abrirá automáticamente en tu navegador:
   - 🌐 **Portal Corporativo, Kiosco y Panel Administrativo:** `http://localhost:3450`
   - 📐 **Visor Interactivo de Diagramas y Documentación:** `http://localhost:3450/documentacion` (o haz doble clic en [`abrir-documentacion.bat`](./abrir-documentacion.bat)).
3. Para ejecutar la suite automatizada de pruebas QA (15 casos de prueba al 100%):
   ```bash
   node scripts/qa-test-suite.js
   ```

---

## 🔐 Credenciales de Acceso al Panel de Seguridad e IAM

*(Cuentas preconfiguradas para pruebas y demostraciones operativas)*:

| Rol | Correo Electrónico | Contraseña | Alcance Operativo y Permisos |
|---|---|---|---|
| **👑 Super Administrador General** | `admin@sentinelpro.com` | `admin123` | Control total: Planta, Portería, RR.HH., Zonas, Configuración y Administración de Seguridad IAM (18/18 permisos). |
| **🛡️ Vigilante de Portería / Garita** | `vigilante@sentinelpro.com` | `vigi123` | Consola de garita, fichaje de entradas/salidas, control de aforo en vivo, registro y salida de visitantes con gafetes. |
| **👥 Supervisor de RR.HH.** | `rrhh@sentinelpro.com` | `rrhh123` | Padrón de trabajadores, emisión de credenciales, turnos, consulta y exportación de historiales de asistencia. |
| **🔒 Administrador de Seguridad IAM** | `seguridad@sentinelpro.com` | `segu123` | Auditoría de usuarios, asignación de roles y concesión de permisos individuales (`ALLOW`/`DENY`). |

---

## 📚 Documentación Técnica y Planes Estratégicos

### 📄 Documentos Word Oficiales (.docx)
1. **[📘 Plan Maestro de Evolución Tecnológica y Recomendaciones de Ingeniería (`.docx`)](./Documentacion_Plan_Estrategico_Y_Recomendaciones.docx)**  
   *Diagnóstico del sistema, mitigación de cuellos de botella, migración a PostgreSQL 16 y Redis, autenticación MFA (TOTP), tokens OAuth2 con cookies HttpOnly, integración de hardware OSDP/RFID en torniquetes, arquitectura de Garita Offline-First con SQLite, Dockerización y Roadmap a 30, 60, 90 y 180 días.*
2. **[📗 Documentación Completa y Especificación SRS SentinelPro IAM (`.docx`)](./Documentacion_Completa_SentinelPro_IAM.docx)**  
   *Especificación IEEE 830, catálogo de 18 permisos granulares, arquitectura de capas y los 8 diagramas UML de alta resolución.*

### 📑 Guías en Markdown (`docs/`)
| # | Documento | Descripción |
|---|---|---|
| **01** | [`docs/01_SRS_Especificacion_Requisitos.md`](./docs/01_SRS_Especificacion_Requisitos.md) | Especificación IEEE 830: Actores, 20 Requisitos Funcionales (`RF-01..20`), RNF y Reglas de Negocio. |
| **02** | [`docs/02_Diagramas_Casos_De_Uso.md`](./docs/02_Diagramas_Casos_De_Uso.md) | Diagramas UML de Casos de Uso (General, Portería, RR.HH. y Seguridad IAM). |
| **03** | [`docs/03_Arquitectura_Y_Base_De_Datos.md`](./docs/03_Arquitectura_Y_Base_De_Datos.md) | Arquitectura en Capas, Diagrama Entidad-Relación (`ERD`) y Diccionario de Datos Relacional. |
| **04** | [`docs/04_Diagramas_Flujo_Secuencia_Estados.md`](./docs/04_Diagramas_Flujo_Secuencia_Estados.md) | Diagramas de Secuencia (Autenticación, Autorización), Flujo de Acceso y Estados de Sesión. |
| **05** | [`docs/05_Arquitectura_UI_UX_Y_Modulos.md`](./docs/05_Arquitectura_UI_UX_Y_Modulos.md) | Mapa de Navegación, Wireframes de Portería, Kiosco, Endpoints API REST y Diseño Visual. |
| **06** | [`docs/06_Manual_Usuario_Y_Administrador.md`](./docs/06_Manual_Usuario_Y_Administrador.md) | Manual de Operación para el Vigilante de Garita y para el Administrador de Seguridad IAM. |
| **07** | [`docs/07_Plan_Pruebas_Y_Validacion_QA.md`](./docs/07_Plan_Pruebas_Y_Validacion_QA.md) | Matriz de Trazabilidad y 15 Casos de Prueba Funcionales y de Seguridad Criptográfica. |
| **08** | [`docs/08_Plan_Estrategico_Recomendaciones_Y_Roadmap.md`](./docs/08_Plan_Estrategico_Recomendaciones_Y_Roadmap.md) | **Plan Estratégico y Roadmap Tecnológico (Fases 30, 60, 90 y 180 días)** con matriz de riesgos. |
| **🖥️** | [`docs/VISOR_DOCUMENTACION.html`](./docs/VISOR_DOCUMENTACION.html) | **Visor Interactivo en Navegador** con todos los diagramas y manuales integrados. |

---

## 🏗️ Estructura del Repositorio

```text
G:\PROGRAMAS\SentinelPro_IAM\
│
├── iniciar-sistema.bat                                  # Lanzador del servidor + navegador web
├── abrir-documentacion.bat                              # Abre el visor interactivo de documentación
├── package.json                                         # Configuración del proyecto Node.js y scripts
├── README.md                                            # Documentación principal del repositorio
├── .gitignore                                           # Exclusiones seguras de control de versiones
├── Documentacion_Plan_Estrategico_Y_Recomendaciones.docx # Plan maestro de mejoras y recomendaciones (Word)
├── Documentacion_Completa_SentinelPro_IAM.docx          # Especificación y manual completo (Word)
│
├── docs\                                                # Documentación técnica, manuales y diagramas
│   ├── 01_SRS_Especificacion_Requisitos.md
│   ├── 02_Diagramas_Casos_De_Uso.md
│   ├── 03_Arquitectura_Y_Base_De_Datos.md
│   ├── 04_Diagramas_Flujo_Secuencia_Estados.md
│   ├── 05_Arquitectura_UI_UX_Y_Modulos.md
│   ├── 06_Manual_Usuario_Y_Administrador.md
│   ├── 07_Plan_Pruebas_Y_Validacion_QA.md
│   ├── 08_Plan_Estrategico_Recomendaciones_Y_Roadmap.md  # Plan estratégico y recomendaciones (MD)
│   ├── Documentacion_Plan_Estrategico_Y_Recomendaciones.docx
│   ├── Documentacion_Completa_SentinelPro_IAM.docx
│   ├── VISOR_DOCUMENTACION.html                         # Visor interactivo web
│   └── diagramas_png\                                   # 8 diagramas UML en alta resolución PNG
│
├── database\                                            # Capa de Persistencia y Modelado
│   ├── schema.sql                                       # Esquema relacional SQL completo y seeds
│   ├── sentinelpro_iam.sql                              # Script relacional SQL alternativo
│   └── db.json                                          # Base de datos JSON activa para entorno local
│
├── server\                                              # Backend API REST, Seguridad y Criptografía
│   ├── server.js                                        # Servidor HTTP nativo, endpoints y lógica de planta
│   ├── security.js                                      # scrypt, HMAC-SHA256, matriz RBAC + Overrides
│   └── presets.js                                       # Datos semilla (Planta industrial, empleados, zonas)
│
├── public\                                              # Frontend SPA (Consola Garita, Kiosco, Admin)
│   ├── index.html                                       # Interfaz web unificada con pestañas dinámicas
│   ├── styles.css                                       # Estilos corporativos y responsive design
│   └── app.js                                           # Lógica de interfaz de usuario y llamadas API
│
└── scripts\                                             # Herramientas de automatización y QA
    ├── qa-test-suite.js                                 # Suite de 15 pruebas automatizadas (100% aprobadas)
    ├── test-sql-syntax.js                               # Validador de sintaxis SQL
    ├── generar_documento_word.py                        # Generador de documentación general Word
    ├── generar_documento_recomendaciones_word.py        # Generador del documento de recomendaciones Word
    └── generar_diagramas_png.py                         # Generador de diagramas de alta resolución
```

---

## 🧪 Validación de Calidad y Pruebas Automatizadas

Para certificar el correcto funcionamiento de todos los mecanismos de seguridad, aforo y concurrencia:

```bash
npm test
# o directamente:
node scripts/qa-test-suite.js
```

**Resultado actual:**
```text
======================================================================
📊 REPORTE FINAL: 15 APROBADOS / 0 FALLIDOS
🎉 TODAS LAS PRUEBAS (15/15) PASARON CON ÉXITO AL 100%
======================================================================
```
