#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para construir o executável do Montador de Imagens
"""

import subprocess
import sys
import os

def build_executable():
    """Constrói o executável usando PyInstaller"""
    
    print("🔨 Construindo executável...")
    print()
    
    # Comando PyInstaller
    cmd = [
        "pyinstaller",
        "--name=MontadorImagens",
        "--onefile",  # Cria um único arquivo executável
        "--windowed",  # Não mostra console (GUI)
        "--hidden-import=tkinter",
        "--hidden-import=PIL",
        "--hidden-import=reportlab",
        "--hidden-import=reportlab.pdfgen",
        "--hidden-import=reportlab.lib.pagesizes",
        "--hidden-import=reportlab.lib.units",
        "montador_imagens.py"
    ]
    
    try:
        subprocess.run(cmd, check=True)
        print()
        print("✅ Executável criado com sucesso!")
        print("📁 Localização: dist/MontadorImagens.exe")
        print()
        print("💡 Dica: Você pode mover o arquivo .exe para onde quiser!")
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao construir executável: {e}")
        sys.exit(1)
    except FileNotFoundError:
        print("❌ PyInstaller não encontrado!")
        print("   Execute: pip install pyinstaller")
        sys.exit(1)

if __name__ == "__main__":
    build_executable()

