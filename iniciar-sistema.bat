@echo off
title SentinelPro IAM — Suite de Control de Acceso Granular y Gestion Operativa
echo ======================================================================
echo   Iniciando SentinelPro IAM (Servidor Web + Control de Acceso RBAC)...
echo   Abriendo http://localhost:3450 en tu navegador...
echo ======================================================================
cd /d "%~dp0"
start "" "http://localhost:3450"
node server/server.js
pause
