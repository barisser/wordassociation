import string
import pickle
import requests
import math

words=[]
lastidused=-1
weights=[]
weight_ids=[]
all_weights=0

class word:
    id=-1
    theword=''

    weight=0.0  
    connected_words=[]  # only have the id here
    connection_weight=[]
    adjusted_weight=[]

    def __init__(self,theword):
        global words,lastidused
        self.theword=theword
        self.id=lastidused+1
        lastidused=lastidused+1
        self.connected_words=[]
        self.connection_weight=[]
        words.append(self)

    def printword(self):
        print self.theword
        for x in self.connected_words:
            print words[x].theword

    def connect(self,towhom):
        found=False
        a=0
        while a<len(self.connected_words):
            if self.connected_words[a]==towhom:
                found=True
                self.connection_weight[a]=self.connection_weight[a]+1.0
                a=len(self.connected_words)
            a=a+1
        if found==False:
            self.connected_words.append(towhom)
            self.connection_weight.append(1.0)
        

def printall():
    for x in words:
        print x.theword

def break_into_sentences(txt):
  
    global sofar, sentences
    sofar=''
    sentences=[]
    for x in txt:
        if x=="." or x=="?" or x=="!":
            sofar=sofar+x
            sentences.append(sofar)
            sofar=''
        else:
           sofar=sofar+x
            
    return sentences

def parse_sentence(sentence):
    sentence=sentence.translate(None,string.punctuation)
    word_list=[]
    thisword=''

    for x in sentence:
        x=x.lower()
        if x==' ' or x=='-':  #put symbols here that end words
            if len(thisword)>0 and not thisword.isdigit():
                word_list.append(thisword)
                thisword=''
        elif (not x=='.' and not x=='\r' and not x=='?' and not x=='\n' and not x=='  ' and not x=="-" and not x=='!' and not x==',' and not x.isdigit()):
            thisword=thisword+x

    if len(thisword)>0:  # at end of sentence last word is not yet appended
        word_list.append(thisword)

    word_list2=[]
    for y in word_list:  #remove duplicates (n^2 time not great)
        ok=True
        for x in word_list2:
            if x==y:
                ok=False
        if ok:
            word_list2.append(y)

    return word_list2

    

def read_sentence(sentence):
    
    global words, word_ids
    s_words=parse_sentence(sentence)
    word_ids=[]

    t=0
    for x in s_words:
      #  print str(t)+ "  characters processed"
        t=t+1
        
        found=False
        for y in words:
            if x==y.theword:
                found=True
                word_ids.append(y.id)
                #do stuff to that word entry                
        if not found:
            new_word=word(x) #add new word to main list
            word_ids.append(new_word.id)

    for x in word_ids:   #INEFFICIENT
        for y in word_ids:
            if not x==y:
                words[x].connect(y)
    
def read(txt):
    s=break_into_sentences(txt)
    a=0
    h=len(s)
    while a<len(s):
        print str(a) + " / "+str(h) + " sentences read"
        read_sentence(s[a])
        a=a+1
    refresh()

    #for a in s:
     #   read_sentence(a)


def save():  #saves WORD OBJECT list "WORDS", does not save weights or weight_ids which can be computed
    with open("words.dat","wb") as f:
        pickle.dump(words,f)

def load():
    global words
    with open("words.dat") as f:
        words=pickle.load(f)

def findword(word):
    a=0
    answer=-1
    while a<len(words):
        if words[a].theword==word:
            answer=a
            a=len(words)
        a=a+1
    return answer

def findinlist(x,list):
    b=len(list)
    a=-1.5
    if(b>0):
        lowerbound=0
        upperbound=b
        a=(lowerbound+upperbound)/2
        p=b
        h=int(str(x).encode("hex"),32)
        depth=0
        g=0
        cont=True
        while(cont):
            g=g+1
            a=(lowerbound+upperbound)/2
            hexa=int(str(list[a]).encode("hex"),32)
            
            if(h==hexa):
                cont=False
            elif(upperbound-lowerbound<2 and h>hexa):
                cont=False
                a=-upperbound
            elif(upperbound-lowerbound<2 and h<hexa):
                cont=False
                a=-lowerbound
            
            elif(h<hexa):
                
                upperbound=a
                                
            elif(h>hexa):
                
                lowerbound=a
            elif(g>math.log(b,2)*3):
                cont=False
                a=-1
                    
    return a


def sort():   #sort weights and weight_ids lists
    global weights, weight_ids

    weights2=[]
    weight_ids2=[]
    a=0
    while a<len(weights):
        place=findinlist(weights[a],weights2)

        if place==-1.5:  #list is totally empty
            weights2.append(weights[a])
            weight_ids2.append(weight_ids[a])
        elif place<=0:  #does not exist in list, should usually be this
            weights2.insert(-1*place, weights[a])
            weight_ids2.insert(-1*place,weight_ids[a])
        else:
            weights2.insert(place,weights[a])
            weight_ids2.insert(place,weight_ids[a])
        
        a=a+1
    weights=weights2
    weight_ids=weight_ids2

   

#call this before refresh_weights
def calculate_weights():  #sum weights, individual totals, individual adjusted amts
    global all_weights, words
    a=0
    for x in words:
        a=a+sum(x.connection_weight)
    all_weights=a

    g=0
    while g<len(words):
        words[g].weight=sum(words[g].connection_weight)+1
        
        g=g+1

    popularity_exponent = 0.5 #by what degree to penalize populat words, higher is more penalized
    
    number_of_words=len(words)
    f=0
    while f<len(words):        
        r=0
        print str(f)+ " / "+str(number_of_words)
        words[f].adjusted_weight=[] #reset this to be reconstituted each time
        while r<len(words[f].connected_words):
            internalratio=(float(words[f].connection_weight[r])/float(words[f].weight))
            toword=words[f].connected_words[r]
            massratio=float(words[toword].weight)/float(all_weights)+.001
            adjusted=internalratio/math.pow(massratio,popularity_exponent)
            #print str(f)+ " to "+str(toword)+ " i: "+str(internalratio)+" / "+str(massratio)
            words[f].adjusted_weight.append(adjusted)
            r=r+1
        y=sum(words[f].adjusted_weight)
        t=0
        while t<len(words[f].connected_words):
            words[f].adjusted_weight[t]=words[f].adjusted_weight[t]/y
            t=t+1
        
        f=f+1

def add_weight_to_neighbors(word_id, factor):
    for x in words[word_id].connected_words:
        #find position in weight_ids
        a=0
        g=0
        while a<len(weight_ids):
            if weight_ids[a]==x: #you have found the correct index in weight_ids
               g=a
               a=len(weight_ids)
            a=a+1
        weights[g]=weights[g]+weights[word_id]*factor #your weight plus my weight times factor
                

def refresh_weights(word_id):  #creates side lists of weights and weight ids
                                 #call this before sort 
    
    global weights, weight_ids
 
    if word_id==-1:
        #then reset
        weights=[]
        weight_ids=[]
        for x in words:
            weights.append(x.weight/all_weights)
            weight_ids.append(x.id)
    else:
        #start by diminishing all weights by set prefactor
       t=0
       while t<len(weights):
            weights[t]=weights[t]/all_weights
            t=t+1

       a=0
       while a<len(words[word_id].connected_words):  #for each connected word
            otherword=words[word_id].connected_words[a]
            theweight=words[word_id].adjusted_weight[a]
            print a
            #find the position in weights to modify
            g=0
            s=0
            while g<len(weight_ids):
                if weight_ids[g]==otherword:
                   s=g
                   g=len(weight_ids)
                g=g+1


            #modify that weight
            #weights[s]=weights[s]*theweight/all_weights   #/node_diminution
            
            weights[s]=weights[s]+theweight*all_weights
            add_weight_to_neighbors(otherword,0.3)
            
            a=a+1

        #normalize new weights
    p=0
    for x in weights:
            p=p+x
    a=0
    while a<len(weights):
        weights[a]=weights[a]/p
        a=a+1

def correlated(word_id):
    a=0
    
    while a<len(words[word_id].adjusted_weight):
        wordstring=words[words[word_id].connected_words[a]].theword
        weight=words[word_id].adjusted_weight[a]
        print wordstring + "  "+str(weight)
        ws.append(wordstring)
        we.append(weight)
        a=a+1

def print_weights(n):
    a=0
    while a<n:
        print words[weight_ids[a]].theword+"  "+str(weights[a])
        a=a+1
  

f=open('b.txt')
data=f.read()

def wordcheck(word):  #so you can input strings
    a=findword(word)
    if a>-1:   #meaning it has been found, -1 means not found
        refresh_weights(a)
        #sort()
        for x in weight_ids[0:10]:
            print words[x].theword
    
        

def refresh():
    calculate_weights()
    refresh_weights(-1)


from HTMLParser import HTMLParser
class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ''.join(self.fed)

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

def read_site(web_address):
    a=requests.get(web_address)
    print a.status_code
    if a.status_code==200:
        data=a.content
        cleaned=strip_tags(data)
        read(cleaned)

a='the cat eats meat. '
b= 'the cat also likes to go home. '
c = 'meat is good for dogs and cats. '
d= 'this guy has no home. '
f=' the cat has a home for a home inside that place.'
e=a+b+c+d+f
read(e)
