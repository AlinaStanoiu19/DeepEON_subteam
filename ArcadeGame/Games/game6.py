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
SPECTRUM_SLOTS = 8

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
            if node in self.nodes_availability[self.current_node]:
                self.text_box(node,3,1,arcade.color.WHITE,str(node))
            else:
                self.text_box(node,3,1,arcade.color.BLACK,str(node))

        for column in range(COLUMN_COUNT):
            if self.spec_grid[column] == 0:
                self.text_box(column+1,2,1,arcade.color.BALL_BLUE)
            else:
                self.text_box(column+1,2,1,arcade.color.GREEN, str(self.current_node))

        self.text_box(1,10,12,arcade.color.PINK,str(f"Request: (Source:{self.source}, Target:{self.target}, Slots:{self.slots})")) #print source node
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
        if text: 
            arcade.draw_text(text,col*(MARGIN+WIDTH)-(WIDTH/4),row*(MARGIN+HEIGHT)-(WIDTH/4),arcade.color.BLACK,12)

    def link(self, node1, node2 ):
        if ((node1,node2) in self.link_grid.keys()):
            return (node1, node2)
        elif ((node2,node1) in self.link_grid.keys()):   
            return (node2, node1)
        else: 
            # print("there is no link between these two nodes")
            return


    def on_key_press(self, key, modifiers):
        print("you pressed something ...")
        if key == arcade.key.RIGHT and self.position < (COLUMN_COUNT)-1:
            self.position+=1
            self.update_spec_grid()
        elif key == arcade.key.LEFT and self.position > 0:
            self.position -=1
            self.update_spec_grid()
        elif key == arcade.key.ENTER:
            self.next_node = self.position + 1
            if self.next_node in self.nodes_availability[self.current_node]: 
                # move to node 
                self.move_to_node()
                # check if it is the destination 
                if (self.current_node == self.target):
                    print("You  have reached the destination")
                    self.score += 720/len(self.constructed_path)
                    self.update_link_grid()
                    print(f"this is the updated link grid: {self.link_grid}")
                    self.new_round()
                else: 
                    print("Let's select the next node of the path, we are not there yet")
            else: 
                self.blocks += 1
                if (self.blocks > 3):
                    print("Game has ended")
                    self.new_game()

    
    def move_to_node(self):
        # add the node to the self.constructed_path
        self.constructed_path.append(self.next_node)
        # add the link to the self.route_of_links
        self.route_of_links.append(self.link(self.current_node,self.next_node))
        # name the current node = the next node 
        self.current_node = self.next_node
        # update the available_nodes for the new node
        self.update_node_availability()

    def update_node_availability(self):
        # this update is made for the self.current_node
        for node in self.nodes:
            if (node in self.constructed_path):
                # make it black or don't add it to the availability
                print("This node has been already visited")
            elif(self.link(self.current_node,node) in self.link_grid.keys()):  
                print("there is a link to this node")
                # we have to check for spectrum on the link 
                if (self.check_spectrum(self.link(self.current_node,node))):
                    self.nodes_availability[self.current_node].append(node)
                else:
                    # make it black or don't add it to the availability
                    print("there is no spectrum on this link")
            else: 
                # make it black or don't add it to the availability
                print("there is no link to this node")


    
    def check_spectrum(self, link):
        if not(self.rps[link].size == 0):  # the link is not completely full
            if (self.current_node == self.source):  # we are at the first link in the path
                print(f"we are checking the link: {link}")
                if (self.check_with_link_grid(link)):
                    return True
                else:
                    return False
            else: 
                if (self.check_with_link_grid(link) and self.check_with_history(link)):
                    return True
                else: 
                    return False
        else: 
            return False

    def check_with_link_grid(self,link):
        unavailable_options = []
        for option_index in range(len(self.rps[link])):
            if not all(item == 0 for item in np.bitwise_and(self.rps[link][option_index],self.link_grid[link])):
                unavailable_options.append(option_index)
        self.rps[link] = np.delete(self.rps[link],unavailable_options,axis=0)
        print(f"this is the rsp after checking: {self.rps[link]} and the size: {len(self.rps[link])}")
        if(self.rps[link].size == 0):
            return False
        else: 
            return True


    def check_with_history(self,link):

        unavailable_options = []
        for option_index in range(len(self.rps[link])):
            option_available = 0
            for previous_link in self.route_of_links:
                if self.rps[link][option_index] in self.rps[previous_link]:
                    option_available +=1 
            if not(option_available == len(self.route_of_links)):
                unavailable_options.append(option_index)
        

        self.rps[link] = np.delete(self.rps[link],unavailable_options,axis=0)
        if(self.rps[link].size == 0):
            return False
        else: 
            return True


    def update_link_grid(self): 
        # update the link grid with the first fit, so the first option available in the rps array  
        last_link = self.route_of_links[-1]
        for link in self.route_of_links:
            self.link_grid[link] = np.bitwise_or(self.link_grid[link],self.rps[last_link][0])
    
        

    def update_spec_grid(self):
        self.spec_grid = np.zeros(COLUMN_COUNT, dtype= int)
        self.spec_grid[self.position] = 1
        print("this is spec grid..")
        print(self.spec_grid)

    
    def new_game(self):
        self.score = 0
        self.blocks = 0
        self.edges = [(1,2),(2,3),(1,4),(3,5),(2,5),(4,5),(3,6),(4,6)]
        self.nodes = [1,2,3,4,5,6]
        self.G = nx.Graph()
        self.G.add_edges_from(self.edges)
        self.link_grid = OrderedDict()
        for edge in self.edges: #populate link grid
            self.link_grid[edge] = np.zeros(SPECTRUM_SLOTS, dtype= int)
        print("This is the link grid")
        print(self.edges)
        self.new_round()
                        
    def new_round(self):
        """
        Sets up all parameters for a new round, one roud = one request 
        """
        self.position = 0 
        self.slots = np.random.randint(2,5) 
        self.target = np.random.randint(2,7)
        self.source = np.random.randint(1,self.target)
        self.current_node = self.source
        self.next_node = self.source
        self.constructed_path = [self.source]
        self.route_of_links = []
        rps_array = np.zeros((SPECTRUM_SLOTS+1-self.slots,SPECTRUM_SLOTS),dtype=int)
        first_slot = 0
        for option in range(SPECTRUM_SLOTS+1-self.slots):
            rps_array[option][first_slot:(first_slot+self.slots)] = np.ones(self.slots, dtype=int)
            first_slot += 1
        self.rps = {key: rps_array for key in self.edges}
        self.update_spec_grid() 
        self.nodes_availability = {key: [] for key in self.nodes}
        self.update_node_availability()
        print(f"this is the request: (sorce: {self.source},destination: {self.target}, scpectrum slots: {self.slots})")


def main():
 
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT) 
    start_view=GameView() 
    window.show_view(start_view)  
    arcade.run()


if __name__ == "__main__":
    main()