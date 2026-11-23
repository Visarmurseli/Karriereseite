@echo off
title GMX Multi-Account Bewerbungs-Sync
cd /d "%~dp0"
echo ============================================================
echo   Starte GMX Multi-Account Bewerbungs-Synchronisation...
echo ============================================================
echo.
python scripts\dump_all_emails.py
python scripts\update_bewerbungsverlauf_excel.py
echo.
echo ============================================================
echo   Synchronisation erfolgreich abgeschlossen!
echo   Bewerbungsverlauf.xlsx und Obsidian Cockpit sind aktuell.
echo ============================================================
pause
