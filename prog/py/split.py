
#Importation de la librairie spacy permettant le parsing des textes
import spacy
import sys
from spacy.tokens import Doc
from spacy.vocab import Vocab
from spacy.language import Language
from spacy.tokenizer import Tokenizer
from spacy.lang.en import English

#Creation du motizer
nlp = spacy.load("en_core_web_sm")
tokenizer = nlp.Defaults.create_tokenizer(nlp)

print("==========================================================================================================")
print("Bienvenu dans le programme de décomposition et de recherche de sens de l'équipe les Seigneurs du temps !\n")
print("==========================================================================================================")

#Pour utiliser ce code il faut lancer le fichier avec cette commande : python start.py text.txt où text.txt est le fichier de data.

def open_file(road):
    with open(road) as file:
        text = file.read()
    return text

def research(text):
    #Tableau contenant le sujet, l'action et la date
    result=[]
    test=[]
    id=0
    #Application du NLP sur le text
    doc = nlp(text)

    for mot in doc:
        taille_result=len(result)-1
        print("#################### Données du mot ###########################")
        print(mot.text, mot.dep_, mot.head.text, mot.head.pos_,[enfant for enfant in mot.children])
        stop=0
        if("ROOT"==mot.dep_):
            action = mot.text
            for enfant in mot.children:
                if(stop==1):
                    break
                if(result[len(result)-1][0]!=enfant.text):
                    if(enfant.dep_!="aux" and enfant.dep_!="punct" and enfant.dep_!="advc1"):
                        for token_test in enfant.children:
                            test.append(enfant.text)
                        if(test != []):
                            first_step=1
                            for petit_enfant in enfant.children:
                                if(petit_enfant.dep_=="poss" or petit_enfant.dep_=="aux"):
                                    action +=" "+petit_enfant.text+" "+enfant.text
                                elif(first_step):
                                    action += " "+enfant.text+" "+petit_enfant.text
                                else:
                                    action += " "+petit_enfant.text
                                first_step=0
                                if(petit_enfant.dep_=="pobj" or petit_enfant.dep_=="acomp"):
                                    stop=1;
                        else:
                            action += " "+enfant.text
                        if(enfant.dep_=="pobj" or enfant.dep_=="acomp" or enfant.dep_=="dobj" or enfant.dep_=="advc1"):
                            break
            result[len(result)-1].append(action)
        if(mot.dep_=="nsubj"):
            result.append([mot.text])
        #print(mot.text,' | ',mot.dep_)


    for entity in doc.ents:
        if(entity.label_=="DATE"):
            result[id].append(entity.text)
            id+=1
    return result

def affich_result(result):
    print("=======================================================================================================")
    print("Tableau finaux :")
    print("=======================================================================================================")
    print("Qui ? | Quoi ? | Quand ?")
    for line in result:
        print(line)
    print("=======================================================================================================")


text = open_file(sys.argv[1])
result = research(text)
affich_result(result)
