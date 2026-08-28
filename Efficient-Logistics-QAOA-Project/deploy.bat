@echo off
REM Quantum Logistics Optimizer - Windows Deployment Script

echo ========================================
echo Quantum Logistics Optimizer
echo Deployment Script for Windows
echo ========================================
echo.

:menu
echo Select deployment platform:
echo 1. Streamlit Cloud (Recommended)
echo 2. Docker (Local)
echo 3. View Deployment Guide
echo 4. Exit
echo.
set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto streamlit
if "%choice%"=="2" goto docker
if "%choice%"=="3" goto guide
if "%choice%"=="4" goto end
echo Invalid choice!
goto menu

:streamlit
echo.
echo ========================================
echo Streamlit Cloud Deployment
echo ========================================
echo.
echo Steps to deploy on Streamlit Cloud:
echo.
echo 1. Push your code to GitHub:
echo    git add .
echo    git commit -m "Prepare for deployment"
echo    git push origin main
echo.
echo 2. Go to https://share.streamlit.io
echo 3. Sign in with GitHub
echo 4. Click 'New app'
echo 5. Select your repository
echo 6. Set main file path: frontend/streamlit_app.py
echo 7. Click 'Deploy'
echo.
echo Configuration files are ready!
echo.
pause
goto end

:docker
echo.
echo ========================================
echo Docker Deployment
echo ========================================
echo.
echo Checking for Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo Docker not found!
    echo Please install Docker Desktop from:
    echo https://docs.docker.com/desktop/install/windows-install/
    pause
    goto end
)

echo Docker found!
echo.
echo Building Docker image...
docker build -f Dockerfile.streamlit -t quantum-logistics:latest .

if errorlevel 1 (
    echo Build failed!
    pause
    goto end
)

echo.
echo Running container...
docker run -d -p 8501:8501 --name quantum-app quantum-logistics:latest

if errorlevel 1 (
    echo Failed to start container!
    pause
    goto end
)

echo.
echo ========================================
echo Container started successfully!
echo ========================================
echo.
echo Access your app at: http://localhost:8501
echo.
echo Useful commands:
echo   View logs: docker logs quantum-app
echo   Stop: docker stop quantum-app
echo   Remove: docker rm quantum-app
echo.
pause
goto end

:guide
echo.
echo Opening deployment guide...
start DEPLOYMENT_GUIDE.md
goto end

:end
echo.
echo Done!
pause
