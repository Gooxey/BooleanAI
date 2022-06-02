import random


class Cell:
    
    def __init__(self, AI, id, table: list = None, inputs: list = []):
        self.AI = AI
        self.id = id
        self.table = table
        self.inputs = inputs


    def processInput(self) -> None:
        input_values = []
        statePOS = 0

        print('         ', self.id, self.inputs, self.table)

        # get the Inputs
        for i in range(len(self.inputs)):
            state = self.AI.getState(self.inputs[i])
            if state == None:
                raise ValueError('Cell %s has not yet processed its Inputs!' % i)
            input_values.append(state)

        
        # process the the inputvalues to an decimal number to get the position of the correct state
        for i in range(len(input_values)):
            if input_values[i] == '1':
                statePOS += 2 ** i

        print(self.id, len(self.table), statePOS)
        # write the cells state to the global state list
        self.AI.setState(self.id, self.table[statePOS])


    def safeToFile(self) -> None:
       self.AI.AIdata.write(cellid=self.id, newtable=self.table, newinputs=self.inputs)


    def generateNewConnections(self) -> None:
        newinputs = []

        # generate new inputs
        # generate all required inputs
        for i in range(self.AI.AIdata.createmin):
            # generate a number between 0 and the inputcount + cellcount
            # if the new input already is in the inputs list of this cell, try a new one
            # if the new input is equal to the id of this cell, try a new one
            for ii in range(self.AI.AIdata.maxtries):
                newinput = random.randint(0, self.AI.AIdata.inputcount + self.AI.AIdata.cellcount - 1)

                if newinput in self.inputs:
                    pass
                elif newinput == self.id:
                    pass
                else:
                    if random.randint(1, 100) < self.AI.AIdata.spawnchance:
                        self.AI.spawnCell(self.id)
                        break
                    newinputs.append(newinput)
                    break
        
        # generate all additional inputs
        for i in range(self.AI.AIdata.createmax - self.AI.AIdata.createmin):
            # stop the additional input generation if the chance for additional one is 0%
            # else generate a new input if the cell is lucky enough
            if self.AI.AIdata.createchance == 0:
                break
            elif random.randint(1, 100) < self.AI.AIdata.createchance:
                # generate a number between 0 and the inputcount + cellcount
                # if the new input already is in the inputs list of this cell, try a new one
                # if the new input is equal to the id of this cell, try a new one
                for ii in range(self.AI.AIdata.maxtries):
                    newinput = random.randint(0, self.AI.AIdata.inputcount + self.AI.AIdata.cellcount - 1)

                    if newinput in self.inputs:
                        pass
                    elif newinput == self.id:
                        pass
                    else:
                        if random.randint(1, 100) < self.AI.AIdata.spawnchance:
                            self.AI.spawnCell(self.id)
                            break
                        newinputs.append(newinput)
                        break

        for i in range(len(newinputs)):
            self.inputs.append(newinputs[i])


    def destroyConnections(self) -> None:        
        # destroy random connections
        # destroy all required connections
        for i in range(self.AI.AIdata.destroymin):
            # generate a number between 0 and the number of how many connections the cell has
            # destroy the connection at the position of this number            
            if len(self.inputs) - 1 <= 0:
                connectiontodestroy = 0
            else:
                connectiontodestroy = random.randint(0, len(self.inputs) - 1)

            self.inputs.pop(connectiontodestroy)

                
        # destroy all additional connections
        for i in range(self.AI.AIdata.destroymax - self.AI.AIdata.destroymin):
            # stop the additional connection destruction if the chance for additional one is 0%
            # else destroy a new connection if the cell is lucky enough
            if self.AI.AIdata.destroychance == 0:
                break
            elif random.randint(1, 100) < self.AI.AIdata.destroychance:
                # generate a number between 0 and the number of how many inputs the cell has
                # destroy the connection at the position of this number              
                
                if len(self.inputs) - 1 == 0:
                    connectiontodestroy = 0
                else:
                    connectiontodestroy = random.randint(0, len(self.inputs) - 1)

                self.inputs.pop(connectiontodestroy)
        
        print(self.id, self.inputs)


    def giveInputs(self) -> list:
        return self.inputs


    def generateNewTable(self) -> None:
        if self.table == None:
            oldstatementcount= 0
        else:
            oldstatementcount = len(self.table)
        newstatementcount = 2 ** len(self.inputs)

        newtable = []

        # if the new table has less inputs, throw away the ones that are to much
        # if the new table has more inputs, keep the old table and generate new inputs for the missing positions
        # if the new table has the same amount of inputs, keep the old table
        if oldstatementcount > newstatementcount:
            for i in range(newstatementcount):
                newtable.append(self.table[i])
        elif oldstatementcount < newstatementcount:
            for i in range(oldstatementcount):
                newtable.append(self.table[i])

            for i in range(newstatementcount - oldstatementcount):
                newtable.append(str(random.randint(0, 1)))
        else:
            newtable = self.table[:]

        
        # generate new statements
        # generate all required statements
        required = len(newtable) + len(newtable) * self.AI.AIdata.statementchangemin
        limit = len(newtable) + len(newtable) * self.AI.AIdata.statementchangemax - required
        for i in range(required):
            # generate a random number between 0 and newstatementcount - 1
            # change the statement at this position from 0 to 1 or 1 to 0
            statement = newtable[random.randint(0, newstatementcount - 1)]

            if statement == '1':
                newtable[random.randint(0, newstatementcount - 1)] = '0'
            else:
                newtable[random.randint(0, newstatementcount - 1)] = '1'
        
        # generate all additional statements
        for i in range(limit):
            # stop the additional statement generation if the chance for additional one is 0%
            # else generate a new statement if the cell is lucky enough
            if self.AI.AIdata.statementchangechance == 0:
                break
            elif random.randint(1, 100) < self.AI.AIdata.statementchangechance:
                # generate a random number between 0 and newstatementcount - 1
                # change the statement at this position from 0 to 1 or 1 to 0
                statement = newtable[random.randint(0, newstatementcount - 1)]

                if statement == '1':
                    newtable[random.randint(0, newstatementcount - 1)] = '0'
                else:
                    newtable[random.randint(0, newstatementcount - 1)] = '1'

        # save the new table to the cell
        self.table = newtable[:]