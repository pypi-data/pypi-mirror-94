#gabrielrg (11/02/2021)
#A classe utiliza o algoritmo de distancia de edicão, conhecido como distancia de levenshtein para determinar a semelhanca entre as duas palavras

import os, sys, random, pickle
import numpy as np

class StringAnalysis:
    def __init__(self, streamstring='nada'):
       self.words = streamstring.split(' ')
       self.words.sort()
       self.words = [''.join(letter.strip()	 for letter in word if letter.isalnum()) for word in self.words]
       
    #this method finds the distance between two words 
    def levenshtein(self, w1, w2):
        w1 = w1.lower()
        w2 = w2.lower()
        
        sizex = len(w1)+1
        sizey = len(w2)+1
        matrix = np.zeros((sizex, sizey))
        for x in range(sizex):
            matrix[x,0] = x
            
        for y in range(sizey):
            matrix[0,y] = y

        for x in range(1, sizex):
            for y in range(1, sizey):
                if w1[x-1] == w2[y-1]: matrix[x,y] = min(matrix[x-1,y]+1, matrix[x-1,y-1], matrix[x,y-1]+1)
                else: matrix [x,y] = min(matrix[x-1,y] + 1, matrix[x-1,y-1]+1, matrix[x,y-1]+1)
                
        return matrix[-1, -1]
    
    #this approach gets the distance between all stream words and another argument one
    def get_most_similar_word(self, word):
        mini = -1.0
        min_word = self.words[0]
        
        for stream_word in self.words:
            result = self.levenshtein(word, stream_word)
            if (mini == -1.0) or (result < mini):
                min_word = stream_word
                mini = result
        
        return min_word
        
        
"""string_analyzer = StringAnalysis("Ola, esse codigo foi gerado como parte da avaliacao tecnica da take. Meu nome e gabriel resende goncalves e estou terminando o doutorado na UFMG. Minhas principais areas de pesquisa sao aprendizagem de maquina ou inteligencia artificial, reconhecimento de padroes visuais e visao computacional. Tenho 29 anos e moro em Belo Horizonte")

print(string_analyzer.get_most_similar_word("Guilherme"))
print(string_analyzer.get_most_similar_word("Took"))
print(string_analyzer.get_most_similar_word("Ei"))
print(string_analyzer.get_most_similar_word("programando"))
print(string_analyzer.get_most_similar_word("50"))
print(string_analyzer.get_most_similar_word("Feio"))
print(string_analyzer.get_most_similar_word("artificial"))"""
