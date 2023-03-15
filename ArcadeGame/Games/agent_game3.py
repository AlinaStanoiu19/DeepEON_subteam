from itertools import islice
from pickletools import pystring
import pygame 
import numpy as np
import random
import networkx as nx
import sys
from typing import OrderedDict
from config import all_configs

SPECTRUM_SLOTS = all_configs["number_of_slots"]
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 200
COLUMN_COUNT = 6
WIDTH = 20
HEIGHT = 20
WHITE = all_configs["white"]
BLACK = all_configs["black"]
GREEN = all_configs["green"]
RED = all_configs["red"]

class ArcadeGame:
    def __init__(self):
        self.window = (SCREEN_WIDTH,SCREEN_HEIGHT)
        self.background = pygame.Surface(self.window)
        self.edges = [(1,2),(2,3),(1,4),(3,5),(2,5),(4,5),(3,6),(4,6)]
        self.nodes = [1,2,3,4,5,6]
        self.G = nx.Graph()
        self.G.add_edges_from(self.edges)
        self.seed()
        self.request_id = 0
    
    def new_game(self):
        self.blocks = 0
        self.link_grid = OrderedDict()
        for edge in self.edges: #populate link grid
            self.link_grid[edge] = np.zeros(SPECTRUM_SLOTS, dtype= int)
        self.new_round()

    def new_round(self):
        print("-   NEW ROUND   -")
        first_slot = 0
        self.slots = np.random.randint(2,5) 
        self.target, self.source = random.sample(range(1,7), 2)
        print(f"Target: {self.target} | Source: {self.source} | Slots: {self.slots}")
        self.position = self.source-1
        self.current_node = self.source
        self.next_node = self.source
        self.constructed_path = [self.source]
        self.route_of_links = []

        rps_array = np.zeros((SPECTRUM_SLOTS+1-self.slots,SPECTRUM_SLOTS),dtype=int)

        for option in range(SPECTRUM_SLOTS+1-self.slots):
            rps_array[option][first_slot:(first_slot+self.slots)] = np.ones(self.slots, dtype=int)
            first_slot += 1

        self.rps = {key: rps_array for key in self.edges}
        self.update_spec_grid() 
        self.nodes_availability = {key: [] for key in self.nodes}
        self.update_node_availability()

        self.request_id += 1

    def draw_screen(self):
        self.background.fill(RED)

        for node in self.nodes: 
            # prints out target node layer (top row)
            if node == self.target:
                self.draw_box(node,2,GREEN)
            
            # prints out the next available nodes (mid row)
            if node in self.nodes_availability[self.current_node]:
                self.draw_box(node,3,WHITE)
            else: 
                self.draw_box(node,3,BLACK)
            
        # prints out current node selection (bot row)
        for column in range(COLUMN_COUNT):
            if self.spec_grid[column] != 0:
                self.draw_box(column+1,4,GREEN)

        self.surfarr = pygame.surfarray.array3d(self.background)
        return self.surfarr

    def draw_box(self,col,row,colour):
        pygame.draw.rect(self.background,colour,(col*20,row*20,WIDTH,HEIGHT))

    def link(self, node1, node2 ):
        if ((node1,node2) in self.link_grid.keys()):
            return (node1, node2)
        elif ((node2,node1) in self.link_grid.keys()):   
            return (node2, node1)
        else: 
            # print("there is no link between these two nodes")
            return

    def check_solution(self, node):
        done = False
        self.next_node = node
        reward = 0 # should not be like this

        if self.next_node in self.nodes_availability[self.current_node]: 
            # move to node 
            self.move_to_node()
            # check if it is the destination 
            if (self.current_node == self.target):
                # print("You  have reached the destination")
                reward = all_configs["solution_reward"]
                print(f"!!! Target reached ({reward})")
                self.update_link_grid()
                # print(f"this is the updated link grid: {self.link_grid}")
                self.new_round()

        else: 
            self.blocks += 1
            reward = all_configs["rejection_reward"]
            print(f"! Rejection ({reward})")
            if (self.blocks > 3):
                # print("Game has ended")
                done = True
        request_info = {'id': self.request_id, 'source': self.source, 'target': self.target, 
                   'slots': self.slots, 'constructed_path':self.constructed_path,
                     'route_of_links':self.route_of_links}

        return reward, done, request_info

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
                # print("This node has been already visited")
                pass
            elif(self.link(self.current_node,node) in self.link_grid.keys()):  
                # print("there is a link to this node")
                # we have to check for spectrum on the link 
                if (self.check_spectrum(self.link(self.current_node,node))):
                    self.nodes_availability[self.current_node].append(node)
                else:
                    # make it black or don't add it to the availability
                    # print("there is no spectrum on this link")
                    pass
            else: 
                # make it black or don't add it to the availability
                # print("there is no link to this node")
                pass

    def check_spectrum(self, link):
        if not(self.rps[link].size == 0):  # the link is not completely full
            if (self.current_node == self.source):  # we are at the first link in the path
                # print(f"we are checking the link: {link}")
                return (self.check_with_link_grid(link))
            else: 
                return (self.check_with_link_grid(link) and self.check_with_history(link))
        else: 
            return False

    def check_with_link_grid(self,link):
        unavailable_options = []
        for option_index in range(len(self.rps[link])):
            if not all(item == 0 for item in np.bitwise_and(self.rps[link][option_index],self.link_grid[link])):
                unavailable_options.append(option_index)
        self.rps[link] = np.delete(self.rps[link],unavailable_options,axis=0)
        # print(f"this is the rsp after checking: {self.rps[link]} and the size: {len(self.rps[link])}")
        return self.rps[link].size != 0


    def check_with_history(self,link):

        unavailable_options = []
        for option_index in range(len(self.rps[link])):
            option_available = 0
            for previous_link in self.route_of_links:
                for op in self.rps[previous_link]:
                    if all(op == self.rps[link][option_index]):
                        option_available +=1
            if (option_available != len(self.route_of_links)):
                unavailable_options.append(option_index)

        self.rps[link] = np.delete(self.rps[link],unavailable_options,axis=0)
        return (self.rps[link].size != 0)



    def update_link_grid(self): 
        # update the link grid with the first fit, so the first option available in the rps array  
        last_link = self.route_of_links[-1]
        for link in self.route_of_links:
            self.link_grid[link] = np.bitwise_or(self.link_grid[link],self.rps[last_link][0])
    
    def update_spec_grid(self):
        self.spec_grid = np.zeros(COLUMN_COUNT, dtype= int)
        self.spec_grid[self.position] = 1
        print(f"Current node selection grid: {self.spec_grid}")

    def render(self):
        self.screen = pygame.display.set_mode(self.window)
        self.screen.blit(self.background,(0,0))
        pygame.display.flip()
        
    def seed(self):
        np.random.seed(all_configs["seed"])

    def exit(self):
        pygame.quit()
        sys.exit()