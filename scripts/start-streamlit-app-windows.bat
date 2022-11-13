set file_path=%~dp0
echo %~dp0
set PYTHONPATH=%PYTHONPATH%;%file_path%;

streamlit run app.py