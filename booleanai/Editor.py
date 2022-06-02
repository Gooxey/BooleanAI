from math import floor

from bitarray import bitarray


class Editor:
    def __init__(self, path):
        self.path = path

        self.__refresh()
        
    
    def __read(self):
        data = bitarray()

        # read the file
        with open(self.path, 'rb') as file:
            data.fromfile(file)
            file.close()


        # convert bitarray item to list
        listed_data = data.tolist()
        

        # merge the single bits to pairs of three
        merged_data = []
        for i in range(0, len(listed_data), 3):
            try:
                merged_data.append(str(listed_data[i]) + str(listed_data[i+1]) + str(listed_data[i+2]))
            except IndexError:
                break


        # devide the data into statements
        buffereddata = ''
        devided_data = []
        for i in range(len(merged_data)):
            if merged_data[i] == '001':
                devided_data.append(buffereddata)
                buffereddata = ''
            else:
                buffereddata += merged_data[i]
        # delete the additional bits
        buffereddata = None


        # convert bits to useable data
        decoded_data = []
        table = []
        inputs = []
        inputbuffer = []
        paramdatadone = False
        for ii in range(len(devided_data)):
            statement = devided_data[ii]
            
            value = 0
            e = 0
            for i in range(0, len(statement), 3):
                # do this during parameter conversion
                if not paramdatadone:
                    # set paramdatadone to True if the first bool appears
                    if statement[i] + statement[i+1] + statement[i+2] == '111' or not paramdatadone and statement[i] + statement[i+1] + statement[i+2] == '110':
                        paramdatadone = True
                        value = None
                    # convert encoded parameter data to usable data by converting it to integers
                    elif statement[i] + statement[i+1] + statement[i+2] == '101':
                        value += (2 ** e)
                        e += 1
                    elif statement[i] + statement[i+1] + statement[i+2] == '100':
                        e += 1
                
                # do this during celldata reading
                else:
                    # if the data is a input, covert the encoded value to a usable integer
                    if statement[i] + statement[i+1] + statement[i+2] == '101':
                        value += (2 ** e)
                        e += 1
                    elif statement[i] + statement[i+1] + statement[i+2] == '100':
                        e += 1

                    # if the statement is not an input, add it to the table variable
                    else:
                        # converting the encoded table to a usable format
                        converted_table = ''
                        for i in range(0, len(statement), 3):
                            if statement[i] + statement[i+1] + statement[i+2] == '111':
                                converted_table += '1'
                            elif statement[i] + statement[i+1] + statement[i+2] == '110':
                                converted_table += '0'

                        table.append(converted_table)
                        value = None
                        break
                

            # if the converison process is still at converting parameters, add the converted values to the final variable decoded_data
            if not paramdatadone:
                decoded_data.append(value)
            # if the input got converted, add it to the inputs variable
            elif paramdatadone and value != None:
                inputbuffer.append(value)
            
            # if the inputbuffer is either full or if the last statement is reached, add the inputbuffer to the inputs list
            elif paramdatadone and inputbuffer != []:
                inputs.append(inputbuffer)
                inputbuffer = []
            if ii == len(devided_data) - 1:
                inputs.append(inputbuffer)
                inputbuffer = []
                

        decoded_data.append(table)
        decoded_data.append(inputs)


        return decoded_data


    def __refresh(self):
        self.decoded_data = self.__read()

        self.maxtries = self.decoded_data[0]
        self.performencecycles = self.decoded_data[1]
        self.createmin = self.decoded_data[2]
        self.createmax = self.decoded_data[3]
        self.createchance = self.decoded_data[4]
        self.spawnchance = self.decoded_data[5]
        self.destroymin = self.decoded_data[6]
        self.destroymax = self.decoded_data[7]
        self.destroychance = self.decoded_data[8]
        self.statementchangemin = self.decoded_data[9]
        self.statementchangemax = self.decoded_data[10]
        self.statementchangechance = self.decoded_data[11]

        self.inputcount = self.decoded_data[12]
        self.cellcount = self.decoded_data[13]
        self.outputcount = self.decoded_data[14]

        self.performence = self.decoded_data[15]

        self.celltables = self.decoded_data[16]
        self.cellinputs = self.decoded_data[17]


    def write(
            self,
            maxtries: int = None,
            newperformencecycles: int = None,
            newcreatemin: int = None,
            newcreatemax: int = None,
            newcreatechance: int = None,
            newspawnchance: int = None,
            newdestroymin: int = None,
            newdestroymax: int = None,
            newdestroychance: int = None,
            newstatementchangemin: int = None,
            newstatementchangemax: int = None,
            newstatementchangechance: int = None,
            inputcount: int = None,
            cellcount: int = None,
            outputcount: int = None,
            cellid: int = None,
            newtable: list = None,
            newinputs: list = None) -> None:


        # raise an error if a number under 0 or over 100 has been given to a specific parameter
        if newcreatemin and (newcreatemin < 0 or newcreatemin > 100): raise ValueError('Only values between 0 and 100 are allowed')
        elif newcreatemax and (newcreatemax < 0 or newcreatemax > 100): raise ValueError('Only values between 0 and 100 are allowed')
        elif newcreatechance and (newcreatechance < 0 or newcreatechance > 100): raise ValueError('Only values between 0 and 100 are allowed')
        elif newspawnchance and (newspawnchance < 0 or newspawnchance > 100):  raise ValueError('Only values between 0 and 100 are allowed')
        elif newdestroychance and (newdestroychance < 0 or newdestroychance > 100): raise ValueError('Only values between 0 and 100 are allowed')
        elif newspawnchance and (newspawnchance < 0 or newspawnchance > 100): raise ValueError('Only values between 0 and 100 are allowed')
        

        # raise an error if a negative number has been given to a specific parameter
        if maxtries and maxtries < 0: raise ValueError('Only positive numbers are allowed')
        elif newperformencecycles and newperformencecycles < 0: raise ValueError('Only positive numbers are allowed')
        elif newdestroymin and newdestroymin < 0: raise ValueError('Only positive numbers are allowed')
        elif newdestroymax and newdestroymax < 0: raise ValueError('Only positive numbers are allowed')
        elif newstatementchangemin and newstatementchangemin < 0: raise ValueError('Only positive numbers are allowed')
        elif newstatementchangemax and newstatementchangemax < 0: raise ValueError('Only positive numbers are allowed')
        elif inputcount and inputcount < 0: raise ValueError('Only positive numbers are allowed')
        elif cellcount and cellcount < 0: raise ValueError('Only positive numbers are allowed')
        elif outputcount and outputcount < 0: raise ValueError('Only positive numbers are allowed')



        # put the new values into a list
        newvalues = []
        newvalues.append(maxtries)
        newvalues.append(newperformencecycles)
        newvalues.append(newcreatemin)
        newvalues.append(newcreatemax)
        newvalues.append(newcreatechance)
        newvalues.append(newspawnchance)
        newvalues.append(newdestroymin)
        newvalues.append(newdestroymax)
        newvalues.append(newdestroychance)
        newvalues.append(newstatementchangemin)
        newvalues.append(newstatementchangemax)
        newvalues.append(newstatementchangechance)
        newvalues.append(inputcount)
        newvalues.append(cellcount)
        newvalues.append(outputcount)

        
        # replace the old parameters by the new ones if given
        newdecodeddata = self.decoded_data
        for i in range(len(newvalues) - 3):
            if newvalues[i]:
                newdecodeddata[i] = newvalues[i]

        # replace the old cells by the new ones if given
        if cellid != None:    
            # replace the tables if given
            if newtable != None:
                newdecodeddata[len(newdecodeddata) - 2][cellid] = newtable
            # replace the inputs if given
            if newinputs != None:
                newdecodeddata[len(newdecodeddata) - 1][cellid] = newinputs
        

        # convert the decimal numbers to bits
        parameter_data = []
        for i in range(len(newdecodeddata) - 2):
            bin = ''
            n = newdecodeddata[i]
            # figure out if the number n is odd or even
            while True:
                oe = n
                # if the last oe value is 1 it is an odd number and if it is an 0 it is an even number
                while True:
                    if oe == 1:
                        break
                    elif oe == 0:
                        break
                    else:
                        oe -= 2


                # if it was an even number add an 0 to the binary number and devide n by 2
                # if it was an odd number add an 1 to the binary number and floor the result of n devided by 2
                if oe == 0:
                    n /= 2
                    bin += '100'
                elif oe == 1:
                    n = floor(n / 2)
                    bin += '101'

                # if the decimal number reached 0 break the loop
                if n == 0:
                    break
            
            parameter_data.append(bin)


        # convert the celldata to bits
        encoded_celldata = ''
        for ii in range(len(self.celltables)):
            table = self.celltables[ii]
            inputs = self.cellinputs[ii]
            encoded_table = ''
            encoded_inputs = []


            # encode the decoded table
            for i in range(len(table)):
                if table[i]== '1':
                    encoded_table += '111'
                elif table[i] == '0':
                    encoded_table += '110'
            
            # add the encoded table to the encoded celldata variable
            encoded_celldata += encoded_table + '001'


            # encode the decoded inputs
            for i in range(len(inputs)):
                bin = ''
                n = inputs[i]
                # figure out if the number n is odd or even
                while True:
                    oe = n
                    # if the last oe value is 1 it is an odd number and if it is an 0 it is an even number
                    while True:
                        if oe == 1:
                            break
                        elif oe == 0:
                            break
                        else:
                            oe -= 2


                    # if it was an even number add an 0 to the binary number and devide n by 2
                    # if it was an odd number add an 1 to the binary number and floor the result of n devided by 2
                    if oe == 0:
                        n /= 2
                        bin += '100'
                    elif oe == 1:
                        n = floor(n / 2)
                        bin += '101'

                    # if the decimal number reached 0 break the loop
                    if n == 0:
                        break
                encoded_inputs.append(bin)

            
            # add the encoded inputs to the encoded celldata variable
            for i in range(len(encoded_inputs)):
                encoded_celldata += encoded_inputs[i] + '001'


        # merge the single statements to a single one
        encoded_data = ''
        for i in range(len(parameter_data)):
            encoded_data += parameter_data[i] + '001'

        encoded_data += encoded_celldata


        # wirte the encoded data to the file
        data = bitarray(encoded_data)
        with open(self.path, 'wb') as file:
            data.tofile(file)
            file.close()


        # refresh data
        self.__refresh()