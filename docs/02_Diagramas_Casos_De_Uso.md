# 02. Diagramas y Especificación de Casos de Uso (UML)

Este documento contiene los **Diagramas de Casos de Uso** divididos por actores y subsistemas, seguidos de las **Fichas Técnicas de Casos de Uso** con precondiciones, flujo normal, flujos alternativos y postcondiciones.

---

## 1. Diagrama General de Casos de Uso del Sistema

```mermaid
flowchart LR
    %% Actores
    Cliente(["👤 Cliente / Visitante"])
    Profesional(["💇‍♂️ Profesional / Especialista"])
    Recepcion(["🛎️ Recepcionista"])
    Admin(["👨‍💼 Administrador / Dueño"])

    %% Herencia de Roles Internos
    Admin -.->|"Hereda permisos de"| Recepcion

    subgraph Sistema["📦 Sistema Web + Panel de Reservas y Gestión (ReservaPro)"]
        direction TB
        subgraph WebPublica["🌐 Subsistema 1: Portal Web Público"]
            CU01(["CU-01: Explorar Catálogo de Servicios y Precios"])
            CU02(["CU-02: Consultar Disponibilidad de Horarios"])
            CU03(["CU-03: Reservar Cita en Línea"])
            CU04(["CU-04: Consultar / Cancelar Cita con Código"])
            CU05(["CU-05: Calificar Servicio Recibido"])
        end

        subgraph PanelOperativo["📅 Subsistema 2: Gestión Operativa de Agenda y Clientes"]
            CU06(["CU-06: Iniciar Sesión en el Panel"])
            CU07(["CU-07: Visualizar Agenda Personal y Comisiones"])
            CU08(["CU-08: Cambiar Estado de Atención de Cita"])
            CU09(["CU-09: Agendar Cita Presencial / Telefónica (Walk-in)"])
            CU10(["CU-10: Gestionar Directorio e Historial CRM de Clientes"])
            CU11(["CU-11: Registrar Cobro en Caja y Liquidar Turno"])
        end

        subgraph PanelGerencial["⚙️ Subsistema 3: Administración y Configuración"]
            CU12(["CU-12: Administrar Catálogo de Servicios y Categorías"])
            CU13(["CU-13: Administrar Profesionales, Horarios y Comisiones"])
            CU14(["CU-14: Visualizar Dashboard Financiero y Reportes KPI"])
            CU15(["CU-15: Configurar Marca y Parámetros del Negocio (White-Label)"])
        end
    end

    %% Relaciones Cliente
    Cliente --> CU01
    Cliente --> CU03
    Cliente --> CU04
    Cliente --> CU05
    CU03 -.->|"<<include>>"| CU02

    %% Relaciones Profesional
    Profesional --> CU06
    Profesional --> CU07
    Profesional --> CU08

    %% Relaciones Recepción
    Recepcion --> CU06
    Recepcion --> CU08
    Recepcion --> CU09
    Recepcion --> CU10
    Recepcion --> CU11
    CU09 -.->|"<<include>>"| CU02

    %% Relaciones Administrador
    Admin --> CU12
    Admin --> CU13
    Admin --> CU14
    Admin --> CU15
```

---

## 2. Diagrama de Casos de Uso — Subsistema Portal Web Público (Cliente)

Detalla todas las interacciones que realiza el cliente en la página web pública, incluyendo relaciones `<<include>>` y `<<extend>>`.

```mermaid
flowchart LR
    Cliente(["👤 Cliente"])

    subgraph PortalWeb["🌐 Portal Web Público"]
        UC_VerLanding(["Visualizar Información del Negocio y Promociones"])
        UC_FiltrarCat(["Filtrar Servicios por Categoría"])
        UC_ElegirProf(["Seleccionar Profesional o 'Cualquiera Disponible'"])
        UC_CalcSlots(["Validar Horarios Libres en Fecha Seleccionada"])
        UC_CrearReserva(["Confirmar Reserva Online"])
        UC_VincularCRM(["Vincular o Crear Ficha de Cliente por Teléfono"])
        UC_GenerarCodigo(["Generar Código Único de Seguimiento y Ticket"])
        UC_NotificarWA(["Enviar Resumen Rápido por WhatsApp"])

        UC_BuscarCodigo(["Consultar Estado de Cita por Código/Teléfono"])
        UC_CancelarCita(["Cancelar Cita Dentro del Plazo Permitido"])
        UC_DejarResena(["Enviar Calificación y Reseña del Servicio"])
    end

    Cliente --> UC_VerLanding
    Cliente --> UC_FiltrarCat
    Cliente --> UC_CrearReserva
    Cliente --> UC_BuscarCodigo

    %% Includes obligatorios al reservar
    UC_CrearReserva -.->|"<<include>>"| UC_ElegirProf
    UC_CrearReserva -.->|"<<include>>"| UC_CalcSlots
    UC_CrearReserva -.->|"<<include>>"| UC_VincularCRM
    UC_CrearReserva -.->|"<<include>>"| UC_GenerarCodigo

    %% Extends opcionales
    UC_NotificarWA -.->|"<<extend>>"| UC_GenerarCodigo
    UC_CancelarCita -.->|"<<extend>> (Si estado = Pendiente/Confirmada)"| UC_BuscarCodigo
    UC_DejarResena -.->|"<<extend>> (Si estado = Completada)"| UC_BuscarCodigo
```

---

## 3. Diagrama de Casos de Uso — Subsistema Panel Administrativo (Roles Internos)

Detalla cómo interactúan el **Especialista**, el **Recepcionista** y el **Administrador** dentro del Panel de Control (Dashboard).

```mermaid
flowchart LR
    Prof(["💇‍♂️ Profesional"])
    Recep(["🛎️ Recepcionista"])
    Admin(["👨‍💼 Administrador"])

    subgraph PanelAdmin["🔐 Panel de Administración (Dashboard)"]
        direction TB
        subgraph ModAgenda["Módulo de Agenda y Atención"]
            A_VerAgenda(["Ver Calendario Diario/Semanal"])
            A_CheckIn(["Confirmar Llegada (Check-in)"])
            A_IniciarAtencion(["Marcar Cita 'En Atención'"])
            A_FinalizarAtencion(["Marcar Cita 'Completada'"])
            A_NoShow(["Marcar 'No Asistió' (No-Show)"])
            A_CitaManual(["Registrar Cita Manual / Walk-In"])
            A_BloquearHoras(["Registrar Bloqueo de Horario / Descanso"])
        end

        subgraph ModCajaCRM["Módulo de Caja y CRM"]
            C_RegistrarPago(["Registrar Pago (Efectivo/Tarjeta/Transferencia)"])
            C_CalcularComision(["Calcular Comisión Automática del Profesional"])
            C_FichaCliente(["Ver Historial de Visitas y Notas de Cliente"])
        end

        subgraph ModConfig["Módulo Gerencial y Configuración"]
            G_CRUDServicios(["Gestionar Servicios, Duración y Precios"])
            G_CRUDPersonal(["Gestionar Profesionales y % de Comisión"])
            G_VerReportes(["Consultar Ingresos, KPIs y Liquidaciones"])
            G_PersonalizarMarca(["Personalizar Nombre, Colores y Políticas"])
        end
    end

    %% Profesional
    Prof --> A_VerAgenda
    Prof --> A_IniciarAtencion
    Prof --> A_FinalizarAtencion
    Prof --> C_FichaCliente

    %% Recepcionista
    Recep --> A_VerAgenda
    Recep --> A_CheckIn
    Recep --> A_CitaManual
    Recep --> A_NoShow
    Recep --> C_RegistrarPago
    Recep --> C_FichaCliente

    %% Relación automática al cobrar
    C_RegistrarPago -.->|"<<include>>"| C_CalcularComision
    C_RegistrarPago -.->|"<<include>>"| A_FinalizarAtencion

    %% Administrador
    Admin --> A_BloquearHoras
    Admin --> G_CRUDServicios
    Admin --> G_CRUDPersonal
    Admin --> G_VerReportes
    Admin --> G_PersonalizarMarca
    Admin --> C_RegistrarPago
    Admin --> A_CitaManual
```

---

## 4. Especificación Detallada de Casos de Uso (Fichas Técnicas)

### Ficha CU-03: Reservar Cita en Línea (Portal Web)

| Campo | Descripción |
|---|---|
| **ID y Nombre** | **CU-03: Reservar Cita en Línea** |
| **Actor Principal** | Cliente / Visitante Web |
| **Objetivo** | Permitir al cliente agendar una cita seleccionando servicio, profesional, fecha y hora libre, obteniendo un código único de reserva. |
| **Precondiciones** | 1. Debe existir al menos un servicio activo y un profesional activo asignado a ese servicio.<br>2. El profesional debe tener horarios disponibles en la fecha seleccionada. |
| **Flujo Principal (Camino Feliz)** | 1. El cliente selecciona el botón *"Agendar Cita"* en la página web o elige un servicio del catálogo.<br>2. El sistema muestra la lista de profesionales que realizan dicho servicio (incluyendo la opción *"Cualquiera disponible"*).<br>3. El cliente selecciona el profesional y elige una fecha en el calendario.<br>4. El sistema ejecuta el motor de disponibilidad (`CU-02`) y muestra los bloques de hora libres (ej. `09:00`, `09:45`, `10:30`).<br>5. El cliente selecciona la hora deseada e ingresa su Nombre Completo, Teléfono/WhatsApp, Correo (opcional) y Notas adicionales.<br>6. El sistema verifica que el horario siga disponible (control de concurrencia), registra o actualiza al cliente en el CRM por su teléfono, guarda la cita en estado `CONFIRMADA` (o `PENDIENTE` según configuración) y genera un código único (ej. `RES-4821`).<br>7. El sistema muestra en pantalla el comprobante con el código, resumen de la cita y botón para enviar confirmación por WhatsApp. |
| **Flujos Alternativos** | **FA-1 (Sin horarios disponibles en la fecha):** En el paso 4, si el día está lleno o es día libre, el sistema informa *"No hay turnos disponibles en esta fecha"* y sugiere pasar al día siguiente.<br>**FA-2 (Horario tomado en el último segundo):** En el paso 6, si otro usuario reservó ese mismo bloque segundos antes, el sistema alerta al usuario y refresca los horarios libres sin borrar sus datos personales. |
| **Postcondiciones** | La cita queda almacenada en el sistema, el horario queda bloqueado para evitar dobles reservas y la cita aparece inmediatamente en el Dashboard Administrativo. |

---

### Ficha CU-04: Consultar o Cancelar Cita con Código de Seguimiento

| Campo | Descripción |
|---|---|
| **ID y Nombre** | **CU-04: Consultar / Cancelar Cita con Código** |
| **Actor Principal** | Cliente |
| **Objetivo** | Permitir al cliente verificar el estado de su reserva o cancelarla sin tener que llamar al negocio. |
| **Precondiciones** | El cliente cuenta con su Código de Reserva (ej. `RES-4821`) o el número de teléfono con el que agendó. |
| **Flujo Principal** | 1. El cliente accede a la sección *"Consultar mi Cita"* en la página web.<br>2. Ingresa su Código de Reserva (o su teléfono).<br>3. El sistema busca la cita y muestra una tarjeta detallada con: Estado actual (`Pendiente`, `Confirmada`, `En Atención`, `Completada`, `Cancelada`), Servicio, Profesional asignado, Fecha, Hora y Precio.<br>4. Si el cliente desea cancelar, presiona *"Cancelar Reserva"* e indica opcionalmente el motivo.<br>5. El sistema valida que falten más de $X$ horas (según política del negocio) y cambia el estado a `CANCELADA`, liberando inmediatamente el horario en el calendario. |
| **Flujos Alternativos** | **FA-1 (Código no encontrado):** El sistema muestra un mensaje indicando que verifique el código o número telefónico.<br>**FA-2 (Fuera del límite de tiempo para cancelar):** Si falta menos del tiempo mínimo permitido (ej. menos de 2 horas), el sistema deshabilita el botón de cancelación automática y muestra un enlace directo al WhatsApp de recepción. |
| **Postcondiciones** | Si se cancela, el bloque horario vuelve a estar disponible en la web pública para otros clientes. |

---

### Ficha CU-11: Registrar Cobro en Caja y Liquidar Turno (Panel Admin)

| Campo | Descripción |
|---|---|
| **ID y Nombre** | **CU-11: Registrar Cobro en Caja y Liquidar Turno** |
| **Actor Principal** | Recepcionista o Administrador |
| **Objetivo** | Finalizar la atención de una cita, registrar el método de pago y calcular automáticamente la comisión del profesional y la ganancia del negocio. |
| **Precondiciones** | El usuario ha iniciado sesión con rol `ADMIN` o `RECEPCION` y existe una cita en estado `CONFIRMADA` o `EN_ATENCION`. |
| **Flujo Principal** | 1. El operador selecciona la cita en la agenda o lista del día y hace clic en *"Finalizar y Cobrar"*.<br>2. El sistema precarga el precio del servicio (permitiendo ajustar el monto o aplicar un descuento/servicio extra si corresponde).<br>3. El operador selecciona el método de pago (`Efectivo`, `Transferencia / QR`, `Tarjeta`).<br>4. El sistema consulta el porcentaje de comisión configurado para el profesional que atendió (ej. 45%) y calcula:<br>   - `Monto Comisión Profesional`<br>   - `Ingreso Neto del Negocio`<br>5. El sistema cambia el estado de la cita a `COMPLETADA`, registra la transacción en Caja, suma una visita completada al historial del cliente (CRM) y actualiza las métricas del Dashboard en tiempo real. |
| **Postcondiciones** | La cita queda cerrada, el ingreso se refleja en el arqueo de caja del día y la comisión se suma a la cuenta de liquidación del profesional. |

---

### Ficha CU-13: Administrar Profesionales, Horarios y Comisiones

| Campo | Descripción |
|---|---|
| **ID y Nombre** | **CU-13: Administrar Profesionales, Horarios y Comisiones** |
| **Actor Principal** | Administrador / Dueño |
| **Objetivo** | Configurar el equipo de trabajo, los servicios que realiza cada uno, su horario semanal y su porcentaje de ganancia. |
| **Precondiciones** | El usuario tiene sesión activa con rol `ADMIN`. |
| **Flujo Principal** | 1. El Administrador accede al módulo *"Equipo / Profesionales"*.<br>2. Crea o edita un profesional ingresando: Nombre, Especialidad/Cargo, Teléfono, Foto/Avatar, Color en calendario y `% de Comisión` (0% a 100%).<br>3. Selecciona mediante casillas de verificación qué servicios del catálogo está capacitado para realizar.<br>4. Define su jornada laboral (días activos de Lunes a Domingo, hora de inicio, hora de fin y rango de descanso/almuerzo).<br>5. Guarda los cambios. |
| **Postcondiciones** | El motor de disponibilidad web empieza a ofrecer inmediatamente los horarios de ese profesional únicamente para los servicios que tiene asignados. |
