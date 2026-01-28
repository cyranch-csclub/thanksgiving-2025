import turtle
import random
from PIL import Image, ImageTk

#--------------------# Setup #--------------------#

# Board Size
board_Size = 500

# Background
bg = turtle.Screen()
bg.setup(750, 775)
bg.setworldcoordinates(-375, -300, 375, 475)
bg.bgcolor('#f7f5f0')

# Speedy Turtle
turtle.delay(0)
turtle.tracer(0, 0)

#-------------------# Prompt #-------------------#

def map_Size():
    # Prompt for Grid Size
    answer = None
    while answer not in ('small', 'regular', 'large'):
        answer = bg.textinput('Grid Size', 'Please enter a grid size: small, regular, or large')

    # Assign num_side_tiles and tile_pix/mid_tile_pix according to response
    if answer == 'small':
        num_Side_Tiles = 5
    elif answer == 'regular':
        num_Side_Tiles = 10
    else:
        num_Side_Tiles = 20

    tile_Pix = board_Size // num_Side_Tiles
    mid_Tile_Pix = tile_Pix // 2

    return num_Side_Tiles, tile_Pix, mid_Tile_Pix

#-------------------# Images #-------------------#

def import_Images(tile_Pix):
    # Cookies N Creme
    cookies_N_Creme = Image.open('Cookies_N_Creme.gif')

    # Score Board Cookies N Creme
    resized_Score_Cookies_N_Creme = cookies_N_Creme.resize((100, 100))
    tk_Score_Cookies_N_Creme = ImageTk.PhotoImage(resized_Score_Cookies_N_Creme)
    bg.addshape('score_Cookies_N_Creme', turtle.Shape('image', tk_Score_Cookies_N_Creme))

    # Snake Food Cookies N Creme
    resized_Cookies_N_Creme = cookies_N_Creme.resize((tile_Pix, tile_Pix))
    tk_Cookies_N_Creme = ImageTk.PhotoImage(resized_Cookies_N_Creme)
    bg.addshape('cookies_N_Creme', turtle.Shape('image', tk_Cookies_N_Creme))

    # Snake Trophy
    snake_Trophy = Image.open('Snake_Trophy.gif')
    resized_Snake_Trophy = snake_Trophy.resize((100, 100))
    tk_Snake_Trophy = ImageTk.PhotoImage(resized_Snake_Trophy)
    bg.addshape('snake_Trophy', turtle.Shape('image', tk_Snake_Trophy))

    # Snake Head in all 4 Directions
    snake_Head = Image.open('Snake_Head2.gif')
    resized_Snake_Head = snake_Head.resize((tile_Pix, tile_Pix))

    for i, direction in enumerate(('0', '90', '180', '270')):
        tk_Snake_Head = ImageTk.PhotoImage(resized_Snake_Head.rotate(90 * i))
        turtle.addshape(direction, turtle.Shape("image", tk_Snake_Head))

    # Snake Body
    snake_Body = Image.open('Snake_Body.gif')
    resized_Snake_Body = snake_Body.resize((tile_Pix, tile_Pix))
    tk_Snake_Body = ImageTk.PhotoImage(resized_Snake_Body)
    bg.addshape('snake_Body', turtle.Shape('image', tk_Snake_Body))

#------------------# Turtles- #------------------#

def all_Turtles(tile_Pix):
    # Background painter
    bg_painter = turtle.Turtle()
    bg_painter.hideturtle()
    bg_painter.shape('square')
    bg_painter.shapesize(tile_Pix / 20)
    bg_painter.penup()
    bg_painter.pensize(50)

    # Segment Turtle
    turtle.register_shape('segment', ((-18.75, 0), (-15, 3.75), (15, 3.75), (18.75, 0), (15, -3.75), (-15, -3.75)))
    base_Segment = turtle.Turtle()
    base_Segment.shape('segment')
    base_Segment.color('#038fff')
    base_Segment.penup()

    # Score Board Cookies N Creme
    score_Cookies_N_Creme = turtle.Turtle()
    score_Cookies_N_Creme.shape('score_Cookies_N_Creme')
    score_Cookies_N_Creme.penup()

    # Snake Food Cookies'n Creme
    cookies_N_Creme = turtle.Turtle()
    cookies_N_Creme.shape('cookies_N_Creme')
    cookies_N_Creme.penup()

    # Snake Trophy
    snake_Trophy = turtle.Turtle()
    snake_Trophy.shape('snake_Trophy')
    snake_Trophy.penup()

    # Snake Head
    snake_Head = turtle.Turtle()
    snake_Head.shape('0')
    snake_Head.penup()

    # Snake Body
    snake_Body = turtle.Turtle()
    snake_Body.shape('snake_Body')
    snake_Body.penup()

    # All Snake Turtles
    snake_Turtles = [snake_Head, snake_Body]

    return bg_painter, base_Segment, score_Cookies_N_Creme, cookies_N_Creme, snake_Trophy, snake_Turtles

#-----------------# Background #-----------------#

def setting_Up_Board_Looks(bg_painter, all_Tile_Cords):
    # Making Outer Edges of Board
    bg_painter.color('#FDCE59')
    bg_painter.goto(board_Size // 2, board_Size // 2)
    bg_painter.setheading(180)
    bg_painter.pendown()
    for i in range(4):
        bg_painter.fd(board_Size)
        bg_painter.lt(90)
    bg_painter.penup()

    # Filling in Board
    bg_painter.color('#fefcfa', '#01589D')
    for cords in all_Tile_Cords:
        bg_painter.goto(cords)
        bg_painter.stamp()
    bg_painter.penup()

def setting_Up_Score_Counter_Looks(bg_painter, score_Cookies_N_Creme, snake_Trophy):
    # Making Outer Edges of Score Counter
    bg_painter.color('#FDCE59')
    bg_painter.goto(-306.5, 325)
    bg_painter.setheading(90)
    bg_painter.pendown()
    for i in range(4):
        bg_painter.fd(100 if i % 2 == 0 else 613)
        bg_painter.rt(90)
    bg_painter.penup()

    # Filling in Score Counter
    bg_painter.color('#01589D')
    bg_painter.goto(-306.5, 325)
    bg_painter.setheading(90)
    bg_painter.begin_fill()
    for i in range(4):
        bg_painter.fd(100 if i % 2 == 0 else 613)
        bg_painter.rt(90)
    bg_painter.end_fill()

    # Adding Score Counter Cookies N Creme
    score_Cookies_N_Creme.goto(-231.5, 375)
    score_Cookies_N_Creme.clone()

    # Adding Snake Trophy
    snake_Trophy.goto(62.5, 375)
    snake_Trophy.clone()

#----------------# Coordinates- #----------------#

def generate_All_Tile_Cords(tile_pix, mid_tile_pix):
    # Generating Possible Coordinate Values
    smallest_Possible_Value = -board_Size // 2 + mid_tile_pix
    largest_Possible_Value = board_Size // 2 - mid_tile_pix
    possible_Cord_Values = list(range(smallest_Possible_Value, largest_Possible_Value + 1, tile_pix))

    # Generating All Tile Coordinates
    all_Tile_Cords = []
    for x in possible_Cord_Values:
        for y in possible_Cord_Values:
            all_Tile_Cords.append((x, y))

    return all_Tile_Cords

def generate_Whole_Snake_Cords_And_Cookies_N_Creme_Repawn_Cords(snake_Turtles, mid_Tile_Pix, all_Tile_Cords):
    whole_Snake_Cords = []
    '''for i in range(len(snake_Turtles) - 1, 0, -1):
        whole_Snake_Cords.append((snake_Turtles[i].xcor() + mid_Tile_Pix, snake_Turtles[i].ycor()))'''
    cookies_N_Creme_Respawn_Cords = all_Tile_Cords
    '''for i in range(len(whole_Snake_Cords) - 1, 0, -1):
        cookies_N_Creme_Respawn_Cords.remove(whole_Snake_Cords[i])'''

    return whole_Snake_Cords, cookies_N_Creme_Respawn_Cords

def respawn_Cookies_N_Creme(possible_Tile_Cords, cookies_N_Creme):
    cookies_N_Creme.goto(possible_Tile_Cords[random.randint(0, len(possible_Tile_Cords) - 1)])

#---------------# Score Counter- #---------------#

def setting_Up_Score_Counter_Function(base_Segment):

    y = 375
    offset = 18.75

    # Format [[Hundreds], [Tens], [Ones]]
    record_Score_Display = [[], [], []]
    current_Score_Display = [[], [], []]

    # Setting All Digit Segment Positions
    for i in range(6):
        # Finding Out Which Counter to Add To
        if i < 3:
            x = -134.5 + 50 * i
        else:
            x = 159.5 + 50 * (i % 3)

        # Calculate All 7 Positions Relative To The Center
        cords = [
            (x, y + (offset * 2), 90),  # Top
            (x + offset, y + offset, 0),  # Upper Right
            (x + offset, y - offset, 0),  # Lower Right
            (x, y - (offset * 2), 90),  # Bottom
            (x - offset, y - offset, 0),  # Lower Left
            (x - offset, y + offset, 0),  # Upper Left
            (x, y, 90)  # Middle
        ]

        # Moving All 7 Segments To Their Positions
        for x, y, heading in cords:
            segment = base_Segment.clone()
            segment.setheading(heading)
            segment.goto(x, y)
            if i < 3:
                current_Score_Display[i].append(segment)
            else:
                record_Score_Display[i % 3].append(segment)
    base_Segment.hideturtle()

    # 7 Segment Signals
    seven_Segment_Patterns = [
        '1111110', # 0
        '0110000', # 1
        '1101101', # 2
        '1111001', # 3
        '0110011', # 4
        '1011011', # 5
        '1011111', # 6
        '1110000', # 7
        '1111111', # 8
        '1111011'  # 9
    ]

    return seven_Segment_Patterns, record_Score_Display, current_Score_Display

def adding_To_Score(seven_Segment_Patterns, record_Score_Display, current_Score_Display, current_Score_Int, record_Score_Int):
    # Increasing Current Score Display
    cover = current_Score_Int
    cnt = -1
    while cover > 0:
        num = cover % 10
        pattern = seven_Segment_Patterns[num]
        for i in range(7):
            current_Score_Display[cnt][i].color('#038fff' if pattern[i] == '0' else '#f7f5f0')
        cover //= 10
        cnt -= 1

    # Increasing Record Score Display If Valid
    if current_Score_Int > record_Score_Int:
        record_Score_Int = current_Score_Int
        cover = record_Score_Int
    cnt = -1
    while cover > 0:
        num = cover % 10
        pattern = seven_Segment_Patterns[num]
        for i in range(7):
            record_Score_Display[cnt][i].color('#038fff' if pattern[i] == '0' else '#f7f5f0')
        cover //= 10
        cnt -= 1

    return record_Score_Int

#---------------# Checking Death #---------------#

def checking_Death(snake_Turtles):
    death = 'maybe'

#-------------------# Reset- #-------------------#

def setting_Up_Respawn_Points(num_Side_Tiles, tile_Pix, mid_Tile_Pix):
    respawn_Points = []

    # Making Snake Head Respawn Point
    x = ((num_Side_Tiles // 2) - (num_Side_Tiles * 2 // 5)) * tile_Pix * -1 - (mid_Tile_Pix if num_Side_Tiles % 2 == 1 else 0)
    y = 0
    if num_Side_Tiles % 2 == 0:
        y -= mid_Tile_Pix
    respawn_Points.append((x, y))

    # Making Snake Body Respawn Point
    respawn_Points.append((x - tile_Pix, y))

    # Making Cookies N Creme Respawn Point
    x = ((num_Side_Tiles * 4 // 5) - (num_Side_Tiles // 2) - 1) * tile_Pix + (0 if num_Side_Tiles % 2 == 1 else mid_Tile_Pix)
    y = -mid_Tile_Pix if num_Side_Tiles % 2 == 0 else 0
    respawn_Points.append((x, y))

    return respawn_Points

def restart_Game(snake_Turtles, cookies_N_Creme, respawn_Points, current_Score_Display):
    # Going To Respawn Points
    for i in range(len(snake_Turtles), 1):
        del snake_Turtles[i]

    snake_Turtles[0].shape('0')
    snake_Turtles[0].goto(respawn_Points[0])

    snake_Turtles[1].goto(respawn_Points[1])

    cookies_N_Creme.goto(respawn_Points[2])

    # Resetting Score Counter
    ''' don't feel like doing right now'''

#------------------# Movement #------------------#

def listening_key_presses(future_Turns, snake_turtles):
    bg.listen()

    for key in ('w', 'Up'):
        bg.onkeypress(lambda: up(future_Turns, snake_turtles), key)
    for key in ('a', 'Left'):
        bg.onkeypress(lambda: left(future_Turns, snake_turtles), key)
    for key in ('s', 'Down'):
        bg.onkeypress(lambda: down(future_Turns, snake_turtles), key)
    for key in ('d', 'Right'):
        bg.onkeypress(lambda: right(future_Turns, snake_turtles), key)

def up(future_Turns, snake_turtles):
    current = snake_turtles[0].heading() if len(future_Turns) == 0 else future_Turns[0]
    if len(future_Turns) <= 1 and current not in (90, 270): future_Turns.append(90)

def left(future_Turns, snake_turtles):
    current = snake_turtles[0].heading() if len(future_Turns) == 0 else future_Turns[0]
    if len(future_Turns) <= 1 and current not in (0, 180): future_Turns.append(180)

def down(future_Turns, snake_turtles):
    current = snake_turtles[0].heading() if len(future_Turns) == 0 else future_Turns[0]
    if len(future_Turns) <= 1 and current not in (90, 270): future_Turns.append(270)

def right(future_Turns, snake_turtles):
    current = snake_turtles[0].heading() if len(future_Turns) == 0 else future_Turns[0]
    if len(future_Turns) <= 1 and current not in (0, 180): future_Turns.append(0)

#-----------------# Snake Moving #-----------------#

def snake_Moving(future_Turns, snake_Turtles, cookies_N_Creme, tile_Pix, mid_Tile_Pix, whole_Snake_Cords, cookies_N_Creme_Respawn_Cords, seven_Segment_Patterns, record_Score_Display, current_Score_Display, current_Score_Int, record_Score_Int, position_Count, tail):
    # Checking If Snake Head Is In The Middle Of A Tile
    if position_Count == tile_Pix:
        position_Count = 0

        # Updating All Whole Coordinates
        '''whole_Snake_Cords.insert(0, snake_Turtles[0].pos())
        cookies_N_Creme_Respawn_Cords.remove(whole_Snake_Cords[0])
        if not tail:
            cookies_N_Creme_Respawn_Cords.insert(-1, whole_Snake_Cords[-1])
            whole_Snake_Cords.pop(-1)'''

        # Stopping the Tail From Growing If Can
        tail = False

        # Seeing If Snake Head Is In Cookies N Creme
        if snake_Turtles[0].distance(cookies_N_Creme) < mid_Tile_Pix:
            # Respawning Apple
            respawn_Cookies_N_Creme(cookies_N_Creme_Respawn_Cords, cookies_N_Creme)

            # Adding to Score
            current_Score_Int += 1
            record_Score_Int = adding_To_Score(seven_Segment_Patterns, record_Score_Display, current_Score_Display, current_Score_Int, record_Score_Int)

            # Making Tail
            snake_Turtles.append(snake_Turtles[-1].clone())
            tail = True

        # Making The Body Turtles Change Their Orientation According To The One In Front
        for i in range(-1, -len(snake_Turtles), -1):
            ahead_Turtles_Heading = snake_Turtles[i - 1].heading()
            snake_Turtles[i].setheading(ahead_Turtles_Heading)

        # Making the Head Snake Turn
        if len(future_Turns) >= 1:
            snake_Turtles[0].setheading(future_Turns[0])
            snake_Turtles[0].shape(f'{int(future_Turns[0])}')
            future_Turns.pop(0)

    # Moving Every Snake Turtle
    for i in range(len(snake_Turtles) - (1 if tail else 0)):
        snake_Turtles[i].fd(1)
    bg.update()

    # Updating Position Count
    position_Count += 1

    checking_Death(snake_Turtles)
    turtle.ontimer(lambda: snake_Moving(future_Turns, snake_Turtles, cookies_N_Creme, tile_Pix, mid_Tile_Pix, whole_Snake_Cords, cookies_N_Creme_Respawn_Cords, seven_Segment_Patterns, record_Score_Display, current_Score_Display, current_Score_Int, record_Score_Int, position_Count, tail), 0)

#--------------------# Main #--------------------#

def main():
    # Prompt
    num_Side_Tiles, tile_Pix, mid_Tile_Pix = map_Size()

    # Importing All Images
    import_Images(tile_Pix)

    # Making All Turtles
    bg_painter, base_Segment, score_Cookies_N_Creme, cookies_N_Creme, snake_Trophy, snake_Turtles = all_Turtles(tile_Pix)

    # Generating All Tile Cords
    all_Tile_Cords = generate_All_Tile_Cords(tile_Pix, mid_Tile_Pix)

    # Setting Up Background Looks
    setting_Up_Board_Looks(bg_painter, all_Tile_Cords)
    setting_Up_Score_Counter_Looks(bg_painter, score_Cookies_N_Creme, snake_Trophy)

    # Setting Up Pre-Game Variables
    seven_Segment_Patterns,  record_Score_Display, current_Score_Display = setting_Up_Score_Counter_Function(base_Segment)
    respawn_Points = setting_Up_Respawn_Points(num_Side_Tiles, tile_Pix, mid_Tile_Pix)

    # Starting Game
    cookies_N_Creme = cookies_N_Creme.clone()
    for i in range(len(snake_Turtles)):
        snake_Turtles[i] = snake_Turtles[i].clone()
    restart_Game(snake_Turtles, cookies_N_Creme, respawn_Points, current_Score_Display)

    # Making Coordinates
    whole_Snake_Cords, cookies_N_Creme_Respawn_Cords = generate_Whole_Snake_Cords_And_Cookies_N_Creme_Repawn_Cords(snake_Turtles, mid_Tile_Pix, all_Tile_Cords)

    # Waiting For Key Press
    future_Turns = []
    listening_key_presses(future_Turns, snake_Turtles)

    # Begin Game
    bg.onkeypress(lambda: turtle.ontimer(lambda: snake_Moving(future_Turns, snake_Turtles, cookies_N_Creme, tile_Pix, mid_Tile_Pix, whole_Snake_Cords, cookies_N_Creme_Respawn_Cords, seven_Segment_Patterns, record_Score_Display, current_Score_Display, current_Score_Int = 0, record_Score_Int = 0, position_Count = mid_Tile_Pix, tail = False), 0))

main()
bg.update()
turtle.done()