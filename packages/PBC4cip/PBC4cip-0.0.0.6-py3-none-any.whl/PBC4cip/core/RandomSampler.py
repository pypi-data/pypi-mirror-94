import random

def SampleWithoutRepetition(poulation, sampleSize):
    result =  random.sample(list(
        map(lambda attribute: attribute, poulation)), sampleSize)
    return result