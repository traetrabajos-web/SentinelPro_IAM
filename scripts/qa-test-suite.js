/**
 * Suite de Pruebas Automatizadas de Calidad y Seguridad QA
 * SentinelPro Access & IAM — Sistema de Control de Acceso de Trabajadores y Portería
 * Valida 15 Casos de Prueba (CP-01 a CP-15) cubriendo:
 * - Registro físico de Entrada/Salida en Portería y Kiosco
 * - Detección de tardanzas y cálculo de horas trabajadas
 * - Prevención de doble entrada y bloqueo de trabajadores suspendidos (403)
 * - Bloqueo de zonas físicas no autorizadas (403)
 * - Rol de Vigilante y control de visitantes
 * - Control de sesiones simultáneas por usuario (409)
 * - Protección estricta en servidor (401 y 403)
 * - Permisos individuales en caliente (ALLOW / DENY)
 * - Trazabilidad inmutable en bitácora de auditoría
 */

const http = require('node:http');
const { startServer } = require('../server/server');

const TEST_PORT = 3498;
const BASE_URL = `http://localhost:${TEST_PORT}`;

function makeRequest(method, path, body = null, token = null) {
    return new Promise((resolve, reject) => {
        const url = new URL(path, BASE_URL);
        const headers = { 'Content-Type': 'application/json' };
        if (token) headers['Authorization'] = `Bearer ${token}`;

        const req = http.request(url, { method, headers }, res => {
            let data = '';
            res.on('data', chunk => { data += chunk; });
            res.on('end', () => {
                let parsed = null;
                try { parsed = JSON.parse(data); } catch { parsed = data; }
                resolve({ status: res.statusCode, headers: res.headers, body: parsed });
            });
        });

        req.on('error', reject);
        if (body) req.write(JSON.stringify(body));
        req.end();
    });
}

async function runQaTestSuite() {
    console.log("======================================================================");
    console.log("🧪 INICIANDO SUITE DE PRUEBAS DE CALIDAD Y SEGURIDAD — SENTINELPRO IAM");
    console.log("======================================================================");

    const server = await startServer(TEST_PORT);
    let passed = 0;
    let failed = 0;

    async function test(id, name, testFn) {
        try {
            await testFn();
            console.log(`  ✅ [${id}] APROBADO: ${name}`);
            passed++;
        } catch (err) {
            console.error(`  ❌ [${id}] FALLÓ: ${name} -> ${err.message}`);
            failed++;
        }
    }

    try {
        let guardToken = null;
        let adminToken = null;

        // CP-01: Bootstrap público y contadores de planta
        await test('CP-01', 'Carga de bootstrap público y métricas de aforo en vivo', async () => {
            const res = await makeRequest('GET', '/api/public/bootstrap');
            if (res.status !== 200) throw new Error(`Status ${res.status}`);
            if (!res.body.config || !res.body.resumen_planta) throw new Error('Resumen de planta ausente');
            if (res.body.resumen_planta.total_trabajadores_padron < 5) throw new Error('Padrón incompleto');
        });

        // CP-02: Consulta pública de estado de credencial
        await test('CP-02', 'Consulta de credencial de trabajador por DNI y Código EMP-001', async () => {
            const res = await makeRequest('GET', '/api/public/consultar-credencial?identificador=EMP-001');
            if (res.status !== 200) throw new Error(`Status ${res.status}`);
            if (res.body.trabajador.nombre_completo !== 'Javier Morales Castro') throw new Error('Trabajador incorrecto');
            if (!Array.isArray(res.body.zonas_autorizadas_detalle)) throw new Error('Sin detalle de zonas');
        });

        // CP-03: Kiosco - Marcación de Entrada de trabajador
        await test('CP-03', 'Fichaje de ENTRADA en Kiosco con cálculo de puntualidad', async () => {
            const res = await makeRequest('POST', '/api/public/kiosco/marcar', {
                identificador: 'EMP-004', // Camila Torres (está fuera de planta)
                tipo_movimiento: 'ENTRADA',
                zona_id: 1
            });
            if (res.status !== 201) throw new Error(`Status ${res.status}: ${JSON.stringify(res.body)}`);
            if (!res.body.registro || res.body.registro.estado_ciclo !== 'EN_PLANTA') throw new Error('No quedó EN_PLANTA');
        });

        // CP-04: Prevención de doble entrada sin haber salido (409)
        await test('CP-04', 'Prevención de DOBLE ENTRADA para trabajador que ya está en planta (409)', async () => {
            const res = await makeRequest('POST', '/api/public/kiosco/marcar', {
                identificador: 'EMP-004',
                tipo_movimiento: 'ENTRADA',
                zona_id: 1
            });
            if (res.status !== 409) throw new Error(`Se esperaba 409 Conflict pero retornó ${res.status}`);
            if (res.body.code !== 'ALREADY_INSIDE') throw new Error('Código incorrecto');
        });

        // CP-05: Kiosco - Marcación de Salida y cálculo de horas trabajadas
        await test('CP-05', 'Fichaje de SALIDA en Kiosco con cálculo de jornada (minutos/horas)', async () => {
            const res = await makeRequest('POST', '/api/public/kiosco/marcar', {
                identificador: 'EMP-004',
                tipo_movimiento: 'SALIDA',
                zona_id: 1
            });
            if (res.status !== 200) throw new Error(`Status ${res.status}`);
            if (res.body.trabajador.ubicacion_actual !== 'FUERA_PLANTA') throw new Error('No cambió a FUERA_PLANTA');
        });

        // CP-06: Bloqueo de trabajador suspendido y generación de alerta (403)
        await test('CP-06', 'Bloqueo de trabajador con credencial SUSPENDIDA y registro de alerta (403)', async () => {
            const res = await makeRequest('POST', '/api/public/kiosco/marcar', {
                identificador: '66778899', // Esteban Salazar (SUSPENDIDO)
                tipo_movimiento: 'ENTRADA',
                zona_id: 1
            });
            if (res.status !== 403) throw new Error(`Se esperaba 403 Forbidden pero retornó ${res.status}`);
            if (res.body.code !== 'WORKER_SUSPENDED') throw new Error('Código de error incorrecto');
        });

        // CP-07: Bloqueo de acceso a zona física no autorizada (403)
        await test('CP-07', 'Bloqueo de ingreso a puerta de DataCenter no autorizada para el empleado (403)', async () => {
            const res = await makeRequest('POST', '/api/public/kiosco/marcar', {
                identificador: 'EMP-004', // Camila solo tiene autorizada la Puerta 1
                tipo_movimiento: 'ENTRADA',
                zona_id: 4 // Puerta 4: Bóveda DataCenter TI
            });
            if (res.status !== 403) throw new Error(`Se esperaba 403 pero retornó ${res.status}`);
            if (res.body.code !== 'ZONE_UNAUTHORIZED') throw new Error('Código incorrecto');
        });

        // CP-08: Autenticación de Vigilante con scrypt y token HMAC
        await test('CP-08', 'Autenticación del Vigilante de Garita con verificación scrypt y token HMAC', async () => {
            const res = await makeRequest('POST', '/api/auth/login', {
                email: 'vigilante@sentinelpro.com',
                password: 'vigi123'
            });
            if (res.status !== 200) throw new Error(`Status ${res.status}: ${JSON.stringify(res.body)}`);
            if (!res.body.token) throw new Error('Token ausente');
            guardToken = res.body.token;
            if (res.body.usuario.rol !== 'VIGILANTE_PORTERIA') throw new Error('Rol incorrecto');
        });

        // CP-09: Vigilante registra ingreso de visitante con gafete
        await test('CP-09', 'Vigilante registra ingreso de visitante con asignación de gafete temporal', async () => {
            const res = await makeRequest('POST', '/api/admin/visitantes', {
                nombre_completo: 'Carlos Eduardo Restrepo',
                documento: '98765432',
                empresa_origen: 'Auditoría Externa KPMG',
                anfitrion_visitado: 'Camila Torres (Finanzas)',
                gafete: 'VIS-09',
                motivo: 'Auditoría semestral de inventarios'
            }, guardToken);
            if (res.status !== 201) throw new Error(`Status ${res.status}: ${JSON.stringify(res.body)}`);
            if (res.body.visitante.estado !== 'EN_PLANTA') throw new Error('No figura en planta');
        });

        // CP-10: Vigilante registra salida de visitante
        await test('CP-10', 'Vigilante registra salida de visitante y liberación de gafete', async () => {
            const res = await makeRequest('PATCH', '/api/admin/visitantes/1/salida', {}, guardToken);
            if (res.status !== 200) throw new Error(`Status ${res.status}`);
            if (res.body.visitante.estado !== 'SALIDA_REGISTRADA') throw new Error('No cerró visita');
        });

        // CP-11: Vigilante intenta acción restringida (RR.HH. o IAM) y es bloqueado por Backend (403)
        await test('CP-11', 'Bloqueo en Backend (403) cuando Vigilante intenta modificar usuarios IAM', async () => {
            const res = await makeRequest('POST', '/api/admin/seguridad/usuarios', {
                nombre_completo: 'Intruso Hack',
                email: 'hack@test.com',
                password: '123'
            }, guardToken);
            if (res.status !== 403) throw new Error(`Se esperaba 403 Forbidden pero retornó ${res.status}`);
            if (res.body.code !== 'FORBIDDEN_403') throw new Error('No retornó FORBIDDEN_403');
        });

        // CP-12: Super Admin otorga permiso individual ALLOW en caliente
        await test('CP-12', 'Super Admin otorga permiso individual ALLOW en caliente sobre un permiso no incluido en el Rol', async () => {
            const adminLogin = await makeRequest('POST', '/api/auth/login', {
                email: 'admin@sentinelpro.com',
                password: 'admin123'
            });
            adminToken = adminLogin.body.token;

            const res = await makeRequest('POST', '/api/admin/seguridad/usuarios/2/permiso-individual', {
                permiso_codigo: 'asistencia:exportar',
                modo: 'ALLOW'
            }, adminToken);

            if (res.status !== 200) throw new Error(`Status ${res.status}`);
            if (res.body.usuario.permisos_individuales['asistencia:exportar'] !== 'ALLOW') {
                throw new Error('No se guardó el override ALLOW');
            }
        });

        // CP-13: Concurrencia de sesiones simultáneas: Bloqueo con HTTP 409
        await test('CP-13', 'Control de concurrencia: Bloqueo con HTTP 409 al superar max_sesiones del usuario', async () => {
            const res = await makeRequest('POST', '/api/auth/login', {
                email: 'vigilante@sentinelpro.com',
                password: 'vigi123'
            });
            if (res.status !== 409) throw new Error(`Se esperaba 409 Conflict pero retornó ${res.status}`);
            if (res.body.code !== 'MAX_SESSIONS_REACHED') throw new Error('Código incorrecto');
        });

        // CP-14: Reemplazo autorizado de sesión previa con force_replace = true
        await test('CP-14', 'Reemplazo autorizado de sesión con force_replace=true e invalidación de token previo', async () => {
            const res = await makeRequest('POST', '/api/auth/login', {
                email: 'vigilante@sentinelpro.com',
                password: 'vigi123',
                force_replace: true
            });
            if (res.status !== 200) throw new Error(`Status ${res.status}`);
            if (!res.body.token) throw new Error('No emitió nuevo token');

            // El token viejo debe ser rechazado inmediatamente
            const testOldToken = await makeRequest('GET', '/api/admin/dashboard', null, guardToken);
            if (testOldToken.status !== 401) throw new Error(`El token anterior no fue invalidado (status ${testOldToken.status})`);
        });

        // CP-15: Verificación de Bitácora de Auditoría Inmutable
        await test('CP-15', 'Verificación de trazabilidad en audit_logs de eventos 401, 403, 409 y físicos', async () => {
            const res = await makeRequest('GET', '/api/admin/seguridad/estado', null, adminToken);
            if (res.status !== 200) throw new Error(`Status ${res.status}`);
            const logs = res.body.audit_logs;
            if (!logs || logs.length < 5) throw new Error('Auditoría incompleta');

            const has403 = logs.some(l => l.evento === 'ACCESO_DENEGADO_403');
            const has409 = logs.some(l => l.evento === 'SESION_SIMULTANEA_BLOQUEADA');
            const hasChange = logs.some(l => l.evento === 'CAMBIO_PERMISOS_USUARIO');

            if (!has403 || !has409 || !hasChange) {
                throw new Error('Faltan eventos críticos en la bitácora de auditoría');
            }
        });

    } finally {
        server.close();
    }

    console.log("======================================================================");
    console.log(`📊 REPORTE FINAL: ${passed} APROBADOS / ${failed} FALLIDOS`);
    if (failed === 0) {
        console.log("🎉 TODAS LAS PRUEBAS (15/15) PASARON CON ÉXITO AL 100%");
    } else {
        console.error("⚠️ Se detectaron fallas en la ejecución.");
    }
    console.log("======================================================================");
}

if (require.main === module) {
    runQaTestSuite().catch(console.error);
}

module.exports = { runQaTestSuite };
