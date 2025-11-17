#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Montador de Imagens para PDF A4
Programa para montar 9 imagens em um PDF A4 com layout 3x3
com margens de sangria para guia de corte
"""

import os
import sys
from pathlib import Path
from PIL import Image, ImageDraw
import tkinter as tk
from tkinter import filedialog, messagebox
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
import math

class MontadorImagens:
    def __init__(self):
        # Dimensões em cm
        self.largura_original = 6.85  # cm
        self.altura_original = 9.35  # cm
        self.largura_final = 6.35    # cm (com sangria)
        self.altura_final = 8.89     # cm (com sangria)
        
        # Modo de processamento:
        # "com_sangria": imagens já incluem a margem extra (6,85 x 9,35)
        # "sem_sangria": imagens estão no tamanho final (6,35 x 8,89)
        self.modo = None
        
        # Margem de sangria (diferença entre original e final)
        self.sangria_largura = (self.largura_original - self.largura_final) / 2  # 0.25cm
        self.sangria_altura = (self.altura_original - self.altura_final) / 2     # 0.23cm
        
        # Dimensões da página A4
        self.largura_a4 = 21.0  # cm
        self.altura_a4 = 29.7   # cm
        
        # Margens da página (mínimas para caber na A4)
        self.margem_esquerda = 0.1  # cm
        self.margem_superior = 0.1  # cm
        
        # Espaçamento entre imagens (zero para refiladora)
        self.espacamento = 0.0  # cm
        
    def redimensionar_imagem(self, imagem_path, largura_cm, altura_cm):
        """Redimensiona uma imagem para as dimensões especificadas em cm"""
        try:
            # Abrir imagem
            img = Image.open(imagem_path)
            
            # Converter cm para pixels (assumindo 300 DPI)
            dpi = 300
            largura_px = int(largura_cm * dpi / 2.54)
            altura_px = int(altura_cm * dpi / 2.54)
            
            # Redimensionar mantendo proporção
            img_redimensionada = img.resize((largura_px, altura_px), Image.Resampling.LANCZOS)
            
            return img_redimensionada
        except Exception as e:
            print(f"Erro ao processar {imagem_path}: {e}")
            return None
    
    def compor_imagem_sem_sangria(self, imagem_path):
        """Cria uma imagem 6,85x9,35 cm colocando a arte 6,35x8,89 cm ao centro.
        A arte é ajustada exatamente para 6,35x8,89 cm para garantir medidas de impressão.
        """
        try:
            # Configurações de pixels (300 DPI)
            dpi = 300
            largura_canvas_px = int(self.largura_original * dpi / 2.54)
            altura_canvas_px = int(self.altura_original * dpi / 2.54)
            largura_final_px = int(self.largura_final * dpi / 2.54)
            altura_final_px = int(self.altura_final * dpi / 2.54)

            # Canvas branco tamanho com sangria
            canvas_img = Image.new('RGB', (largura_canvas_px, altura_canvas_px), 'white')

            # Abrir e ajustar a arte para o tamanho final
            img = Image.open(imagem_path)
            img_ajustada = img.resize((largura_final_px, altura_final_px), Image.Resampling.LANCZOS)

            # Centralizar arte no canvas
            x_offset = (largura_canvas_px - largura_final_px) // 2
            y_offset = (altura_canvas_px - altura_final_px) // 2
            canvas_img.paste(img_ajustada, (x_offset, y_offset))

            # Adicionar linhas de guia (mesmo método)
            canvas_img = self.adicionar_linhas_guia(canvas_img)

            return canvas_img
        except Exception as e:
            print(f"Erro ao compor imagem sem sangria: {e}")
            return None
    
    
    def adicionar_linhas_guia(self, imagem):
        """Adiciona linhas de guia para corte"""
        
        draw = ImageDraw.Draw(imagem)
        
        # Dimensões em pixels
        largura_px = imagem.width
        altura_px = imagem.height
        
        # Calcular posições das linhas de guia (área de corte 6,35cm x 8,89cm)
        # Margem de sangria em pixels
        sangria_largura_px = int(self.sangria_largura * 300 / 2.54)
        sangria_altura_px = int(self.sangria_altura * 300 / 2.54)
        
        # Linhas de guia (bordas da área de corte)
        # Linha superior
        y_guia_superior = sangria_altura_px
        draw.line([(0, y_guia_superior), (largura_px, y_guia_superior)], fill='red', width=2)
        
        # Linha inferior
        y_guia_inferior = altura_px - sangria_altura_px
        draw.line([(0, y_guia_inferior), (largura_px, y_guia_inferior)], fill='red', width=2)
        
        # Linha esquerda
        x_guia_esquerda = sangria_largura_px
        draw.line([(x_guia_esquerda, 0), (x_guia_esquerda, altura_px)], fill='red', width=2)
        
        # Linha direita
        x_guia_direita = largura_px - sangria_largura_px
        draw.line([(x_guia_direita, 0), (x_guia_direita, altura_px)], fill='red', width=2)
        
        return imagem
    
    def calcular_posicoes(self):
        """Calcula as posições das 9 imagens na página A4"""
        posicoes = []
        
        # Dimensões de cada célula (sem espaçamento)
        largura_celula = self.largura_original
        altura_celula = self.altura_original
        
        # Verificar se cabe na A4
        largura_total = self.margem_esquerda + 3 * largura_celula + self.margem_esquerda
        altura_total = self.margem_superior + 3 * altura_celula + self.margem_superior
        
        print(f"Largura necessária: {largura_total:.2f}cm (A4: {self.largura_a4}cm)")
        print(f"Altura necessária: {altura_total:.2f}cm (A4: {self.altura_a4}cm)")
        
        if largura_total > self.largura_a4 or altura_total > self.altura_a4:
            print("⚠️  Aviso: As imagens podem não caber perfeitamente na A4")
        
        for linha in range(3):
            for coluna in range(3):
                x = self.margem_esquerda + coluna * largura_celula
                y = self.margem_superior + linha * altura_celula
                posicoes.append((x, y))
        
        return posicoes
    
    def criar_pdf(self, imagens_paths, output_path):
        """Cria o PDF com até 9 imagens"""
        try:
            # Criar canvas PDF
            c = canvas.Canvas(output_path, pagesize=A4)
            
            # Calcular posições
            posicoes = self.calcular_posicoes()
            
            # Processar cada imagem (máximo 9 por página)
            for i, img_path in enumerate(imagens_paths[:9]):
                if i >= len(posicoes):
                    break
                    
                print(f"Processando imagem {i+1}: {os.path.basename(img_path)}")
                
                if self.modo == "com_sangria":
                    # Redimensionar imagem para tamanho original (6,85cm x 9,35cm)
                    img_redimensionada = self.redimensionar_imagem(
                        img_path, 
                        self.largura_original, 
                        self.altura_original
                    )
                    if img_redimensionada is None:
                        continue
                    # Adicionar linhas de guia diretamente na imagem redimensionada
                    img_final = self.adicionar_linhas_guia(img_redimensionada)
                else:
                    # Sem sangria: compor em canvas 6,85x9,35 com arte 6,35x8,89
                    img_final = self.compor_imagem_sem_sangria(img_path)
                    if img_final is None:
                        continue
                
                # Salvar imagem temporária
                temp_path = f"temp_img_{i}.png"
                img_final.save(temp_path, "PNG")
                
                # Adicionar ao PDF
                x, y = posicoes[i]
                c.drawImage(temp_path, x*cm, (self.altura_a4 - y - self.altura_original)*cm, 
                           width=self.largura_original*cm, height=self.altura_original*cm)
                
                # Remover arquivo temporário
                os.remove(temp_path)
            
            # Salvar PDF
            c.save()
            print(f"PDF criado com sucesso: {output_path}")
            return True
            
        except Exception as e:
            print(f"Erro ao criar PDF: {e}")
            return False
    
    def selecionar_arquivos(self):
        """Interface para seleção de arquivos"""
        root = tk.Tk()
        root.withdraw()  # Esconder janela principal
        
        # Selecionar arquivos
        arquivos = filedialog.askopenfilenames(
            title="Selecione as imagens (quantas quiser)",
            filetypes=[
                ("Imagens", "*.jpg *.jpeg *.png *.bmp *.tiff"),
                ("Todos os arquivos", "*.*")
            ]
        )
        
        return arquivos
    
    def selecionar_modo(self):
        """Pergunta ao usuário qual modo deseja utilizar."""
        root = tk.Tk()
        root.withdraw()
        resposta = messagebox.askyesno(
            "Modo de processamento",
            "Suas imagens já incluem sangria (tamanho 6,85 x 9,35 cm)?\n\nSim = Já incluem sangria\nNão = Estão no tamanho final (6,35 x 8,89 cm)"
        )
        self.modo = "com_sangria" if resposta else "sem_sangria"
        print(f"Modo selecionado: {self.modo}")
        return self.modo
    
    def processar_multiplos_pdfs(self, arquivos, pasta_saida):
        """Processa todas as imagens criando PDFs a cada 9 imagens"""
        total_imagens = len(arquivos)
        total_pdfs = (total_imagens + 8) // 9  # Arredonda para cima
        
        print(f"Total de imagens: {total_imagens}")
        print(f"Serão criados {total_pdfs} PDF(s)")
        print()
        
        pdfs_criados = []
        
        for pdf_num in range(total_pdfs):
            # Calcular quais imagens vão neste PDF
            inicio = pdf_num * 9
            fim = min(inicio + 9, total_imagens)
            imagens_pdf = arquivos[inicio:fim]
            
            # Nome do arquivo PDF
            nome_pdf = f"proxies_pagina_{pdf_num + 1:02d}.pdf"
            caminho_pdf = os.path.join(pasta_saida, nome_pdf)
            
            print(f"📄 Criando PDF {pdf_num + 1}/{total_pdfs}: {nome_pdf}")
            print(f"   Imagens {inicio + 1} a {fim} de {total_imagens}")
            
            # Criar PDF
            sucesso = self.criar_pdf(imagens_pdf, caminho_pdf)
            
            if sucesso:
                pdfs_criados.append(caminho_pdf)
                print(f"   ✅ Concluído!")
            else:
                print(f"   ❌ Erro ao criar PDF {pdf_num + 1}")
            
            print()
        
        return pdfs_criados
    
    def executar(self):
        """Executa o programa principal"""
        print("=== Montador de Imagens para PDF A4 ===")
        print("Layout: 3x3 (9 imagens)")
        print(f"Dimensões da imagem: {self.largura_original}cm x {self.altura_original}cm")
        print(f"Área de corte: {self.largura_final}cm x {self.altura_final}cm")
        print(f"Sangria: {self.sangria_largura}cm x {self.sangria_altura}cm")
        print()
        
        # Selecionar modo de processamento
        self.selecionar_modo()
        
        # Selecionar arquivos
        arquivos = self.selecionar_arquivos()
        
        if not arquivos:
            print("Nenhum arquivo selecionado.")
            return
        
        print(f"Arquivos selecionados: {len(arquivos)}")
        for i, arquivo in enumerate(arquivos, 1):
            print(f"  {i}. {os.path.basename(arquivo)}")
        
        # Selecionar pasta de saída
        pasta_saida = filedialog.askdirectory(
            title="Selecione a pasta para salvar os PDFs"
        )
        
        if not pasta_saida:
            print("Operação cancelada.")
            return
        
        # Processar múltiplos PDFs
        print("\n🔄 Processando imagens...")
        pdfs_criados = self.processar_multiplos_pdfs(arquivos, pasta_saida)
        
        if pdfs_criados:
            print(f"\n✅ Processamento concluído!")
            print(f"📁 Pasta: {pasta_saida}")
            print(f"📄 PDFs criados: {len(pdfs_criados)}")
            print("\n📋 Instruções:")
            print("- As linhas vermelhas indicam onde cortar")
            print("- Corte seguindo as linhas para obter as dimensões finais")
            print("- Cada imagem terá as dimensões corretas após o corte")
            print("- Use uma refiladora para cortar as páginas")
        else:
            print("\n❌ Nenhum PDF foi criado.")

def main():
    """Função principal"""
    try:
        montador = MontadorImagens()
        montador.executar()
    except KeyboardInterrupt:
        print("\n\nOperação cancelada pelo usuário.")
    except Exception as e:
        print(f"\nErro inesperado: {e}")
        input("Pressione Enter para sair...")

if __name__ == "__main__":
    main()
