#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Lgmrszd'
__version__ = '0.0.1b'

class TuringMachine:
    __alphabet_def='abcdefghigklmnopqrstuvwxyzABCDEFGHIGKLMNOPQRSTUVWXYZ1234567890'
    def __init__(self):
        self.__pointer=1
        self.__null='λ'
        self.__alphabet=self.__alphabet_def+self.__null
        self.__tape=[self.__null]*100
        self.__rules=[]

    def getStatesCount(self):
        print(len(self.__rules))

    def addState(self):
        l=len(self.__rules)
        r={}
        for x in self.__alphabet:
            r[x]=[l,x,0]
        print(r)
        self.__rules.append(r)

    def setRule(self,ifq,ifs,q,s,g):
        self.__rules[ifq][ifs]=[q,s,g]

    def getTapeLenght(self):
        return len(self.__tape)

    def setTapeLenght(self,lenght):
        if (lenght<2) or (lenght>200):
            return False, 'Wrong lenght.'
        else:
            self.__tape=(self.__tape+(lenght-len(self.__tape))*[self.__null])[:lenght]
            return True, None

    def setTape(self,pos,tape):
        self.__tape=(pos*[self.__null]+list(tape)+(len(self.__tape)-len(tape))*[self.__null])[:len(self.__tape)]

    def getTape(self):
        return self.__tape

    def importConfig(self,file):
        pass

    def exportConfig(self,file):
        pass

if __name__ == '__main__':
    tm=TuringMachine()
    print(tm.getTape())
    tm.setTape(4,['a']*100)
    print(tm.getTape())
    tm.addState()