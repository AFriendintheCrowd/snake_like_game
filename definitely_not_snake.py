# definitely_not_snake.py
#WASD to move
#get burger
#---Import Statements---
import turtle
import random
import leaderboard as lb

#---Game Configurations---
burgerShape = "burger.gif"
dogShape = "dog.gif"

wn = turtle.Screen()
wn.addshape(burgerShape) # Make the screen aware of the new file
wn.addshape(dogShape)

score = -1
font_setup = ("Arial",20,"normal")
timer = 30
counter_interval = 1000   #1000 represents 1 second
timer_up = False
leaderboard_file_name = "a122_leaderboard.txt"
print("W = up, A = left, S = down, D = right")
player_name = input("Input your name:")

#---Initialize Turtles---
burger = turtle.Turtle()
burger.speed(0)
burger.shape(burgerShape)

score_writer = turtle.Turtle()
score_writer.speed(0)
score_writer.penup()
score_writer.goto(-450, 350)
score_writer.hideturtle()

counter = turtle.Turtle()
counter.speed(0)
counter.penup()
counter.goto(350, 350)
counter.hideturtle()

burgerDog = turtle.Turtle()
burgerDog.penup()
burgerDog.shape(dogShape)
burgerDog.speed(0)
burgerDogX = burgerDog.xcor()
burgerDogY = burgerDog.ycor()
#---Game Functions---
#subtracts one from timer until it is less than or equal to zero
#then it will set a boolean to true and call the leaderboard function
def countdown():
  global timer, timer_up
  counter.clear()
  if timer <= 0:
    counter.write("Time's Up", font=font_setup)
    timer_up = True
    manage_leaderboard()
    burger.hideturtle()
    burgerDog.hideturtle()
  else:
    counter.write("Timer: " + str(timer), font=font_setup)
    timer -= 1
    counter.getscreen().ontimer(countdown, counter_interval) 

#move burger to a random location
def change_position():
  burger.penup()
  burger.hideturtle()
  new_xpos = random.randint(-375,375)
  new_ypos = random.randint(-325,325)
  burger.goto(new_xpos,new_ypos)
  burger.showturtle()

#checks the x and y coordinates of the burger and the dog
#if they are close enough together and the timer isn't
#greater than or equal to zero it will add one to the score
#and move the burger to a random location
def burgerCollected():
    if abs(burgerDog.xcor() - burger.xcor()) <= 40:
        if abs(burgerDog.ycor() - burger.ycor()) <= 40:
          if timer_up != True:
            update_score()
            change_position()
          else:
            burger.hideturtle()
            burgerDog.hideturtle()

#adds one to the score
#makes turtle clear then write the new score
def update_score():
  global score
  score += 1
  score_writer.clear()
  score_writer.write(score,font = font_setup) 

#manages the leader board by getting the names from the txt file and draws the leaderboard
def manage_leaderboard():

  global score
  global burger

  # get the names and scores from the leaderboard file
  leader_names_list = lb.get_names(leaderboard_file_name)
  leader_scores_list = lb.get_scores(leaderboard_file_name)

  # show the leaderboard with or without the current player
  if (len(leader_scores_list) < 5 or score >= leader_scores_list[4]):
    lb.update_leaderboard(leaderboard_file_name, leader_names_list, leader_scores_list, player_name, score)
    lb.draw_leaderboard(True, leader_names_list, leader_scores_list, burger, score)

  else:
    lb.draw_leaderboard(False, leader_names_list, leader_scores_list, burger, score)

#Checks if the dog's x and y coordinates is past a certain point
#If dog is past that point they will teleport to the other side
def outOfBounds():
  if burgerDog.xcor() <= -400:
    burgerDog.penup()
    burgerDog.hideturtle()
    burgerDog.goto(390, burgerDog.ycor())
    burgerDog.showturtle()
  if burgerDog.xcor() >= 400:
    burgerDog.penup()
    burgerDog.hideturtle()
    burgerDog.goto(-390, burgerDog.ycor())
    burgerDog.showturtle()
  if burgerDog.ycor() <= -325:
    burgerDog.penup()
    burgerDog.hideturtle()
    burgerDog.goto(burgerDog.xcor(), 310)
    burgerDog.showturtle()
  if burgerDog.ycor() >= 325:
    burgerDog.penup()
    burgerDog.hideturtle()
    burgerDog.goto(burgerDog.xcor(), -310)
    burgerDog.showturtle()

#Dog goes forward every ten milliseconds
#Looks to see if a burger is collected every ten milliseconds
#As long as the timer hasn't reached 0  
def dogForward():
  if timer_up != True:
    burgerDog.forward(10 + score)
    outOfBounds()
    wn.ontimer(dogForward, 10)
    wn.ontimer(burgerCollected, 10)
  else:
    burgerDog.hideturtle()
    burger.hideturtle()

#Turns where the turtle is facing accordingly
def north():
  burgerDog.setheading(90)
def south():
  burgerDog.setheading(270)
def east():
  burgerDog.setheading(0)
def west():
  burgerDog.setheading(180)
#---Events---
#Movement keys
wn.onkey(north,"w")
wn.onkey(south, "s")
wn.onkey(west, "a")
wn.onkey(east, "d")

wn.listen()

dogForward()

wn.ontimer(countdown, counter_interval) 
wn.mainloop()