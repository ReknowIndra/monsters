# -*- coding: utf-8 -*-
"""
Created on Thu Jan  4 12:48:42 2024

@author: ReichelErwinWIVAP&G
"""

import pygame
import sys

# Pygame initialisieren
pygame.init()

# Fenster erstellen
width, height = 800, 600
screen = pygame.display.set_mode((width, height),pygame.SRCALPHA,32)
pygame.display.set_caption("Durchscheinender Kreis über einer Grafik")

# Erzeuge ein Bild mit einem Alphakanal (Transparenz)
image = pygame.Surface((width, height), pygame.SRCALPHA,32)
pygame.draw.rect(image, (255, 0, 0, 128), pygame.Rect(50, 50, 100, 100))  # Rotes Rechteck als Hintergrund

# Hauptschleife
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Hier kommt die Hauptspiellogik hin

    # Hier werden die Grafiken gezeichnet
    screen.fill((255, 255, 255,0))  # Hintergrundfarbe

    # Zeichne das Bild mit Alphakanal
    screen.blit(image, (0, 0))

    # Zeichne einen durchscheinenden Kreis
    pygame.draw.circle(screen, (0, 0, 255, 128), (width // 5, height // 4), 50)

    pygame.display.flip()

#%%
# Pygame beenden
pygame.quit()

# Das beendet auch das Python-Programm
sys.exit()
