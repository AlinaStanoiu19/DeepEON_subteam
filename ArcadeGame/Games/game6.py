from typing import OrderedDict
import arcade
import numpy as np
import networkx as nx
import time
from itertools import islice

WIDTH = 20
HEIGHT = 20
MARGIN = 5
ROW_COUNT = 8
COLUMN_COUNT = 6
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 350
TIME = 30

class GameView(arcade.View):
    """
    Main application class.
    """

    def __init__(self):
        super().__init__()
        arcade.set_background_color(arcade.color.CANDY_APPLE_RED)
        self.high_score = 0
        self.new_game()
        
    def on_draw(self):
        """
        Render the screen.
        """
        arcade.start_render()

        for node in self.nodes: 
            if self.is_node_available(node):
                self.text_box(node,3,1,arcade.color.WHITE,str(node))
            else: 
                self.text_box(node,3,1,arcade.color.BLACK,str(node))

        for column in range(COLUMN_COUNT): #print slots
            if self.spec_grid[column] == 0:
                self.text_box(column+1,2,1,arcade.color.BALL_BLUE)
            else:
                self.text_box(column+1,2,1,arcade.color.GREEN, str(self.current_node))

        self.text_box(1,10,12,arcade.color.PINK,str(f"Request: (Source:{self.source}, Target:{self.target})")) #print source node
        self.text_box(18,12,4,arcade.color.PINK,"Topology") 
        self.text_box(8,12,4,arcade.color.PINK,"Score: {}".format(self.score))
        self.text_box(1,12,6,arcade.color.PINK,"High Score: {}".format(self.high_score))


    def text_box(self,col,row,width,colour,text=None):
        """
        Prints a rectangle with given dimensions and colour and inserts given text 
        """
        if width%2 == 0:
            arcade.draw_rectangle_filled((col + width/2)*(MARGIN+WIDTH) - (MARGIN+WIDTH)/2,row*(MARGIN+HEIGHT),width*(WIDTH+MARGIN)-MARGIN,HEIGHT,colour)
        else:
            arcade.draw_rectangle_filled((col + width//2)*(MARGIN+WIDTH),row*(MARGIN+HEIGHT),width*(WIDTH+MARGIN)-MARGIN,HEIGHT,colour)
        if text: #print text
            arcade.draw_text(text,col*(MARGIN+WIDTH)-(WIDTH/4),row*(MARGIN+HEIGHT)-(WIDTH/4),arcade.color.BLACK,12)


    def on_key_press(self, key, modifiers):
        print("you pressed something ...")
        if key == arcade.key.RIGHT and self.position < (COLUMN_COUNT)-1:
            self.position+=1
            self.update_spec_grid()
        elif key == arcade.key.LEFT and self.position > 0:
            self.position -=1
            self.update_spec_grid()
        elif key == arcade.key.ENTER:
            self.check_node()

    def check_node(self):

        if self.is_node_available(self.position+1):
            print(self.current_node,self.next_node)
            print("It is a link")
            self.constructed_path.append(self.next_node)
            self.update_link_grid()
            self.current_node = self.next_node
            print("this is the path so far")
            print(self.constructed_path)
            print("this is the link grid")
            print(self.link_grid)
            if ((self.current_node) == self.target):
                print("you have reached the destination")
                self.score += 720/len(self.constructed_path)
                self.new_round()
            else:
                print("Let's select the next node of the path, we are not there yet")
        else: 
            print("try again")

    def is_node_available(self, node): 
        self.next_node = node
        if (self.next_node in self.constructed_path):
            return False
        elif(((self.current_node,self.next_node) in self.link_grid.keys()) or ((self.next_node,self.current_node) in self.link_grid.keys())):
            return True
        else: 
            return False


    def update_link_grid(self):
        if ((self.current_node,self.next_node) in self.link_grid.keys()):
            self.link_grid[(self.current_node,self.next_node)][0] =1
        else:   
             self.link_grid[(self.next_node,self.current_node)][0] =1

    def update_spec_grid(self):
        self.spec_grid = np.zeros(COLUMN_COUNT, dtype= int)
        self.spec_grid[self.position] = 1
        print("this is spec grid..")
        print(self.spec_grid)

    
    def new_game(self):
        self.score = 0
        self.edges = [(1,2),(2,3),(1,4),(3,5),(2,5),(4,5),(3,6),(4,6)]
        self.nodes = [1,2,3,4,5,6]
        self.G = nx.Graph()
        self.G.add_edges_from(self.edges)
        self.link_grid = OrderedDict()
        for edge in self.edges: #populate link grid
            self.link_grid[edge] = np.zeros(1, dtype= int)
        print("This is the link grid")
        print(self.edges)
        self.new_round()                  
                        
    def new_round(self):
        """
        Sets up all parameters for a new round
        """
        self.position = 0 
        self.target = np.random.randint(2,7)
        self.source = np.random.randint(1,self.target)
        self.current_node = self.source
        self.next_node = self.source
        self.constructed_path = [self.source]
        self.update_spec_grid()#populate spectrum grid


def main():
 
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT) #initiate window
    start_view=GameView() #start with game view
    window.show_view(start_view)  
    arcade.run() #this will run the on_draw() function 


if __name__ == "__main__":
    main()