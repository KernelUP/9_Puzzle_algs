import math
from copy import deepcopy

######################################################################################
###################################################################### MATRIX ########
######################################################################################
class matrix:
    orig_matrix = None
    result_matrix = None
    act_matrix = None
    matrix_size = None
    movable_elem = None
    move_limit = None
    inversions = 0
    step = 0
    moves = []
  
    root = None
    current_node = None

###################################################################### INIT
    def __init__(self, puzzle):
        self.move_limit = puzzle.pop(len(puzzle) - 1)
        self.matrix_size = int(math.sqrt(len(puzzle)))
        self.orig_matrix = matrix.make_matrix_from_array(self, puzzle)
        self.act_matrix = matrix.make_matrix_from_array(self, puzzle)
        self.movable_elem = matrix.find_movable_elem()
        self.result_matrix = matrix.make_result_matrix(self, self.matrix_size)
        self.inversions = matrix.count_inversions()
        self.root = node(self, 0, None)
        self.current_node = self.root

    def make_matrix_from_array(self, puzzle):
        size = int(math.sqrt(len(puzzle)))
        res_matrix = [[0 for m in range(size)] for n in range(size)]
        i, j = (0, 0)
        for item in puzzle:
            if i < size:
                res_matrix[j][i] = item
                i += 1
            else:
                j += 1
                res_matrix[j][0] = item
                i = 1
        return res_matrix

    def find_movable_elem(self):
        elem = self.matrix_size ** 2 
        for m in range(self.matrix_size):
            for n in range (self.matrix_size):
                if self.act_matrix[m][n] == elem:
                    elem_coord = [m,n]
        return elem_coord

    def make_result_matrix(self, matrix_size):
        temp = []
        for k in range(matrix_size ** 2):
            temp.append(k+1)
        return matrix.make_matrix_from_array(self, temp)   

###################################################################### NODES
    def set_current_node(self, node):
        self.current_node = node
    def get_current_node(self):
        return self.current_node
    def get_root_node(self):
        return self.root
    
###################################################################### MOVABLE
    def set_movable_elem(self, coords):
        self.movable_elem = coords
    def get_movable_elem(self):
        return self.movable_elem

###################################################################### MOVES
    def add_new_move(self, move):
        self.moves.append(move)
    def remove_last_move(self):
        self.moves.pop(self.step)

###################################################################### STEP
    def incf_step(self):
        self.step += 1
    def decf_step (self):
        self.step -= 1
    def get_step(self):
        return self.step

###################################################################### INVERSIONS
    def count_inversions(self):
        inv_count = 0
        temp_arr = []
        for m in range(self.matrix_size):
            for n in range(self.matrix_size):
                if self.act_matrix[m][n] == self.movable_elem:
                    continue
                else:
                    temp_arr.append(self.act_matrix[m][n])
        for k in range(len(temp_arr)):
            for i in range(k+1, len(temp_arr)):
                if temp_arr[k] > temp_arr[i]:
                    inv_count += 1
        return inv_count
                
    def has_no_result(self):
        if matrix.eql_matrix(self, self.result_matrix):
            return True
        if self.matrix_size % 2 == 1:
            if self.inversions % 2 == 1:
                return True
            else: return False
        elif self.matrix_size % 2 == 0:
            if self.inversions % 2 == 1:
                if self.movable_elem[0] % 2 == 1:
                    return True
                else: return False
            elif self.inversions % 2 == 0:
                if self.movable_elem[0] % 2 == 0:
                    return True
                else: return False

###################################################################### MATRIX OPERATIONS
    def eql_matrix(self, matrix2):
        for m in range(self.matrix_size):
            for n in range (self.matrix_size):
                if self.act_matrix[m][n] != matrix2[m][n]:
                    return False
        return True

    def is_result(self):
        return matrix.eql_matrix(self, self.result_matrix)

###################################################################### UPRAVY
    def move(self, move):
        if move == 'D':
            move_to = [self.movable_elem[0] + 1, self.movable_elem[1]]
        elif move == 'U':
            move_to = [self.movable_elem[0] - 1, self.movable_elem[1]]
        elif move == 'R':
            move_to = [self.movable_elem[0], self.movable_elem[1] + 1]
        elif move == 'L':
            move_to = [self.movable_elem[0], self.movable_elem[1] - 1]

        self.act_matrix[self.movable_elem[0]][self.movable_elem[1]],
        self.act_matrix[move_to[0]][move_to[1]] = self.act_matrix[move_to[0]][move_to[1]], 
        self.act_matrix[self.movable_elem[0]][self.movable_elem[1]]
        self.add_new_move(move)


###################################################################### SOLVE
    def set_act_matrix(self, matrix):
        self.act_matrix = matrix

    def solve(self):
        if matrix.has_no_result(self):
            return self.moves
        else:
            while self.current_node.depth < self.move_limit:
                if self.current_node.can_go_forward():
                    self.do_step()
                else: self.undo_step()

                if self.is_result():
                    return self.moves


    def do_step(self):
        self.set_current_node(self.current_node.do_step())
        self.incf_step()

    def undo_step(self):
        self.set_current_node(self.current_node.undo_step())
        self.decf_step()
        
        
            

######################################################################################
###################################################################### NODE ##########
######################################################################################
class node:  
    matrix = None

    depth = 0
    parrent = None
    
    child_d = None
    child_u = None
    child_r = None
    child_l = None

    tried = [False for m in range(4)]
    best_move_order = [0 for n in range(4)]

###################################################################### INIT
    def __init__(self, matrix, parrent, depth):
        self.depth = depth
        self.matrix = matrix
        self.parrent = parrent
        self.best_move_order = node.eval_moves(self, matrix)

###################################################################### GET/SET
    def get_matrix(self):
        return self.matrix
    def get_parrent(self):
        return self.parrent
    def get_depth(self):
        return self.depth
    
###################################################################### EVAL
    def eval_moves(self):
        D = -math.inf; U = -math.inf; R = -math.inf; L = -math.inf
        if (self.matrix.movable_elem[0] + 1) < self.matrix.matrix_size:
            act_matrix_copy = deepcopy(self.matrix.act_matrix)
            mov_el = self.matrix.movable_elem
            #new_pos = 
            return D
        if (self.matrix.movable_elem[0] - 1) >= 0:
            return U
        if (self.matrix.movable_elem[1] + 1) < self.matrix.matrix_size:
            return R
        if (self.matrix.movable_elem[1] - 1) >= 0:
            return L
    
###################################################################### FUNCS

    def do_step(self):
        if self.can_go_forward():
            self.best_move_order = self.eval_moves()
            self.create_children()
            direction = self.choose_best_path() 
            self.matrix.move(direction) 
            new_node = self.move(direction)
            return new_node
        else: return False

    def choose_best_path(self):
        return

    def undo_step(self):
        return

    def create_children(self):
        return
    
    def move(self, direction):
        return

    def can_go_forward(self):
        for k in range(4):
            if self.tried[k] == False:
                return True
        return False


