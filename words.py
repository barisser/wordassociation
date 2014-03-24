import string
import pickle

words=[]
lastidused=-1
weights=[]
weight_ids=[]
all_weights=0

node_diminution= 0.2

a='the cat has a wonderful hat'
b='the man fed his cat'
c='I went to school.  I was really hungry.  SO?'

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
        print str(a) + " / "+str(h)
        read_sentence(s[a])
        a=a+1

    #for a in s:
     #   read_sentence(a)


def save():
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

def sort():   #sort weights and weight_ids lists
    global words, weights, weight_ids
    weights3=weights
    weight_ids3=weight_ids
    weights2=[]
    weight_ids2=[]
    a=0
    b=0
    c=0
    d=0
    while d<len(weights):
        a=0
        b=0
        c=0
        while a<len(weights3):
            if weights3[a]>b:
                b=weights3[a]
                c=a
            a=a+1
        
        weights2.append(b)
        weight_ids2.append(weight_ids3[c])
        del weights3[c]
        del weight_ids3[c]
        d=d+1
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

    f=0
    while f<len(words):        
        r=0
        print f
        words[f].adjusted_weight=[] #reset this to be reconstituted each time
        while r<len(words[f].connected_words):
            internalratio=(float(words[f].connection_weight[r])/float(words[f].weight))
            toword=words[f].connected_words[r]
            massratio=float(words[toword].weight)/float(all_weights)+.001
            adjusted=internalratio/massratio
            #print str(f)+ " to "+str(toword)+ " i: "+str(internalratio)+" / "+str(massratio)
            words[f].adjusted_weight.append(adjusted)
            r=r+1
        y=sum(words[f].adjusted_weight)
        t=0
        while t<len(words[f].connected_words):
            words[f].adjusted_weight[t]=words[f].adjusted_weight[t]/y
            t=t+1
        
        f=f+1

    

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

            #find the position in weights to modify
            g=0
            s=0
            while g<len(weight_ids):
                if g==otherword:
                   s=g
                   g=len(weight_ids)
                g=g+1


            #modify that weight
            weights[s]=weights[s]*theweight/all_weights   #/node_diminution
            
            
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
    for x in words[word_id].connected_words:
        print words[x].theword

f=open('b.txt')
data=f.read()

def refresh():
    calculate_weights()
    refresh_weights(-1)
    
    
