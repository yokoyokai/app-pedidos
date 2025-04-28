@echo off
cd /d %~dp0
git add .
git commit -m "Actualización"
git push
pause
