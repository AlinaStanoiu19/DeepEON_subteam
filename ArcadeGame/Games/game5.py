from itertools import islice
from pickletools import pystring
import pygame 
import numpy as np
import networkx as nx
import sys

from config import all_configs

SCREEN_WIDTH = 920
SCREEN_HEIGHT = 150
COLUMN_COUNT = 8
WIDTH = 20
HEIGHT = 20
WHITE = (255,255,255)
BLACK = (0,0,0)
GREEN = (0,255,0)
RED = (255,0,0)

class ArcadeGame:

    def __init__(self):
        self.window = (SCREEN_WIDTH,SCREEN_HEIGHT)
        self.background = pygame.Surface(self.window)
        self.highscore = 0
        self.edges = [(1,2),(2,3),(1,4),(3,5),(2,5),(4,5),(3,6),(4,6)]
        self.G = nx.Graph()
        self.G.add_edges_from(self.edges)
        self.seed()
        self.request_id = 0
    
    def draw_screen(self):
        self.background.fill(RED)
        for k, path in enumerate(self.paths):
            for i,row in enumerate(self.path_grid(path).values()): #print links grid
                for column in range(COLUMN_COUNT):
                    if row[column] == 0:
                        self.draw_box(column+1 + k*9,5 - i,WHITE)
                    else:
                        self.draw_box(column+1 + k*9,5 - i,BLACK)

        for column in range(COLUMN_COUNT*5 + 4): #print slots
            if self.spec_grid[column] == 0:
                self.draw_box(column+1,6,RED)
            else:
                self.draw_box(column+1,6,GREEN)
        
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
            self.link_grid[edge] = np.zeros(COLUMN_COUNT, dtype= int)
        self.new_round()                  
                            
    def new_round(self):
        """
        Sets up all parameters for a new round
        """
        self.request_id += 1
        self.first_slot = 0
        self.target = np.random.randint(2,7)
        self.source = np.random.randint(1,self.target)
        p = nx.shortest_simple_paths(self.G,self.source,self.target)
        self.paths = list(islice(p,5))
        self.slots = np.random.randint(2,5)
        self.update_spec_grid()#populate spectrum grid
        self.constructed_path = [self.source]
        self.route_of_links = []

    def update_spec_grid(self):
        self.spec_grid = np.zeros(COLUMN_COUNT*5 + 4, dtype= int)
        for i in range(self.slots):
            self.spec_grid[self.first_slot+i] = 1

    
    def get_request_info(self):
        return {'id': self.request_id, 'source': self.source, 'target': self.target, 
                   'slots': self.slots, 'constructed_path':self.constructed_path,
                     'route_of_links':self.route_of_links}
    
    def link(self, node1, node2 ):
        if ((node1,node2) in self.link_grid.keys()):
            return (node1, node2)
        elif ((node2,node1) in self.link_grid.keys()):   
            return (node2, node1)
        # else: 
            # print("there is no link between these two nodes")
            # return

    def check_solution(self):
        done = False
        selected_path = self.first_slot//9 # !!check first slot is correct
        self.constructed_path = self.paths[selected_path]
        print(f"this is the selected path: {selected_path} and constructed_paths: {self.constructed_path}")
        for n in range(len(self.constructed_path)-1):
            self.route_of_links.append(self.link(self.constructed_path[n], self.constructed_path[n+1]))
        print(f"this is the route of links: {self.route_of_links}")
        if self.is_solution():
            reward = all_configs["solution_reward"]
            self.score += all_configs["solution_reward"]
            self.update_link_grid()
            request_info = self.get_request_info()
            self.new_round()
            print(f"SOLUTION TRUE {reward}")
        else:
            self.blocks += 1
            reward = all_configs["rejection_reward"]
            self.score += all_configs["rejection_reward"]
            request_info = self.get_request_info()
            if self.blocks > 2:
                if self.score > self.highscore:
                    self.highscore = self.score
                done = True
            print(f"SOLUTION FALSE {reward}")
        return reward, done, request_info

    def is_solution(self, first_slot = -1):
        """
        Checks for solution
        """
        if first_slot == -1:
            first_slot = self.first_slot

        if not self.spec_grid[8] == 1 and not self.spec_grid[17] == 1 and not self.spec_grid[26] == 1 and not self.spec_grid[35] == 1:
            self.path_selected = first_slot//9
            self.ans_grid = self.path_grid(self.paths[self.path_selected])
            self.temp_first_slot = first_slot - self.path_selected*9
            for row in self.ans_grid.values(): #for spectrum of each link
                for i in range(self.slots): #for each slot
                    #print(self.temp_first_slot + i, first_slot)
                    if row[self.temp_first_slot + i] != 0: #if slot in spectrum is occupied 
                        return False
            return True
        else:
            return False

    def path_grid(self, path):
        i = 0 
        all_edges = []
        while i < len(path)-1: #prepare all edges in path
            if path[i] < path[i+1]:
                all_edges.append((path[i],path[i+1]))
            else:
                all_edges.append((path[i+1],path[i]))
            i+=1

        temp_path_grid = {}
        for edge in all_edges: #populate answer grid with edges 
            temp_path_grid[edge]= self.link_grid[edge]
        return temp_path_grid

    def update_link_grid(self):
        for edge in self.ans_grid.keys():
            grid = self.link_grid[edge]
            for i in range(self.slots):
                grid[self.temp_first_slot+i] = 1
            self.link_grid[edge] = grid

    def seed(self):
        np.random.seed(all_configs["seed"])

    def exit(self):
        pygame.quit()
        sys.exit()