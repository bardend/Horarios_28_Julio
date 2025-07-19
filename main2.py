import pygame
import random
from gen import f

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
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
font = pygame.font.Font(None, 100)
title_font = pygame.font.Font(None, 48)
group_font = pygame.font.Font(None, 36)


# Leer nombres desde el archivo (sin cambios)
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


start_index = 4
before_shuffle = nombres[:start_index]
to_shuffle = nombres[start_index:]

# Aplicar shuffle solo a la parte deseada
random.shuffle(to_shuffle)

# Combinar las partes nuevamente
nombres = before_shuffle + to_shuffle



# Botón
button_rect = pygame.Rect(WIDTH // 2 - 225, HEIGHT - 200, 550, 150)


def draw_groups():
    group_width = (WIDTH - 100) // 4  # 4 columnas
    group_height = HEIGHT // 4  # Reducir la altura
    group_font = pygame.font.Font(None, 40)  # Reducir un poco el tamaño de fuente
    name_font = pygame.font.Font(None, 32)  # Reducir un poco el tamaño de fuente

    for i, grupo in enumerate(grupos):
        x = (i % 4) * (group_width + 20) + 20
        y = (i // 4) * (group_height + 10) + 60  # Reducir el espacio vertical
        pygame.draw.rect(screen, COLORS[i % len(COLORS)], (x, y, group_width, group_height))
        pygame.draw.rect(screen, BLACK, (x, y, group_width, group_height), 2)
        grupo_letra = chr(65 + i)  # Convierte 0 a 'A', 1 a 'B', 2 a 'C', etc.
        text = group_font.render(f"Grupo {grupo_letra}", True, BLACK)
        screen.blit(text, (x + 10, y + 5))
        for j, nombre in enumerate(grupo):
            text = name_font.render(nombre, True, BLACK)
            screen.blit(text, (x + 10, y + 45 + j * 30))  # Reducir el espacio entre nombres
import datetime

# Definir la duración de cada partido en minutos
DURACION_PARTIDO = 30  # Puedes cambiar este valor a 20, 30, 40, etc.

def draw_partidos(partidos):
    print(f"Dibujando {len(partidos)} partidos")

    partido_font = pygame.font.Font(None, 32)

    partido_width = (WIDTH - 100) // 4
    partido_height = 70

    movey = 250
    x_offset = 50
    y_offset = HEIGHT // 2 - movey

    title = title_font.render("Partidos", True, BLACK)
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - movey - 80))

    numero_partidos = len(partidos)

    # Definir la hora de inicio y el intervalo entre partidos
    hora_inicio = datetime.datetime(2024, 7, 21, 8, 0)
    intervalo = datetime.timedelta(minutes=DURACION_PARTIDO)  # Duración del partido definida por DURACION_PARTIDO

    hora_actual = hora_inicio
    for i, (g, id1, id2) in enumerate(partidos):
        equipo1 = grupos[g][id1]
        equipo2 = grupos[g][id2]

        col = i % 4
        row = i // 4

        x = x_offset + col * (partido_width + 20)
        y = y_offset + row * (partido_height + 10)

        bg_rect = pygame.Rect(x, y, partido_width, partido_height)
        pygame.draw.rect(screen, GRAY, bg_rect)
        pygame.draw.rect(screen, BLACK, bg_rect, 2)

        # Calcular la hora del partido
        if hora_actual.time() > datetime.time(17, 30):
            # Si es después de las 5:30 PM, avanzar al siguiente día a las 8 AM
            hora_actual += datetime.timedelta(days=1)
            hora_actual = hora_actual.replace(hour=8, minute=0)

        # Formatear la hora del partido
        hora_str = hora_actual.strftime("%d/%m %I:%M %p")

        # Número de partido
        num_text = partido_font.render(f"{i + 1}.", True, BLACK)
        screen.blit(num_text, (x + 5, y + 5))

        # Información del partido en dos líneas
        grupo_letra = chr(65 + g)
        texto1 = f"G{grupo_letra}: {equipo1} vs {equipo2}"
        texto2 = f"Hora: {hora_str}"

        text1 = partido_font.render(texto1, True, BLACK)
        text2 = partido_font.render(texto2, True, BLACK)

        screen.blit(text1, (x + 40, y + 5))
        screen.blit(text2, (x + 40, y + 35))

        # Avanzar la hora para el próximo partido
        hora_actual += intervalo
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
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 300))
        else:
            text = font.render("Asignación completada", True, BLACK)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT - 120))

        pygame.display.flip()
        if current_name_index == len(nombres) :
            n_grupos = len(grupos)

            max_len = max(len(grupo) for grupo in grupos)

            if ok :
                """
                for i in range(max_len):
                    for j in range(i+1, max_len):
                        match.append((i, j))

                random.shuffle(match)
                """
                tmp_match = f(max_len)
                match = tmp_match




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


        pygame.time.wait(1000)  # Espera 100 milisegundos

    pygame.quit()


if __name__ == "__main__":
    main()
