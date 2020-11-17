#!/usr/bin/python3
import tkinter
import random
from tkinter import messagebox
import math
import sys

class CalculateNError(Exception):
    def __init__(self, msg):
        self.msg = msg


gachaProb =   [[0,      400000], # R essence
               [400000, 520000], # SR essence
               [520000, 560000], # SSR essence
               [560000, 960000], # R servant
               [960000, 990000], # SR servant
               [990000, 1000000]]# SSR servant

def multiRangeRandom(args):
    max_val = 0
    normalize = []
    for i in args:
        max_val = i[1] - i[0]
    pass

def calculatePMonteCarlo(cycles, servant, rarity, probability, reliability):

    if rarity < 3 or rarity > 5:
        raise CalculateNError("¯\_(ツ)_/¯")

    if (servant):
        shift = rarity
    else:
        shift = rarity - 3

    success = 0
    min_val = int(gachaProb[shift][0])
    max_val = min_val + int(probability * 1000000)
    if max_val > int(gachaProb[shift][1]):
            raise CalculateNError("Its imposible!")

    garantServant = random.randint(1,10)
    garantSR = random.randint(1,10)
    for iter in range(0,cycles):
        for currentCard in range(1,11):
            if currentCard == garantServant:
                if currentCard == garantSR:
                    value = random.randint(gachaProb[4][0],gachaProb[5][1] - 1)
                else:
                    value = random.randint(gachaProb[3][0],gachaProb[5][1] - 1)
            else:
                if currentCard == garantSR:
                    pserv = gachaProb[5][1] - gachaProb[4][0]
                    pwhole = gachaProb[5][1] - gachaProb[4][0] + gachaProb[2][1] - gachaProb[1][0]
                    if random.randint(1,pwhole) < pserv:
                        value = random.randint(gachaProb[4][0],gachaProb[5][1] - 1)
                    else:
                        value = random.randint(gachaProb[1][0],gachaProb[2][1] - 1)
                else:
                    value = random.randint(gachaProb[0][0],gachaProb[5][1] - 1)

            if value >= min_val and value < max_val:
                success += 1

    oneProb = success / cycles
    if oneProb >= 1:
        oneProb = 0.999
    return oneProb

def calculateServantP(rarity, p, reliability):
    if (rarity == 5):
        if (p > 0.01):
            raise CalculateNError("Its imposible!")
        oneRollProb = 1 - (((1 - p) ** 8) * ((0.44 - p) / 0.44) * 0.9 * ((0.2 - p)/ 0.2) + ((1 - p) ** 9) * ((0.04 - p)/0.04) * 0.1)
    elif (rarity == 4):
        if (p > 0.03):
            raise CalculateNError("Its imposible!")
        oneRollProb = 1 - (((1 - p) ** 8) * ((0.44 - p) / 0.44) * 0.9 * ((0.2 - p)/ 0.2) + ((1 - p) ** 9) * ((0.04 - p)/0.04) * 0.1)
    elif (rarity == 3):
        if (p > 0.40):
            raise CalculateNError("Its imposible!")
        oneRollProb = 1 - (((1 - p) ** 8) * ((0.44 - p) / 0.44) * 0.9 )#+ 0.1 * ((1 - p) ** 9))
    else:
        raise CalculateNError("WTF????")
    return oneRollProb

def calculateEssenceP(rarity,p,reliability):
    if (rarity == 5):
        if (p > 0.04):
            raise CalculateNError("Its imposible!")
        oneRollProb = 1 - (((1 - p) ** 8) * ((0.2 - p)/ 0.2) * 0.9 + 0.1 * ((1 - p) ** 9))
    elif (rarity == 4):
        if (p > 0.12):
            raise CalculateNError("Its imposible!")
        oneRollProb = 1 - (((1 - p) ** 8) * ((0.2 - p)/ 0.2) * 0.9 + 0.1 * ((1 - p) ** 9))
    elif (rarity == 3):
        if (p > 0.40):
            raise CalculateNError("Its imposible!")
        oneRollProb = 1 - (((1 - p) ** 8))
    else:
        raise CalculateNError("WTF????")
    return oneRollProb

def calculateN (MonteCarlo, servant, rarity, p, reliability, cycles):
    oneRoll = 0
    if (MonteCarlo):
        oneRoll = calculatePMonteCarlo(cycles, servant, rarity, p, reliability)
    else:
        if (servant):
            oneRoll = calculateServantP(rarity, p, reliability)
        else:
            oneRoll = calculateEssenceP(rarity, p, reliability)
    return (oneRoll, math.log(1 - reliability, 1 - oneRoll))
    

class Window:
    def __init__(self):
        self.window = tkinter.Tk()

        self.type = tkinter.StringVar(self.window)
        self.type.set("Servant")
        self.type.trace("w",self.reset)

        self.reliability = tkinter.StringVar(self.window)
        self.reliability.set("95.0")

        self.probability = tkinter.StringVar(self.window)
        self.probability.set("1.0")

        self.rarity = tkinter.IntVar(self.window)
        self.rarity.set(5)

        self.MonteCarlo = tkinter.IntVar(self.window)
        self.MonteCarlo.set(1)
        self.MonteCarloCycles = tkinter.IntVar(self.window)


        self.typeOptMenu = tkinter.OptionMenu(self.window,self.type,"Servant", "Essence")
        self.raritySBox = tkinter.Spinbox(self.window, from_ = 3, to = 5, textvariable = self.rarity, command=self.reset)

        self.pLab = tkinter.Label(self.window, text="Probability(%):")
        self.rLab = tkinter.Label(self.window, text="Reliability(%):")
        self.pEntry = tkinter.Entry(self.window, textvariable = self.probability)
        self.rEntry = tkinter.Entry(self.window, textvariable = self.reliability)

        self.CheckMonteCarlo = tkinter.Checkbutton(self.window, text = "Monte-Carlo method", variable = self.MonteCarlo,command = self.enableMonteCarlo)
        self.MonteCarloCyclesBox = tkinter.Spinbox(self.window, from_ = 10000,to = sys.maxsize, textvariable = self.MonteCarloCycles)

        self.CalcButton = tkinter.Button(self.window, text = "Calculate", command=self.calc)
        self.RstButton = tkinter.Button(self.window, text = "Reset", command=self.reset)

        self.labNumber = tkinter.Label(self.window, text = "Number:")
        self.labProbRoll = tkinter.Label(self.window, text = "Probability for one Roll:")
        self.labMX = tkinter.Label(self.window, text = "Expected value:")
        self.labTNumber = tkinter.Label(self.window, text = "Number of Tickets:")

        self.outNumber = tkinter.Label(self.window)
        self.outProbRoll = tkinter.Label(self.window)
        self.outMX = tkinter.Label(self.window)
        self.outNumber = tkinter.Label(self.window)
        self.outTNumber = tkinter.Label(self.window)

        self.typeOptMenu.grid(row=0, column= 0); self.raritySBox.grid(row=0,column=1)
        self.pLab.grid(row=1, column=0,sticky=tkinter.E); self.pEntry.grid(row=1, column=1)
        self.rLab.grid(row=2, column=0,sticky=tkinter.E); self.rEntry.grid(row=2, column=1)
        self.CheckMonteCarlo.grid(row=3, column=0,sticky=tkinter.E);self.MonteCarloCyclesBox.grid(row=3, column=1,sticky=tkinter.W)
        self.CalcButton.grid(row=4,column=0); self.RstButton.grid(row=4,column=1)
        self.labNumber.grid(row=5, column=0,sticky=tkinter.E); self.outNumber.grid(row=5, column=1,sticky=tkinter.W)
        self.labProbRoll.grid(row=6, column=0,sticky=tkinter.E); self.outProbRoll.grid(row=6, column=1,sticky=tkinter.W)
        self.labMX.grid(row=7, column=0,sticky=tkinter.E); self.outMX.grid(row=7, column=1,sticky=tkinter.W)
        self.labTNumber.grid(row=8, column=0,sticky=tkinter.E); self.outTNumber.grid(row=8, column=1,sticky=tkinter.W)
        self.window.mainloop()

    def clear(self):
        self.outNumber.config(text="")
        self.outProbRoll.config(text="")
        self.outMX.config(text="")
        self.outTNumber.config(text="")

    def reset(self, *args):
        if(self.type.get() == "Servant"):
            rarity = self.rarity.get()
            if (rarity == 3):
                self.probability.set("40.0")
            elif (rarity == 4):
                self.probability.set("3.0")
            elif (rarity == 5):
                self.probability.set("1.0")
        elif(self.type.get() == "Essence"):
            rarity = self.rarity.get()
            if (rarity == 3):
                self.probability.set("40.0")
            elif (rarity == 4):
                self.probability.set("12.0")
            elif (rarity == 5):
                self.probability.set("4.0")
        self.clear()

    def output(self, N, p, M, TN):
        self.outNumber.config(text=str(math.ceil(N)))
        self.outProbRoll.config(text=str(round(p,2))+" %")
        self.outMX.config(text=str(round(M,2)))
        self.outTNumber.config(text=str(math.ceil(TN)))

    def enableMonteCarlo(self):
        if (not self.MonteCarlo.get()):
            self.MonteCarloCyclesBox.config(state = tkinter.DISABLED)
        else:
            self.MonteCarloCyclesBox.config(state = tkinter.NORMAL)

    def calc(self):
        self.clear()
        try:
            servant = (self.type.get() == "Servant")
            rarity = self.rarity.get()
            probability = float(self.probability.get())/100
            reliability = float(self.reliability.get())/100
            oneRollProb, N = calculateN(self.MonteCarlo.get(), servant, rarity, probability, reliability, self.MonteCarloCycles.get())
            TicketN = math.log(1 - reliability, 1 - probability)
            MX = oneRollProb * N
        except ValueError:
            messagebox.showerror("Error","You should input correct values")
        except CalculateNError as error:
            messagebox.showerror("Error",error.msg)
        except ZeroDivisionError:
            messagebox.showerror("Sasi","Sasi")
        else:
            self.output(N, oneRollProb * 100, MX, TicketN)
Window()
