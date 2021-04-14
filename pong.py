import pygame

# Pong.py
# Jaden Lee

def main():
   # initialize all pygame modules (some need initialization)
   pygame.init()
   # create a pygame display window
   pygame.display.set_mode((600, 500))
   # set the title of the display window
   pygame.display.set_caption('Pong Game')   
   # get the display surface
   w_surface = pygame.display.get_surface() 
   # create a game object
   game = Game(w_surface)
   # start the main game loop by calling the play method on the game object
   game.play() 
   # quit pygame and clean up the pygame window
   pygame.quit() 


# User-defined classes

class Game:
   # An object in this class represents a complete game.

   def __init__(self, surface):
      # Initialize a Game.
      self.surface = surface
      self.bg_color = pygame.Color('black')
      
      self.FPS = 90
      self.game_Clock = pygame.time.Clock()
      self.close_clicked = False
      self.continue_game = True
      self.score1 = 0
      self.score2 = 0
      self.maxscore = 11
      self.createBall()
      self.createPaddle()

      
   def createBall (self):
      # Create a ball 
      ball_color = 'white'
      ball_radius = 5
      self.ball_center = [250,250]
      self.ball_velocity = [5,5]
      self.small_ball = Ball(ball_color, ball_radius, self.ball_center, self.ball_velocity, self.surface)
         
      
   def createPaddle(self):
      # Create two paddles
      self.rect_one_center = [100,200]
      self.rect_two_center= [500,200]
      self.rect_size = [10,50]
      self.rect_velocity1 = [0,0]
      self.rect_velocity2 = [0,0]
      self.rect_up = -5
      self.rect_down = 5      
      self.Paddle_One = Paddle('white',self.rect_one_center, self.rect_size, self.rect_velocity1, self.surface, self.ball_center)
      self.Paddle_Two = Paddle('white',self.rect_two_center, self.rect_size, self.rect_velocity2, self.surface, self.ball_center)

   def play(self):
      # Play the game until the player presses the close box.
      while not self.close_clicked:  # until player clicks close box

         self.handle_events()
         self.draw()            
         if self.continue_game:
            self.update()
            self.decide_continue()
         self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 

   def handle_events(self):
      # Handle each user event by changing the game state appropriately.
      self.events = pygame.event.get()

      for event in self.events:
         if event.type == pygame.QUIT:
            self.close_clicked = True
         if event.type == pygame.KEYDOWN:
            self.Keydowns(event)
         if event.type == pygame.KEYUP:
            self.Keyups(event)
            
   def Keyups(self,event):
      # releasing key will stop the paddle from moving 
      if event.key == pygame.K_q:
         self.rect_velocity1[1] = 0
      
      if event.key == pygame.K_a:
         self.rect_velocity1[1] = 0
      
      if event.key == pygame.K_p:
         self.rect_velocity2[1] = 0
         
      if event.key == pygame.K_l:
         self.rect_velocity2[1] = 0

   def Keydowns(self, event):
      
      # Sets velocity of paddles when the key is pressed 
      if event.key == pygame.K_q:
         self.rect_velocity1[1] = self.rect_up
      
      if event.key == pygame.K_a:
         self.rect_velocity1[1] = self.rect_down
      
      if event.key == pygame.K_p:
         self.rect_velocity2[1] = self.rect_up
  
      if event.key == pygame.K_l:
         self.rect_velocity2[1] = self.rect_down
   
   def moveBall(self):
      # Move the ball and Bounce if collision is true
      
      # The ball collides with paddle one
      if self.Paddle_One.collide() and self.ball_velocity[0] < 0:
            self.ball_velocity[0] = -self.ball_velocity[0]
            self.small_ball.move()
      
      # The ball collides with paddle two
      if self.Paddle_Two.collide() and self.ball_velocity[0] > 0:
            self.ball_velocity[0] = -self.ball_velocity[0]
            self.small_ball.move()
      else:
         self.small_ball.move()
     

   def Displayscore1(self):
      # Display player 1's score
      text_color = pygame.Color('white')
      text_bg = pygame.Color('black')
      text_font = pygame.font.SysFont('',50)
      text_image = text_font.render(str(self.score1), True, text_color, text_bg)
      text_loc = (10, 10)
      self.surface.blit(text_image, text_loc)
      
   def Displayscore2(self):
      # Display player 2's score
      text_color = pygame.Color('white')
      text_bg = pygame.Color('black')
      text_font = pygame.font.SysFont('',50)
      text_image = text_font.render(str(self.score2), True, text_color, text_bg)
      text_loc = (560, 10)
      self.surface.blit(text_image, text_loc)
   
   def scoreUpdate(self):
      # Add score by one when the ball hits either side of the boundaries
      ballcenter = self.small_ball.get_center()
      ballradius = self.small_ball.get_radius()
      rightside = self.surface.get_width()
      if  ballcenter[0] < ballradius:
         self.score2 += 1
      if ballcenter[0] + ballradius > rightside:
         self.score1 += 1
      
   def draw(self):
      # Draw all game objects.   
      # clear the display surface first
      self.surface.fill(self.bg_color)
      self.small_ball.draw()
      self.Paddle_One.draw()
      self.Paddle_Two.draw()
      self.Displayscore1() 
      self.Displayscore2()
      pygame.display.update() # make the updated surface appear on the display

   def update(self):
      # Update the game objects for the next frame.
      # - self is the Game to update
      self.scoreUpdate()
      self.moveBall()
      self.Paddle_One.move()
      self.Paddle_Two.move()
      self.Paddle_One.withinBoundary()
      self.Paddle_Two.withinBoundary()
      
   def decide_continue(self):
      # Check and remember if the game should continue
      
      # if a player's score reach the max, discontinue the game
      if self.score1 == self.maxscore or self.score2 == self.maxscore:
         self.continue_game = False


class Ball:
   # An object in this class represents a ball that moves 
   
   def __init__(self, ball_color, ball_radius, ball_center, ball_velocity, surface):
      # Initialize a Dot.
      self.color = pygame.Color(ball_color)
      self.radius = ball_radius
      self.center = ball_center
      self.velocity = ball_velocity
      self.surface = surface
 
   def move(self):
      # Change the location of the ball by adding the corresponding 
      size = self.surface.get_size()
      
      for i in range(0,2):
         self.center[i] = (self.center[i] + self.velocity[i])
         
         # Reverse velocity if the ball hits the boundary
         if self.center[i] < self.radius or self.center[i] + self.radius > size[i]:
            self.velocity[i] = -self.velocity[i]
            
   def get_radius(self):
      # Returns the ball radius
      return self.radius
   
   def get_center(self):
      # Returns the ball center (x,y)
      return self.center
   
   def get_velocity(self):
      # Returns the balls velocity
      return self.velocity
 
   def draw(self):
      # Draw the dot on the surface
      pygame.draw.circle(self.surface, self.color, self.center, self.radius)

class Paddle:
   # Create paddle drawing 
   # Coordinate the movemnt
   # Bounces the ball
   def __init__ (self, color, center, size, velocity, surface, ball_center):
      # Initialize the paddle
      # self is the paddle
      self.color = pygame.Color(color)
      self.surface = surface
      self.center = center
      self.size = size
      self.velocity = velocity
      self.ball_center = ball_center
      
   def move(self):
      # Update the rectengle position by the velocity 
      self.center[1] = self.center[1] + self.velocity[1]
  
   def collide(self):
      # Returns true if the ball collides with the rectangle
      rect = pygame.Rect(self.center,self.size)
      
      return rect.collidepoint(self.ball_center)
      
   def withinBoundary(self):
      # Checks if the ball is out of range and re-center it to the edge
      # Bottom boundary
      if self.center[1] < 0:
         self.center[1] = 0
      
      # Top boundary
      if self.center[1] + self.size[1] > self.surface.get_height():
         self.center[1] = self.surface.get_height() -self.size[1]
         
   
   def draw(self):
      # Draws the paddles to the surface
      pygame.draw.rect(self.surface, self.color, pygame.Rect(self.center, self.size))
      
               
main()