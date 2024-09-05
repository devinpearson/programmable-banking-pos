from statemachine import StateMachine, State

class PointOfSale(StateMachine):
 
    # creating states
    startUpState = State("startup", initial = True)
    standbyState = State("standby")
    readState = State("read")
    processState = State("process")
      
    # transitions of the state
    switchFromInit = startUpState.to(standbyState)
    switchToRead = standbyState.to(readState)
    switchToStandby = readState.to(standbyState)
    switchToProcess = readState.to(processState)
    switchBackToStandby = processState.to(standbyState)