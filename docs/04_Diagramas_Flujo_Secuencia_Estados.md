# 04. Diagramas de Secuencia, Estados y Flujo de Procesos

Este documento modela el comportamiento dinámico del sistema **ReservaPro (`Sist_Reservas_Citas`)** mediante diagramas UML de **Secuencia**, **Máquina de Estados** y **Flujo Algorítmico**.

---

## 1. Diagrama de Secuencia 01: Proceso de Reserva Online (Portal Web)

Representa la interacción cronológica desde que el cliente selecciona un servicio en la web hasta que obtiene su **Código Único de Reserva (`RES-XXXX`)** y la cita impacta en el Panel Administrativo.

```mermaid
sequenceDiagram
    autonumber
    actor Cliente as 👤 Cliente (Web)
    participant UI as 🌐 Frontend Portal Web
    participant SlotEngine as ⏱️ Motor de Disponibilidad
    participant BookingAPI as 📅 Controlador de Reservas
    participant DB as 🗄️ Base de Datos

    Cliente->>UI: Selecciona Servicio (ej. Corte + Barba, 45 min) y Profesional
    Cliente->>UI: Elige Fecha en el Calendario (ej. 25/10/2026)
    UI->>SlotEngine: GET /disponibilidad?servicio=2&prof=1&fecha=2026-10-25
    SlotEngine->>DB: Consulta horario laboral, descansos, bloqueos y citas activas del día
    DB-->>SlotEngine: Retorna jornada (09:00-19:00) y citas ocupadas
    SlotEngine->>SlotEngine: Calcula intervalos libres donde caben 45 min sin solaparse
    SlotEngine-->>UI: Lista de Slots Libres ["09:00", "09:45", "11:30", "15:00"...]
    UI-->>Cliente: Muestra botones de horarios disponibles

    Cliente->>UI: Elige "11:30", ingresa Nombre, Teléfono y Notas, y pulsa "Confirmar"
    UI->>BookingAPI: POST /reservas (datos_cliente, servicio, prof, fecha, "11:30")
    BookingAPI->>DB: Verifica que el bloque 11:30 - 12:15 siga libre (Control de concurrencia)

    alt El horario sigue disponible
        BookingAPI->>DB: Busca cliente por Teléfono (Si no existe lo crea; si existe vincula ID)
        BookingAPI->>BookingAPI: Genera código único (ej. "RES-7391")
        BookingAPI->>DB: INSERT en tabla CITAS (estado = CONFIRMADA, origen = WEB)
        DB-->>BookingAPI: Confirmación de registro exitoso
        BookingAPI-->>UI: HTTP 201 Created (Ticket + Código "RES-7391")
        UI-->>Cliente: Muestra Comprobante Digital + Botón WhatsApp
    else El horario fue tomado segundos antes
        DB-->>BookingAPI: Conflicto de horario detectado
        BookingAPI-->>UI: HTTP 409 Conflict ("Horario recién ocupado, elige otro turno")
        UI-->>Cliente: Refresca lista de horarios libres manteniendo sus datos
    end
```

---

## 2. Diagrama de Secuencia 02: Atención, Cobro en Caja y Cálculo de Comisión (Panel Admin)

Muestra cómo trabajan en equipo la Recepción/Administrador y el sistema financiero cuando el cliente asiste al negocio y paga su servicio.

```mermaid
sequenceDiagram
    autonumber
    actor Admin as 👨‍💼 Admin / Recepción
    participant Dashboard as 📊 Panel Administrativo
    participant FinanceSvc as 💰 Servicio de Caja y Comisiones
    participant DB as 🗄️ Base de Datos

    Admin->>Dashboard: Abre Agenda del Día y selecciona cita "RES-7391"
    Admin->>Dashboard: Cambia estado a "EN_ATENCION" cuando el cliente pasa con el profesional
    Dashboard->>DB: UPDATE CITAS SET estado = 'EN_ATENCION'

    Note over Admin,DB: El profesional finaliza el servicio y el cliente se acerca a caja

    Admin->>Dashboard: Pulsa "Finalizar y Cobrar Turno"
    Dashboard-->>Admin: Abre Modal de Caja con Subtotal precargado ($25.00)
    Admin->>Dashboard: Aplica descuento opcional ($0.00), elige "TRANSFERENCIA_QR" y confirma
    Dashboard->>FinanceSvc: POST /caja/cobrar (cita_id, descuento, metodo_pago)

    FinanceSvc->>DB: Obtiene % de comisión del Profesional asignado (ej. 40%)
    FinanceSvc->>FinanceSvc: Calcula Comisión Profesional ($10.00) y Neto Negocio ($15.00)
    FinanceSvc->>DB: Transacción Atómica:<br/>1. INSERT en PAGOS_TRANSACCIONES<br/>2. UPDATE CITAS SET estado = 'COMPLETADA'<br/>3. UPDATE CLIENTES (total_visitas + 1, total_gastado + $25.00)
    DB-->>FinanceSvc: Transacción confirmada
    FinanceSvc-->>Dashboard: Datos de cierre + Recibo actualizado
    Dashboard-->>Admin: Actualiza KPIs de Ingresos del Día y Liquidación en tiempo real
```

---

## 3. Diagrama de Secuencia 03: Consulta y Cancelación por Código de Seguimiento

```mermaid
sequenceDiagram
    autonumber
    actor Cliente as 👤 Cliente
    participant WebTrack as 🌐 Módulo "Consultar mi Cita"
    participant BookingAPI as 📅 Controlador de Reservas
    participant DB as 🗄️ Base de Datos

    Cliente->>WebTrack: Ingresa código "RES-7391" (o su número de teléfono)
    WebTrack->>BookingAPI: GET /reservas/consulta?codigo=RES-7391
    BookingAPI->>DB: SELECT cita, servicio, profesional, config_negocio
    DB-->>BookingAPI: Datos de la cita (Fecha, Hora, Estado, Horas mínimas cancelación)
    BookingAPI-->>WebTrack: Retorna detalle de la cita y flag `puede_cancelar`
    WebTrack-->>Cliente: Muestra estado actual en vivo y línea de progreso

    opt El cliente decide cancelar y `puede_cancelar == true`
        Cliente->>WebTrack: Pulsa "Cancelar mi Cita" y confirma motivo
        WebTrack->>BookingAPI: PATCH /reservas/RES-7391/cancelar
        BookingAPI->>DB: Valida diferencia de horas >= horas_min_cancelacion
        BookingAPI->>DB: UPDATE CITAS SET estado = 'CANCELADA'
        DB-->>BookingAPI: Horario liberado
        BookingAPI-->>WebTrack: Confirmación de cancelación
        WebTrack-->>Cliente: Notifica cancelación exitosa (el horario vuelve a estar libre en la web)
    end
```

---

## 4. Diagrama de Máquina de Estados: Ciclo de Vida de una Cita

Modela todos los estados posibles por los que atraviesa una cita desde su creación hasta su cierre definitivo, incluyendo quién dispara cada transición.

```mermaid
stateDiagram-v2
    [*] --> PENDIENTE : Cliente reserva en Web<br/>(Si confirmación manual está activa)
    [*] --> CONFIRMADA : Cliente reserva en Web (Auto-confirmación)<br/>o Recepción crea Walk-In

    PENDIENTE --> CONFIRMADA : Recepción / Admin aprueba el turno
    PENDIENTE --> CANCELADA : Cliente cancela con su código<br/>o Admin rechaza por falta de cupo

    CONFIRMADA --> EN_ATENCION : Cliente llega al local (Check-in)<br/>y pasa con el Profesional
    CONFIRMADA --> CANCELADA : Cliente cancela a tiempo en Web<br/>o llama a Recepción
    CONFIRMADA --> NO_ASISTIO : Pasa la hora del turno y<br/>el cliente no se presenta

    EN_ATENCION --> COMPLETADA : Se finaliza el servicio y<br/>se registra el Cobro en Caja

    COMPLETADA --> [*] : Habilita Reseña 5★ y<br/>suma Comisión + LTV Cliente
    CANCELADA --> [*] : Libera inmediatamente el<br/>horario en el calendario público
    NO_ASISTIO --> [*] : Registra alerta de inasistencia<br/>en la ficha CRM del cliente
```

---

## 5. Diagrama de Flujo Algorítmico: Motor Inteligente de Disponibilidad (`SlotEngine`)

Este diagrama detalla la lógica exacta que utilizaremos al programar el cálculo de horarios libres para evitar cruces de turnos:

```mermaid
flowchart TD
    Start(["🚀 Inicio: Solicitud de Horarios Libres<br/>(Fecha, Servicio_ID, Profesional_ID)"]) --> GetServ["Obtener `duracion_minutos` del Servicio"]
    GetServ --> CheckGlobalBlock{"¿Existe bloqueo general<br/>del negocio en esa Fecha?"}
    CheckGlobalBlock -- "Sí (Feriado/Cerrado)" --> ReturnEmpty["Retornar Lista Vacía []"]

    CheckGlobalBlock -- "No" --> GetSchedule["Consultar `HORARIOS_PROFESIONAL` para el día de la semana"]
    GetSchedule --> IsWorkDay{"¿El profesional trabaja<br/>ese día de la semana?"}
    IsWorkDay -- "No (Día Libre)" --> ReturnEmpty

    IsWorkDay -- "Sí" --> LoadBusy["Cargar rangos ocupados del Profesional en esa Fecha:<br/>1. Horario de Descanso/Almuerzo<br/>2. Bloqueos parciales (`BLOQUEOS_AGENDA`)<br/>3. Citas con estado PENDIENTE, CONFIRMADA o EN_ATENCION"]
    LoadBusy --> InitPointer["Inicializar puntero `T_actual = hora_inicio_jornada`"]

    InitPointer --> LoopCond{"¿`T_actual + duracion_minutos`<br/><= `hora_fin_jornada`?"}
    LoopCond -- "No (Fin del día)" --> ReturnSlots(["✅ Retornar Lista de `Slots_Disponibles`"])

    LoopCond -- "Sí" --> CheckPast{"¿La Fecha es HOY y<br/>`T_actual` ya pasó?"}
    CheckPast -- "Sí" --> StepNext["Avanzar puntero: `T_actual = T_actual + intervalo_base (ej. 30 min)`"]

    CheckPast -- "No" --> CheckOverlap{"¿El bloque `[T_actual, T_actual + duracion]`<br/>se cruza con algún rango ocupado?"}
    CheckOverlap -- "Sí (Ocupado)" --> StepNext
    CheckOverlap -- "No (Libre)" --> AddSlot["Agregar `T_actual` a `Slots_Disponibles`"]
    AddSlot --> StepNext
    StepNext --> LoopCond
```
