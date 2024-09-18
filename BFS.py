class SemanticNetsAgent:
    def __init__(self):
        pass
    
    # Tester for valid states
    def vaildTest(self, state, initialsheep, initialwolves):
        rightside_sheep = initialsheep - state[0]
        rightside_wolves = initialwolves - state[1]

        # No negative number of animals
        if state[0] < 0 or state[1] < 0 or rightside_sheep < 0 or rightside_wolves < 0:
            return False
        
        # Can't have exceeding number of animals than initial number of animals
        elif state[0] > initialsheep or state[1] > initialwolves:
            return False
        elif rightside_sheep > initialsheep or rightside_wolves > initialwolves:
            return False
        
        # Number of wolves cannot be more than number of sheep when they exist together
        elif state[0] < state[1] and state[0] > 0:
            return False
        elif rightside_sheep < rightside_wolves and rightside_sheep > 0:
            return False
        
        # Eliminate a state with one animial with a boat (unproductive move)
        elif state[2] == "Right" and sum([state[0],state[1]]) == sum([initialsheep,initialwolves]) - 1:
            return False
        # elif state[2] == "Left" and sum([rightside_sheep, rightside_wolves]) == sum([initialsheep,initialwolves]) - 1:
        #     return False
        
        else:
            return True

    # Tester for duplicate states
    def duplicateTest (self, state, previousStates):
        if state not in previousStates:
            return True
        else:
            return False

    # Function to trace back moves between states    
    def traceMove (self, currentState, newState):
        currentSheep, currentWolf, currentBoat = currentState
        newSheep, newWolf, newBoat = newState

        if currentBoat == "Left":
            movedSheep = currentSheep - newSheep
            movedWolf = currentWolf - newWolf
        if currentBoat == "Right":
            movedSheep = newSheep - currentSheep
            movedWolf = newWolf - currentWolf

        return (movedSheep,movedWolf)
    
    # Dumb Generator for creating states with all 5 possible moves
    def nextStateFunc (self, sheep, wolves, boat):
        possibleMoves = [(1,0), (0,1), (1,1), (2,0), (0,2)]
        nextPossibleStates = []
        if boat == "Left":
            for moves in possibleMoves:
                movingSheep, movingWolf = moves
                newState = (sheep - movingSheep, wolves - movingWolf, "Right")
                nextPossibleStates.append(newState)
        else:
            for moves in possibleMoves:
                movingSheep, movingWolf = moves
                newState = (sheep + movingSheep, wolves + movingWolf, "Left")
                nextPossibleStates.append(newState)

        return possibleMoves, nextPossibleStates

    def solve(self, initial_sheep, initial_wolves):
        # Using BFS (Breadth First Search) algorithm to find the shortest path from initial state to state(0,0)
        visitedStates = {}
        queueState =[(initial_sheep, initial_wolves, "Left")]
        targetState = (0,0,"Right")

        visitedStates[(initial_sheep, initial_wolves, "Left")] = None

        while queueState:
            currentState = queueState.pop(0)
            possMoves, possStates = self.nextStateFunc(currentState[0],currentState[1],currentState[2])
            for state in possStates:
                if self.vaildTest(state, initial_sheep, initial_wolves) and self.duplicateTest(state, visitedStates):
                    queueState.append(state)
                    visitedStates[state] =currentState # Assigning new state to prior state in dict to allow backtrace   
            if currentState == targetState:
                solutionState = []
                solutionMove =[]
                while currentState:
                    solutionState.append(currentState)
                    if visitedStates[currentState]:
                        solutionMove.append(self.traceMove(currentState, visitedStates[currentState]))
                    currentState = visitedStates[currentState] # Tracing back to prior state
        if targetState not in visitedStates: # No solution found case
                return []     
        return solutionMove[::-1]
