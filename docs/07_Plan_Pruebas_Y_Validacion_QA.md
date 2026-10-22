# 07. Plan de Pruebas Funcionales y Matriz de Trazabilidad (QA)

Este documento establece la **Matriz de Trazabilidad** que conecta cada Requisito Funcional con su Caso de Uso y su Caso de Prueba, garantizando que el sistema cumple al 100% con la especificación documental.

---

## 1. Matriz de Trazabilidad de Ingeniería

| Requisito (SRS) | Caso de Uso (UML) | Módulo de Código | Caso de Prueba (QA) |
|---|---|---|---|
| **RF-01, RF-02** | `CU-01`: Explorar Catálogo y Precios | `public/index.html` + `GET /api/public/bootstrap` | `CP-01` |
| **RF-03, RF-04** | `CU-02`: Consultar Disponibilidad de Horarios | `server/server.js` (`computeAvailableSlots`) | `CP-02`, `CP-03` |
| **RF-05, RF-06** | `CU-03`: Reservar Cita en Línea + Código Único | `POST /api/public/reservas` | `CP-04`, `CP-05` |
| **RF-07** | `CU-04`: Consultar / Cancelar Cita con Código | `GET/PATCH /api/public/reservas/:codigo` | `CP-06` |
| **RF-08, RF-19** | `CU-05`: Calificar Servicio y Moderar Reseña | `POST /api/public/resenas` | `CP-07` |
| **RF-09** | `CU-06`: Iniciar Sesión por Rol (`RBAC`) | `POST /api/auth/login` | `CP-08` |
| **RF-11, RF-12, RF-13** | `CU-08, CU-09`: Gestión de Agenda y Walk-In | `POST/PATCH /api/admin/citas` | `CP-09` |
| **RF-18, RN-04** | `CU-11`: Cobro en Caja y Cálculo de Comisión | `POST /api/admin/caja/cobrar` | `CP-10` |
| **RF-14, RF-15, RF-16** | `CU-12, CU-13`: CRUD Servicios, Personal y Bloqueos | `/api/admin/servicios`, `/api/admin/profesionales` | `CP-11` |
| **RF-20** | `CU-15`: Configuración White-Label y Plantillas | `PUT /api/admin/configuracion`, `POST /api/admin/preset` | `CP-12` |

---

## 2. Casos de Prueba Funcionales (Suite QA)

| ID | Escenario de Prueba | Datos de Entrada | Resultado Esperado |
|---|---|---|---|
| **CP-01** | Carga dinámica de catálogo y filtro por categoría en Web Pública | Seleccionar categoría específica en el Portal Web | Se muestran únicamente los servicios activos de esa categoría con su duración y precio formateado. |
| **CP-02** | Cálculo de horarios libres respetando hora de descanso | Profesional con jornada `09:00-19:00` y almuerzo `13:00-14:00` | Ningún bloque horario retornado por `SlotEngine` se superpone con el rango `13:00-14:00`. |
| **CP-03** | Prevención de doble reserva (Anti-Solapamiento `RN-01`) | Intentar reservar el mismo profesional y fecha en un horario ya ocupado por una cita `CONFIRMADA` | El horario ocupado no aparece en los slots libres, y si se envía por API directa devuelve error `HTTP 409 Conflict`. |
| **CP-04** | Reserva exitosa y generación de código único `RES-XXXX` | Completar los 4 pasos del Wizard con nombre y teléfono | Se crea la cita, se retorna un código único `RES-XXXX` y se vincula o crea la ficha CRM del cliente. |
| **CP-05** | Reconocimiento automático de cliente recurrente (`RN-05`) | Agendar una segunda cita usando el mismo número de teléfono | No se duplica el registro en `CLIENTES`; la nueva cita se asocia al mismo `cliente_id`. |
| **CP-06** | Consulta de cita por código y cancelación con liberación de turno | Buscar `RES-XXXX` en "Consultar mi Cita" y pulsar "Cancelar" | El estado pasa a `CANCELADA` y el horario vuelve a aparecer inmediatamente disponible en el calendario web. |
| **CP-07** | Envío de calificación 5★ en cita completada | Buscar una cita con estado `COMPLETADA` y enviar reseña | La reseña queda registrada y visible tras aprobación en el listado de opiniones. |
| **CP-08** | Control de acceso por rol en Panel Administrativo | Iniciar sesión con cuenta `PROFESIONAL` vs `ADMIN` | El perfil `PROFESIONAL` ve su agenda y comisiones; el perfil `ADMIN` tiene acceso completo a Configuración y Catálogo. |
| **CP-09** | Registro de cita presencial (*Walk-In*) desde Recepción | Crear cita manual desde el modal del Panel Admin | La cita se inserta con origen `PANEL_WALKIN`, estado `CONFIRMADA` y bloquea el horario en la web pública. |
| **CP-10** | Cobro en Caja y partición exacta de Comisión vs. Neto Negocio | Cobrar cita de `$20.00` atendida por profesional con `45%` de comisión | Se registra transacción: Total `$20.00`, Comisión Profesional `$9.00`, Ganancia Neta Negocio `$11.00`, Estado `COMPLETADA`. |
| **CP-11** | Bloqueo de agenda por permiso/vacaciones | Agregar bloqueo para un profesional en fecha específica de `15:00` a `19:00` | El motor de disponibilidad en la web pública deja de ofrecer turnos a partir de las `15:00` para ese profesional. |
| **CP-12** | Cambio instantáneo de Rubro Comercial (*White-Label*) | Cambiar plantilla de *Barbería* a *Clínica Dental* en Configuración | Toda la web pública y el panel actualizan su marca, colores, servicios, categorías y especialistas al nuevo rubro. |
