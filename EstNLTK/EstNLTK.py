# -*- coding: utf-8 -*-
import subprocess as sp
import re
import os

class EstNLTK:

    def __init__(self):
        self.t3mesta    = '/opt/home/rsirel/public_html/mag/ressursid/mrf/prog-lin32/t3mesta -Y -path $HOME/bin:/opt/home/rsirel/public_html/mag/ressursid/mrf/noarch/data +1 -cio utf8'
        self.lausestaja = '/opt/home/rsirel/public_html/mag/ressursid/lausestaja/lausestaja.pl'
        self.wordnet    = '/opt/home/rsirel/public_html/mag/ressursid/wordnet/wnonto.owl'

    def unikaliseeriList(self, s):
        ### Funktsioon kaotab listist kordused. ############
        ### Funktsiooni sisendiks ja väljundiks on list. ###
        output = []
        for x in s:
          if x not in output:
            output.append(x)
        return output

    def lausesta(self, sisend):
        ### Funktsioon lausestab sisestatud stringi. ####
        ### Funktsiooni sisendiks on string. ############
        ### Funktsiooni väljundiks on list lausetega. ###
        lausestatud = sp.Popen('echo "'+sisend+'" | '+self.lausestaja, stdout=sp.PIPE, shell=True).communicate()[0]
        lausestatud = lausestatud.replace('<s> ','')
        lausestatudlist = lausestatud.split(' </s> ')
        return lausestatudlist[0:-1]

    ###################
    ### MORFOLOOGIA ###
    ###################

    def t3_lemmatiseeri(self, sisend, otype):
        ### Funktsioon lemmatiseerib kõik lauses leiduvad sõnavormid. ##########
        ### Funktsiooni sisendiks on string, mida soovitakse lemmatiseerida. ###
        ### Funktsiooni väljundiks on lemmatiseeritud string. ##################
        mrf = sp.Popen('echo "'+sisend+'" | '+self.t3mesta, stdout=sp.PIPE, shell=True).communicate()[0]
        lemmad = []
        for a in mrf.split('\n'):
            sona = []
            for b in a.split('    ')[1:]:
                if '_V_' in b:
                    b = re.compile('\+.*//').sub('ma', b)
                else:
                    b = re.compile('\+.*//').sub('', b)
                    b = re.compile(' //.*//').sub('', b)
                b = b.replace('=','')
                b = b.replace('_','')
                sona.append(b)
            if len(sona) > 0 and sona[0] != '####':
                lemmad.append(' '.join(self.unikaliseeriList(sona)))
        if otype == 'string':
            return ' '.join(lemmad)
        elif otype == 'list':
            return lemmad
        else:
            return 'Viga: väljundi tüüp ei vasta nõuetele (valiukud "list" ja "string")'

    def t3_yhesta(self, sisend, otype):
        mrf = sp.Popen('echo "'+sisend+'" | '+self.t3mesta, stdout=sp.PIPE, shell=True).communicate()[0]
        output = []
        if otype == 'list':
            for a in mrf.split('\n'):
                if len(a) > 0:
                    a = a.replace(', //','')
                    output.append(a)
        elif otype == '2dlist':
            for a in mrf.split('\n'):
                if len(a) > 0:
                    a = a.replace(', //','')
                    a = a.split('    ')
                    output.append(a)
        return output

    ###############
    ### WORDNET ###
    ###############
        
    def wn_synonyymid(self, otsitav):
        ### Funktsioon leiab WordNetist sõnale sünonüümid. ###
        ### Funktsiooni sisendiks on string. #################
        ### Funktsiooni väljundiks on list sünonüümidega. ####
        fh=open(self.wordnet,"r")
        fail = fh.read()
        fh.close
        fail = fail.replace("\n","")
        fail = fail.replace("<owl:Class","\n<owlClass")
        read = fail.split("\n")
        synonyymid = []
        for rida in read:
            if "["+otsitav+"]" in rida:
                for a in rida.split("    "):
                    if "<rdfs:label" in a:
                        a = a.replace('<rdfs:label xml:lang="et"><![CDATA[','')
                        a = a.replace(']]></rdfs:label>','')
                        synonyymid.append(a)
        synonyymid = self.unikaliseeriList(synonyymid)
        for synonyym in synonyymid:
            if synonyym == otsitav:
                synonyymid.remove(synonyym)
        return synonyymid

    def wn_hyperonyymid(self, otsitav):
        ### Funktsioon leiab WordNetist sõnale hüponüümid. ###
        ### Funktsiooni sisendiks on string. #################
        ### Funktsiooni väljundiks on list hüponüümidega. ####
        fh=open(self.wordnet,"r")
        fail = fh.read()
        fh.close
        fail = fail.replace("\n","")
        fail = fail.replace("<owl:Class","\n<owlClass")
        read = fail.split("\n")
        hyponyymid = []
        for rida in read:
            if "["+otsitav+"]" in rida:
                for a in rida.split("    "):
                    if "<rdfs:subClassOf" in a:
                        a = a.replace('<rdfs:subClassOf rdf:resource="&eo2009r1;','')
                        a = a.replace('"/>  </owl:Class>','')
                        a = a.strip()
                        for rida in read:
                            if '<owlClass rdf:ID="'+a+'">' in rida:
                                for b in rida.split("    "):
                                    if "<rdfs:label" in b:
                                        b = b.replace('<rdfs:label xml:lang="et"><![CDATA[','')
                                        b = b.replace(']]></rdfs:label>','')
                                        hyponyymid.append(b)
        hyponyymid = self.unikaliseeriList(hyponyymid)
        for hyponyym in hyponyymid:
            if hyponyym == otsitav:
                hyponyymid.remove(hyponyym)
        return hyponyymid

    def wn_definitsioonid(self, otsitav):
        ### Funktsioon leiab Wordnetist sõnale definitsioonid. ###
        ### Funktsiooni sisendiks on string. #####################
        ### Funktsiooni väljundiks on list definitsioonidega. ####
        fh=open(self.wordnet,"r")
        fail = fh.read()
        fh.close
        fail = fail.replace("\n","")
        fail = fail.replace("<owl:Class","\n<owlClass")
        read = fail.split("\n")
        definitsioonid = []
        for rida in read:
            if "["+otsitav+"]" in rida:
                for a in rida.split('    '):
                    if '<rdfs:comment' in a:
                        a = a.replace('<rdfs:comment xml:lang="et"><![CDATA[','')
                        a = a.replace(']]></rdfs:comment>','')
                        a = a.replace('</owl:Class>','')
                        a = a.strip()
                        definitsioonid.append(a)
        return definitsioonid

    #################
    ### BIGRAMMID ###
    #################

    def bigrammid(self,sisend):
        ### Funktsioon leiab sisendstringist bigrammid. #############
        ### Ei arvesta bigramme, kus esimese sõne küljes on märk. ###
        ### Väljund on listina. #####################################
        margid = [',','.',':',';','*']
        sisend = sisend.lower().split(' ')
        output = []
        cnt=0
        for a in sisend:
            cnt+=1
            try:
                bigram = [a,sisend[cnt]]
            except IndexError:
                return output
            sobib = True
            for mark in margid:
                if mark in bigram[0]:
                    sobib = False
                    break
            if len(bigram[1]) < 2:
                break
            if sobib == True:
                for mark in margid:
                    bigram[1] = bigram[1].replace(mark,'')
                output.append(" ".join(bigram))
        return output

    def bigrammid_kitsendustega(self,sisend,kitsendus_1,kitsendus_2):
        ### Funktsioon leiab sisendstringist bigrammid (kitsendustega). #############
        ### Ei arvesta bigramme, kus esimese sõne küljes on märk. ###################
        ### Väljund on listina. #####################################################
        margid = [',','.',':',';','*']
        sisend = self.t3_yhesta(sisend,'2dlist')
        output = []
        cnt=0
        for a in sisend:
            cnt+=1
            try:
                bigram = [a,sisend[cnt]]
            except IndexError:
                return output
            sobib = True
            for mark in margid:
                if mark in bigram[0][0]:
                    sobib = False
                    break
            if kitsendus_1 not in bigram[0][1]:
                sobib = False
            if kitsendus_2 not in bigram[1][1]:
                sobib = False
            if sobib == True:
                for mark in margid:
                    bigram[1][0] = bigram[1][0].replace(mark,'')
                output.append(str(bigram[0][0])+' '+str(bigram[1][0]))
        return output
