import sys
import os
from cx_Freeze import setup, Executable

# Caminho absoluto das .ui
include_files = [
    "Projeto_CadastroQT.ui",
    "RelatoriosClientes.ui",
    "Alterar.ui"
]

# Opções de build
build_exe_options = {
    "packages": ["os", "sys", "mysql.connector", "PyQt5.QtWidgets", "PyQt5.uic"],
    "include_files": include_files
}

# Base para remover console no Windows
base = None
if sys.platform == "win32":
    base = "Win32GUI"  # remove console mesmo no Windows 64-bit

setup(
    name="PROJETO_python+SQL+QT_programacao",
    version="1.0",
    description="Sistema de cadastro com Qt e MySQL",
    options={"build_exe": build_exe_options},
    executables=[
    Executable(
        "ProjetoFinal.py",
        base=base,
        icon="icone REal.ico"
    )
]


)
