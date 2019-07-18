f = open('TABLES/SUMMARY.hits_all_terms.tex')
all = []
cse = []
for line in f:
    fields = line.strip().split('&')
    try:
        all.append(int(fields[1]))
        cse.append(int(fields[2]))
    except:
        pass

print(sorted(all, reverse=True)[:10])

print(sorted(cse, reverse=True)[:10])