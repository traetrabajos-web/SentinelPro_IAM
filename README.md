# 📅 Sist_Reservas_Citas (ReservaPro) — Sistema Web + Panel Administrativo Multi-Rubro

> **Producto Listo para Venta (White-Label / Multi-Nicho):** Sistema completo que integra una **Página Web Pública de Reservas 24/7** y un **Panel Administrativo (Dashboard, Agenda, Caja, Liquidación Automática de Comisiones y CRM)** adaptable en 1 clic a **Barberías, Clínicas Dentales, Consultorios Médicos, Spas/Estéticas y Veterinarias**.

---

## ⚡ Cómo Iniciar el Sistema en 1 Clic

1. Haz doble clic sobre [`iniciar-sistema.bat`](./iniciar-sistema.bat) (o ejecuta en consola `node server/server.js`).
2. Se abrirá automáticamente en tu navegador:
   - 🌐 **Portal Web Público + Panel Admin:** `http://localhost:3450`
   - 📐 **Visor Interactivo de Diagramas UML:** `http://localhost:3450/documentacion` (o haz doble clic en [`abrir-documentacion.bat`](./abrir-documentacion.bat)).
3. Para ejecutar la suite automatizada de pruebas QA (12 casos de prueba):
   ```bash
   node scripts/qa-test-suite.js
   ```

---

## 🔐 Credenciales de Acceso al Panel Administrativo

*(También cuentas con botones de acceso rápido de 1 clic en la pantalla de Login para tus demostraciones de venta)*:

| Rol | Correo | Contraseña | Permisos |
|---|---|---|---|
| **👨‍💼 Administrador / Dueño** | `admin@reservapro.com` | `admin123` | Acceso total (Dashboard, Agenda, Caja, Comisiones, CRM, Catálogo, Personal, Reseñas y Marca White-Label). |
| **🛎️ Recepcionista / Caja** | `recepcion@reservapro.com` | `recep123` | Gestión operativa de agenda, citas manuales (*Walk-in*), *Check-in*, cobros en Caja y CRM. |
| **💇‍♂️ Profesional / Especialista** | `mateo@reservapro.com` | `prof123` | Visualización de su propia agenda, inicio de atención y consulta de comisiones. |

---

## 📂 Documentación Completa de Ingeniería de Software (`docs/`)

| # | Archivo | Descripción |
|---|---|---|
| **01** | [`docs/01_SRS_Especificacion_Requisitos.md`](./docs/01_SRS_Especificacion_Requisitos.md) | Especificación IEEE 830: Actores, 20 Requisitos Funcionales (`RF-01..20`), No Funcionales (`RNF`) y Reglas de Negocio (`RN-01..05`). |
| **02** | [`docs/02_Diagramas_Casos_De_Uso.md`](./docs/02_Diagramas_Casos_De_Uso.md) | Diagramas UML de Casos de Uso (General, Web Pública, Panel Admin) y Fichas Técnicas detalladas. |
| **03** | [`docs/03_Arquitectura_Y_Base_De_Datos.md`](./docs/03_Arquitectura_Y_Base_De_Datos.md) | Arquitectura en Capas, Diagrama Entidad-Relación (`ERD`) de 12 tablas y Diccionario de Datos. |
| **04** | [`docs/04_Diagramas_Flujo_Secuencia_Estados.md`](./docs/04_Diagramas_Flujo_Secuencia_Estados.md) | 3 Diagramas de Secuencia, Máquina de Estados de la Cita y Algoritmo Anti-Solapamiento (`SlotEngine`). |
| **05** | [`docs/05_Arquitectura_UI_UX_Y_Modulos.md`](./docs/05_Arquitectura_UI_UX_Y_Modulos.md) | Mapa de Navegación (Sitemap), Wireframes, Endpoints API y Estrategia Comercial de Venta. |
| **06** | [`docs/06_Manual_Usuario_Y_Administrador.md`](./docs/06_Manual_Usuario_Y_Administrador.md) | Manual paso a paso para el Cliente Web y para el Administrador/Recepcionista. |
| **07** | [`docs/07_Plan_Pruebas_Y_Validacion_QA.md`](./docs/07_Plan_Pruebas_Y_Validacion_QA.md) | Matriz de Trazabilidad y 12 Casos de Prueba Funcionales (`CP-01` a `CP-12`). |
| **🖥️** | [`docs/VISOR_DOCUMENTACION.html`](./docs/VISOR_DOCUMENTACION.html) | **Visor Interactivo en Navegador** con todos los diagramas UML renderizados. |

---

## 🏗️ Estructura Completa Construida

```text
G:\PROGRAMAS\Sist_Reservas_Citas\
│
├── iniciar-sistema.bat                # Lanzador rápido del servidor + navegador
├── abrir-documentacion.bat            # Abre el visor gráfico de diagramas UML
├── package.json                       # Configuración Node.js y scripts
├── README.md                          # Guía maestra del proyecto
│
├── docs\                              # Ingeniería de Software y Manuales (7 docs + Visor HTML)
│   ├── 01_SRS_Especificacion_Requisitos.md
│   ├── 02_Diagramas_Casos_De_Uso.md
│   ├── 03_Arquitectura_Y_Base_De_Datos.md
│   ├── 04_Diagramas_Flujo_Secuencia_Estados.md
│   ├── 05_Arquitectura_UI_UX_Y_Modulos.md
│   ├── 06_Manual_Usuario_Y_Administrador.md
│   ├── 07_Plan_Pruebas_Y_Validacion_QA.md
│   └── VISOR_DOCUMENTACION.html
│
├── database\                          # Capa de Datos
│   ├── schema.sql                     # Esquema relacional SQL (12 tablas)
│   └── db.json                        # Base de datos persistente activa
│
├── server\                            # Backend API REST y Lógica de Negocio
│   ├── server.js                      # Servidor HTTP, SlotEngine, Caja/Comisiones y CRM
│   └── presets.js                     # 4 Plantillas Comerciales (Barbería, Dental, Spa, Vet)
│
├── public\                            # Frontend Responsivo (Web Pública + Panel Admin)
│   ├── index.html                     # Interfaz unificada Web + Dashboard + Modales
│   ├── styles.css                     # Diseño moderno con tema dinámico White-Label
│   └── app.js                         # Lógica interactiva del cliente y administrador
│
└── scripts\
    └── qa-test-suite.js               # Suite automatizada de validación QA (CP-01 a CP-12)
```
