#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  2 14:04:20 2025

@author: roycruz
"""

# Packages imported
import random
import numpy as np
import matplotlib.pyplot as plt

bases = ['A','C','T','G']

mutationRate = 5
genomeLength = 100
popSize = 300

class indiv: #genome,fitness, constructor, print
    def __init__(self): # constructor
        self.fitness = 0
        self.genome = []
        for i in range(0,genomeLength):
            self.genome.append(random.choice(bases))
    
    def mutate(self):
        #self.genome[random.randint(0,len(self.genome)-1)]
        mutation_type = random.choice(["point", "insdel", "inversion"])
        
        if mutation_type == "point":
            for i in range(len(self.genome)):
                if random.randint(0, 100) < mutationRate:  # Mutation chance, this changes one base pair
                    self.genome[i] = random.choice(bases)

        elif mutation_type == "insdel":  # Insert/Delete mutation at a base pair
            if random.random() < 0.5 and len(self.genome) < genomeLength + 5:  # Insert
                insert_pos = random.randint(0, len(self.genome)-1)
                self.genome.insert(insert_pos, random.choice(bases))
            elif len(self.genome) > 5:  # Delete
                del_pos = random.randint(0, len(self.genome) - 1)
                del self.genome[del_pos]

        elif mutation_type == "inversion":  # Reverse a section of genome
            start, end = sorted(random.sample(range(len(self.genome)), 2))
            self.genome[start:end+1] = reversed(self.genome[start:end+1])
        
        
    #def mutate2(self):
     #   for i in range(0,len(self.genome)):
      #      if(random.randint(0,100) < mutationRate):
       #         self.genome[i] = random.choice(bases)
                
        
    # one point crossover
    def crossover(self, other):
        min_length = min(len(self.genome), len(other.genome))  # Ensure we don't exceed either list's length
        crossPoint = random.randint(0, min_length - 1)  # Select a valid crossover point
        for i in range(crossPoint, min_length):  # Only swap within the valid range
            temp = self.genome[i]
            self.genome[i] = other.genome[i]
            other.genome[i] = temp
    
    # uniform crossover, it walks the genome and there is a 50% swap rate
    def crossover2(self,other):
        for i in range(0,len(self.genome)-1):
            if(random.randint(0,100) < 10):
                temp = self.genome[i]
                self.genome[i] = other.genome[i]
                other.genome[i] = temp
                
                
    def calcFitness(self):
        self.fitness = 0
        for i in range(0,len(self.genome)): #self.genome:
            if self.genome[i]=='A': # count A's
                self.fitness += 1
                
    def print(self):
        print(self.genome)
        print("fitness = ", self.fitness)
        
    def __str__(self):
        return_str = str(self.genome)
        return_str += "\nfitness = " + str(self.fitness)
        return return_str

    def copy(self,source):
        #self.genome = copy.copy(source.genome) wont work because we don't have copy function installed
        for i in range(len(source.genome)):
            self.genome.append(source.genome[i])
            
    

    
class pop:
    def __init__(self):  # constructor
        self.population = []
        for i in range(popSize):
            self.population.append(indiv())
        self.bestFit = 0 # best fitness
        self.best = 0 # index of best individual
        self.avgFit = 0
        self.calcStats()
        #self.population[0].setGenome('A')
        #self.population[1].setGenome('C')

    def generation(self):
        tempPop = pop()
        # tempPop = []
        for i in range(0,popSize,2):
            p1 = self.tourn() # tournament selection
            p2 = self.tourn()
            tempPop.population[i].copy(self.population[p1])
            tempPop.population[i+1].copy(self.population[p2])
            tempPop.population[i].crossover(tempPop.population[i+1])
            tempPop.population[i].mutate()
            tempPop.population[i+1].mutate()
        #self.population = tempPop
        for i in range(0,popSize):
            self.population[i].copy(tempPop.population[i])

    def tourn(self):
        best = random.randint(0,popSize-1) # the winner so far
        bestfit = self.population[best].fitness # best fit so far
        for i in range(10): # tournament size of 10!!!!
            p2 = random.randint(0,popSize-1)
            if(self.population[p2].fitness > bestfit):
                bestfit = self.population[p2].fitness
                best = p2
        return best

    def calcStats(self):
        self.avgFit = 0
        self.population[0].calcFitness()
        self.bestFit = self.population[0].fitness
        self.best = 0
        for i in range(len(self.population)):
            self.population[i].calcFitness() # update fitnesses
            if(self.population[i].fitness > self.bestFit): # compare fitness to best
                self.bestFit = self.population[i].fitness
                self.best = i
            self.avgFit += self.population[i].fitness
        self.avgFit = self.avgFit/len(self.population)
            
            
#p = pop()
#.calcStats()
#for g in range(0,10):
 #   print("Generations ",g)
  #  print(p.population[p.best])
   # print("Avg.fit = ",p.avgFit)
    # for i in range(0,popSize)
        # p.population[i].print()
   # p.generation()
   # p.calcStats()

#print("Generations ",g)
#print(p.population[p.best])
#print("Avg fit =", p.avgFit)

#notice that after a generation the avg fit increased; the best fit is the same
# but a different individual may have been selected as best (ties can be broken randomly)
# add a loop to do lots of generations


p =pop()
data = []
p.calcStats()
for g in range(0,10): # organizing data for plotting
    print(g,p.bestFit, p.avgFit)
    data.append([g,p.bestFit,p.avgFit])
    for i in range(0, popSize):
        fit =[]
        fit.append(p.population[i].fitness)
        allfit = []
        allfit.append(fit)
    p.generation()
    p.calcStats()
print(data)
data2 = np.array(data)
print(allfit)


plt.plot(data2[:,0],data2[:,1],label ="Max.fit", linewidth =5)
plt.plot(data2[:,0],data2[:,2], color = (0,1,0),label = "Avg.fit")
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.title("Fitness over time")
plt.legend()
plt.savefig("fitness.png")
plt.show()
