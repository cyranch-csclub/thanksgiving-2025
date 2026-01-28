import turtle
import math
import random
from PIL import Image, ImageTk

# -----#Setup#-----#

bg = turtle.Screen()
bg.setup(750, 750)
bg.bgcolor('#2E3532')
original_apple = Image.open('Apple.gif')
snake_head = Image.open('Snake_head.gif')
# gainsboro

turtle.colormode(255)
turtle.delay(0)
turtle.tracer(0, 0)
bg._pic_ref = None

# Variable to store the original resized image data
BASE_SNAKE_HEAD_IMAGE = None
# Variable to prevent the head Tk image from garbage collection
bg._head_pic_ref = None

def map_size():
    # Prompt for grid size
    num_side_tiles = None
    while num_side_tiles not in ('small', 'regular', 'large'):
        num_side_tiles = bg.textinput('Map Size', 'Please choose a tile size: small, regular or large.')

    # Assign num_side_tiles, tile_pix/mid_tile, and grid_size
    if num_side_tiles == 'small':
        num_side_tiles, tile_pix = 5, 100
    elif num_side_tiles == 'regular':
        num_side_tiles, tile_pix = 10, 50
    else:
        num_side_tiles, tile_pix = 20, 25

    mid_tile = tile_pix // 2
    grid_size = num_side_tiles * tile_pix

    return num_side_tiles, tile_pix, mid_tile, grid_size

def generating_all_tile_cords(grid_size, mid_tile, tile_pix):
    # Generating Possible Cordinate Values
    start = -grid_size // 2 + mid_tile
    end = grid_size // 2
    pos_cord_vals = list(range(start, end, tile_pix))

    # Generating All Tile Cordinates
    all_tile_cords = []
    for x in pos_cord_vals:
        for y in pos_cord_vals:
            all_tile_cords.append((x, y))
    return all_tile_cords, pos_cord_vals


def generate_map(num_side_tiles, tile_pix, grid_size, all_tile_cords):
    # Turtles
    '''tile_maker'''
    tile_maker = turtle.Turtle()
    tile_maker.hideturtle()
    tile_maker.shape('square')
    tile_maker.shapesize(tile_pix / 20)
    tile_maker.color('#999999', 'black')
    tile_maker.penup()

    '''Outer_edge'''
    outer_edge_maker = turtle.Turtle()
    outer_edge_maker.hideturtle()
    outer_edge_maker.pensize(50)
    # outer_edge_maker.pencolor('#8B2635')
    outer_edge_maker.pencolor('gainsboro')

    # Speedy Turtles
    tile_maker.speed(0)
    outer_edge_maker.speed(0)

    # Outer Edge
    outer_edge_maker.penup()
    outer_edge_maker.goto(-grid_size / 2, -grid_size / 2)
    outer_edge_maker.pendown()
    for i in range(4):
        outer_edge_maker.fd(grid_size)
        outer_edge_maker.lt(90)

    # Making of Tiles

    # If you wanted Multi colored Tiles
    '''color1, color2 = '#E0E2DB', '#D2D4C8'
    for i, cord in enumerate(all_tile_cords):
        j = i // num_side_tiles if num_side_tiles % 2 == 0 else 0
        tile_maker.color(color1 if (i + j) % 2 == 0 else color2)
        tile_maker.goto(cord)
        tile_maker.stamp()'''

    # If you want Single colored Tiles
    for cord in all_tile_cords:
        tile_maker.goto(cord)
        tile_maker.stamp()

    # THE END
    bg.update()

def mr_snakey(num_side_tiles, tile_pix, all_tile_cords, mid_tile):
    '''resized_head = snake_head.resize((tile_pix, tile_pix))
    pic = ImageTk.PhotoImage(snake_head)

    # 2. CRITICAL FIX: Store the reference to prevent garbage collection
    bg._pic_ref = pic'''

    # MODIFIED/ADDED: Store the base resized PIL image globally for later use
    global BASE_SNAKE_HEAD_IMAGE, bg
    BASE_SNAKE_HEAD_IMAGE = snake_head.resize((tile_pix, tile_pix))

    # MODIFIED: Use the base image copy to start
    resized_head = BASE_SNAKE_HEAD_IMAGE.copy()

    # MODIFIED: Use resized_head not snake_head for initial registration
    pic = ImageTk.PhotoImage(resized_head)

    # 2. CRITICAL FIX: Store the reference to prevent garbage collection
    # MODIFIED: Use the dedicated head ref
    bg._head_pic_ref = pic

    bg.addshape('resized_head', turtle.Shape("image", pic))

    # Snake Head and Tail
    head_circle = turtle.Turtle()
    head_circle.speed(0)
    head_circle.shape('resized_head')
    #head_semisquare = turtle.Turtle()
    head_circle.penup()

    # Making Turtle Army
    turtle_army = []
    for i in range(len(all_tile_cords) - 1):
        body = turtle.Turtle()
        body.hideturtle()
        body.penup()
        body.shape('circle')
        body.shapesize(1.25)
        body.speed(0)
        body.shapesize(tile_pix / 20)
        body.color('#181F37', 'white')
        turtle_army.append(body)

    # Snake Head Start Position
    column = int(num_side_tiles * 0.2) * num_side_tiles
    row = math.ceil(num_side_tiles * 0.5)
    head_tile_start_pos = all_tile_cords[column + row - 1]
    head_start_pos = (head_tile_start_pos[0] + mid_tile, head_tile_start_pos[1])
    head_circle.goto(head_start_pos)

    # Snake Start Body
    even = 1 if num_side_tiles % 2 == 0 else 0

    snake_turtles = [head_circle]
    whole_snake_cords = [(head_circle.pos())]
    for i in range(num_side_tiles // 2 + head_start_pos[0] // tile_pix - even):
        # Making Snake Beginning Body
        turtle_army[i].goto(head_start_pos[0] + -tile_pix * (i + 1), head_start_pos[1])
        turtle_army[i].showturtle()

        # Adding to Snake Turtles
        snake_turtles.append(turtle_army[i])

        # Making Snakes Current Coordinates
        whole_snake_cords.append(turtle_army[i].pos())

        # Removing Turtle from Turtle Army
        turtle_army.pop()

    print(whole_snake_cords)
    # for i in range(len(snake_turtles) - 1):


    return head_circle, turtle_army, snake_turtles, whole_snake_cords, resized_head

def add_body():
    # turtle_army[count].goto(head_start_pos
    count += 1

def snake_movin(snake_turtles, tile_pix, pos_cord_vals, future_turns, resized_head, rand_apple_pos, whole_snake_cords, all_tile_cords, num_side_tiles, mid_tile, total_grid_size, cnt, apple_spawner, tail):

    # Rename 'resized_head' parameter to 'current_head_pil_image' for clarity
    current_head_pil_image = resized_head

    # Seeing if the Turtle is at the Middle of a Tile
    if snake_turtles[0].xcor() in pos_cord_vals and snake_turtles[0].ycor() in pos_cord_vals:
        tail = False

        # Updating Whole Snake Cords

        even = 1 if tile_pix % 2 != 0 else 0
        whole_snake_cords.insert(0, snake_turtles[0].pos())

        # Checking if the Head is at the Apple
        if snake_turtles[0].distance(rand_apple_pos) < 1:
            apple_spawner.hideturtle()
            apple_spawner.clear()


            snake_turtles.append(snake_turtles[-1].clone())
            tail = True

            apple_spawner, rand_apple_pos, cnt = rand_apple(whole_snake_cords, all_tile_cords, num_side_tiles, tile_pix, mid_tile, total_grid_size, cnt)
            # rand_apple(whole_snake_cords, all_tile_cords, num_side_tiles, tile_pix, mid_tile, total_grid_size, cnt)
        else:
            whole_snake_cords.pop()
        # Making The Body Turtles Change Their Orientation
        for i in range(-1, -len(snake_turtles), -1):
            ahead_turtles_heading = snake_turtles[i - 1].heading()
            snake_turtles[i].setheading(ahead_turtles_heading)

        # Making the Head Snake Turn
        if len(future_turns) >= 1:
            # Turn
            snake_turtles[0].setheading(future_turns[0])
            future_turns.pop(0)

            # Past Snake Head Heading
            past_head_heading = snake_turtles[0].heading()

            # Turning Direction
            #turn_direction = 90 if snake_turtles[0].heading() / 90 < past_head_heading / 90 else -90
            turn_direction = past_head_heading

            global BASE_SNAKE_HEAD_IMAGE, bg
            # Use the consistent base image every time
            new_pil_image = BASE_SNAKE_HEAD_IMAGE.rotate(turn_direction)

            # 4. Convert the NEW PIL image to a Turtle PhotoImage
            new_tk_image = ImageTk.PhotoImage(new_pil_image)

            # 5. Store the new reference to prevent garbage collection
            bg._head_pic_ref = new_tk_image

            # 6. Update the 'resized_head' shape definition in the Turtle Screen
            bg.addshape('resized_head', turtle.Shape("image", new_tk_image))

            # 7. Update the turtle to use the newly updated shape definition
            snake_turtles[0].shape('resized_head')

            # 8. Update the variable for the next loop iteration
            current_head_pil_image = new_pil_image


    for seg in snake_turtles:
        if tail and seg == snake_turtles[-1]:
            continue
        seg.fd(1)
    bg.update()


    bg.ontimer(lambda: snake_movin(snake_turtles, tile_pix, pos_cord_vals, future_turns, current_head_pil_image, rand_apple_pos,  whole_snake_cords, all_tile_cords, num_side_tiles, mid_tile, total_grid_size, cnt, apple_spawner, tail), 0)

def listening_key_presses(future_turns, snake_turtles):
    bg.listen()

    bg.onkey(lambda: up(future_turns, snake_turtles), 'w')
    bg.onkey(lambda: left(future_turns, snake_turtles), 'a')
    bg.onkey(lambda: down(future_turns, snake_turtles), 's')
    bg.onkey(lambda: right(future_turns, snake_turtles), 'd')

def up(future_turns, snake_turtles):
    current = snake_turtles[0].heading() if len(future_turns) == 0 else future_turns[0]
    if len(future_turns) <= 1 and current not in (90, 270): future_turns.append(90)

def left(future_turns, snake_turtles):
    current = snake_turtles[0].heading() if len(future_turns) == 0 else future_turns[0]
    if len(future_turns) <= 1 and current not in (0, 180): future_turns.append(180)

def down(future_turns, snake_turtles):
    current = snake_turtles[0].heading() if len(future_turns) == 0 else future_turns[0]
    if len(future_turns) <= 1 and current not in (90, 270): future_turns.append(270)

def right(future_turns, snake_turtles):
    current = snake_turtles[0].heading() if len(future_turns) == 0 else future_turns[0]
    if len(future_turns) <= 1 and current not in (0, 180): future_turns.append(0)

def rand_apple(whole_snake_cords, all_tile_cords, num_side_tiles, tile_pix, mid_tile, total_grid_size, cnt):
    '''# Apple Proportions
    resized_apple = original_apple.resize((tile_pix // 20, tile_pix // 20))
    pic = ImageTk.PhotoImage(resized_apple)
    bg.addshape('resized_apple', turtle.Shape("image", pic))'''

    resized_apple = original_apple.resize((tile_pix, tile_pix + tile_pix // 20 * 4))
    pic = ImageTk.PhotoImage(resized_apple)

    # 2. CRITICAL FIX: Store the reference to prevent garbage collection
    bg._pic_ref = pic

    # 3. Handle the Shape Registration Manually (No try-except needed this way)
    # Check if the shape name already exists in the screen's dictionary of shapes
    if 'resized_apple' in bg._shapes:
        # If it exists, remove the old one before adding the new size
        del bg._shapes['resized_apple']

    bg.addshape('resized_apple', turtle.Shape("image", pic))

    # Turtle
    apple_spawner = turtle.Turtle()
    apple_spawner.hideturtle()
    apple_spawner.speed(0)
    apple_spawner.shape('resized_apple')
    apple_spawner.penup()

    # Proportion Mult of Apple
    mult = tile_pix / 20

    # Random Square Cords Generator

    # Making Apple
    random_cord = all_tile_cords[random.randint(0, len(all_tile_cords) - 1)]
    apple_spawner.goto(random_cord)
    apple_spawner.showturtle()

    cnt += 1


    # THE END
    bg.update()

    return apple_spawner, apple_spawner.pos(), cnt

def main():
    # Prompt for map size
    num_side_tiles, tile_pix, mid_tile, grid_size = map_size()

    # Making of all tile cords
    all_tile_cords, pos_cord_vals = generating_all_tile_cords(grid_size, mid_tile, tile_pix)

    # Generating Map
    generate_map(num_side_tiles, tile_pix, grid_size, all_tile_cords)

    # Mr. Snakey
    head_circle, turtle_army, snake_turtles, whole_snake_cords, resized_head = mr_snakey(num_side_tiles, tile_pix, all_tile_cords, mid_tile)

    # Listening For Key presses
    future_turns = []
    listening_key_presses(future_turns, snake_turtles)

    cnt = 0
    apple_spawner, rand_apple_pos, cnt = rand_apple(whole_snake_cords, all_tile_cords, num_side_tiles, tile_pix, mid_tile, grid_size, cnt)

    # Making Mr. Snakey Move
    tail = False
    turtle.ontimer(lambda: snake_movin(snake_turtles, tile_pix, pos_cord_vals, future_turns, resized_head, rand_apple_pos,  whole_snake_cords, all_tile_cords, num_side_tiles, mid_tile, grid_size, cnt, apple_spawner, tail), 0)



main()

turtle.done()