from datetime import datetime
from time import time
from typing import List

from .Cell import Cell
from .Editor import Editor




INFOtxt = '\033[34m\033[1mINFO\033[0m |'
WARNtxt = '\033[33m\033[1mWARN\033[0m |' 
ERROtxt = '\033[31m\033[1mERRO\033[0m |'




class BaseCostumFunctions:
    def __init__(self, ai, rightanswer):
        self.latest_outputs = ai.latest_outputs
        self.rightanswer = rightanswer

    def calcPerformance(self):
        pass


class AI:
    def __init__(self, CustomAIFunctions, AIpath, AIname):
        self.CustomAIFunctions = CustomAIFunctions
        self.AIdatapath = AIpath + AIname + '_AIData.dat'
        
        self.AIdata = Editor(self.AIdatapath)

        self.loadAI(log = True)


    def loadAI(self, log: bool = False):
        self.states = []
        self.cells = []
        self.outputcells = []
        self.latest_outputs = []
        self.performancecounter = 0
        self.performances = []


        init_time = time()        


        # load general data from the savefile
        self.inputcount = self.AIdata.inputcount
        self.cellcount = self.AIdata.cellcount
        self.outputcount = self.AIdata.outputcount

        # create placeholder for each state
        for i in range(self.inputcount + self.cellcount + self.outputcount):
            self.states.append(None)

        # activate the cells and add them to the list
        for i in range(self.cellcount):
            # convert the table from string to list format
            table = []
            for ii in range(len(self.AIdata.celltables[i])):
                table.append(self.AIdata.celltables[i][ii])

            self.cells.append(Cell(self, i, table, self.AIdata.cellinputs[i]))
            if log:
                print('%s %s Loaded Cell %s' % ((datetime.now().strftime('\033[2m\033[1m%Y-%m-%d\033[0m | \033[2m\033[1m%H:%M:%S\033[0m |')), INFOtxt, i))
        
        # activate the outputcells and add them to the list
        for i in range(self.cellcount, self.cellcount + self.outputcount):
            # convert the table from string to list format
            table = []
            for ii in range(len(self.AIdata.celltables[i])):
                table.append(self.AIdata.celltables[i][ii])

            self.outputcells.append(Cell(self, i - self.cellcount, table, self.AIdata.cellinputs[i]))
            if log:
                print('%s %s Loaded Output-Cell %s' % ((datetime.now().strftime('\033[2m\033[1m%Y-%m-%d\033[0m | \033[2m\033[1m%H:%M:%S\033[0m |')), INFOtxt, i - self.cellcount))
        
        if log:
            print('%s %s #########################' % ((datetime.now().strftime('\033[2m\033[1m%Y-%m-%d\033[0m | \033[2m\033[1m%H:%M:%S\033[0m |')), INFOtxt))
            print('%s %s Loaded AI! (%.2f seconds)' % ((datetime.now().strftime('\033[2m\033[1m%Y-%m-%d\033[0m | \033[2m\033[1m%H:%M:%S\033[0m |')), INFOtxt, (time() - init_time)))
            print('%s %s #########################' % ((datetime.now().strftime('\033[2m\033[1m%Y-%m-%d\033[0m | \033[2m\033[1m%H:%M:%S\033[0m |')), INFOtxt))


    def processInput(self, inputs) -> List:
        self.latest_outputs = []


        print('%s %s Processing Input: %s' % ((datetime.now().strftime('\033[2m\033[1m%Y-%m-%d\033[0m | \033[2m\033[1m%H:%M:%S\033[0m |')), INFOtxt, inputs))
        process_time = time()


        # load the inputs to the states variable
        try:
            for i in range(self.inputcount):
                self.states[i] = inputs[i]

        
        # print an error message and return None if an indexError occurs
        except IndexError as err:
            print('%s %s %s' % ((datetime.now().strftime('\033[2m\033[1m%Y-%m-%d\033[0m | \033[2m\033[1m%H:%M:%S\033[0m |')), ERROtxt, err))

            return err
        
        # let each cell process the inputs
        for cell in self.cells:
            cell.processInput()
        
        # let each outputcell process the inputs
        for i in range(len(self.outputcells)):
            cell = self.outputcells[i]
            cell.processInput()

        # write the outputs to a output variable and return it
        for i in range(self.outputcount):
            self.latest_outputs.append(self.states[self.inputcount + self.cellcount + i])


        print('%s %s Result: %s (%.2f seconds)' % ((datetime.now().strftime('\033[2m\033[1m%Y-%m-%d\033[0m | \033[2m\033[1m%H:%M:%S\033[0m |')), INFOtxt, self.latest_outputs, (time() - process_time)))

        return self.latest_outputs

    
    def train(self, rightanswer):
        performancecycles = self.AIdata.performencecycles
        
        # calculate performance for the last outputs and add them to the performance list
        costumFunctions = self.CustomAIFunctions(self, rightanswer)
        performance = costumFunctions.calcPerformance()
        self.performances.append(performance)
        self.performancecounter += 1

        # if all performence cycles have been done, save and evolve the current AI
        if self.performancecounter == performancecycles:
            x = 0

            # calculate the average performance
            for i in range(performancecycles):
                x += self.performances[i]
            averageperformance = x / performancecycles
            
            # reset the performence values
            self.performances = []
            self.performancecounter = 0


            print('%s %s Reached configured Performence cycles of %s cycles' % ((datetime.now().strftime('\033[2m\033[1m%Y-%m-%d\033[0m | \033[2m\033[1m%H:%M:%S\033[0m |')), INFOtxt, performancecycles))
            print('%s %s Average Performence: %s / 100' % ((datetime.now().strftime('\033[2m\033[1m%Y-%m-%d\033[0m | \033[2m\033[1m%H:%M:%S\033[0m |')), INFOtxt, averageperformance))
            print('%s %s Starting Evolution process' % ((datetime.now().strftime('\033[2m\033[1m%Y-%m-%d\033[0m | \033[2m\033[1m%H:%M:%S\033[0m |')), INFOtxt))
            evolution_time = time()


            # if this AI has reached a better performence, refresh the AI data file with this AI model
            if averageperformance > self.AIdata.performence:
                # go through every cell and give them the command to save themselfs to the file
                for i in range(len(self.cells)):
                    cell = self.cells[i]
                    cell.safeToFile()

                # go through every output-cell and give them the command to save themselfs to the file
                for i in range(len(self.cells)):
                    cell = self.outputcells[i]
                    cell.safeToFile()
            else:
                # give the AI the command to load the old AI
                self.loadAI()
                print('%s %s Average Performence did not exceed the best one. Reseting AI to the best state.' % ((datetime.now().strftime('\033[2m\033[1m%Y-%m-%d\033[0m | \033[2m\033[1m%H:%M:%S\033[0m |')), INFOtxt))

            # --------------------
            # EVOLUTION PROCESS
            # --------------------

            # # save a copy of the outputcells to a seperate variable so the validator can use them later
            # output_cells = []
            # for i in range(self.AIdata.cellcount, len(self.cells)):
            #     output_cells.append(self.cells[i])
            

            # CONNECTION GENERATION

            # generate a new model based on the one saved in the file
            # go through every cell and give them the command to generate new connections
            for i in range(len(self.cells)):
                cell = self.cells[i]
                cell.generateNewConnections()

            # go through every output-cell and give them the command to generate new connections
            for i in range(len(self.outputcells)):
                cell = self.outputcells[i]
                cell.generateNewConnections()

            print('_______Cells_______')
            # go through every cell and give them the command to destroy connections
            for i in range(len(self.cells)):
                cell = self.cells[i]
                cell.destroyConnections()

            print('___Output-Cells____')
            # go through every output-cell and give them the command to destroy connections
            for i in range(len(self.outputcells)):
                cell = self.outputcells[i]
                cell.destroyConnections()


            # PATH-VALIDATION / CELL SORTING
            execution_order = []
                # output marking

            output_marked = []
            output_marked_buffer = []
            # go through each outputcell and mark their input cells as outputed
            for i in range(len(self.outputcells)):
                cell = self.outputcells[i]

                inputs = cell.giveInputs()
                
                # go through each input and check if it is a cell
                # if it is one, add it to the output_marked and output_marked_buffer list
                for i in range(len(inputs) - 1):
                    if inputs[i] >= self.inputcount:
                        output_marked.append(inputs[i])
                        output_marked_buffer.append(inputs[i])

            
            # while there are still cells in the output-marked-buffer mark their inputs as outputmarked if they are new and not an official input
            while output_marked_buffer != []:
                nextcellstocheck = output_marked_buffer[:]
                output_marked_buffer = []
                for i in range(len(nextcellstocheck) - 1):
                    if nextcellstocheck[i] >= self.inputcount:
                        cell = self.cells[nextcellstocheck[i] - self.inputcount]
                        inputstomark = cell.giveInputs()

                        # go through each input and check if it is in the outputs_marked variable or an offcial input
                        # if it is there skip this input
                        # else save it in the outputs_marked and outputs_marked_buffer variable
                        for ii in range(len(inputstomark)):
                            inputalreadymarked = False
                            for iii in range(len(output_marked)):
                                if inputstomark[ii] == output_marked[iii]:
                                    inputalreadymarked = True
                                    break
                                elif inputstomark[ii] < self.inputcount:
                                    inputalreadymarked = True
                                    break
                            
                            if not inputalreadymarked:
                                output_marked.append(inputstomark[ii])
                                output_marked_buffer.append(inputstomark[ii])
            

            # --------------------
                # input marking / cell sorting
            input_marked = []
            check_inputed = output_marked[:]
            for i in range(len(check_inputed)):
                cellid = check_inputed.pop() - self.inputcount
                cell = self.cells[cellid]

                inputs = cell.giveInputs()

                # go through each input and check if its an official input or an inputmarked input
                # if something inputmarked has been found, add this cell to the inputmarked list
                inputmarked = False
                for ii in range(len(inputs)):
                    if inputs[ii] < self.inputcount:
                        inputmarked = True
                        break
                    elif inputs[ii] in input_marked:
                        inputmarked = True
                        break
                
                if inputmarked:
                    input_marked.append(cellid + self.inputcount)
                    execution_order.append(cellid)

            print('exec', execution_order)

            


            # -----------------
                # Termination


            # check if the cell is outputmarked and inputmarked or an output cell
            # if it is not in one of them it get appended to the termination pit as long as is not already there
            termination_pit = []
            for i in range(len(self.cells)):
                cellid = i + self.inputcount
                
                output_vaild = False
                input_vaild = False
                # if it is an output cell it cannot be terminated and therefore skips the termination check
                if cellid >= (self.inputcount + self.cellcount):
                    output_vaild = True
                    input_vaild = True
                else:
                    for ii in range(len(output_marked)):
                        if output_marked[ii] == cellid:
                            output_vaild = True
                    for ii in range(len(input_marked)):
                        if input_marked[ii] == cellid:
                            input_vaild = True

                if output_vaild and input_vaild:
                    pass
                else:
                    termination_pit.append(i)


            # # ------------------------
            #     # final cell sorting

            # go through every cell in the execution order
            # if the id matches one of the cells, append it to the newcells list
            # after all cells have been put in the right order, delete the old one and replace it with the new one
            newcelllist = []
            for i in range(len(execution_order)):
                for i in range(len(self.cells)):
                    if ii == i:
                        newcelllist.append(self.cells[ii])
                        break
            self.cells = newcelllist

            # newcelllist = []
            # for i in range(len(execution_order)):
            #     newcelllist.append(self.cells[execution_order[i]])
            # self.cells = newcelllist[:]
            # newcelllist = None


            # -----------------------
            # STATEMENT GENERATION

            for i in range(len(self.cells)):
                cell = self.cells[i]
                cell.generateNewTable()

            for i in range(len(self.outputcells)):
                cell = self.outputcells[i]
                cell.generateNewTable()


            print('____order____')
            for i in range(len(self.cells)):
                cell = self.cells[i]
                print(cell.id)
            
            print('%s %s Finished Evolution process in %.2f seconds!' % ((datetime.now().strftime('\033[2m\033[1m%Y-%m-%d\033[0m | \033[2m\033[1m%H:%M:%S\033[0m |')), INFOtxt, (time() - evolution_time)))



    def spawnCell(self, spawner):
        # create a placeholder for the cell
        self.states.append(None)

        # create the cell and add it to the newly generated list and the general one
        cell = Cell(self, len(self.cells), inputs=[spawner])
        self.cells.append(cell)
        print('%s %s Spawned a new Cell with the id %s by Cell %s!' % ((datetime.now().strftime('\033[2m\033[1m%Y-%m-%d\033[0m | \033[2m\033[1m%H:%M:%S\033[0m |')), INFOtxt, len(self.cells) - 1, spawner))
        cell.generateNewConnections()
        


    def getState(self, stateid):
        try:
            return self.states[stateid]
        except IndexError as err:
            print('%s %s %s' % ((datetime.now().strftime('\033[2m\033[1m%Y-%m-%d\033[0m | \033[2m\033[1m%H:%M:%S\033[0m |')), ERROtxt, err))
            return None


    def setState(self, stateid, value):
        try:
            self.states[stateid + self.inputcount] = value
        except IndexError as err:
            print('%s %s %s' % ((datetime.now().strftime('\033[2m\033[1m%Y-%m-%d\033[0m | \033[2m\033[1m%H:%M:%S\033[0m |')), ERROtxt, err))


    def terminate(self, cellid):
        self.cells.pop(cellid)
        print('%s %s Terminated Cell %s' % ((datetime.now().strftime('\033[2m\033[1m%Y-%m-%d\033[0m | \033[2m\033[1m%H:%M:%S\033[0m |')), INFOtxt, cellid))