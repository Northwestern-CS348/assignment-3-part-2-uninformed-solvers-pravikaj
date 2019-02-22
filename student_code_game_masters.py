from game_master import GameMaster
from read import *
from util import *

class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### student code goes here
        peg1List = []
        peg2List = []
        peg3List = []

        factpass1 = parse_input("fact: (on ?x peg1)")
        bindings1 = self.kb.kb_ask(factpass1)
        if bindings1:
            for i in bindings1:
                peg1List.append(i[1][4:])

        factpass2 = parse_input("fact: (on ?x peg2)")
        bindings2 = self.kb.kb_ask(factpass2)
        if bindings2:
            for i in bindings2:
                peg2List.append(i[1][4:])

        factpass3 = parse_input("fact: (on ?x peg3)")
        bindings3 = self.kb.kb_ask(factpass3)
        if bindings3:
            for i in bindings3:
                peg3List.append(i[1][4:])

        peg1List.sort()
        peg2List.sort()
        peg3List.sort()

        outputTuple = tuple((peg1List, peg2List, peg3List))
        return outputTuple


    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        # Student code goes here
        terms = movable_statement.terms
        disk = terms[0]
        opeg = terms[1]
        npeg = terms[2]

        # RETRACT EMPTY PEG IF DISK MOVED TO AN EMPTY PEG
        # = self.kb.getGameState()

        # RULES
        above_rule = parse_input("rule: ((on ?x ?a)(on ?y ?a)(smaller ?x ?y)) -> (above ?x ?y)")
        move_top = parse_input("rule: ((top ?x ?a)(top ?y ?b)(smaller ?x ?y)) -> (movable ?x ?a ?b)")
        move_empty = parse_input("rule: ((top ?x ?a)(empty ?b)) -> (movable ?x ?a ?b)")


        above_fact = parse_input("fact: (above %(disk)s ?x)" % {'disk': disk})
        above_bindings = self.kb.kb_ask(above_fact)
        if above_bindings:
            new_top = above_bindings[0][1]
            assert_new_top = parse_input("fact: (top %(disk)s %(peg)s)" % {'disk': new_top, 'peg': opeg})
            self.kb.kb_assert(assert_new_top)
            retract_above = parse_input("fact: (above %(diska)s ?(diskb)s)" % {'diska': disk, 'diskb': new_top})
            self.kb.kb_retract(retract_above)
        else:
            assert_empty = parse_input("fact: (empty %(peg)s)" % {'peg': opeg})
            self.kb.kb_assert(assert_empty)

        # ASSERT on and top for newly moved disk
        assert_on = parse_input("fact: (on %(disk)s %(peg)s)" % {'disk': disk, 'peg': npeg})
        assert_top = parse_input("fact: (top %(disk)s %(peg)s)" % {'disk': disk, 'peg': npeg})
        self.kb.kb_assert(assert_on)
        self.kb.kb_assert(assert_top)

        # RETRACT on and top for newly moved disk
        retract_on = parse_input("fact: (on %(disk)s %(peg)s)" % {'disk': disk, 'peg': opeg})
        retract_top = parse_input("fact: (top %(disk)s %(peg)s)" % {'disk': disk, 'peg': opeg})
        self.kb.kb_retract(retract_on)
        self.kb.kb_retract(retract_top)

        # INFER new facts with the newly asserted facts
        self.kb.ie.fc_infer(assert_on, above_rule, self.kb)
        self.kb.ie.fc_infer(assert_top, move_top, self.kb)
        self.kb.ie.fc_infer(assert_top, move_empty, self.kb)



    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here

        row1 = []
        row2 = []
        row3 = []

        factpass1 = parse_input("fact: (position ?tilex ?posa pos1)")
        bindings1 = self.kb.kb_ask(factpass1)
        if bindings1:
            for i in bindings1:
                row1.append(i[1].constant.element[4:])

        factpass2 = parse_input("fact: (position ?tilex ?posa pos2)")
        bindings2 = self.kb.kb_ask(factpass2)
        if bindings2:
            for i in bindings2:
                row2.append(i[1].constant.element[4:])

        factpass3 = parse_input("fact: (position ?tilex ?posa pos3)")
        bindings3 = self.kb.kb_ask(factpass3)
        if bindings3:
            for i in bindings3:
                row3.append(i[1].constant.element[4:])

        outputTuple = tuple((row1, row2, row3))
        return outputTuple



    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here
        terms = movable_statement.terms
        tile = terms[0]
        oposx = terms[1]
        oposy = terms[2]
        nposx = terms[3]
        nposy = terms[4]

        # ASSERT
        assert_pos = parse_input("fact: (position %(tile)s %(posa)s %(posb)s"
                                 % {'tile': tile,'posa': nposx, 'posb': nposy})

        assert_empty_pos = parse_input("fact: (position empt-1 %(posa)s %(posb)s"
                                       % {'posa': oposx, 'posb': oposy})
        self.kb.kb_assert(assert_pos)
        self.kb.kb_assert(assert_empty_pos)

        # RETRACT
        retract_pos = parse_input("fact: (position %(tile)s %(posa)s %(posb)s"
                                  % {'tile': tile,'posa': oposx, 'posb': oposy})
        retract_empty_pos = parse_input("fact: (position empt-1 %(posa)s %(posb)s"
                                        % {'posa': nposx, 'posb': nposy})
        self.kb.kb_retract(retract_pos)
        self.kb.kb_retract(retract_empty_pos)

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
