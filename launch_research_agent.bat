@echo off
echo 🚀 Starting AI Research Agent System
echo =====================================

echo.
echo 📡 Starting FastAPI Backend Server...
start "AI Research API" cmd /k "python main.py"

echo.
echo ⏳ Waiting 5 seconds for API to initialize...
timeout /t 5 /nobreak >nul

echo.
echo 🔬 Starting Research Interface...
start "Research Interface" cmd /k "streamlit run research_interface.py --server.port 8502"

echo.
echo 🎉 AI Research Agent is starting up!
echo =====================================
echo 📍 API Backend:        http://127.0.0.1:8000
echo 📍 Research Interface: http://localhost:8502  
echo 📍 API Documentation:  http://127.0.0.1:8000/docs
echo 📍 Health Check:       http://127.0.0.1:8000/api/health
echo =====================================
echo.
echo ⚡ Quick Test:
echo 1. Visit http://localhost:8502
echo 2. Upload the test_research_data.txt file
echo 3. Ask: "What are the benefits of AI in healthcare?"
echo 4. See your structured research report with citations!
echo.
echo Press any key to open the Research Interface...
pause >nul
start http://localhost:8502

echo.
echo ✅ System launched successfully!
echo Close this window when done (the services will keep running)
pause
