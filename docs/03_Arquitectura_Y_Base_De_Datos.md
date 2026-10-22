# 03. Arquitectura del Sistema y Diseño de Base de Datos (ERD)

Este documento describe la arquitectura tecnológica en capas del sistema **ReservaPro (`Sist_Reservas_Citas`)**, el **Diagrama Entidad-Relación (ERD)** y el **Diccionario de Datos** completo.

---

## 1. Diagrama de Arquitectura de Software (En Capas)

El sistema separa claramente el **Portal Web Público** del **Panel Administrativo**, ambos consumiendo una capa de lógica de negocio centralizada que garantiza que ninguna reserva se duplique y que los cambios en el panel se reflejen al instante en la web pública.

```mermaid
flowchart TB
    subgraph CapaPresentacion["🖥️ Capa de Presentación (Frontend Responsivo)"]
        direction LR
        WebPublica["🌐 Portal Web Público<br/>• Landing Comercial White-Label<br/>• Catálogo Filtrable<br/>• Wizard de Reserva en 4 Pasos<br/>• Buscador de Cita por Código"]
        PanelAdmin["📊 Panel de Administración (Dashboard)<br/>• KPIs e Ingresos en Vivo<br/>• Calendario Interactivo y Walk-ins<br/>• Caja, Cobros y Liquidación de Comisiones<br/>• CRM de Clientes y Configuración"]
    end

    subgraph CapaNegocio["⚙️ Capa de Lógica de Negocio y Controladores (API / Servicios)"]
        direction LR
        AuthSvc["🔐 Servicio de Autenticación y Roles<br/>(Admin / Recepción / Profesional)"]
        SlotEngine["⏱️ Motor de Disponibilidad<br/>(Cálculo de Slots, Cruce de Citas y Bloqueos)"]
        BookingSvc["📅 Gestor de Reservas y Códigos<br/>(Validación Anti-Solapamiento + CRM Auto-Link)"]
        FinanceSvc["💰 Motor de Caja y Comisiones<br/>(Arqueo Diario + % Liquidación Profesional)"]
    end

    subgraph CapaDatos["🗄️ Capa de Persistencia (Base de Datos Relacional / Almacenamiento)"]
        DB[("Base de Datos Principal<br/>• Configuración White-Label<br/>• Usuarios y Profesionales<br/>• Servicios y Categorías<br/>• Clientes (CRM) y Citas<br/>• Transacciones y Reseñas")]
    end

    subgraph Integraciones["📲 Canales Externos"]
        WhatsApp["💬 Integración Directa WhatsApp<br/>(Confirmación de Ticket y Recordatorios)"]
        PrintPDF["🖨️ Generador de Comprobantes / Reportes<br/>(Ticket de Reserva y Cierre de Caja)"]
    end

    WebPublica -->|"Consulta catálogo y horarios / Crea reserva"| SlotEngine
    WebPublica -->|"Registra cita / Consulta código"| BookingSvc
    PanelAdmin -->|"Login por Rol"| AuthSvc
    PanelAdmin -->|"Gestión de agenda y Walk-ins"| BookingSvc
    PanelAdmin -->|"Cobros, arqueo y comisiones"| FinanceSvc
    PanelAdmin -->|"Configuración de horarios y catálogo"| SlotEngine

    AuthSvc --> DB
    SlotEngine --> DB
    BookingSvc --> DB
    FinanceSvc --> DB

    BookingSvc --> WhatsApp
    BookingSvc --> PrintPDF
    FinanceSvc --> PrintPDF
```

---

## 2. Diagrama Entidad-Relación (ERD — Base de Datos)

```mermaid
erDiagram
    CONFIGURACION_NEGOCIO {
        int id PK
        string nombre_negocio
        string rubro_tipo
        string eslogan
        string telefono_whatsapp
        string direccion
        string moneda_simbolo
        string color_primario
        int horas_min_cancelacion
        boolean confirmar_automatico
    }

    USUARIOS {
        int id PK
        string nombre_completo
        string email UK
        string password_hash
        string rol "ADMIN | RECEPCION | PROFESIONAL"
        boolean activo
        datetime fecha_creacion
    }

    PROFESIONALES {
        int id PK
        int usuario_id FK "Opcional si tiene login propio"
        string nombre_mostrar
        string especialidad_cargo
        string telefono
        string color_agenda
        decimal porcentaje_comision "Ej: 45.00"
        boolean activo
    }

    HORARIOS_PROFESIONAL {
        int id PK
        int profesional_id FK
        int dia_semana "0=Dom, 1=Lun ... 6=Sab"
        boolean es_laborable
        string hora_inicio "Ej: 09:00"
        string hora_fin "Ej: 19:00"
        string descanso_inicio "Ej: 13:00"
        string descanso_fin "Ej: 14:00"
    }

    BLOQUEOS_AGENDA {
        int id PK
        int profesional_id FK "NULL = Todo el negocio cerrado"
        date fecha
        string hora_inicio
        string hora_fin
        string motivo "Vacaciones, Permiso, Feriado"
    }

    CATEGORIAS_SERVICIO {
        int id PK
        string nombre
        string icono
        int orden_visual
        boolean activo
    }

    SERVICIOS {
        int id PK
        int categoria_id FK
        string nombre
        string descripcion
        int duracion_minutos "Ej: 30, 45, 60"
        decimal precio
        boolean destacado
        boolean activo
    }

    PROFESIONAL_SERVICIOS {
        int profesional_id PK, FK
        int servicio_id PK, FK
    }

    CLIENTES {
        int id PK
        string nombre_completo
        string telefono UK "Clave de identificación rápida"
        string email
        string notas_preferencias "Alergias, corte preferido, etc."
        int total_visitas
        int total_inasistencias
        decimal total_gastado
        datetime ultima_visita
    }

    CITAS {
        int id PK
        string codigo_reserva UK "Ej: RES-8492"
        int cliente_id FK
        int profesional_id FK
        int servicio_id FK
        date fecha_cita
        string hora_inicio "Ej: 10:30"
        string hora_fin "Ej: 11:15"
        decimal precio_pactado
        string origen "WEB | PANEL_WALKIN | TELEFONO"
        string estado "PENDIENTE | CONFIRMADA | EN_ATENCION | COMPLETADA | CANCELADA | NO_ASISTIO"
        string notas_cliente
        string notas_internas
        datetime fecha_registro
    }

    PAGOS_TRANSACCIONES {
        int id PK
        int cita_id FK
        decimal subtotal
        decimal descuento
        decimal monto_total
        string metodo_pago "EFECTIVO | TRANSFERENCIA_QR | TARJETA"
        decimal porcentaje_comision_aplicado
        decimal monto_comision_profesional
        decimal monto_neto_negocio
        datetime fecha_pago
    }

    RESENAS {
        int id PK
        int cita_id FK
        int cliente_id FK
        int calificacion "1 a 5 estrellas"
        string comentario
        boolean visible_en_web
        datetime fecha_resena
    }

    %% Relaciones
    USUARIOS ||--o| PROFESIONALES : "asociado_a"
    PROFESIONALES ||--o{ HORARIOS_PROFESIONAL : "tiene_jornada"
    PROFESIONALES ||--o{ BLOQUEOS_AGENDA : "registra_ausencias"
    CATEGORIAS_SERVICIO ||--o{ SERVICIOS : "agrupa"
    PROFESIONALES ||--o{ PROFESIONAL_SERVICIOS : "habilitado_en"
    SERVICIOS ||--o{ PROFESIONAL_SERVICIOS : "realizado_por"
    CLIENTES ||--o{ CITAS : "agenda"
    PROFESIONALES ||--o{ CITAS : "atiende"
    SERVICIOS ||--o{ CITAS : "incluye"
    CITAS ||--o| PAGOS_TRANSACCIONES : "genera_cobro"
    CITAS ||--o| RESENAS : "evaluada_en"
    CLIENTES ||--o{ RESENAS : "escribe"
```

---

## 3. Diccionario de Datos Principal

### 3.1 Tabla `CITAS` (Núcleo Operativo)
Almacena tanto las reservas creadas desde la página web como los turnos agendados manualmente en recepción.

| Columna | Tipo | Restricción | Descripción |
|---|---|---|---|
| `id` | `INTEGER` | `PK, AUTO_INCREMENT` | Identificador único interno de la cita. |
| `codigo_reserva` | `VARCHAR(15)` | `UNIQUE, NOT NULL` | Código público de seguimiento para el cliente (ej. `RES-4920`). |
| `cliente_id` | `INTEGER` | `FK -> CLIENTES(id)` | Cliente titular del turno. |
| `profesional_id` | `INTEGER` | `FK -> PROFESIONALES(id)` | Especialista asignado a la atención. |
| `servicio_id` | `INTEGER` | `FK -> SERVICIOS(id)` | Servicio contratado. |
| `fecha_cita` | `DATE` | `NOT NULL, INDEX` | Fecha programada del turno (`YYYY-MM-DD`). |
| `hora_inicio` | `VARCHAR(5)` | `NOT NULL` | Hora de inicio en formato 24h (`HH:MM`). |
| `hora_fin` | `VARCHAR(5)` | `NOT NULL` | Hora calculada sumando `duracion_minutos` del servicio a `hora_inicio`. |
| `precio_pactado` | `DECIMAL(10,2)` | `NOT NULL` | Precio congelado al momento de agendar (protege ante cambios futuros de tarifa). |
| `origen` | `ENUM` | `NOT NULL` | Canal de creación: `WEB`, `PANEL_WALKIN`, `TELEFONO`. |
| `estado` | `ENUM` | `NOT NULL` | Estado actual: `PENDIENTE`, `CONFIRMADA`, `EN_ATENCION`, `COMPLETADA`, `CANCELADA`, `NO_ASISTIO`. |
| `notas_cliente` | `TEXT` | `NULL` | Comentario dejado por el cliente al reservar. |
| `notas_internas` | `TEXT` | `NULL` | Observaciones técnicas/clínicas privadas del profesional o recepción. |

---

### 3.2 Tabla `PAGOS_TRANSACCIONES` (Núcleo Financiero y Comisiones)
Garantiza la transparencia financiera entre el dueño del negocio y sus profesionales.

| Columna | Tipo | Restricción | Descripción |
|---|---|---|---|
| `id` | `INTEGER` | `PK, AUTO_INCREMENT` | Identificador único del cobro. |
| `cita_id` | `INTEGER` | `FK -> CITAS(id), UNIQUE` | Cita que origina el ingreso. |
| `subtotal` | `DECIMAL(10,2)` | `NOT NULL` | Valor base del servicio más adicionales. |
| `descuento` | `DECIMAL(10,2)` | `DEFAULT 0.00` | Descuento promocional aplicado en caja. |
| `monto_total` | `DECIMAL(10,2)` | `NOT NULL` | Monto final cobrado al cliente (`subtotal - descuento`). |
| `metodo_pago` | `ENUM` | `NOT NULL` | `EFECTIVO`, `TRANSFERENCIA_QR`, `TARJETA`. |
| `porcentaje_comision_aplicado` | `DECIMAL(5,2)` | `NOT NULL` | Porcentaje vigente del profesional en el momento del cobro. |
| `monto_comision_profesional` | `DECIMAL(10,2)` | `NOT NULL` | Dinero que le corresponde al profesional por ese servicio. |
| `monto_neto_negocio` | `DECIMAL(10,2)` | `NOT NULL` | Ganancia neta que queda en caja para la empresa. |
| `fecha_pago` | `DATETIME` | `NOT NULL` | Fecha y hora exacta del cierre del cobro. |
