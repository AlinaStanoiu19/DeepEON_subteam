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
COLORS = [	(161, 202, 241), (114, 160, 193),(80, 114, 167),(0, 0, 255), 	(6, 42, 120),	(112, 41, 99),  (148, 87, 235),	(212, 115, 212)]


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
            if node == self.target:
                self.text_box(node, 4, 1, arcade.color.GREEN, str(node))
            
            if node in self.nodes_availability[self.current_node]:
                self.text_box(node,3,1,arcade.color.WHITE,str(node))
            else:
                self.text_box(node,3,1,arcade.color.BLACK,str(node))

        for column in range(COLUMN_COUNT):
            if self.spec_grid[column] != 0:
                self.text_box(column+1,2,1,arcade.color.GREEN, str(self.current_node))


        row = 2
        column = COLUMN_COUNT + 2
        i = 0
        # network represemtation 
        
        for edge in self.edges:
            edge_color = COLORS[i]
            self.text_box(column , row,2 , arcade.color.CANDY_APPLE_RED, str(edge))

            for slot in range(len(self.link_grid[edge])):
                if edge in self.route_of_links:
                    if (self.rps[edge][0][slot] == 1) :
                        self.text_box(column + 2 + slot, row,1 , arcade.color.GREEN)
                    elif (self.link_grid[edge][slot] == 1): 
                        self.text_box(column + 2 + slot, row,1 , arcade.color.BLACK)
                    else:
                        self.text_box(column + 2 + slot, row,1 , edge_color)
        
                elif (self.link_grid[edge][slot] == 1):
                    self.text_box(column + 2 + slot, row,1 , arcade.color.BLACK)
                else:
                    self.text_box(column + 2 + slot, row,1 , edge_color)
                    
            row = row + 1 
            i = i+1

        self.text_box(1,12,12,arcade.color.PINK,str(f"Request: (Source:{self.source}, Target:{self.target}, Slots:{self.slots})")) #print source node
        # self.text_box(18,12,4,arcade.color.PINK,"Topology") 
        # self.text_box(8,12,4,arcade.color.PINK,"Score: {}".format(self.score))
        # self.text_box(1,12,6,arcade.color.PINK,"High Score: {}".format(self.high_score))


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


    def enter(self):
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
                print("---------------------------------------------------------")
                self.new_round()
            else: 
                print("Let's select the next node of the path, we are not there yet")
        else: 
            self.blocks += 1
            if (self.blocks > 3):
                print("Game has ended")
                print("---------------------------------------------------------------")
                self.new_game()

    def on_key_press(self, key, modifiers):
        print(f"route of links so far: {self.route_of_links}")
        if key == arcade.key.KEY_1:
            self.position = 0
            self.update_spec_grid()
            self.enter()
        elif key == arcade.key.KEY_2:
            self.position = 1
            self.update_spec_grid()
            self.enter()
        elif key == arcade.key.KEY_3:
            self.position = 2
            self.update_spec_grid()
            self.enter()
        elif key == arcade.key.KEY_4:
            self.position = 3
            self.update_spec_grid()
            self.enter()
        elif key == arcade.key.KEY_5:
            self.position = 4
            self.update_spec_grid()
            self.enter()
        elif key == arcade.key.KEY_6:
            self.position = 5
            self.update_spec_grid()
            self.enter()
        else: 
            print("INVALID KEY")

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
                print(f"Node {node} has been already visited")
            elif(self.link(self.current_node,node) in self.link_grid.keys()):  
                print(f"there is a link to node {node}")
                # we have to check for spectrum on the link 
                if (self.check_spectrum(self.link(self.current_node,node))):
                    self.nodes_availability[self.current_node].append(node)
                else:
                    # make it black or don't add it to the availability
                    print(f"there is no spectrum on link {self.link(self.current_node,node)}")
            else: 
                # make it black or don't add it to the availability
                print(f"there is no link to node {node}")


    
    def check_spectrum(self, link):
        if not(self.rps[link].size == 0):  # the link is not completely full
            if (self.current_node == self.source):  # we are at the first link in the path
                print(f"we are checking the link: {link}")
                if (self.check_with_link_grid(link)):
                    return True
                else:
                    return False
            else: 
                print(f"we are checking the link: {link}")
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
        print(f"this is the rsp after checking with link grid: {self.rps[link]} and the size: {len(self.rps[link])}")
        if(self.rps[link].size == 0):
            return False
        else: 
            return True


    def check_with_history(self,link):

        available_options = []
        print(f"this is the history: {self.route_of_links}")
        for option_index in range(len(self.rps[link])):
            option_available = 0
            for previous_link in self.route_of_links:
                print(f"previous link rps: {self.rps[previous_link]}")
                print(f"wtf we compare with previous: {self.rps[link][option_index]}")
                if self.rps[link][option_index] in self.rps[previous_link]: # this does not work 
                    option_available +=1 
            print(f"options available: {option_available} and length: {len(self.route_of_links)}")
            if (option_available == len(self.route_of_links)):  #this might not make sense 
                available_options.append(option_index)
                print(f"option index: {option_index}")
        
        total_options = [x for x in range(len(self.rps[link]))]
        unavailable_options = []
        for option in total_options:
            if option not in available_options:
                unavailable_options.append(option) 
        print(f"unavailable option: {unavailable_options}")
        self.rps[link] = np.delete(self.rps[link],unavailable_options,axis=0)
        print(f"this is the rsp after checking with history: {self.rps[link]} and the size: {len(self.rps[link])}")
        
        return (self.rps[link].size != 0)


    def update_link_grid(self): 
        # update the link grid with the first fit, so the first option available in the rps array  
        print(f"the route is: {self.route_of_links}")
        last_link = self.route_of_links[-1]
        print(f"the chosen spectrum is: {self.rps[last_link][0]}")
        
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
        print("----------------------new gamee------------------------------")
        print("This is the link grid")
        print(self.edges)
        self.new_round()
                        
    def new_round(self):
        """
        Sets up all parameters for a new round, one roud = one request 
        """
        self.slots = np.random.randint(2,5) 
        self.target = np.random.randint(1,7)
        self.source = np.random.randint(1,7)
        while self.target == self.source:
            self.source = np.random.randint(1,7)
        self.position = self.source -1
        print("----------------------------------------new round -----------------------------------------")
        print(f"this is the request: (sorce: {self.source},destination: {self.target}, scpectrum slots: {self.slots})")
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
        

def main():
    np.random.seed(42)
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT) 
    start_view=GameView() 
    window.show_view(start_view)  
    arcade.run()


if __name__ == "__main__":
    main()

