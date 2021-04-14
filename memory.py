# Memory v5.1
# 
# To do list : 
# - bug fixes - DONE 


import pygame, random, time

# User-defined functions

def main():
   # initialize all pygame modules (some need initialization)
   pygame.init()
   # create a pygame display window
   pygame.display.set_mode((500, 400))
   # set the title of the display window
   pygame.display.set_caption('Memory')   
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
      
      self.FPS = 60
      self.game_Clock = pygame.time.Clock()
      self.close_clicked = False
      self.continue_game = True
      
      # === game specific objects
      self.board_size = 4
      self.width = self.surface.get_width()//5
      self.height = self.surface.get_height()//4      
      self.board = []
      self.tiles_selected = []
      self.previus_clicked = ''
      self.total_opened = []
      self.init_tiles()
      self.create_board()
      self.clicked = False
      self.hidden_board()
      
      self.score = 0
      
   def init_tiles(self):
      # concatenate image strings into a list then shuffle
      self.image0 = pygame.image.load('image0.bmp')
      self.tiles = []
      
      for number in range (0,2):   
         for number in range (1,9):
            # self.tiles contain list of images
            self.tiles.append('image'+str(number)+ '.bmp')
      # shufffling the list
      random.shuffle(self.tiles)
      
   def create_board(self):
      # Create a cover-faced card board 
      i = 0
      for row_index in range(0,self.board_size):
         # create row as an empty list
         row = []
         # for each column index
         
         for col_index in range(0,self.board_size):
            # create tile using row index and column index
            x = col_index * self.width
            y = row_index * self.height
            tile = Tile(x,y,self.width,self.height, self.image0,self.tiles[i], self.surface)
            row.append(tile)
            i += 1
      
         # self.board contains list of Tile classes in 4x4
         self.board.append(row)
      self.total_images = i

   def play(self):
      # Play the game until the player presses the close box.
      # - self is the Game that should be continued or not.

      while not self.close_clicked:  # until player clicks close box
         # play frame
         self.handle_events()
         self.draw()            
         if self.continue_game:
            self.update()
            self.decide_continue()
         self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 

   def handle_events(self):
      # Handle each user event by changing the game state appropriately.
      # - self is the Game whose events will be handled

      events = pygame.event.get()
      for event in events:
         if event.type == pygame.QUIT:
            self.close_clicked = True
         
         if event.type == pygame.MOUSEBUTTONUP:
            self.handle_mouseup(event)
   
   def handle_mouseup (self, event):
      # Handle mouse up events
      
      for row in self.board:
         for tile in row:
            self.clicked = tile.select(event.pos)
            if self.clicked == True:
               self.tiles_selected.append(tile)       
      
   def hidden_board(self):
      # All tiles hidden 
      for row in self.board:
         for tile in row:
            tile.hide_tile()
            
   def update_clock(self):
      self.score = pygame.time.get_ticks() //1000
   
   def draw_score(self):
      # draws score at the top right corner of the window's surface
      score_string = str(self.score)
      font_size = 72
      fg_color = pygame.Color('white') # game = Game(w_surface)

      font = pygame.font.SysFont('',font_size) # SysFont is a function

      text_box = font.render(score_string,True,fg_color,self.bg_color)

      location = (self.surface.get_width() - text_box.get_width(),0)

      self.surface.blit(text_box,location)   
      
   def draw(self):
      # Draw all game objects.
      # - self is the Game to draw
      self.draw_score()
      
      pygame.display.update() # make the updated surface appear on the display
      
   def check_no_match(self):
      # Hide tiles if the two images are not a match
      if len(self.tiles_selected) == 2:  
         
         # Hides tile if they are no match
         if not self.tiles_selected[0].is_same(self.tiles_selected[1]):
            time.sleep(1)
            self.tiles_selected[0].hide_tile()
            self.tiles_selected[1].hide_tile()
            
         # Tracks how many tiles are a match
         elif self.tiles_selected[0].get_class() != self.tiles_selected[1].get_class():
 
            self.tiles.remove(self.tiles_selected[0].get_image())
            self.tiles.remove(self.tiles_selected[1].get_image())
            print(self.tiles)
         
         # If they are duplicate clicks, hide back the tile
         else:
            time.sleep(1)
            self.tiles_selected[0].hide_tile()
            self.tiles_selected[1].hide_tile()            
         
         self.tiles_selected = []      
            
   def update(self):
      # Update the game objects for the next frame.
      # - self is the Game to update
      self.check_no_match()
      self.update_clock()

   def decide_continue(self):
      # Check and remember if the game should continue
      # - self is the Game to check
      if len(self.tiles) == 0:
         self.continue_game = False


class Tile:
   # An object in this class represents a Dot that moves 
   
   def __init__(self, x, y, width, height, hidden_image, image_name, surface):
      # Initialize a card.
      # - surface is the window's pygame.Surface object
      self.rect = pygame.Rect(x,y,width, height)
      self.surface = surface
      self.color = pygame.Color('black')
      self.border_width = 3      
      self.hidden = hidden_image
      self.image_name = image_name
      self.image = pygame.image.load(self.image_name)

   def show_tile(self):
      # Draw the dot on the surface
      # - self is the tile
      self.surface.blit(self.image, self.rect)
      pygame.draw.rect(self.surface, self.color, self.rect, self.border_width)      
      
   def hide_tile(self):
      # Hides a tile
      self.surface.blit(self.hidden, self.rect)
      pygame.draw.rect(self.surface, self.color, self.rect, self.border_width)
      
   def get_image(self):
      # Return string image name
      return self.image_name
      
   def is_same(self, other_tile):
      # returns true if two tiles are the same
      if self.image_name == other_tile.get_image():
         return True
      else:
         return False
         
   def select(self, mouse):
      # returns true if mouse clicks on the card
      selected = False
      if self.rect.collidepoint(mouse):
         selected = True
         self.show_tile()

      return selected
   
   def get_class(self):
      # get tile class for the purpose of duplicate check
      return self
            
         
      
      
main()
