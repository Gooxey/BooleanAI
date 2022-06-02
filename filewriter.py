from bitarray import bitarray


maxtries = '101101100100101100100001'
performencecycles = '101100001'
createmin = '101001'
createmax = '101100100001'
createchance = '101100101100100100001'
spawnchance = '101100101001'
destroymin = '101001'
destroymax = '101001'
destroychance = '100001'
statementchangemin = '101001'
statementchangemax = '101100101001'
statementchangechance = '101100101100100001'

inputcount = '101101100100101100100001'
cellcount = '101100001'
outputcount = '101100101100001'

performence = '101001'

parameters = maxtries + performencecycles + createmin + createmax + createchance + spawnchance + destroymin + destroymax + destroychance + statementchangemin + statementchangemax + statementchangechance + inputcount + cellcount + outputcount + performence

celltables = [
    '110110110110001',
    '110110110111001',
    '110110111110001',
    '110110111111001',
    '110111110110001',
    '110111110111001',
    '110111111110001',
    '110111111111001',
    '111110110110001',
    '111110110111001',
    '111110111110001',
    '111111110110001'
]
cellinputs = [
    ['100001', '101001'],
    ['101101001'],
    ['101100100101101001', '101100101100100101101001'],
    ['100101001', '101101001'],
    ['101001', '100101001'],
    ['101101001'],
    ['100001'],
    ['100101001', '101101001'],
    ['100001', '101001'],
    ['101101001'],
    ['101101001'],
    ['101101001']
]

oldcell_1 = celltables[0] + cellinputs[0][0] + cellinputs[0][1]

oldcellinfo = oldcell_1

cells = []
cellinfo = ''

for i in range(len(celltables)):
    cells.append(celltables[i])

    for ii in range(len(cellinputs[i])):
        cells.append(cellinputs[i][ii])

for i in range(len(cells)):
    cellinfo += cells[i]


AIdata = parameters + '011001' + cellinfo

a = bitarray(AIdata)


with open('C:/Users/dennis/Documents/0_Other/lil/Boolean AI file editor/data.dat', 'w') as aww:
    a.tofile(aww)
    aww.close()
