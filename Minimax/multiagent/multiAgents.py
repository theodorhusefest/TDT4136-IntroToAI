# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        "*** YOUR CODE HERE ***"
    
        legalActions = gameState.getLegalActions()  
        possiblePacmanStates = [gameState.generateSuccessor(0, action) for action in legalActions] 
        possiblePacmanValues = [self.minimax(state, 0, 1) for state in possiblePacmanStates]

        bestPacmanValue = max(possiblePacmanValues)
        bestIndices = [index for index in range(len(possiblePacmanValues)) if possiblePacmanValues[index] == bestPacmanValue]
        chosenIndex = random.choice(bestIndices)

        return legalActions[chosenIndex] 

        
    def minimax(self, currState, depth, currAgent):
        if currAgent == currState.getNumAgents(): # Iterate one ply once all agents are iterated through
            depth += 1;

        currAgent = currAgent  % currState.getNumAgents() # Fix agent index

        if depth == self.depth or currState.isWin() or currState.isLose(): # Termination node
            return self.evaluationFunction(currState)

        legalActions = currState.getLegalActions(currAgent)
        possibleStates = [currState.generateSuccessor(currAgent, action) for action in legalActions]
        if currAgent == 0: # MAX agent / Pacman
            value = -float('inf')
            for state in possibleStates:
                value = max(value, self.minimax(state, depth, currAgent + 1))
            return value
        else: # MIN agent / Ghost
            value = float('inf')
            for state in possibleStates:
                value = min(value, self.minimax(state, depth, currAgent + 1))
            return value
        
class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    
    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** MY CODE HERE ***"
        #print("self.depth: {0}".format(self.depth))
        currState = gameState
        legalActions  = currState.getLegalActions(0)
        possiblePacmanStates = [currState.generateSuccessor(0, action) for action in legalActions]

        alpha = -float('inf') # Lower bound on evaluation of MAX node
        beta = float('inf') # Upper bound on evaluation of MIN node

        possiblePacmanValues = []

        for state in possiblePacmanStates:
            value = self.alphabeta(state, 0, 1, alpha, beta)
            possiblePacmanValues.append(value)
            alpha = max(alpha, value)

        bestPacmanValue = max(possiblePacmanValues)
        bestIndices = [index for index in range(len(possiblePacmanValues)) if possiblePacmanValues[index] == bestPacmanValue]

        return legalActions[random.choice(bestIndices)]

    def alphabeta(self, currState, depth, agentIndex, alpha, beta):
        if agentIndex == currState.getNumAgents():
            depth += 1; # Go down one ply once all agents are iterated through

        agentIndex = agentIndex % currState.getNumAgents() # Fix agent index
        legalActions = currState.getLegalActions(agentIndex)

        if depth == self.depth or currState.isWin() or currState.isLose():
            return self.evaluationFunction(currState) # Stop at terminal nodes

        if agentIndex == 0: # Pacman agent
            value = -float('inf')
            for action in legalActions:
                state = currState.generateSuccessor(agentIndex, action) # Only expand one node at a time
                value = max(value, self.alphabeta(state, depth, agentIndex + 1, alpha, beta))
                alpha = max(value, alpha)
                if (alpha > beta):
                    break # Cut away tree from beta node
            return value

        else: # Ghost agent
            value = float('inf')
            for action in legalActions:
                state = currState.generateSuccessor(agentIndex, action) # Only expand one node at a time
                value = min(value, self.alphabeta(state, depth, agentIndex + 1, alpha, beta))
                beta = min(value, beta)
                if (beta < alpha):
                    break # Cut away tree from alpha node
            return value


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

