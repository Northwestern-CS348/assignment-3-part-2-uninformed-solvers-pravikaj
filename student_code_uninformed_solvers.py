
from solver import *

class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        #

        # Student code goes here:

        # CHECK VICTORY CONDITION
        if self.currentState == self.victoryCondition:
            return True
        if self.currentState not in self.visited:
            self.visited[self.currentState] = True
            return self.currentState == self.victoryCondition

        # GENERATE CHILDREN
        parent = self.currentState
        if not parent.children:
            moves_list = self.gm.getMovables()

            if moves_list:
                for m in moves_list:
                    self.gm.makeMove(m)
                    new_game_state = self.gm.getGameState
                    if parent.parent and new_game_state is parent.parent.state:
                        self.gm.reverseMoveMove(m)
                    else:
                        new_child = GameState(new_game_state, parent.depth+1, m)
                        parent.children.append(new_child)
                        new_child.parent = parent
                        self.gm.reverseMove(m)

        # Traverse Tree
        number_of_children = len(parent.children)
        while parent.nextChildToVisit < number_of_children:
            child = parent.children[parent.nextChildToVisit]
            parent.nextChildToVisit += 1
            if child not in self.visited:
                self.gm.makeMove(child.requiredMovable)
                self.currentState = child
                self.visited[self.currentState] = True
            if child == self.victoryCondition:
                return True
            elif child != self.victoryCondition:
                return False
            else:
                self.gm.reverseMove(self.currentState.requiredMovable)
                self.currentState = self.currentState.parent

        # self.DFS_Traverse(parent)


    # def DFS_Traverse(self, parent):
    #     number_of_children = len(parent.children)
    #     children_length = range(parent.nextChildToVisit, number_of_children)
    #     for i in children_length:
    #         # child_index = parent.nextChildToVisit
    #         child = parent.children[i]
    #         if child not in self.visited:
    #             parent.nextChildToVisit = i
    #             self.gm.makeMove(child.requiredMovable)
    #             self.currentState = child
    #             self.visited[self.currentState] = True
    #             break
    #
    #     if self.currentState.state == self.victoryCondition:
    #         return True
    #     else:
    #         self.gm.reverseMove(self.currentState.requiredMovable)
    #         self.currentState = self.currentState.parent
    #         self.solveOneStep()



class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        ### Student code goes here
        # CHECK VICTORY CONDITION
        if self.currentState == self.victoryCondition:
            return True
        if self.currentState not in self.visited:
            self.visited[self.currentState] = True
            return self.currentState == self.victoryCondition

        # GENERATE CHILDREN
        parent = self.currentState
        if not parent.children:
            moves_list = self.gm.getMovables()
            if moves_list:
                for m in moves_list:
                    self.gm.makeMove(m)
                    new_child = GameState(self.gm.getGameState, parent.depth+1, m)
                    parent.children.append(new_child)
                    new_child.parent = parent
                    self.gm.reverseMove(m)

        # Traverse Tree
        self.BFS_Traverse()
        return False

    def BFS_Traverse(self):
        state = self.currentState
        # if node is anything but root node
        while state.parent and self.last_child(state) is True:
            self.gm.reverseMove(state.requiredMovable)
            self.currentState = state.parent

        if self.currentState.parent:  # if the parent exists
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState.nextChildToVisit += 1
            self.currentState = self.currentState.parent.children[self.currentState.nextChildToVisit]
            self.gm.makeMove(self.currentState.requiredMovable)

        # when there are children still to visit
        while self.visited.get(self.currentState, False) and self.currentState.children:
            child_index = self.currentState.nextChildToVisit
            self.currentState = self.currentState.children[child_index]
            self.gm.makeMove(self.currentState.requiredMovable)
        if self.visited.get(self.currentState, False):
            self.BFS_Traverse()
        return True

    def last_child(self, state):
        number_of_children = len(state.parent.children)
        if number_of_children-1 == state.parent.children.index(state):
            return True
        else:
            return False
