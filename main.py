import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 1000, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Asignación de Grupos")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BUTTON_COLOR = (100, 200, 100)
BUTTON_HOVER_COLOR = (150, 250, 150)
COLORS = [(255, 200, 200), (200, 255, 200), (200, 200, 255),
          (255, 255, 200), (255, 200, 255), (200, 255, 255)]

# Fuentes
font = pygame.font.Font(None, 28)
title_font = pygame.font.Font(None, 40)


# Leer nombres desde el archivo
def leer_nombres():
    try:
        with open('nombres.txt', 'r', encoding='utf-8') as file:
            return [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        print("Error: No se encontró el archivo 'nombres.txt'")
        return []


nombres = leer_nombres()
if not nombres:
    print("No se pudieron cargar los nombres. El programa se cerrará.")
    pygame.quit()
    exit()

# Crear grupos
num_grupos = (len(nombres) + 4) // 5
grupos = [[] for _ in range(num_grupos)]
partidos = []

# Mezclar los nombres
random.shuffle(nombres)

# Botón
button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT - 80, 200, 50)


def draw_groups():
    for i, grupo in enumerate(grupos):
        x = (i % 3) * (WIDTH // 3) + 20
        y = (i // 3) * 180 + 80
        pygame.draw.rect(screen, COLORS[i % len(COLORS)], (x, y, WIDTH // 3 - 40, 160))
        text = title_font.render(f"Grupo {i + 1}", True, BLACK)
        screen.blit(text, (x + 10, y + 10))
        for j, nombre in enumerate(grupo):
            text = font.render(nombre, True, BLACK)
            screen.blit(text, (x + 10, y + 50 + j * 30))

ok2 = 1
def draw_partidos(partidos):
    print(f"Dibujando {len(partidos)} partidos")
    y_offset = 400  # Posición vertical inicial para los partidos

    for g, id1, id2 in partidos:
        equipo1 = grupos[g][id1]
        equipo2 = grupos[g][id2]
        texto = f"{equipo1} vs {equipo2}"
        print(f"Dibujando: {texto}")
        text = font.render(texto, True, BLACK)
        screen.blit(text, (50, y_offset))
        y_offset += 30  # Mover hacia abajo para el próximo enfrentamiento
    pygame.display.update()


def draw_button(mouse_pos):
    color = BUTTON_HOVER_COLOR if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, color, button_rect)
    pygame.draw.rect(screen, BLACK, button_rect, 2)
    text = font.render("Asignar Nombre", True, BLACK)
    text_rect = text.get_rect(center=button_rect.center)
    screen.blit(text, text_rect)



def main():
    current_name_index = 0
    ok = 1
    ok2 = 1
    val = 1
    end_partidos = 0
    maxn = 10
    running = True
    match = []
    random_grup = []
    vis = [[[False for _ in range(maxn)] for _ in range(maxn)] for _ in range(maxn)]
    while running:
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rect.collidepoint(mouse_pos) and current_name_index < len(nombres):
                    nombre = nombres[current_name_index]

                    min_len = min(len(grupo) for grupo in grupos)

                    cand = [i for i, grupo in enumerate(grupos) if len(grupo) == min_len]
                    grupo_elegido = random.choice(cand)
                    grupos[grupo_elegido].append(nombre)
                    current_name_index += 1


        screen.fill(WHITE)

        # Título
        title = title_font.render("Asignación de Grupos", True, BLACK)
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 20))

        draw_groups()
        draw_button(mouse_pos)

        if current_name_index < len(nombres):
            text = font.render(f"Próximo: {nombres[current_name_index]}", True, BLACK)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 120))
        else:
            text = font.render("Asignación completada", True, BLACK)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 120))

        pygame.display.flip()
        if current_name_index == len(nombres) :
            n_grupos = len(grupos)

            max_len = max(len(grupo) for grupo in grupos)

            if ok :
                for i in range(max_len):
                    for j in range(i+1, max_len):
                        match.append((i, j))


                random.shuffle(match)
                tmp = [i for i in range(n_grupos)]
                random.shuffle(tmp)
                for e in tmp :
                    random_grup.append(e)

                ok = 0


                for i, j in match :

                    for id in  random_grup :

                        print("=============")
                        grupo = grupos[id]
                        l = len(grupo)

                        if l == max_len :
                            vis[id][i][j] = True
                            partidos.append((id, i, j))
                            print("Anadi 1")
                        else :
                            exist = 0
                            for x in range(l):
                                for y in range(x+1, l):
                                    if vis[id][x][y] == 0 and y > x and y < l  and x < l:
                                        exist = 1

                            if(exist == 0):
                                continue
                            else :
                                fill = 0
                                if(j < l ) :
                                    if(vis[id][i][j] == 0) :
                                        vis[id][i][j] = 1
                                        fill = 1
                                        partidos.append((id, i, j))
                                        print("Anadi 2")
                                    else :
                                        b1 = 0
                                        for ii in range(i, l):
                                            for jj in range(max(j, ii+1), l):
                                                if(vis[id][ii][jj] == 0 and ii < l and jj < l and jj>ii) :
                                                    vis[id][ii][jj] = 1
                                                    fill = 1
                                                    partidos.append((id, ii, jj))
                                                    print("Anadi 3")
                                                    b1 = 1
                                                    break
                                            if(b1):
                                                break

                                        if(b1 == 0) :
                                            for ii in range(i, l):
                                                for jj in range(j, ii, -1):

                                                    if(vis[id][ii][jj] == 0 and ii < l and jj < l and jj>ii) :
                                                        vis[id][ii][jj] = 1
                                                        fill = 1
                                                        partidos.append((id, ii, jj))
                                                        print("Anadi 4")
                                                        b1 = 1
                                                        break
                                                if(b1) :
                                                    break
                                else  :
                                    b1 = 0
                                    tmpj = j-1
                                    for ii in range(i, min(l, i+2)):
                                        for jj in range(tmpj, ii, -1) :
                                            if(vis[id][ii][jj] == 0 and ii < l and jj < l and jj>ii) :
                                                vis[id][ii][jj] = 1
                                                fill = 1
                                                partidos.append((id, ii, jj))
                                                print("Anadi 5")
                                                b1 = 1
                                                break

                                        if(b1) :
                                            break

                                if fill == 0 :
                                    b1 = 0
                                    for ii in range(0, l):
                                        for jj in range(ii+1, l):
                                            if(vis[id][ii][jj] == 0 and ii < l and jj < l and jj>ii):
                                                vis[id][ii][jj] = 1
                                                fill = 1
                                                partidos.append((id, ii, jj))
                                                print("Anadi 6")
                                                b1 = 1
                                                break

                                        if (b1):
                                                break

                        last = partidos[-1]
                        if(last[2] >= l) :
                            print("Aca esta el problema")
                            print(last)


                print(f"El grupo random es :{random_grup}")
                print(f"Los enfrentamientos son :{match}")

                # Test

                target = set(match)
                prueba = set()
                for id, x, y in partidos :
                    prueba.add((x, y))

                cnt = 0
                for i in random_grup:
                    l = len(grupos[i])
                    cnt += (l*(l-1)//2)

                if(target == prueba and cnt == len(partidos)) :
                    print("Tamos good" )
                end_partidos = 1
        if end_partidos :
            draw_partidos(partidos)
        pygame.display.flip()
        pygame.time.wait(100)  # Espera 100 milisegundos

    pygame.quit()


if __name__ == "__main__":
    main()
