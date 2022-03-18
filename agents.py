import random
import math


BOT_NAME = "INSERT NAME FOR YOUR BOT HERE OR IT WILL THROW AN EXCEPTION"


class RandomAgent:
    """Agent that picks a random available move.  You should be able to beat it."""
    def __init__(self, sd=None):
        if sd is None:
            self.st = None
        else:
            random.seed(sd)
            self.st = random.getstate()

    def get_move(self, state):
        if self.st is not None:
            random.setstate(self.st)
        return random.choice(state.successors())


class HumanAgent:
    """Prompts user to supply a valid move."""
    def get_move(self, state, depth=None):
        move__state = dict(state.successors())
        prompt = "Kindly enter your move {}: ".format(sorted(move__state.keys()))
        move = None
        while move not in move__state:
            try:
                move = int(input(prompt))
            except ValueError:
                continue
        return move, move__state[move]


class MinimaxAgent:
    """Artificially intelligent agent that uses minimax to optimally select the best move."""

    def get_move(self, state):
        """Select the best available move, based on minimax value."""
        nextp = state.next_player()
        best_util = -math.inf if nextp == 1 else math.inf
        best_move = None
        best_state = None

        for move, state in state.successors():
            util = self.minimax(state)
            if ((nextp == 1) and (util > best_util)) or ((nextp == -1) and (util < best_util)):
                best_util, best_move, best_state = util, move, state
        return best_move, best_state

    def minimax(self, state):
        """Determine the minimax utility value of the given state.

        Args:
            state: a connect383.GameState object representing the current board

        Returns: the exact minimax utility value of the state
        """
        # #
        # # Fill this in!
        # #
        # return 42  # Change this line!

        next_player = state.next_player()
        utility = 0
        if next_player == -1:
            utility = self.min_val(state)
        elif next_player == 1:
            utility = self.max_val(state)

        return utility

    def max_val(self, state, **kwargs):
        if state.is_full() is True:  # if no more moves -> return utility
            return state.utility()
        v = -math.inf
        successors = state.successors()
        for move, next in successors:
            v = max(v, self.min_val(next))
        return v

    def min_val(self, state, **kwargs):
        if state.is_full() is True:  # if no more moves -> return utility
            return state.utility()
        v = math.inf
        successors = state.successors()
        for move, next in successors:
            v = min(v, self.max_val(next))
        return v


class MinimaxHeuristicAgent(MinimaxAgent):
    """Artificially intelligent agent that uses depth-limited minimax to select the best move.
    Hint: Consider what you did for MinimaxAgent. What do you need to change to get what you want? 
    """

    def __init__(self, depth_limit):
        self.depth_limit = depth_limit

    def minimax(self, state):
        ## Reviewed by Cole
        """Determine the heuristically estimated minimax utility value of the given state.

        The depth data member (set in the constructor) determines the maximum depth of the game 
        tree that gets explored before estimating the state utilities using the evaluation() 
        function.  If depth is 0, no traversal is performed, and minimax returns the results of 
        a call to evaluation().  If depth is None, the entire game tree is traversed.

        Args:
            state: a connect383.GameState object representing the current board

        Returns: the minimax utility value of the state
        """
        # #
        # # Fill this in!
        # #
        # return 9  # Change this line!


        ##TODO
        ## Possibly do if next_player return ___
        ## elif next_player return ____
        ## else:
        ## return_value = 0
        next_player = state.next_player()
        return_value = 0

        if next_player == -1:
            return_value = self.get_min_val(state, depth=0)  # find min value


        elif next_player == 1:
            return_value = self.get_max_val(state, depth=0) # find max value
        return return_value

    def get_max_value(self, state, **arguments):
        ## Reviewed by Cole

        curr_depth = arguments["depth"]

        if curr_depth == self.depth_limit:
            return self.evaluation(state)

        if state.is_full():
            return state.utility()

        value = -math.inf
        successors = state.successors()
        next_depth = curr_depth + 1

        for i, j in successors:
            maximum = self.get_max_value(j, depth=next_depth)
            if maximum < value:
                value = maximum

        return value

    def get_min_value(self, state, **arguments):
        ## Reviewed by Cole
        curr_depth = arguments["depth"]

        if curr_depth == self.depth_limit:
            return self.evaluation(state)

        if state.is_full():
            return state.utility()

        value = math.inf
        successors = state.successors()
        next_depth = curr_depth + 1

        for i, j in successors:
            minimum = self.get_min_value(j, depth=next_depth)
            if minimum < value:
                value = minimum

        return value

    def minimax_depth(self, state, depth):
        """This is just a helper method fir minimax(). Feel free to use it or not. """

        # return 4 # Change this line!


    def evaluation(self, state):
        """Estimate the utility value of the game state based on features.

        N.B.: This method must run in O(1) time!

        Args:
            state: a connect383.GameState object representing the current board

        Returns: a heuristic estimate of the utility value of the state
        """
        # #
        # # Fill this in!
        # #

        # Change this line!
        # Note: This cannot be "return state.utility() + c", where c is a constant. 
        e1 = self.e1(state)
        e2 = self.e2(state)
        e3 = self.e3(state)
        estimate = e2  # + e3

        return estimate

        # score based on pieces near the ce

    def e1(self, state):
        mid = state.num_rows // 2
        cols = state.get_cols()
        h = cols[mid].count(1) - cols[mid].count(-1)
        return h

        # score based on pieces near the center (Normal)

    def e2(self, state):
        ncols = state.num_cols
        ci = ncols // 2

        sd = math.ceil(ncols / 4)
        weights = []

        for i in range(-ci, ci + 1):
            w = ncols * (pow(math.pi * 2, -0.5) * pow(sd, -1)) * math.exp(-0.5 * pow((i / sd), 2))
            weights.append(w)

        cols = state.get_cols()
        h = 0
        count = 0
        for col in cols:
            h += (col.count(1) - col.count(-1)) * weights[count]
            count += 1

        return h

        # number of streaks

    def e3(self, state):
        players = [1, -1]
        open_streaks = {1: 0, -1: 0}
        for player in players:
            for run in state.get_rows() + state.get_cols() + state.get_diags():
                garfield = list(zip(*self.streaks(run)))

                if 0 not in garfield[0]:
                    continue

                for s in garfield[1]:
                    if (s >= 3) and (player == garfield[0][garfield[1].index(s)]):
                        open_streaks[player] += 1

        return open_streaks[1] - open_streaks[-1]

    def streaks(self, lst):
        """Get the lengths of all the streaks of the same element in a sequence."""
        rets = []  # list of (element, length) tuples
        prev = lst[0]
        curr_len = 1
        for curr in lst[1:]:
            if curr == prev:
                curr_len += 1
            else:
                rets.append((prev, curr_len))
                prev = curr
                curr_len = 1
        rets.append((prev, curr_len))
        return rets
        
        



class MinimaxPruneAgent(MinimaxAgent):
    """Smarter computer agent that uses minimax with alpha-beta pruning to select the best move.
    Hint: Consider what you did for MinimaxAgent. What do you need to change to get what you want? 
    """

    def minimax(self, state):
        """Determine the minimax utility value the given state using alpha-beta pruning.

        The value should be equal to the one determined by MinimaxAgent.minimax(), but the 
        algorithm should do less work.  You can check this by inspecting the value of the class 
        variable GameState.state_count, which keeps track of how many GameState objects have been 
        created over time.  This agent should also respect the depth limit like HeuristicAgent.

        N.B.: When exploring the game tree and expanding nodes, you must consider the child nodes
        in the order that they are returned by GameState.successors().  That is, you cannot prune
        the state reached by moving to column 4 before you've explored the state reached by a move
        to to column 1.

        Args: 
            state: a connect383.GameState object representing the current board

        Returns: the minimax utility value of the state
        """
        # #
        # # Fill this in!
        # #
        # return 13  # Change this line!

    def alphabeta(self, state,alpha, beta):
        """ This is just a helper method for minimax(). Feel free to use it or not. """
        # return 9 # change this line!


class OtherMinimaxHeuristicAgent(MinimaxAgent):
    """Alternative heursitic agent used for testing."""

    def __init__(self, depth_limit):
        self.depth_limit = depth_limit

    def minimax(self, state):
        """Determine the heuristically estimated minimax utility value of the given state."""
        #
        # Fill this in, if it pleases you.
        #
        return 26  # Change this line, unless you have something better to do.

