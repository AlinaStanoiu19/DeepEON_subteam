from itertools import islice
from pickletools import pystring
import pygame 
import numpy as np
import networkx as nx
import sys
import cv2

SCREEN_WIDTH = 920
SCREEN_HEIGHT = 150
COLUMN_COUNT = 6
WIDTH = 20
HEIGHT = 20
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)

class ArcadeGame:

    def __init__(self, config):
        self.config = config
        self.window = (SCREEN_WIDTH,SCREEN_HEIGHT)
        self.background = pygame.Surface(self.window)
        self.highscore = 0
        self.edges = [(1,2),(2,3),(1,4),(3,5),(2,5),(4,5),(3,6),(4,6)]
        self.nodes = [1,2,3,4,5,6]
        self.G = nx.Graph()
        self.G.add_edges_from(self.edges)
        self.seed()
    
    def draw_screen(self):
        self.background.fill(RED)

        for node in self.nodes: 
            # prints out target node layer (top row)
            if node == self.target:
                self.draw_box(node,4,GREEN)
            else:
                self.draw_box(node,4,WHITE)
            
            # prints out the next available nodes (mid row)
            if self.is_node_available(node):
                self.draw_box(node,3,WHITE)
            else: 
                self.draw_box(node,3,BLACK)
            
        # prints out current node selection (bot row)
        for column in range(COLUMN_COUNT):
            if self.spec_grid[column] == 0:
                self.draw_box(column+1,2,RED)
            else:
                self.draw_box(column+1,2,GREEN)

        # for k, path in enumerate(self.paths):
        #     for i, row in enumerate(self.path_grid(path).values()): #print links grid
        #         for column in range(COLUMN_COUNT):
        #             if row[column] == 0:
        #                 self.draw_box(column+1 + k*9,5 - i,WHITE)
        #             else:
        #                 self.draw_box(column+1 + k*9,5 - i,BLACK)

        # for column in range(COLUMN_COUNT*5 + 4): #print slots
        #     if self.spec_grid[column] == 0:
        #         self.draw_box(column+1,6,RED)
        #     else:
        #         self.draw_box(column+1,6,GREEN)
        
        self.surfarr = pygame.surfarray.array3d(self.background)
        return self.surfarr

    def render(self):
        self.screen = pygame.display.set_mode(self.window)
        self.screen.blit(self.background,(0,0))
        pygame.display.flip()
        print(f"Number of blocks: {self.blocks} Score: {self.score} High Score: {self.highscore}")

    def draw_box(self,col,row,colour):
        pygame.draw.rect(self.background,colour,(col*20,row*20,WIDTH,HEIGHT))

    def new_game(self):
        self.score = 0
        self.blocks = 0
        self.link_grid = {}
        for edge in self.edges: #populate link grid
            self.link_grid[edge] = np.zeros(1, dtype= int)
        print("This is the link grid")
        print(self.edges)
        self.new_round()                  
                            
    def new_round(self):
        """
        Sets up all parameters for a new round
        """
        self.first_slot = 0
        self.target = np.random.randint(2,7)
        self.source = np.random.randint(1,self.target)
        self.position = self.source-1
        self.current_node = self.source
        self.next_node = self.source
        self.constructed_path = [self.source]
        self.update_spec_grid()#populate spectrum grid

    def update_spec_grid(self):
        self.spec_grid = np.zeros(COLUMN_COUNT, dtype= int)
        self.spec_grid[self.position] = 1
        print("This is the spec grid..")
        print(self.spec_grid)

    def check_node(self):
        done = False

        if self.is_node():
            if ((self.current_node) == self.target):
                reward = self.config["solution_reward"]
                print("You have reached the destination")
                self.score += 720/len(self.constructed_path)
                self.update_link_grid()
                self.new_round()
        else:
            reward = self.config["rejection_reward"]
            self.score += self.config["rejection_reward"]
            done = True
            print("try again")
        
        return reward, done

    def is_node_available(self, node): 
        self.next_node = node
        if (self.next_node in self.constructed_path):
            return False
        elif(((self.current_node,self.next_node) in self.link_grid.keys()) or ((self.next_node,self.current_node) in self.link_grid.keys())):
            return True
        else: 
            return False

    def is_node(self):
        self.next_node = self.position+1
        if (self.next_node in self.constructed_path):
            print("you have been here before")
            return False
        elif(((self.current_node,self.next_node) in self.link_grid.keys()) or ((self.next_node,self.current_node) in self.link_grid.keys())):
            print(self.current_node,self.next_node)
            print("It is a link")
            self.constructed_path.append(self.next_node)
            self.update_link_grid()
            self.current_node = self.next_node
            print("this is the path so far")
            print(self.constructed_path)
            print("this is the link grid")
            print(self.link_grid)
            return True
        else: 
            return False

    def update_link_grid(self):
        if ((self.current_node,self.next_node) in self.link_grid.keys()):
            self.link_grid[(self.current_node,self.next_node)][0] =1
        else:   
             self.link_grid[(self.next_node,self.current_node)][0] =1

    def seed(self):
        np.random.seed(self.config["seed"])

    def exit(self):
        pygame.quit()
        sys.exit()