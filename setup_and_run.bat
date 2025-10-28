@echo off
echo Human Detection in Disaster Scenarios - Setup and Run Script
echo ==========================================================

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed or not in PATH
    echo Please install Python 3.7 or higher
    pause
    exit /b 1
)

echo Python found. Checking for pip...
python -m pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo pip is not installed
    echo Installing pip...
    python -m ensurepip --upgrade
)

echo Installing required dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo Failed to install dependencies
    pause
    exit /b 1
)

echo Dependencies installed successfully!

echo.
echo Running complete pipeline...
echo This will:
echo  1. Analyze the dataset
echo  2. Train the human detection model
echo  3. Evaluate the trained model
echo  4. Setup inference capabilities
echo.
echo Note: Training may take several hours depending on your hardware
echo.

python run_complete_pipeline.py

echo.
echo Pipeline execution completed!
echo Check the generated files and reports for results
echo.

pause