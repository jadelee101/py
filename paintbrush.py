# Paint brush

import pygame


# User-defined functions

def main():
   # initialize all pygame modules (some need initialization)
   pygame.init()
   # create a pygame display window
   pygame.display.set_mode((500, 400))
   # set the title of the display window
   pygame.display.set_caption('Painting')   
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
      # - self is the Game to initialize
      # - surface is the display window surface object

      # === objects that are part of every game that we will discuss
      self.surface = surface
      self.bg_color = pygame.Color('black')
      self.FPS = 30
      self.game_Clock = pygame.time.Clock()
      self.close_clicked = False
      self.init_Brush()
      
      
   def init_Brush(self):
      # Initialize the brush 
      
      # sets default color 
      self.color = 'red'
      # starting from mid position 
      self.pos = [self.surface.get_width()//2, self.surface.get_height()//2]
      
      self.velocity = [0,0]
      self.brush = Brush(self.pos, self.velocity, self.surface)


   def play(self):
      # Play the game until the player presses the close box.
      # - self is the Game that should be continued or not.

      while not self.close_clicked:  # until player clicks close box
         # play frame
         self.handle_events()
         self.draw()            
         self.update()
         self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 

   def handle_events(self):
      # Handle each user event by changing the game state appropriately.
      # - self is the Game whose events will be handled

      events = pygame.event.get()
      for event in events:
         if event.type == pygame.QUIT:
            self.close_clicked = True
         
         if event.type == pygame.KEYUP:
            self.KeyUp(event)
         
         if event.type == pygame.KEYDOWN:
            self.KeyDown(event)
         
   def KeyUp(self, event):
      # key up events
      
      if event.key == pygame.K_UP:
         self.velocity[1] = 0
         
      if event.key == pygame.K_DOWN:
         self.velocity[1] = 0
         
      if event.key == pygame.K_RIGHT:
            self.velocity[0] = 0
           
      if event.key == pygame.K_LEFT:
            self.velocity[0] = 0 
            
   def KeyDown (self, event):
      # Occurs during the key down event
      # Moves the brush 
      if event.key == pygame.K_UP:
         self.velocity[1] = -5
      if event.key == pygame.K_DOWN:
         self.velocity[1] = 5
      if event.key == pygame.K_RIGHT:
         self.velocity[0] = 5
      if event.key == pygame.K_LEFT:
         self.velocity[0] = -5 
      
      # set colors based on the key press 
      if event.key == pygame.K_b:
         self.color = 'blue'
      if event.key == pygame.K_r:
         self.color = 'red'
      if event.key == pygame.K_y:
         self.color = 'yellow'
      if event.key == pygame.K_g:
         self.color = "green"
      if event.key == pygame.K_SPACE:
         self.color = 'black'
            

   def draw(self):
      # Draw all game objects.
      # - self is the Game to draw
      self.brush.draw(self.color)
           
      pygame.display.update() # make the updated surface appear on the display

   def update(self):
      # Update the game objects for the next frame.
      # - self is the Game to update
      self.brush.move()
      self.brush.withinBoundary()
      

class Brush:
   # An object in this class represents a Dot that moves 
   
   def __init__ (self, center, velocity, surface):
      # Initialize the brush
      self.surface = surface
      self.center = center
      self.velocity = velocity
      self.size = [10,10]
      
      
   def move(self):
      # Change the location of the Dot by adding the corresponding 
      # speed values to the x and y coordinate of its center
      # - self is the brush
      for index in range(0,2):
         self.center[index] = self.center[index] + self.velocity[index]
         
         
   def withinBoundary(self):
      # Checks if the ball is out of range and re-center it to the edge
      # Bottom boundary
      for i in range (0,2):
         if self.center[i] < 0:
            self.center[i] = 0
      
      for i in range (0,2):
         if self.center[i] + self.size[i] > self.surface.get_size()[i]:
            self.center[i] = self.surface.get_size()[i] -self.size[i]
      
      
   def draw(self, color):
      # Draws the brush to the surface
      pygame.draw.rect(self.surface, pygame.Color(color), pygame.Rect(self.center, self.size))


main()
