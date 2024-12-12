import pygame
import sys
import math
import random

# Inicialização do Pygame
pygame.init()

# Definindo cores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
DARK_GRAY = (100, 100, 100)

# Tamanho da janela
WIDTH, HEIGHT = 800, 600
tela = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulador de Estacionamento")

# Definições do carro
carro_comprimento, carro_altura = 60, 120
carro_velocidade = 5
carro_angulo = 0
carro_x, carro_y = 400, 300

# Definições das vagas
vaga_comprimento, vaga_altura = 80, 140
margem = 50
espaço = 10
estacionamento = []
vaga_correta = None

# Funções auxiliares
def desenho_ruas():
    # Desenha as ruas horizontais e verticais no estacionamento
    pygame.draw.rect(tela, DARK_GRAY, (0, HEIGHT // 2 - 50, WIDTH, 100))
    pygame.draw.rect(tela, DARK_GRAY, (WIDTH // 2 - 50, 0, 100, HEIGHT))

def criar_estacionamento():
    # Cria as vagas de estacionamento ao redor da rua
    global estacionamento
    estacionamento.clear()
    todas_vagas = []

    # Vagas superiores (esquerda da rua)
    for i in range(3):
        x = margem + i * (vaga_comprimento + espaço)
        y = margem
        todas_vagas.append((x, y))

    # Vagas superiores (direita da rua)
    for i in range(3):
        x = WIDTH // 2 + 60 + i * (vaga_comprimento + espaço)
        y = margem
        todas_vagas.append((x, y))

    # Vagas inferiores (esquerda da rua)
    for i in range(3):
        x = margem + i * (vaga_comprimento + espaço)
        y = HEIGHT - margem - vaga_altura
        todas_vagas.append((x, y))

    # Vagas inferiores (direita da rua)
    for i in range(3):
        x = WIDTH // 2 + 60 + i * (vaga_comprimento + espaço)
        y = HEIGHT - margem - vaga_altura
        todas_vagas.append((x, y))

    return todas_vagas

def desenhe_estaciomento(all_spots):
    # Desenha todas as vagas de estacionamento
    for x, y in all_spots:
        if (x, y) == vaga_correta:
            pygame.draw.rect(tela, GREEN, (x, y, vaga_comprimento, vaga_altura), 3)  # Destaca a vaga correta
        else:
            pygame.draw.rect(tela, DARK_GRAY, (x, y, vaga_comprimento, vaga_altura))  # Outras vagas
        estacionamento.append(pygame.Rect(x, y, vaga_comprimento, vaga_altura))

def desenhe_carro(x, y, angle):
    # Desenha o carro na tela com rotação
    points = [
        (x - carro_comprimento // 2, y - carro_altura // 2),
        (x + carro_comprimento // 2, y - carro_altura // 2),
        (x + carro_comprimento // 4, y + carro_altura // 2),
        (x - carro_comprimento // 4, y + carro_altura // 2)
    ]
    rotated_points = []
    for point in points:
        rotated_x = x + (point[0] - x) * math.cos(math.radians(angle)) - (point[1] - y) * math.sin(math.radians(angle))
        rotated_y = y + (point[0] - x) * math.sin(math.radians(angle)) + (point[1] - y) * math.cos(math.radians(angle))
        rotated_points.append((rotated_x, rotated_y))
    pygame.draw.polygon(tela, BLUE, rotated_points)
    return rotated_points

def posição_carro():
    # Posiciona o carro em um lugar inicial aleatório que não colida com as vagas
    while True:
        if random.choice([True, False]):
            car_x = random.randint(vaga_comprimento + margem, WIDTH - vaga_comprimento - margem)
            car_y = random.randint(HEIGHT // 2 - 40, HEIGHT // 2 + 40)
        else:
            car_x = random.randint(WIDTH // 2 - 40, WIDTH // 2 + 40)
            car_y = random.randint(vaga_altura + margem, HEIGHT - vaga_altura - margem)

        car_rect = pygame.Rect(car_x - carro_comprimento // 2, car_y - carro_altura // 2, carro_comprimento, carro_altura)
        collision = any(car_rect.colliderect(spot) for spot in estacionamento)

        if not collision:
            return car_x, car_y

def checa_colisão(car_points):
    # Verifica se o carro colidiu com uma vaga incorreta
    for spot in estacionamento:
        if any(spot.collidepoint(point) for point in car_points):
            if spot.topleft != vaga_correta:
                return True
    return False

def checar_estacionado(car_points):
    # Verifica se o carro está completamente dentro da vaga correta
    x, y = vaga_correta
    target_rect = pygame.Rect(x, y, vaga_comprimento, vaga_altura)
    for point in car_points:
        if not target_rect.collidepoint(point):
            return False
    return True

def resetar_game():
    # Reinicia o jogo
    global carro_x, carro_y, carro_angulo, vaga_correta, estacionamento, todas_vagas
    carro_angulo = 0
    todas_vagas = criar_estacionamento()
    vaga_correta = random.choice(todas_vagas)
    carro_x, carro_y = posição_carro()

# Configuração inicial
todas_vagas = criar_estacionamento()
vaga_correta = random.choice(todas_vagas)
carro_x, carro_y = posição_carro()
movimento_carro = False
tempo = pygame.time.Clock()

# Loop principal
fim_de_jogo = False
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if fim_de_jogo:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_r]:
            fim_de_jogo = False
            resetar_game()
        continue

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        carro_x += carro_velocidade * math.sin(math.radians(carro_angulo))
        carro_y -= carro_velocidade * math.cos(math.radians(carro_angulo))
        movimento_carro = True
    elif keys[pygame.K_DOWN]:
        carro_x -= carro_velocidade * math.sin(math.radians(carro_angulo))
        carro_y += carro_velocidade * math.cos(math.radians(carro_angulo))
        movimento_carro = True
    else:
        movimento_carro = False

    if movimento_carro:
        if keys[pygame.K_LEFT]:
            carro_angulo -= 2 if not keys[pygame.K_DOWN] else -2
        if keys[pygame.K_RIGHT]:
            carro_angulo += 2 if not keys[pygame.K_DOWN] else -2

    tela.fill(GRAY)
    desenho_ruas()
    desenhe_estaciomento(todas_vagas)
    car_points = desenhe_carro(carro_x, carro_y, carro_angulo)

    if checa_colisão(car_points):
        font = pygame.font.Font(None, 48)
        text = font.render("BATEUU! Aperte R para Resetar ", True, RED)
        tela.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        fim_de_jogo = True

    if checar_estacionado(car_points):
        font = pygame.font.Font(None, 48)
        text = font.render("PERFECT! Aperte R para Resetar", True, GREEN)
        tela.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - text.get_height() // 2))
        pygame.display.flip()
        fim_de_jogo = True

    if not fim_de_jogo:
        pygame.display.flip()
        tempo.tick(60)

   # Impedir o carro de ultrapassar os limites da tela
    carro_x = max(carro_comprimento // 2, min(WIDTH - carro_comprimento // 2, carro_x))
    carro_y = max(carro_altura // 2, min(HEIGHT - carro_altura // 2, carro_y))