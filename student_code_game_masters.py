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
        peg1_list = []
        peg2_list = []
        peg3_list = []
        factpass1 = parse_input("fact: (on ?x peg1)")
        factpass2 = parse_input("fact: (on ?x peg2)")
        factpass3 = parse_input("fact: (on ?x peg3)")

        bindings1 = self.kb.kb_ask(factpass1)
        if bindings1:
            for i in bindings1:
                peg1_list.append(int(i.bindings_dict['?x'].replace('disk', '')))

        bindings2 = self.kb.kb_ask(factpass2)
        if bindings2:
            for i in bindings2:
                peg2_list.append(int(i.bindings_dict['?x'].replace('disk', '')))

        bindings3 = self.kb.kb_ask(factpass3)
        if bindings3:
            for i in bindings3:
                peg3_list.append(int(i.bindings_dict['?x'].replace('disk', '')))

        peg1_list.sort()
        peg2_list.sort()
        peg3_list.sort()

        output_list = [tuple(peg1_list), tuple(peg2_list), tuple(peg3_list)]
        output_tuple = tuple(output_list)
        return output_tuple


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
        # Check if move is legal in the first place
        if not(self.isMovableLegal(movable_statement)):
            pass
        else:
            # match_help = self.produceMovableQuery()
            # terms = match(movable_statement, match_help.statement)
            # if terms:
            #     disk = terms.bindings[0].constant
            #     opeg = terms.bindings[1].constant
            #     npeg = terms.bindings[2].constant

                disk = str(movable_statement.terms[0])
                opeg = str(movable_statement.terms[1])
                npeg = str(movable_statement.terms[2])

                # RETRACT on and top for newly moved disk
                retract_on = parse_input("fact: (on %(disk)s %(peg)s)" % {'disk': disk, 'peg': opeg})
                retract_top = parse_input("fact: (top %(disk)s %(peg)s)" % {'disk': disk, 'peg': opeg})
                self.kb.kb_retract(retract_on)
                self.kb.kb_retract(retract_top)

                #  Updating facts of Old Peg
                onTopOf_fact = parse_input("fact: (onTopOf %(disk)s ?x)" % {'disk': disk})
                oto_bindings = self.kb.kb_ask(onTopOf_fact)
                if not oto_bindings:
                    assert_empty = parse_input("fact: (empty %(peg)s)" % {'peg': opeg})
                    self.kb.kb_assert(assert_empty)
                else:
                    new_top = oto_bindings[0].bindings_dict['?x']  # is this how you index into bindings?
                    assert_new_top = parse_input("fact: (top %(disk)s %(peg)s)" % {'disk': new_top, 'peg': opeg})
                    self.kb.kb_assert(assert_new_top)
                    retract_onTopOf = parse_input("fact: (onTopOf %(diska)s %(diskb)s" % {'diska': disk, 'diskb': new_top})
                    self.kb.kb_retract(retract_onTopOf)


                #  Updating facts of Target Peg
                empty_fact = parse_input("fact: (empty ?(newpeg)s" % {'newpeg': npeg})
                empty_bindings = self.kb.kb_ask(empty_fact)
                if empty_bindings:
                    self.kb.kb_retract(empty_fact)

                    # ASSERT on and top for newly moved disk
                    assert_on = parse_input("fact: (on %(disk)s %(peg)s)" % {'disk': disk, 'peg': npeg})
                    self.kb.kb_assert(assert_on)
                    assert_top = parse_input("fact: (top %(disk)s %(peg)s)" % {'disk': disk, 'peg': npeg})
                    self.kb.kb_assert(assert_top)

                else:
                    #  Retract old top on target peg
                    curr_top = parse_input("fact: (top ?x %(peg)s") % {'peg': npeg}
                    old_top_bindings = self.kb.kb_ask(curr_top)
                    old_top = old_top_bindings[0].bindings_dict['?x']
                    retract_old_top = parse_input("fact: (top %(disk)s %(peg)s)" % {'disk': old_top, 'peg': npeg})
                    self.kb.kb_retract(retract_old_top)

                    #  Assert new OnTopOf
                    new_oto = parse_input("fact: (onTopOf %(diska)s %(diskb)s)" % {'diska': disk, 'diskb': old_top})
                    self.kb.kb_assert(new_oto)

                    # ASSERT on and top for newly moved disk
                    assert_on = parse_input("fact: (on %(disk)s %(peg)s)" % {'disk': disk, 'peg': npeg})
                    self.kb.kb_assert(assert_on)
                    assert_top = parse_input("fact: (top %(disk)s %(peg)s)" % {'disk': disk, 'peg': npeg})
                    self.kb.kb_assert(assert_top)



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
        # List is filled with filler values
        row1 = [2, 2, 2]
        row2 = [2, 2, 2]
        row3 = [2, 2, 2]
        factpass1 = parse_input("fact: (coordinate ?tilex ?posa pos1)")
        factpass2 = parse_input("fact: (coordinate ?tilex ?posa pos2)")
        factpass3 = parse_input("fact: (coordinate ?tilex ?posa pos3)")

        bindings1 = self.kb.kb_ask(factpass1)
        if bindings1:
            for i in bindings1:
                column_num = (int(i.bindings_dict['?posa'].replace('pos', ''))) - 1
                row1[column_num] = int(i.bindings_dict['?tilex'].replace('tile', ''))
                # row1.append(int(i.bindings_dict['?tilex'].replace('tile', '')))


        bindings2 = self.kb.kb_ask(factpass2)
        if bindings2:
            for i in bindings2:
                column_num = (int(i.bindings_dict['?posa'].replace('pos', ''))) - 1
                row2[column_num] = int(i.bindings_dict['?tilex'].replace('tile', ''))

        bindings3 = self.kb.kb_ask(factpass3)
        if bindings3:
            for i in bindings3:
                column_num = (int(i.bindings_dict['?posa'].replace('pos', ''))) - 1
                row3[column_num] = int(i.bindings_dict['?tilex'].replace('tile', ''))

        output_list = [tuple(row1), tuple(row2), tuple(row3)]
        output_tuple = tuple(output_list)
        return output_tuple


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
        if not self.isMovableLegal(movable_statement):
            pass
        else:
            # match_help = self.produceMovableQuery()
            # terms = match(movable_statement, match_help.statement)
            #
            # if terms:
            #     tile = terms.bindings[0].constant
            #     oposx = terms.bindings[1].constant
            #     oposy = terms.bindings[2].constant
            #     nposx = terms.bindings[3].constant
            #     nposy = terms.bindings[4].constant

            tile = str(movable_statement.terms[0])
            oposx = str(movable_statement.terms[1])
            oposy = str(movable_statement.terms[2])
            nposx = str(movable_statement.terms[3])
            nposy = str(movable_statement.terms[4])

            # RETRACT
            retract_pos = parse_input("fact: (coordinate %(tile)s %(posa)s %(posb)s"
                                      % {'tile': tile,'posa': oposx, 'posb': oposy})
            retract_empty_pos = parse_input("fact: (coordinate tile-1 %(posa)s %(posb)s"
                                            % {'posa': nposx, 'posb': nposy})
            self.kb.kb_retract(retract_pos)
            self.kb.kb_retract(retract_empty_pos)

            # ASSERT
            assert_pos = parse_input("fact: (coordinate %(tile)s %(posa)s %(posb)s"
                                     % {'tile': tile, 'posa': nposx, 'posb': nposy})

            assert_empty_pos = parse_input("fact: (coordinate tile-1 %(posa)s %(posb)s"
                                           % {'posa': oposx, 'posb': oposy})
            self.kb.kb_assert(assert_pos)
            self.kb.kb_assert(assert_empty_pos)

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
