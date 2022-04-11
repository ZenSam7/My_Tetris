try:
    import pygame
    from random import randint
    from time import time, sleep
    pygame.init()


    window_game_width = 360
    window_menu_width = 180
    window_height = 600
    cell_size = 40

    speed = 0.75
    game_acceleration = 0.984
    how_long_to_wait_after_assembling_row = 0.3
    time_to_move_away_after_collision_with_figur = 0.4
    how_many_times_will_we_move_with_the_key_pressed = 9

    size_text_Score = 30
    size_text_Game_Over = 65

    color_text_Game_Over = (180, 200, 180)
    background_color = (45, 49, 45)
    shadow_color = (50, 55, 50)
    grid_color = (80, 85, 80)


    ######################################### Фигуры
    # Почему картеж? да прост ¯＼_(._.)_/¯
    L = (((1,0), (1,1), (1,2), (2,2)), ((0,0), (1,0), (2,0), (0,1)), ((0,0), (1,0), (1,1), (1,2)), ((0,1), (1,1), (2,1), (2,0)))
    L_color = (40, 100, 40)
    J = (((1,0), (1,1), (1,2), (0,2)), ((0,0), (0,1), (1,1), (2,1)), ((1,0), (2,0), (1,1), (1,2)), ((0,0), (1,0), (2,0), (2,1)))
    J_color = (140, 65, 40)
    O = (((0,0), (1,0), (0,1), (1,1)), ((0,0), (1,0), (0,1), (1,1)), ((0,0), (1,0), (0,1), (1,1)), ((0,0), (1,0), (0,1), (1,1)))
    O_color = (110, 130, 30)
    I = (((0,0), (0,1), (0,2), (0,3)), ((0,0), (1,0), (2,0), (3,0)), ((0,0), (0,1), (0,2), (0,3)), ((0,0), (1,0), (2,0), (3,0)))
    I_color = (50, 120, 100)
    S = (((1,0), (2,0), (0,1), (1,1)), ((0,0), (0,1), (1,1), (1,2)), ((1,0), (2,0), (0,1), (1,1)), ((0,0), (0,1), (1,1), (1,2)))
    S_color = (100, 50, 100)
    Z = (((0,0), (1,0), (1,1), (2,1)), ((1,0), (1,1), (0,1), (0,2)), ((0,0), (1,0), (1,1), (2,1)), ((1,0), (1,1), (0,1), (0,2)))
    Z_color = (30, 50, 110)
    T = (((0,0), (1,0), (2,0), (1,1)), ((1,0), (0,1), (1,1), (1,2)), ((1,0), (0,1), (1,1), (2,1)), ((0,0), (0,1), (1,1), (0,2)))
    T_color = (120, 140, 120)
    #########################################

    RUN = True
    turn = 0
    score = 0
    figur_now = []
    figur_now_list = []
    fallen_figures = []
    fallen_figures_color = []
    color_now = ()
    figur_list = [L, J, O, I, S, Z, T]
    color_list = [L_color, J_color, O_color, I_color, S_color, Z_color, T_color]
    possible_to_move_left = True
    possible_to_move_right = True
    possible_to_move_down = True
    key_right = False
    key_left = False
    key_down = False
    this_time = time()
    this_time_local = time()
    this_local_time = time()
    local_this_time = time()
    countdown = None
    minutes = 0
    seconds = 0
    next_figur_num = randint(0, 6)
    pocketing = False
    pocket = "!"
    pocket_color = "!"
    figure_change = False

    #########################################

    def window():
        global wind
        wind = pygame.display.set_mode((window_game_width + window_menu_width, window_height))
        pygame.display.set_caption("(*^ω^)    Тетрис")
    def draw_figur():
        global figur_now, color_now

        wind.fill((background_color))


        for q in figur_now:
            for h in range(q[1], window_height // cell_size):
                pygame.draw.rect(wind, shadow_color, (q[0] * cell_size, h * cell_size, cell_size, cell_size))


        for i in figur_now:
            pygame.draw.rect(wind, color_now, (i[0] * cell_size, i[1] * cell_size, cell_size, cell_size))


        for t in range(0, len(fallen_figures)):
            for cell in fallen_figures[t]:
                pygame.draw.rect(wind, fallen_figures_color[t], (cell[0] * cell_size, cell[1] * cell_size, cell_size, cell_size))




        for i in range(window_game_width // cell_size):
            for j in range(window_height  // cell_size):
                pygame.draw.rect(wind, grid_color, (i * cell_size, j * cell_size, cell_size, cell_size), 1)


        draw_menu()
    def draw_menu():
        global next_figur, next_figur_color, pocketing, pocket, pocket_color, color_now, figur_num, figure_change
        font = pygame.font.SysFont('Arial', size_text_Score)



        text_Next_Figure = font.render("Next Figure:", True, color_text_Game_Over)
        text_Next_Figure_xy = text_Next_Figure.get_rect(center = (window_game_width + window_menu_width // 2, window_height * 0.08 ))
        wind.blit(text_Next_Figure, text_Next_Figure_xy)
        try:
            for q in next_figur:
                pygame.draw.rect(wind, next_figur_color, (q[0] * cell_size + window_game_width + window_menu_width // 5,
                                                          q[1] * cell_size + window_height * 0.13, cell_size, cell_size))
        except:
            pass




        text_Pocket = font.render("Pocket:", True, color_text_Game_Over)
        text_Pocket_xy = text_Pocket.get_rect(center = (window_game_width + window_menu_width // 2, window_height * 0.45 ))
        wind.blit(text_Pocket, text_Pocket_xy)


        if pocketing and not figure_change:
            figur_num, pocket = pocket, figur_num
            color_now, pocket_color = pocket_color, color_now


            if figur_num == "!":
                random_figur_now()
            else:
                change_figur(figur_num)

            pocketing = False

            figure_change = True

        try:
            for s in figur_list[pocket][0]:
                pygame.draw.rect(wind, pocket_color, (s[0] * cell_size + window_game_width + window_menu_width // 5,
                                                          s[1] * cell_size + window_height * 0.5, cell_size, cell_size))
        except:
            pass




        text_score = font.render(f"Score: {score}", True, color_text_Game_Over)
        text_score_xy = text_score.get_rect( center = (window_game_width + window_menu_width // 2, window_height * 0.85 ))
        wind.blit(text_score, text_score_xy)


        text_time = font.render(f"{minutes}:{seconds}", True, color_text_Game_Over)
        text_time_xy = text_time.get_rect(center = (window_game_width + window_menu_width // 2, window_height * 0.93))
        wind.blit(text_time, text_time_xy)



        pygame.display.update()


    def RESET():
        global speed, turn, score, figur_now, figur_now_list, fallen_figures, fallen_figures_color, color_now, possible_to_move_left
        global possible_to_move_right, possible_to_move_down, key_right, key_left, key_down, this_time, this_time_local, this_local_time
        global local_this_time, countdown, minutes, seconds, pocket, pocket_color, figure_change
        speed = 0.75
        turn = 0
        score = 0
        figur_now = []
        figur_now_list = []
        fallen_figures = []
        fallen_figures_color = []
        color_now = ()
        possible_to_move_left = True
        possible_to_move_right = True
        possible_to_move_down = True
        key_right = False
        key_left = False
        key_down = False
        this_time = time()
        this_time_local = time()
        this_local_time = time()
        local_this_time = time()
        countdown = None
        minutes = 0
        seconds = 0
        pocket = "!"
        pocket_color = "!"
        figure_change = False


    def move_down_every_time():
        global this_time
        if time() >= this_time + speed:
            move_down()

            this_time = time()


    def change_figur(figur_num):
        global figur_now_list, color_now, figur_now

        figur_now_list = []
        for figur in figur_list[figur_num]:
            ll = []
            for figur1 in list(figur):
                ll.append(list(figur1))
            figur_now_list.append(ll)

        figur_now = figur_now_list[0]



        color_now = color_list[figur_num]


    def random_figur_now():
        global figur_now, figur_now_list, color_now, turn, next_figur_num, next_figur, next_figur_color, figur_num, figure_change

        turn = 0



        figur_num = next_figur_num
        next_figur_num = randint(0, 6)


        next_figur = figur_list[next_figur_num][0]
        next_figur_color = color_list[next_figur_num]


        change_figur(figur_num)


        figure_change = False

        game_over()


    def borders():
        global possible_to_move_left, possible_to_move_right, possible_to_move_down
        old0 = True
        old1 = True
        old2 = True


        for cell in figur_now:
            for fall_figur in fallen_figures:
                for fall_cell in fall_figur:
                    if cell[0] == fall_cell[0] +1 and cell[1] == fall_cell[1]:
                        possible_to_move_left = False
                        old0 = False
                    if cell[0] == fall_cell[0] -1 and cell[1] == fall_cell[1]:
                        possible_to_move_right = False
                        old1 = False
                    if cell[0] == fall_cell[0] and cell[1] == fall_cell[1] -1:
                        possible_to_move_down = False
                        old2 = False


            if cell[0] == 0:
                possible_to_move_left = False
                old0 = False
            if cell[0] == window_game_width / cell_size -1:
                possible_to_move_right = False
                old1 = False
            if cell[1] == window_height / cell_size - 1:
                possible_to_move_down = False
                old2 = False


        if old0:
            possible_to_move_left = True
        if old1:
            possible_to_move_right = True
        if old2:
            possible_to_move_down = True


    def move_right():
        global possible_to_move_left
        borders()

        if possible_to_move_right:
            for figur in figur_now_list:
                for cell in figur:
                    cell[0] += 1

        possible_to_move_left = True
    def move_left():
        global possible_to_move_right
        borders()

        if possible_to_move_left:
            for figur in figur_now_list:
                for cell in figur:
                    cell[0] -= 1

        possible_to_move_right = True
    def move_down():
        global countdown
        borders()

        if possible_to_move_down:
            for figur in figur_now_list:
                for cell in figur:
                    cell[1] += 1
            countdown = True


    def rotate_figure():
        global turn, figur_now

        old_figur_now = figur_now_list[turn]


        if turn < 3:
            turn += 1
        else:
            turn = 0


        figur_now = figur_now_list[turn]


        for cell in figur_now:
            while cell[0] < 0:
                for i in figur_now:
                    i[0] += 1
            if cell[0] > window_game_width / cell_size -1:
                for i in figur_now:
                    i[0] -= 1
            if cell[1] > window_height / cell_size -1:
                for i in figur_now:
                    i[1] -= 1


        for cell in figur_now:
            for fall_figur in fallen_figures:
                for fall_cell in fall_figur:
                    if cell[0] == fall_cell[0] and cell[1] == fall_cell[1]:
                        figur_now = old_figur_now
                    elif cell[0] == fall_cell[0] and cell[1] == fall_cell[1]:
                        figur_now = old_figur_now


    def hit_bottom_or_figure():
        global fallen_figures, fallen_figures_color, this_local_time, countdown
        v = True


        for fall_figures in fallen_figures:
            for fallen_cell in fall_figures:
                for now_cell in figur_now:
                    if now_cell[0] == fallen_cell[0] and now_cell[1] == fallen_cell[1] -1:
                        if countdown:
                            borders()
                            if possible_to_move_left or possible_to_move_right:
                                this_local_time = time()
                                countdown = False
                        if time() >= this_local_time + time_to_move_away_after_collision_with_figur:
                            fallen_figures.append(figur_now)
                            fallen_figures_color.append(color_now)
                            random_figur_now()
                            v = False
                            countdown = True

        if v:
            for cell in figur_now:
                if cell[1] >= window_height / cell_size -1:
                    if countdown:
                        borders()
                        if possible_to_move_left or possible_to_move_right:
                            this_local_time = time()
                            countdown = False
                    if time() >= this_local_time + time_to_move_away_after_collision_with_figur:
                        fallen_figures.append(figur_now)
                        fallen_figures_color.append(color_now)
                        random_figur_now()
                        this_local_time = time()
                        countdown = True
                        break


    def row_assembled():
        global score, fallen_figures, speed, figure_change

        row_assembled = False
        cells_in_rows = []

        for fall_figur in fallen_figures:
            for fall_cell in fall_figur:
                cells_in_rows.append([fall_cell[1], fall_cell[0]])
        cells_in_rows.sort()


        for Y in range(0, window_height // cell_size):
            number_cells_in_row = 0

            for cell_in_rows in cells_in_rows:
                if cell_in_rows[0] == Y:
                    number_cells_in_row += 1

            if number_cells_in_row == window_game_width // cell_size:
                score += 1

                for i in range(3):
                    for fall_figur in fallen_figures:
                        for fall_cell in fall_figur:
                            if fall_cell[1] == Y:
                                fall_figur.remove(fall_cell)


                for fall_figur in fallen_figures:
                    for fall_cell in fall_figur:
                        if fall_cell[1] < Y:
                            fall_cell[1] += 1



                speed *= game_acceleration

                row_assembled = True

        if row_assembled:
            sleep(how_long_to_wait_after_assembling_row)


    def game_over():
        global RUN

        for fall_figur in fallen_figures:
            for fall_cell in fall_figur:
                for now_figur in figur_now_list:
                    for new_cell in figur_now:
                        if fall_cell == new_cell:
                            RUN = False


        if not RUN:
            font = pygame.font.SysFont('Arial', size_text_Game_Over)

            text_Game_Over = font.render("Game Over !", True, color_text_Game_Over)
            text_Reset = font.render("'R' = Reset", True, color_text_Game_Over)

            text_Game_Over_xy = text_Game_Over.get_rect( center = (window_game_width // 2, window_height // 2 - size_text_Game_Over ))
            text_Reset_xy = text_Game_Over.get_rect( center = (window_game_width // 2, window_height // 2  + size_text_Game_Over ))

            wind.blit(text_Game_Over, text_Game_Over_xy)
            wind.blit(text_Reset, text_Reset_xy)


            pygame.display.update()


            local_run = True
            while local_run:
                for event in pygame.event.get():
                    if event.type == pygame.KEYDOWN:
                        if event.key == ord('r'):
                            RESET()
                            local_run = False
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()

                    if event.type == pygame.QUIT:
                        pygame.quit()


    def timer():
        global local_this_time, seconds, minutes

        if time() >= local_this_time + 1:
            local_this_time = time()
            seconds += 1

        if seconds == 60:
            seconds = 0
            minutes += 1


    def control():
        global key_right, key_left, key_down, this_time_local, countdown, pocketing
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    key_right = True
                elif event.key == pygame.K_LEFT or event.key == ord('a'):
                    key_left = True
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    key_down = True
                if event.key == pygame.K_UP or event.key == ord('w'):
                    rotate_figure()
                if event.key == pygame.K_SPACE:
                    for i in range(0, window_height // cell_size):
                        move_down()
                    countdown = False
                if event.key == pygame.K_RSHIFT or event.key == pygame.K_LSHIFT:
                    pocketing = True


                if event.key == pygame.K_ESCAPE:
                    pygame.quit()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    key_right = False
                elif event.key == pygame.K_LEFT or event.key == ord('a'):
                    key_left = False
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    key_down = False

            elif event.type == pygame.QUIT:
                pygame.quit()


        how_many = how_many_times_will_we_move_with_the_key_pressed
        if key_right and time() >= this_time_local + 1 / how_many:
            move_right()
            this_time_local = time()
        if key_left and time() >= this_time_local + 1 / how_many:
            move_left()
            this_time_local = time()
        if key_down and time() >= this_time_local + speed / how_many:
            move_down()
            this_time_local = time()



    #########################################


    while True:
        RUN = True

        window()

        random_figur_now()
        while RUN:
            draw_figur()
            row_assembled()
            hit_bottom_or_figure()
            move_down_every_time()
            control()
            timer()
except:
    pass
