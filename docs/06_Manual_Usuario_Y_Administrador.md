# 06. Manual de Usuario y Manual del Administrador — ReservaPro

Este documento guía paso a paso el uso del sistema tanto para el **Cliente Final (Portal Web Público)** como para el personal del negocio (**Administrador, Recepcionista y Profesional**).

---

## 1. Credenciales de Acceso al Panel Administrativo

El sistema incluye tres perfiles preconfigurados para que puedas probar o demostrar los permisos por rol (`RBAC`):

| Rol | Correo / Usuario | Contraseña | Alcance de Permisos |
|---|---|---|---|
| **👨‍💼 Administrador (Dueño)** | `admin@reservapro.com` | `admin123` | Acceso total: Dashboard financiero, Agenda, Caja, Liquidación de comisiones, CRM, Catálogo de servicios, Equipo/Horarios, Reseñas y Configuración White-Label. |
| **🛎️ Recepcionista** | `recepcion@reservapro.com` | `recep123` | Acceso operativo: Agenda del día, creación de citas manuales (*Walk-in*), confirmación de turnos, *Check-in*, cobro en Caja y directorio CRM de clientes. |
| **💇‍♂️ Profesional / Especialista** | `mateo@reservapro.com` | `prof123` | Acceso personal: Visualiza su propia agenda, marca inicio de atención, consulta notas técnicas del cliente y revisa sus comisiones acumuladas. |

---

## 2. Manual del Portal Web Público (Cliente)

### 2.1 Cómo Agendar una Cita Online (En 4 Pasos)
1. **Paso 1 — Elegir Servicio:** En la página principal o en el asistente de reservas, filtra por categoría y haz clic en el servicio deseado (verás el tiempo estimado en minutos y el precio).
2. **Paso 2 — Elegir Especialista:** Selecciona el profesional de tu preferencia o marca la opción *"Cualquier especialista disponible"*.
3. **Paso 3 — Elegir Fecha y Hora:** Selecciona el día en el calendario. El sistema mostrará **únicamente los bloques de hora libres** que no se cruzan con otras citas ni con el horario de almuerzo del profesional.
4. **Paso 4 — Datos de Contacto:** Ingresa tu Nombre completo, número de Teléfono/WhatsApp y una nota opcional. Si ya has reservado antes con ese mismo teléfono, el sistema reconocerá tu ficha automáticamente.
5. **Comprobante Digital (`RES-XXXX`):** Al confirmar, recibirás en pantalla tu **Código Único de Reserva** con opción de imprimir el ticket o enviarlo por WhatsApp al local.

### 2.2 Cómo Consultar, Cancelar o Calificar tu Cita
1. Haz clic en la pestaña **"Consultar mi Cita"** en la barra superior de la web.
2. Escribe tu **Código de Reserva** (ej. `RES-1001`) o tu número de teléfono.
3. Verás en tiempo real la barra de progreso de tu turno:
   - Si tu cita está `PENDIENTE` o `CONFIRMADA` y estás dentro del tiempo permitido por el negocio, podrás hacer clic en **"Cancelar Cita"** (lo cual libera inmediatamente el horario en la agenda).
   - Si tu cita ya figura como `COMPLETADA`, aparecerá habilitado el formulario para **Calificar con 1 a 5 estrellas** y dejar tu comentario de experiencia.

---

## 3. Manual del Panel Administrativo (Back-Office)

### 3.1 Gestión Diaria de la Agenda y Estados
1. En el menú lateral, ingresa a **🗓️ Agenda & Citas**.
2. Puedes filtrar las citas por **Fecha**, **Profesional**, **Estado** o buscar por nombre/código.
3. En cada cita dispones de botones rápidos según la etapa del cliente:
   - **Confirmar:** Pasa una cita de `PENDIENTE` a `CONFIRMADA`.
   - **Atender (Check-in):** Cuando el cliente llega y se sienta con el profesional, cámbiala a `EN_ATENCION`.
   - **Cobrar / Finalizar:** Abre el módulo de Caja para registrar el pago y cerrar el turno.
   - **No Asistió (`No-Show`):** Si el cliente no se presentó, márcalo para que quede registrado en su historial CRM.

### 3.2 Cobro en Caja y Cálculo Automático de Comisiones
1. Al pulsar **Cobrar** sobre una cita (o desde el módulo **💵 Caja & Comisiones**), se abrirá la ventana de liquidación.
2. Verifica el **Subtotal** del servicio, ingresa un **Descuento** si aplica y elige el **Método de Pago** (`Efectivo`, `Transferencia / QR` o `Tarjeta`).
3. El sistema mostrará en vivo:
   - **Comisión para el Profesional:** Calculada según el porcentaje asignado a ese empleado.
   - **Ingreso Neto para el Negocio:** Lo que queda libre para la empresa.
4. En la sección **Liquidación de Personal** dentro de Caja, puedes ver el total acumulado a pagarle a cada profesional en el período.

### 3.3 Cambio de Rubro / Marca Blanca (Para Demostraciones de Venta)
1. Ingresa a **⚙️ Configuración (White-Label)** en el panel administrativo (o usa el selector rápido de demostración).
2. Puedes cambiar en un clic entre plantillas preconfiguradas listas para mostrar a tus clientes:
   - 💈 **Barbería & Salón Estético**
   - 🦷 **Clínica Dental & Consultorio Médico**
   - 🧖‍♀️ **Spa, Masajes & Centro de Bienestar**
   - 🐾 **Veterinaria & Peluquería Canina**
3. También puedes personalizar manualmente el nombre del negocio, color corporativo, símbolo de moneda, teléfono de WhatsApp y políticas de cancelación.
