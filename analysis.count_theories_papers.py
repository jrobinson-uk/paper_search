with open('theories-terms.csv') as f:
    theories = set()
    for line in f:
        fields = line.strip().split(',')
        theory = fields[0]
        theories.add(theory)
    print('Num theories:', len(theories))

with open('SeminalCitations.csv') as f:
    f.readline()
    count = 0
    for line in f:
        fields = line.strip().split(",")
        if fields[0] != '#N/A' and fields[0].strip() != '':
            count += 1
    print ('Num papers:', count)