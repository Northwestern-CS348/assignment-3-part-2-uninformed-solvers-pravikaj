
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
        if self.currentState.state == self.victoryCondition:
            return True
        if self.currentState not in self.visited:
            self.visited[self.currentState] = True

        # GENERATE CHILDREN
        curr_state = self.currentState
        if not curr_state.children:
            moves_list = self.gm.getMovables()

            if moves_list:
                for m in moves_list:
                    self.gm.makeMove(m)
                    new_game_state = self.gm.getGameState()
                    # if curr_state.parent and new_game_state is curr_state.state:
                    #     self.gm.reverseMove(m)
                    # else:
                    new_child = GameState(new_game_state, curr_state.depth + 1, m)
                    if new_child not in self.visited:
                        curr_state.children.append(new_child)
                        new_child.parent = curr_state
                    self.gm.reverseMove(m)

        # TRAVERSE TREE
        self.DFS_Traverse()
        print(self.currentState.state)

    def DFS_Traverse(self):
        number_of_children = len(self.currentState.children)
        while self.currentState.parent is not None and self.currentState.nextChildToVisit == number_of_children:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent

        if self.currentState.nextChildToVisit < number_of_children:
            child = self.currentState.children[self.currentState.nextChildToVisit]
            self.currentState.nextChildToVisit += 1
            if child in self.visited:
                self.DFS_Traverse()
            else:
                self.gm.makeMove(child.requiredMovable)
                self.currentState = child


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
        if self.currentState.state == self.victoryCondition:
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
                    new_child = GameState(self.gm.getGameState(), parent.depth+1, m)
                    parent.children.append(new_child)
                    new_child.parent = parent
                    self.gm.reverseMove(m)

        # Traverse Tree
        self.BFS_Traverse()
        return False

    def BFS_Traverse(self):
        # if node is anything but root node
        while self.currentState.parent and self.last_child(self.currentState) is True:
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState = self.currentState.parent

        if self.currentState.parent:  # if the parent exists and move to next child
            self.gm.reverseMove(self.currentState.requiredMovable)
            self.currentState.nextChildToVisit += 1
            self.currentState = self.currentState.parent.children[self.currentState.nextChildToVisit]
            self.gm.makeMove(self.currentState.requiredMovable)

        # when there are children still to visit
        while self.visited[self.currentState] is not True and self.currentState.children:
            child_index = self.currentState.nextChildToVisit
            self.currentState = self.currentState.children[child_index]
            self.gm.makeMove(self.currentState.requiredMovable)
        if self.visited[self.currentState] is not True:
            self.BFS_Traverse()
        return True

    def last_child(self, state):
        number_of_children = len(state.parent.children)
        if number_of_children-1 == state.parent.children.index(state):
            return True
        else:
            return False
