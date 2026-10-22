/**
 * SentinelPro Access & IAM — Lógica de Frontend SPA
 * Control de Acceso Físico en Portería (Vigilante), Asistencia de Trabajadores,
 * Terminal Kiosco y Centro de Control IAM con Permisos Granulares.
 */

let CURRENT_USER = null;
let AUTH_TOKEN = localStorage.getItem('sentinelpro_token') || null;
let SYSTEM_DATA = null;
let SELECTED_GUARD_WORKER = null;
let SELECTED_IAM_USER_ID = null;

// ============================================================================
// 1. INICIALIZACIÓN Y NAVEGACIÓN PRINCIPAL
// ============================================================================
document.addEventListener('DOMContentLoaded', async () => {
    await loadPublicBootstrap();
    if (AUTH_TOKEN) {
        await restoreAdminSession();
    }
});

function switchMainView(viewName) {
    const pub = document.getElementById('view-public');
    const adm = document.getElementById('view-admin');
    const btnPub = document.getElementById('btn-view-public');
    const btnAdm = document.getElementById('btn-view-admin');

    if (viewName === 'public') {
        pub.classList.remove('hidden');
        adm.classList.add('hidden');
        btnPub.classList.add('active');
        btnAdm.classList.remove('active');
        loadPublicBootstrap();
    } else {
        pub.classList.add('hidden');
        adm.classList.remove('hidden');
        btnPub.classList.remove('active');
        btnAdm.classList.add('active');

        if (CURRENT_USER) {
            document.getElementById('admin-login-card').classList.add('hidden');
            document.getElementById('admin-workspace').classList.remove('hidden');
            loadAdminDashboardData();
        } else {
            document.getElementById('admin-login-card').classList.remove('hidden');
            document.getElementById('admin-workspace').classList.add('hidden');
        }
    }
}

function scrollToElement(id) {
    const el = document.getElementById(id);
    if (el) el.scrollIntoView({ behavior: 'smooth' });
}

// ============================================================================
// 2. PORTAL CORPORATIVO & TERMINAL KIOSCO (PÚBLICO)
// ============================================================================
async function loadPublicBootstrap() {
    try {
        const res = await fetch('/api/public/bootstrap');
        const data = await res.json();
        SYSTEM_DATA = data;

        // Actualizar contadores en vivo
        if (data.resumen_planta) {
            document.getElementById('pub-aforo-val').textContent = data.resumen_planta.aforo_actual;
            document.getElementById('pub-entradas-val').textContent = data.resumen_planta.entradas_hoy;
            document.getElementById('pub-salidas-val').textContent = data.resumen_planta.salidas_hoy;
            document.getElementById('pub-visitantes-val').textContent = data.resumen_planta.visitantes_en_planta;
            document.getElementById('pub-aforo-max').textContent = data.resumen_planta.aforo_maximo;
        }

        if (data.config) {
            document.getElementById('pub-company-name').textContent = data.config.nombre_empresa;
        }

        // Llenar selector de puertas del Kiosco
        const selPuerta = document.getElementById('kiosco-puerta');
        if (selPuerta && data.zonas) {
            selPuerta.innerHTML = data.zonas.map(z => 
                `<option value="${z.id}">${z.codigo}: ${z.nombre} (${z.tipo})</option>`
            ).join('');
        }
    } catch (err) {
        console.error('Error cargando bootstrap público:', err);
    }
}

async function submitKioscoMovement(tipo) {
    const identInput = document.getElementById('kiosco-id');
    const puertaInput = document.getElementById('kiosco-puerta');
    const feedback = document.getElementById('kiosco-feedback');

    const identificador = identInput.value.trim();
    if (!identificador) {
        showFeedback(feedback, 'Por favor digita tu Número de Documento o Código de Tarjeta (ej. EMP-001).', 'error');
        return;
    }

    try {
        const res = await fetch('/api/public/kiosco/marcar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                identificador,
                tipo_movimiento: tipo,
                zona_id: Number(puertaInput.value) || 1,
                metodo_identificacion: 'TERMINAL_KIOSCO_PIN'
            })
        });

        const data = await res.json();

        if (res.ok) {
            showFeedback(feedback, data.mensaje, 'success');
            identInput.value = '';
            loadPublicBootstrap();
        } else {
            showFeedback(feedback, data.error || 'No se pudo procesar la marcación.', 'error');
        }
    } catch (err) {
        showFeedback(feedback, 'Error de conexión con el servidor de portería.', 'error');
    }
}

function showFeedback(el, message, type) {
    el.textContent = message;
    el.className = `feedback-box ${type}`;
    el.classList.remove('hidden');
}

// Modal Consulta de Credencial
function openCredentialModal() {
    document.getElementById('modal-credential').classList.remove('hidden');
    document.getElementById('modal-cred-input').focus();
}

function closeCredentialModal() {
    document.getElementById('modal-credential').classList.add('hidden');
    document.getElementById('modal-cred-result').classList.add('hidden');
}

async function queryCredentialPublic() {
    const q = document.getElementById('modal-cred-input').value.trim();
    const box = document.getElementById('modal-cred-result');
    if (!q) return;

    try {
        const res = await fetch(`/api/public/consultar-credencial?identificador=${encodeURIComponent(q)}`);
        const data = await res.json();

        if (res.ok) {
            const t = data.trabajador;
            const turno = data.turno_asignado ? `${data.turno_asignado.nombre} (${data.turno_asignado.hora_entrada} a ${data.turno_asignado.hora_salida})` : 'Estándar';
            const estadoBadge = t.estado === 'ACTIVO' 
                ? '<span class="badge badge-success">ACTIVO</span>' 
                : '<span class="badge badge-danger">SUSPENDIDO</span>';
            const ubicacionBadge = t.ubicacion_actual === 'DENTRO_PLANTA' 
                ? '<span class="badge badge-info">DENTRO DE LA EMPRESA</span>' 
                : '<span class="badge badge-neutral">FUERA DE PLANTA</span>';

            box.innerHTML = `
                <div style="background:#f8fafc;padding:16px;border-radius:8px;border:1px solid #cbd5e1;">
                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
                        <h4 style="margin:0;">${t.nombre_completo} (${t.codigo_credencial})</h4>
                        <div>${estadoBadge} ${ubicacionBadge}</div>
                    </div>
                    <p style="margin:4px 0;font-size:0.86rem;"><strong>Cargo:</strong> ${t.cargo} | <strong>Departamento:</strong> ${t.departamento}</p>
                    <p style="margin:4px 0;font-size:0.86rem;"><strong>Turno:</strong> ${turno}</p>
                    <p style="margin:4px 0;font-size:0.86rem;"><strong>Última Marcación:</strong> ${t.ultima_entrada}</p>
                    <div style="margin-top:10px;">
                        <strong style="font-size:0.82rem;text-transform:uppercase;color:#475569;">Puertas Físicas Autorizadas:</strong>
                        <ul style="margin:6px 0 0 18px;font-size:0.84rem;">
                            ${data.zonas_autorizadas_detalle.map(z => `<li>${z}</li>`).join('')}
                        </ul>
                    </div>
                </div>
            `;
            box.classList.remove('hidden');
        } else {
            box.innerHTML = `<div class="feedback-box error">${data.error}</div>`;
            box.classList.remove('hidden');
        }
    } catch (err) {
        box.innerHTML = `<div class="feedback-box error">Error al consultar el servidor.</div>`;
        box.classList.remove('hidden');
    }
}

// ============================================================================
// 3. AUTENTICACIÓN Y CONTROL DE SESIÓN (IAM)
// ============================================================================
function quickLogin(email, pass) {
    document.getElementById('login-email').value = email;
    document.getElementById('login-pass').value = pass;
    submitLogin(false);
}

async function submitLogin(forceReplace = false) {
    const email = document.getElementById('login-email').value.trim();
    const password = document.getElementById('login-pass').value.trim();
    const conflictBox = document.getElementById('conflict-box');
    const conflictText = document.getElementById('conflict-text');

    conflictBox.classList.add('hidden');

    try {
        const res = await fetch('/api/auth/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                email,
                password,
                force_replace: forceReplace,
                dispositivo: `SentinelPro Web Client (${navigator.userAgent.slice(0, 50)})`
            })
        });

        const data = await res.json();

        if (res.status === 409) {
            conflictText.textContent = data.error;
            conflictBox.classList.remove('hidden');
            return;
        }

        if (res.ok) {
            AUTH_TOKEN = data.token;
            CURRENT_USER = data.usuario;
            localStorage.setItem('sentinelpro_token', AUTH_TOKEN);

            document.getElementById('admin-login-card').classList.add('hidden');
            document.getElementById('admin-workspace').classList.remove('hidden');

            applyUserNavigationPermissions();
            loadAdminDashboardData();
        } else {
            alert(data.error || 'Credenciales no autorizadas.');
        }
    } catch (err) {
        alert('Error conectando al servidor de seguridad.');
    }
}

async function restoreAdminSession() {
    try {
        const res = await fetch('/api/auth/me', {
            headers: { 'Authorization': `Bearer ${AUTH_TOKEN}` }
        });
        const data = await res.json();
        if (res.ok) {
            CURRENT_USER = data.usuario;
            applyUserNavigationPermissions();
        } else {
            AUTH_TOKEN = null;
            localStorage.removeItem('sentinelpro_token');
        }
    } catch {
        AUTH_TOKEN = null;
        localStorage.removeItem('sentinelpro_token');
    }
}

async function logoutAdmin() {
    try {
        if (AUTH_TOKEN) {
            await fetch('/api/auth/logout', {
                method: 'POST',
                headers: { 'Authorization': `Bearer ${AUTH_TOKEN}` }
            });
        }
    } finally {
        AUTH_TOKEN = null;
        CURRENT_USER = null;
        localStorage.removeItem('sentinelpro_token');
        document.getElementById('admin-login-card').classList.remove('hidden');
        document.getElementById('admin-workspace').classList.add('hidden');
    }
}

// Ocultamiento / Muestra reactiva de pestañas en el Sidebar según permisos_mapa del usuario
function applyUserNavigationPermissions() {
    if (!CURRENT_USER) return;

    // Perfil en el Sidebar
    document.getElementById('sidebar-user-name').textContent = CURRENT_USER.nombre_completo;
    document.getElementById('sidebar-user-role').textContent = CURRENT_USER.rol_nombre || CURRENT_USER.rol;
    document.getElementById('sidebar-user-role').style.backgroundColor = CURRENT_USER.rol_color || '#3730a3';
    document.getElementById('sidebar-avatar').textContent = (CURRENT_USER.nombre_completo || 'U')[0].toUpperCase();
    document.getElementById('sidebar-perm-count').textContent = `${CURRENT_USER.permisos_lista?.length || 0} permisos activos`;

    // Barra superior
    document.getElementById('bar-user-email').textContent = CURRENT_USER.email;
    document.getElementById('bar-user-role').textContent = CURRENT_USER.rol_nombre || CURRENT_USER.rol;

    const perms = CURRENT_USER.permisos_mapa || {};
    const navButtons = document.querySelectorAll('.nav-tab-btn');
    let firstVisibleTab = null;

    navButtons.forEach(btn => {
        const reqPerm = btn.getAttribute('data-perm');
        // Si el usuario tiene el permiso, mostrar botón; de lo contrario, ocultarlo en interfaz
        if (perms[reqPerm]) {
            btn.style.display = 'flex';
            if (!firstVisibleTab) firstVisibleTab = btn.getAttribute('data-tab');
        } else {
            btn.style.display = 'none';
        }
    });

    if (firstVisibleTab) {
        showTab(firstVisibleTab);
    }
}

function showTab(tabId) {
    document.querySelectorAll('.tab-content').forEach(tc => tc.classList.remove('active'));
    document.querySelectorAll('.nav-tab-btn').forEach(tb => tb.classList.remove('active'));

    const targetTab = document.getElementById(tabId);
    if (targetTab) targetTab.classList.add('active');

    const activeBtn = document.querySelector(`.nav-tab-btn[data-tab="${tabId}"]`);
    if (activeBtn) activeBtn.classList.add('active');

    if (tabId === 'tab-iam') {
        loadIamModuleData();
    }
}

// ============================================================================
// 4. CARGA DE DATOS DEL PANEL ADMINISTRATIVO
// ============================================================================
let DASHBOARD_DATA = null;

async function loadAdminDashboardData() {
    if (!AUTH_TOKEN) return;

    try {
        const res = await fetch('/api/admin/dashboard', {
            headers: { 'Authorization': `Bearer ${AUTH_TOKEN}` }
        });
        const data = await res.json();

        if (!res.ok) {
            if (res.status === 401) logoutAdmin();
            return;
        }

        DASHBOARD_DATA = data;

        // Actualizar KPIs
        if (data.kpis) {
            document.getElementById('kpi-en-planta').textContent = data.kpis.en_planta_ahora;
            document.getElementById('kpi-entradas-hoy').textContent = data.kpis.entradas_hoy;
            document.getElementById('kpi-salidas-hoy').textContent = data.kpis.salidas_hoy;
            document.getElementById('kpi-tardanzas-hoy').textContent = data.kpis.tardanzas_hoy;
            document.getElementById('kpi-puntuales-hoy').textContent = `${data.kpis.puntuales_hoy} puntuales`;
            document.getElementById('kpi-visitantes-hoy').textContent = data.kpis.visitantes_en_planta;

            const pct = Math.round((data.kpis.en_planta_ahora / (data.kpis.aforo_maximo || 150)) * 100);
            document.getElementById('kpi-aforo-pct').textContent = `${pct}% de aforo (${data.kpis.aforo_maximo} máx)`;
        }

        renderEnPlantaTable(data.trabajadores_en_planta || []);
        renderGuardConsole(data);
        renderAttendanceTable(data.registros_acceso || []);
        renderWorkersCrudTable(data.trabajadores || []);
        renderVisitorsTable(data.visitantes || []);
        renderZonasTable(data.zonas_acceso || []);
        renderTurnosTable(data.turnos_laborales || []);
        renderAlertasTable(data.incidencias_acceso || []);
        populateConfigForm(data.configuracion_empresa);

    } catch (err) {
        console.error('Error cargando datos del panel:', err);
    }
}

// TAB 1: Tabla de Personal Actualmente en Planta
function renderEnPlantaTable(trabajadores) {
    const tbody = document.querySelector('#table-en-planta tbody');
    document.getElementById('count-en-planta').textContent = trabajadores.length;

    if (!trabajadores.length) {
        tbody.innerHTML = `<tr><td colspan="7" style="text-align:center;color:#64748b;padding:18px;">No hay personal registrado en planta en este momento.</td></tr>`;
        return;
    }

    tbody.innerHTML = trabajadores.map(t => `
        <tr>
            <td><strong>${t.codigo_credencial}</strong></td>
            <td>${t.nombre_completo}</td>
            <td>${t.departamento}</td>
            <td>${t.ultima_entrada || '--'}</td>
            <td>Puerta ${t.ultima_puerta_id || 1}</td>
            <td><span class="badge badge-success">EN PLANTA</span></td>
            <td>
                <button class="btn btn-danger btn-sm" onclick="quickRegisterExitFromTable(${t.id}, '${t.nombre_completo}')">
                    🔴 Fichar Salida
                </button>
            </td>
        </tr>
    `).join('');
}

async function quickRegisterExitFromTable(workerId, name) {
    if (!confirm(`¿Registrar la salida de ${name} en este momento?`)) return;

    try {
        const res = await fetch('/api/admin/porteria/registrar', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${AUTH_TOKEN}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                identificador: workerId,
                tipo_movimiento: 'SALIDA',
                zona_id: 1,
                observacion: 'Salida rápida fichada desde el Monitor de Planta'
            })
        });

        const data = await res.json();
        if (res.ok) {
            alert(data.mensaje);
            loadAdminDashboardData();
        } else {
            alert(data.error || 'No se pudo registrar la salida.');
        }
    } catch {
        alert('Error de conexión.');
    }
}

// TAB 2: Consola de Portería (Vigilante)
function renderGuardConsole(data) {
    const sel = document.getElementById('guard-puerta-select');
    if (sel && data.zonas_acceso) {
        sel.innerHTML = data.zonas_acceso.map(z => `
            <option value="${z.id}">${z.codigo}: ${z.nombre} (${z.nivel_seguridad})</option>
        `).join('');
    }

    // Tabla de movimientos recientes
    const tbody = document.querySelector('#table-guard-recent tbody');
    const recents = (data.registros_acceso || []).slice(0, 6);

    if (!recents.length) {
        tbody.innerHTML = `<tr><td colspan="5" style="text-align:center;color:#64748b;">Sin movimientos registrados hoy.</td></tr>`;
        return;
    }

    tbody.innerHTML = recents.map(r => `
        <tr>
            <td><strong>${r.hora_salida ? r.hora_salida : r.hora_entrada}</strong></td>
            <td>${r.hora_salida ? '<span class="badge badge-danger">SALIDA</span>' : '<span class="badge badge-success">ENTRADA</span>'}</td>
            <td>${r.trabajador_nombre}</td>
            <td>${r.zona_nombre.split('(')[0]}</td>
            <td>${r.estado_asistencia === 'PUNTUAL' ? '<span class="badge badge-success">Puntual</span>' : '<span class="badge badge-warning">Tardanza</span>'}</td>
        </tr>
    `).join('');
}

function searchWorkerInGuard() {
    const q = document.getElementById('guard-worker-search').value.trim().toUpperCase();
    const preview = document.getElementById('guard-worker-preview');
    const feedback = document.getElementById('guard-feedback');

    feedback.classList.add('hidden');
    if (!q || !DASHBOARD_DATA || !DASHBOARD_DATA.trabajadores) return;

    const trab = DASHBOARD_DATA.trabajadores.find(t => 
        String(t.codigo_credencial).toUpperCase() === q ||
        String(t.documento).toUpperCase() === q ||
        t.nombre_completo.toUpperCase().includes(q)
    );

    if (!trab) {
        preview.classList.add('hidden');
        showFeedback(feedback, `No se encontró ningún trabajador con "${q}".`, 'error');
        SELECTED_GUARD_WORKER = null;
        return;
    }

    SELECTED_GUARD_WORKER = trab;
    document.getElementById('prev-name').textContent = `${trab.nombre_completo} (${trab.codigo_credencial})`;
    document.getElementById('prev-state').textContent = trab.estado;
    document.getElementById('prev-state').className = trab.estado === 'ACTIVO' ? 'badge badge-success' : 'badge badge-danger';
    document.getElementById('prev-cargo').textContent = trab.cargo;
    document.getElementById('prev-depto').textContent = trab.departamento;
    document.getElementById('prev-location').textContent = trab.ubicacion_actual === 'DENTRO_PLANTA' ? 'DENTRO DE LA EMPRESA' : 'FUERA DE PLANTA';
    document.getElementById('prev-zones').textContent = `Puertas [${(trab.zonas_autorizadas || []).join(', ')}]`;

    // Alternar visibilidad de botones según estado actual
    document.getElementById('btn-guard-in').disabled = trab.ubicacion_actual === 'DENTRO_PLANTA';
    document.getElementById('btn-guard-out').disabled = trab.ubicacion_actual !== 'DENTRO_PLANTA';

    preview.classList.remove('hidden');
}

async function executeGuardAction(tipo) {
    if (!SELECTED_GUARD_WORKER) return;

    const puertaId = document.getElementById('guard-puerta-select').value;
    const feedback = document.getElementById('guard-feedback');

    try {
        const res = await fetch('/api/admin/porteria/registrar', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${AUTH_TOKEN}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                identificador: SELECTED_GUARD_WORKER.id,
                tipo_movimiento: tipo,
                zona_id: Number(puertaId) || 1,
                observacion: `Marcación validada por el Vigilante en garita`
            })
        });

        const data = await res.json();

        if (res.ok) {
            showFeedback(feedback, data.mensaje, 'success');
            document.getElementById('guard-worker-preview').classList.add('hidden');
            document.getElementById('guard-worker-search').value = '';
            SELECTED_GUARD_WORKER = null;
            loadAdminDashboardData();
        } else {
            showFeedback(feedback, data.error || 'Operación bloqueada por el servidor.', 'error');
        }
    } catch {
        showFeedback(feedback, 'Error de conexión con el servidor.', 'error');
    }
}

// TAB 3: Historial de Asistencia y Reporte CSV
function renderAttendanceTable(registros) {
    const tbody = document.querySelector('#table-attendance-full tbody');
    if (!registros.length) {
        tbody.innerHTML = `<tr><td colspan="10" style="text-align:center;color:#64748b;">No hay registros de asistencia en la base de datos.</td></tr>`;
        return;
    }

    tbody.innerHTML = registros.map(r => `
        <tr>
            <td><strong>${r.codigo_movimiento}</strong></td>
            <td>${r.fecha}</td>
            <td>${r.trabajador_nombre} <small>(${r.codigo_credencial})</small></td>
            <td>${r.departamento}</td>
            <td>${r.zona_nombre.split('(')[0]}</td>
            <td><span style="color:#166534;font-weight:700;">${r.hora_entrada}</span></td>
            <td><span style="color:#991b1b;font-weight:700;">${r.hora_salida || '--'}</span></td>
            <td>${r.horas_formateadas}</td>
            <td>${r.estado_asistencia === 'PUNTUAL' ? '<span class="badge badge-success">PUNTUAL</span>' : '<span class="badge badge-warning">TARDANZA</span>'}</td>
            <td><small>${r.registrado_por_nombre}</small></td>
        </tr>
    `).join('');
}

function exportAttendanceCsv() {
    if (!DASHBOARD_DATA || !DASHBOARD_DATA.registros_acceso || !DASHBOARD_DATA.registros_acceso.length) {
        alert('No hay datos para exportar.');
        return;
    }

    const headers = ['Codigo', 'Fecha', 'Trabajador', 'Credencial', 'Documento', 'Departamento', 'Puerta', 'HoraEntrada', 'HoraSalida', 'HorasTrabajadas', 'Puntualidad', 'Vigilante'];
    const rows = DASHBOARD_DATA.registros_acceso.map(r => [
        r.codigo_movimiento,
        r.fecha,
        `"${r.trabajador_nombre}"`,
        r.codigo_credencial,
        r.documento,
        `"${r.departamento}"`,
        `"${r.zona_nombre}"`,
        r.hora_entrada,
        r.hora_salida || '',
        `"${r.horas_formateadas}"`,
        r.estado_asistencia,
        `"${r.registrado_por_nombre}"`
    ]);

    const csvContent = "data:text/csv;charset=utf-8," + [headers.join(','), ...rows.map(e => e.join(','))].join('\n');
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement('a');
    link.setAttribute('href', encodedUri);
    link.setAttribute('download', `SentinelPro_Reporte_Asistencia_${new Date().toISOString().slice(0, 10)}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// TAB 4: Trabajadores (RR.HH.)
function renderWorkersCrudTable(trabajadores) {
    const tbody = document.querySelector('#table-workers-crud tbody');
    if (!trabajadores.length) {
        tbody.innerHTML = `<tr><td colspan="8" style="text-align:center;color:#64748b;">No hay trabajadores dados de alta.</td></tr>`;
        return;
    }

    tbody.innerHTML = trabajadores.map(t => {
        const isActivo = t.estado === 'ACTIVO';
        const toggleBtn = isActivo 
            ? `<button class="btn btn-warning btn-sm" onclick="toggleWorkerStatus(${t.id}, 'SUSPENDIDO')">⏸️ Suspender Acceso</button>`
            : `<button class="btn btn-success btn-sm" onclick="toggleWorkerStatus(${t.id}, 'ACTIVO')">▶️ Reactivar</button>`;

        return `
            <tr>
                <td><strong>${t.codigo_credencial}</strong></td>
                <td>${t.documento}</td>
                <td>${t.nombre_completo}</td>
                <td>${t.cargo} <br><small style="color:#64748b;">${t.departamento}</small></td>
                <td>Turno ${t.turno_id || 1}</td>
                <td>Puertas: [${(t.zonas_autorizadas || []).join(', ')}]</td>
                <td>${isActivo ? '<span class="badge badge-success">ACTIVO</span>' : '<span class="badge badge-danger">SUSPENDIDO</span>'}</td>
                <td>${toggleBtn}</td>
            </tr>
        `;
    }).join('');
}

async function toggleWorkerStatus(id, newStatus) {
    try {
        const res = await fetch(`/api/admin/trabajadores/${id}`, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${AUTH_TOKEN}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ estado: newStatus })
        });

        const data = await res.json();
        if (res.ok) {
            alert(data.mensaje);
            loadAdminDashboardData();
        } else {
            alert(data.error || 'Error al actualizar estado.');
        }
    } catch {
        alert('Error de conexión.');
    }
}

// Modal Nuevo Trabajador
function openNewWorkerModal() {
    if (!DASHBOARD_DATA) return;
    const selTurno = document.getElementById('mw-turno');
    selTurno.innerHTML = (DASHBOARD_DATA.turnos_laborales || []).map(tn => `
        <option value="${tn.id}">${tn.nombre} (${tn.hora_entrada} - ${tn.hora_salida})</option>
    `).join('');

    const chkZonas = document.getElementById('mw-zones-checkboxes');
    chkZonas.innerHTML = (DASHBOARD_DATA.zonas_acceso || []).map(z => `
        <label class="checkbox-item">
            <input type="checkbox" name="mw_zone" value="${z.id}" checked>
            <span>${z.codigo} (${z.nombre.split('(')[0]})</span>
        </label>
    `).join('');

    document.getElementById('modal-new-worker').classList.remove('hidden');
}

function closeNewWorkerModal() {
    document.getElementById('modal-new-worker').classList.add('hidden');
}

async function saveNewWorker() {
    const name = document.getElementById('mw-name').value.trim();
    const doc = document.getElementById('mw-doc').value.trim();
    const code = document.getElementById('mw-code').value.trim();
    const cargo = document.getElementById('mw-cargo').value.trim();
    const depto = document.getElementById('mw-depto').value.trim();
    const turnoId = document.getElementById('mw-turno').value;
    const estado = document.getElementById('mw-estado').value;

    const selectedZones = Array.from(document.querySelectorAll('input[name="mw_zone"]:checked')).map(cb => Number(cb.value));

    if (!name || !doc) {
        alert('Nombre completo y documento son obligatorios.');
        return;
    }

    try {
        const res = await fetch('/api/admin/trabajadores', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${AUTH_TOKEN}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                nombre_completo: name,
                documento: doc,
                codigo_credencial: code || undefined,
                cargo,
                departamento: depto,
                turno_id: turnoId,
                zonas_autorizadas: selectedZones,
                estado
            })
        });

        const data = await res.json();
        if (res.ok) {
            alert(data.mensaje);
            closeNewWorkerModal();
            loadAdminDashboardData();
        } else {
            alert(data.error || 'No se pudo crear el trabajador.');
        }
    } catch {
        alert('Error de conexión.');
    }
}

// TAB 5: Visitantes
function renderVisitorsTable(visitantes) {
    const tbody = document.querySelector('#table-visitors tbody');
    if (!visitantes.length) {
        tbody.innerHTML = `<tr><td colspan="8" style="text-align:center;color:#64748b;">No hay visitas registradas hoy.</td></tr>`;
        return;
    }

    tbody.innerHTML = visitantes.map(v => {
        const isInside = v.estado === 'EN_PLANTA';
        const actionBtn = isInside 
            ? `<button class="btn btn-warning btn-sm" onclick="markVisitorExit(${v.id}, '${v.nombre_completo}')">🔴 Salida</button>`
            : `<span style="color:#64748b;font-size:0.8rem;">Finalizada</span>`;

        return `
            <tr>
                <td><strong>${v.gafete}</strong></td>
                <td>${v.nombre_completo} <br><small>${v.documento}</small></td>
                <td>${v.empresa_origen}</td>
                <td>${v.anfitrion_visitado}</td>
                <td>${v.hora_entrada}</td>
                <td>${v.hora_salida || '--'}</td>
                <td>${isInside ? '<span class="badge badge-info">EN PLANTA</span>' : '<span class="badge badge-neutral">SALIDA REGISTRADA</span>'}</td>
                <td>${actionBtn}</td>
            </tr>
        `;
    }).join('');
}

function openNewVisitorModal() {
    document.getElementById('modal-new-visitor').classList.remove('hidden');
}

function closeNewVisitorModal() {
    document.getElementById('modal-new-visitor').classList.add('hidden');
}

async function saveNewVisitor() {
    const name = document.getElementById('mvis-name').value.trim();
    const doc = document.getElementById('mvis-doc').value.trim();
    const empresa = document.getElementById('mvis-empresa').value.trim();
    const host = document.getElementById('mvis-host').value.trim();
    const gafete = document.getElementById('mvis-gafete').value.trim();
    const motivo = document.getElementById('mvis-motivo').value.trim();

    if (!name || !doc || !host) {
        alert('Nombre, documento y anfitrión son obligatorios.');
        return;
    }

    try {
        const res = await fetch('/api/admin/visitantes', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${AUTH_TOKEN}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                nombre_completo: name,
                documento: doc,
                empresa_origen: empresa,
                anfitrion_visitado: host,
                gafete: gafete || undefined,
                motivo
            })
        });

        const data = await res.json();
        if (res.ok) {
            alert(data.mensaje);
            closeNewVisitorModal();
            loadAdminDashboardData();
        } else {
            alert(data.error || 'Error al registrar visita.');
        }
    } catch {
        alert('Error de conexión.');
    }
}

async function markVisitorExit(id, name) {
    if (!confirm(`¿Registrar la salida de ${name} y liberar su gafete?`)) return;

    try {
        const res = await fetch(`/api/admin/visitantes/${id}/salida`, {
            method: 'PATCH',
            headers: { 'Authorization': `Bearer ${AUTH_TOKEN}` }
        });
        const data = await res.json();
        if (res.ok) {
            alert(data.mensaje);
            loadAdminDashboardData();
        } else {
            alert(data.error);
        }
    } catch {
        alert('Error de conexión.');
    }
}

// TAB 6: Puertas y Turnos
function renderZonasTable(zonas) {
    const tbody = document.querySelector('#table-zonas tbody');
    tbody.innerHTML = zonas.map(z => `
        <tr>
            <td><strong>${z.codigo}</strong></td>
            <td>${z.nombre}</td>
            <td>${z.nivel_seguridad}</td>
            <td><span class="badge badge-success">${z.estado}</span></td>
        </tr>
    `).join('');
}

function renderTurnosTable(turnos) {
    const tbody = document.querySelector('#table-turnos tbody');
    tbody.innerHTML = turnos.map(tn => `
        <tr>
            <td><strong>${tn.nombre}</strong></td>
            <td>${tn.hora_entrada} a ${tn.hora_salida}</td>
            <td>${tn.tolerancia_minutos} minutos</td>
        </tr>
    `).join('');
}

// TAB 7: Alertas de Acceso Físico
function renderAlertasTable(alertas) {
    const tbody = document.querySelector('#table-alertas tbody');
    if (!alertas.length) {
        tbody.innerHTML = `<tr><td colspan="8" style="text-align:center;color:#64748b;">No hay alertas de acceso denegado registradas.</td></tr>`;
        return;
    }

    tbody.innerHTML = alertas.map(a => {
        const isPend = a.estado_resolucion === 'PENDIENTE';
        const resBtn = isPend 
            ? `<button class="btn btn-secondary btn-sm" onclick="resolveAlert(${a.id})">Resolver</button>`
            : `<span style="color:#166534;font-size:0.8rem;">Resuelta</span>`;

        return `
            <tr>
                <td><strong>${a.fecha_hora}</strong></td>
                <td>${a.trabajador_nombre}</td>
                <td>${a.zona_nombre.split('(')[0]}</td>
                <td><span class="badge badge-danger">${a.tipo_alerta}</span></td>
                <td>${a.severidad}</td>
                <td style="max-width:260px;font-size:0.82rem;">${a.detalle}</td>
                <td>${isPend ? '<span class="badge badge-warning">PENDIENTE</span>' : '<span class="badge badge-success">RESUELTA</span>'}</td>
                <td>${resBtn}</td>
            </tr>
        `;
    }).join('');
}

async function resolveAlert(id) {
    const nota = prompt('Ingresa una justificación u observación para cerrar la alerta:');
    if (nota === null) return;

    try {
        const res = await fetch(`/api/admin/incidencias/${id}`, {
            method: 'PATCH',
            headers: {
                'Authorization': `Bearer ${AUTH_TOKEN}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ nota_resolucion: nota })
        });
        const data = await res.json();
        if (res.ok) {
            alert(data.mensaje);
            loadAdminDashboardData();
        } else {
            alert(data.error);
        }
    } catch {
        alert('Error de conexión.');
    }
}

// ============================================================================
// 5. CENTRO DE CONTROL DE ACCESO IAM (ROLES, MATRIZ ALLOW/DENY, SESIONES, AUDIT)
// ============================================================================
let IAM_STATE = null;

async function loadIamModuleData() {
    if (!AUTH_TOKEN) return;

    try {
        const res = await fetch('/api/admin/seguridad/estado', {
            headers: { 'Authorization': `Bearer ${AUTH_TOKEN}` }
        });
        const data = await res.json();
        if (!res.ok) return;

        IAM_STATE = data;

        // Llenar selector de usuarios IAM
        const picker = document.getElementById('iam-user-picker');
        picker.innerHTML = data.usuarios.map(u => `
            <option value="${u.id}">${u.nombre_completo} (${u.email}) [${u.rol}]</option>
        `).join('');

        if (!SELECTED_IAM_USER_ID && data.usuarios.length) {
            SELECTED_IAM_USER_ID = data.usuarios[0].id;
        }

        picker.value = SELECTED_IAM_USER_ID;
        loadUserPermissionMatrix();
        renderIamSessionsTable(data.sesiones_activas || []);
        renderIamLogsTable(data.audit_logs || []);

    } catch (err) {
        console.error('Error cargando IAM:', err);
    }
}

function loadUserPermissionMatrix() {
    if (!IAM_STATE) return;

    const userId = Number(document.getElementById('iam-user-picker').value);
    SELECTED_IAM_USER_ID = userId;
    const user = IAM_STATE.usuarios.find(u => Number(u.id) === userId);
    if (!user) return;

    // Banner de usuario seleccionado
    const banner = document.getElementById('matrix-user-banner');
    banner.innerHTML = `
        <div style="display:flex;justify-content:space-between;align-items:center;">
            <div>
                <strong>${user.nombre_completo}</strong> (${user.email}) | 
                <strong>Rol Base:</strong> <span class="badge" style="background:${user.rol_color || '#3730a3'};color:#fff;">${user.rol_nombre || user.rol}</span> |
                <strong>Límite de Sesiones:</strong> ${user.max_sesiones_simultaneas}
            </div>
            <div>
                <span style="font-size:0.82rem;color:#475569;">Permisos Efectivos: <strong>${user.permisos_lista?.length || 0} de 18</strong></span>
            </div>
        </div>
    `;

    // Tabla de la Matriz de Permisos
    const tbody = document.querySelector('#table-perm-matrix tbody');
    tbody.innerHTML = (user.desglose_permisos || []).map(p => {
        const ovState = p.override_individual || 'INHERIT';
        const isAllow = ovState === 'ALLOW';
        const isDeny = ovState === 'DENY';
        const isInherit = ovState === 'INHERIT';

        return `
            <tr>
                <td><code>${p.codigo}</code></td>
                <td><strong>${p.modulo}</strong></td>
                <td>${p.nombre}</td>
                <td>${p.heredado_del_rol ? '✓ Sí' : '✕ No'}</td>
                <td>
                    ${isAllow ? '<span class="badge badge-success">+ ALLOW</span>' : ''}
                    ${isDeny ? '<span class="badge badge-danger">- DENY</span>' : ''}
                    ${isInherit ? '<span class="badge badge-neutral">Hereda Rol</span>' : ''}
                </td>
                <td>
                    ${p.concedido_efectivo 
                        ? '<span style="color:#166534;font-weight:700;">🟢 AUTORIZADO</span>' 
                        : '<span style="color:#991b1b;font-weight:700;">🔴 DENEGADO</span>'}
                </td>
                <td>
                    <div class="matrix-btn-group">
                        <button class="btn-matrix ${isInherit ? 'active-inherit' : ''}" onclick="setIndividualPermission(${user.id}, '${p.codigo}', 'INHERIT')">
                            Heredar Rol
                        </button>
                        <button class="btn-matrix ${isAllow ? 'active-allow' : ''}" onclick="setIndividualPermission(${user.id}, '${p.codigo}', 'ALLOW')">
                            + Permitir (ALLOW)
                        </button>
                        <button class="btn-matrix ${isDeny ? 'active-deny' : ''}" onclick="setIndividualPermission(${user.id}, '${p.codigo}', 'DENY')">
                            - Denegar (DENY)
                        </button>
                    </div>
                </td>
            </tr>
        `;
    }).join('');
}

async function setIndividualPermission(userId, permisoCodigo, modo) {
    try {
        const res = await fetch(`/api/admin/seguridad/usuarios/${userId}/permiso-individual`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${AUTH_TOKEN}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                permiso_codigo: permisoCodigo,
                modo
            })
        });

        const data = await res.json();
        if (res.ok) {
            // Si el usuario modificado es el usuario actualmente en sesión, actualizar sus permisos reactivamente
            if (CURRENT_USER && Number(CURRENT_USER.id) === Number(userId)) {
                CURRENT_USER = data.usuario;
                applyUserNavigationPermissions();
            }
            await loadIamModuleData();
        } else {
            alert(data.error || 'Error al cambiar permiso.');
        }
    } catch {
        alert('Error de conexión.');
    }
}

// Sesiones Activas
function renderIamSessionsTable(sesiones) {
    const tbody = document.querySelector('#table-iam-sessions tbody');
    if (!sesiones.length) {
        tbody.innerHTML = `<tr><td colspan="5" style="text-align:center;color:#64748b;">No hay sesiones activas.</td></tr>`;
        return;
    }

    tbody.innerHTML = sesiones.map(s => `
        <tr>
            <td>${s.usuario_email}</td>
            <td><span class="badge badge-neutral">${s.rol}</span></td>
            <td><small>${s.ip}</small></td>
            <td><small>${s.creada_en.slice(11, 19)}</small></td>
            <td>
                <button class="btn btn-danger btn-sm" onclick="revokeSession('${s.session_id}')">
                    Revocar
                </button>
            </td>
        </tr>
    `).join('');
}

async function revokeSession(sid) {
    if (!confirm('¿Cerrar forzosamente esta sesión activa?')) return;

    try {
        const res = await fetch(`/api/admin/seguridad/sesiones/${encodeURIComponent(sid)}`, {
            method: 'DELETE',
            headers: { 'Authorization': `Bearer ${AUTH_TOKEN}` }
        });
        const data = await res.json();
        if (res.ok) {
            alert(data.mensaje);
            loadIamModuleData();
        } else {
            alert(data.error);
        }
    } catch {
        alert('Error de conexión.');
    }
}

// Bitácora de Auditoría
function renderIamLogsTable(logs) {
    const tbody = document.querySelector('#table-iam-logs tbody');
    tbody.innerHTML = logs.slice(0, 15).map(l => `
        <tr>
            <td><small>${l.fecha_hora.slice(11, 19)}</small></td>
            <td><strong>${l.evento}</strong></td>
            <td>${l.usuario_email}</td>
            <td>${l.resultado === 'EXITO' ? '<span class="badge badge-success">EXITO</span>' : '<span class="badge badge-danger">DENEGADO</span>'}</td>
            <td style="max-width:240px;font-size:0.78rem;">${l.detalle}</td>
        </tr>
    `).join('');
}

// Modal Ver Mis Permisos
function openMyPermsModal() {
    if (!CURRENT_USER) return;
    document.getElementById('my-perms-meta').textContent = `Usuario: ${CURRENT_USER.nombre_completo} (${CURRENT_USER.email}) — Rol: ${CURRENT_USER.rol_nombre || CURRENT_USER.rol}`;
    const tbody = document.querySelector('#table-my-perms-breakdown tbody');

    tbody.innerHTML = (CURRENT_USER.desglose_permisos || []).map(p => `
        <tr>
            <td><code>${p.codigo}</code></td>
            <td>${p.modulo}</td>
            <td>${p.heredado_del_rol ? '✓ Sí' : '✕ No'}</td>
            <td>${p.override_individual || 'INHERIT'}</td>
            <td>${p.concedido_efectivo ? '🟢 AUTORIZADO' : '🔴 DENEGADO'}</td>
        </tr>
    `).join('');

    document.getElementById('modal-my-perms').classList.remove('hidden');
}

function closeMyPermsModal() {
    document.getElementById('modal-my-perms').classList.add('hidden');
}

// Simular Petición 403 en Servidor
async function simulate403BackendTest() {
    try {
        // Intenta invocar la creación de un usuario IAM o una zona sin tener el permiso
        const res = await fetch('/api/admin/seguridad/usuarios', {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${AUTH_TOKEN}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ nombre_completo: 'Intruso Test', email: 'test@hack.com', password: '123' })
        });
        const data = await res.json();
        alert(`Respuesta del Servidor (Código HTTP ${res.status}):\n${JSON.stringify(data, null, 2)}`);
    } catch {
        alert('Error ejecutando la prueba.');
    }
}

// Configuración Corporativa
function populateConfigForm(cfg) {
    if (!cfg) return;
    document.getElementById('cfg-nombre').value = cfg.nombre_empresa || '';
    document.getElementById('cfg-nit').value = cfg.nit_ruc || '';
    document.getElementById('cfg-dir').value = cfg.direccion || '';
    document.getElementById('cfg-aforo').value = cfg.aforo_maximo_planta || 150;
    document.getElementById('cfg-tolerancia').value = cfg.tolerancia_tardanza_min || 10;
}

async function saveCompanyConfig() {
    const nombre = document.getElementById('cfg-nombre').value.trim();
    const nit = document.getElementById('cfg-nit').value.trim();
    const dir = document.getElementById('cfg-dir').value.trim();
    const aforo = Number(document.getElementById('cfg-aforo').value);
    const tolerancia = Number(document.getElementById('cfg-tolerancia').value);

    try {
        const res = await fetch('/api/admin/configuracion', {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${AUTH_TOKEN}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                nombre_empresa: nombre,
                nit_ruc: nit,
                direccion: dir,
                aforo_maximo_planta: aforo,
                tolerancia_tardanza_min: tolerancia
            })
        });

        const data = await res.json();
        if (res.ok) {
            alert(data.mensaje);
            loadAdminDashboardData();
        } else {
            alert(data.error);
        }
    } catch {
        alert('Error de conexión.');
    }
}
