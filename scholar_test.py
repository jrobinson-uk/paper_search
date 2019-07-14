import scholarly
from time import sleep
from random import randint

papers = [
"Achievement motivation: Conceptions of ability, subjective experience, task choice, and performance.,Nicholls, John G",
"The theory of affordances,Gibson, James J",
"The organization of behavior. A neuropsychological theory,Hebb, DO",
"Learning and teaching styles in engineering education,Felder, Richard M and Silverman, Linda K and others",
"Cognitive apprenticeship: Teaching the craft of reading, writing and mathematics,Collins, Allan and Brown, John Seely and Newman, Susan E",
"Cognitive load during problem solving: Effects on learning,Sweller, John",
"Multimedia learning,Mayer, Richard E",
"Communities of practice: Learning, meaning, and identity,Wenger, Etienne",
"Conditions of learning,Gagn{\'e}, Robert Mills",
"Connectivism: A Learning Theory for the Digital Age,Siemens, George",
"Conversation, cognition and learning: A cybernetic theory and methodology,Pask, Gordon",
"The act of discovery,Bruner, Jerome S",
"Learner-centered design: The challenge for HCI in the 21st century,Soloway, Elliot and Guzdial, Mark and Hay, K"
]




for paper in papers:
    print(paper)
    search_query = scholarly.search_pubs_query(paper)
    pub=next(search_query)
    cited = [citation.bib for citation in pub.get_citedby()]
    print(cited)
    quit()
        #with open (paper,mode="w") as f:
            #cite = str(cited[
        #    f.write(str(next(cited)))
         #   f.write("\n\n")
          #  input("Waiting...")
           # sleep(randint(30,60))

