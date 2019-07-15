queue = [line. rstrip('\n') for line in open("theories-terms.csv")].copy()
with open("bibs.html",mode="w") as f:
    f.write("<html><table>")
    for term in queue:
        theory, search = term.split(",")
        print ("--{}----{}".format(theory,search))
        url_all = "https://dl.acm.org/exportformats_search.cfm?query={}&filtered=&within=owners%2Eowner%3DHOSTED&dte=&bfr=&srt=%5Fscore&expformat=bibtex".format(term)
        url_cse = "https://dl.acm.org/exportformats_search.cfm?query=%28{}%29%20%20AND%20acmdlCCS%3A%28%252B%22computing%20education%22%29&filtered=&within=owners%2Eowner%3DHOSTED&dte=&bfr=&srt=%5Fscore&expformat=bibtex".format(term)
        f.write("<tr><td>{}</td><td>{}</td><td>{}</td><td><a href='{}'>ALL</a></td><td><a href='{}' download='out.bib'>CSE</a></td></tr>".format(theory,search,term,url_all,url_cse))
    f.write("</table></html>")
