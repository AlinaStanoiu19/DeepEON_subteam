from itertools import islice
from pickletools import pystring
import pygame 
import numpy as np
import networkx as nx
import sys
import cv2
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

    def __init__(self, config):
        self.config = config
        self.window = (SCREEN_WIDTH,SCREEN_HEIGHT)
        self.background = pygame.Surface(self.window)
        self.highscore = 0
        self.edges = [(1,2),(2,3),(1,4),(3,5),(2,5),(4,5),(3,6),(4,6)]
        self.G = nx.Graph()
        self.G.add_edges_from(self.edges)
        self.seed()
    
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
        self.first_slot = 0
        self.target = np.random.randint(2,7)
        self.source = np.random.randint(1,self.target)
        p = nx.shortest_simple_paths(self.G,self.source,self.target)
        self.paths = list(islice(p,5))
        self.slots = np.random.randint(2,5)
        self.update_spec_grid()#populate spectrum grid

    def update_spec_grid(self):
        self.spec_grid = np.zeros(COLUMN_COUNT*5 + 4, dtype= int)
        for i in range(self.slots):
            self.spec_grid[self.first_slot+i] = 1

    def check_solution(self):
        done = False
        if self.is_solution():
            reward = self.config["solution_reward"]
            self.score += self.config["solution_reward"]
            self.update_link_grid()
            self.new_round()
        else:
            self.blocks += 1
            reward = self.config["rejection_reward"]
            self.score += self.config["rejection_reward"]
            if self.blocks > 2:
                if self.score > self.highscore:
                    self.highscore = self.score
                done = True
        return reward, done

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
        np.random.seed(self.config["seed"])

    def exit(self):
        pygame.quit()
        sys.exit()