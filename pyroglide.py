import random
amountofsims = 1000000

done = False
finished = []
ingotsBought = []
epic = ["AK Skin", "Constellation Light", "Axe Skin"]
legendary = ["Outfit Set", "Pyro Bike"]
rare = [1,2,3,4,5,6]
epic_ = [1,2,3,4,5,6,7,8,9]

objectiveEpic_ = [1,2,3,4,5,6,7,8,9]
objectiveRare = [1,2,3,4,5,6]
currency = 0
collection = ["Outfit Set", "Pyro Bike", "AK Skin", "Constellation Light", "Axe Skin"]
lightforgeRound = 30
ingots = 10

def pullFromList(list_):
    if len(list_) != 0:
        pickedItem = random.choice(list_)
        list_.remove(pickedItem)
        if pickedItem in collection:
            collection.remove(pickedItem)
        global lightforgeRound
        return pickedItem
    else:
        return "none"


def pullFromCollection():
    if len(collection) != 0:
        pickedItem = random.choice(collection)
        collection.remove(pickedItem)
        if pickedItem == "Outfit Set" or pickedItem == "Pyro Bike":
            legendary.remove(pickedItem)
        else:
            epic.remove(pickedItem)
        global lightforgeRound
        lightforgeRound = 30
        return pickedItem
    else:
        return "none"

def rarityPicker():
    roll = random.random()
    if roll < 0.004:
        return "Legendary Collection"
    elif roll < 0.049:
        return "Epic Collection"
    elif roll < 0.386:
        return "Rare"
    else: 
        return "Epic"
    
def reset():
    global legendary
    legendary = ["Outfit Set", "Pyro Bike"]
    global epic
    epic = ["AK Skin", "Constellation Light", "Axe Skin"]
    global collection
    collection = ["Outfit Set", "Pyro Bike", "AK Skin", "Constellation Light", "Axe Skin"]
    global lightforgeRound
    lightforgeRound = 30
    global done
    done = False
    global currency
    currency = 0
    global ingots
    ingots = 10
    global rare
    rare = [1,2,3,4,5,6]
    global epic_
    epic_ = [1,2,3,4,5,6,7,8,9]

def convertToCrystgin(cratesOpened,ingotsSpent):
    return (cratesOpened-ingotsSpent-10)*160+10*80

def convertToEuro(crystgin_needed):
    packages = [
        (100, 7880),
        (50, 3880),
        (30, 2280),
        (15, 1090),
        (5, 330),
        (1, 60)
    ]

    total_euro = 0
    package_breakdown = []

    for euro, crystgin in packages:
        if crystgin_needed >= crystgin:
            num_packages = crystgin_needed // crystgin
            total_euro += num_packages * euro
            crystgin_needed -= num_packages * crystgin
            package_breakdown.append((num_packages, euro, crystgin))
    
    return total_euro, package_breakdown

def format_number_with_period(number):
    return "{:,}".format(number).replace(',', '.')

def main():
    for j in range(0,amountofsims):
        global lightforgeRound
        global currency
        global ingots
        global done
        for i in range(0,150):
            if done == False:
                if currency >= 8 and ingots > 0:
                    currency -= 8
                    ingots -= 1
                if lightforgeRound == 0:
                    if pullFromCollection() == "Pyro Bike":
                        finished.append(i)
                        done = True
                
                elif currency >= 650:
                    finished.append(i)
                    done = True
                elif done == False:
                    thisRoll = rarityPicker()
                    if thisRoll == "Legendary Collection":
                        lightforgeRound = 30
                        if pullFromList(legendary) == "Pyro Bike":
                            finished.append(i)
                            done = True
                    if len(epic) == 0 and thisRoll == "Epic Collection":
                        i -= 1
                    elif thisRoll == "Epic Collection":
                        lightforgeRound = 30
                        pullFromList(epic)
                    if thisRoll == "Rare":
                        lightforgeRound -= 1
                        pulledRare = pullFromList(rare)
                        if pulledRare in objectiveRare:
                            pass
                        else:
                            currency += 2
                    if thisRoll == "Epic":
                        lightforgeRound -= 1
                        pulledEpic = pullFromList(epic_)
                        if pulledEpic in objectiveEpic_:
                            pass
                        else:
                            currency += 3
            else:
                ingotsBought.append(10-ingots)
                i = 149
        
        reset()

main()
reset()
import numpy
print("Amount of crates opened in this experiment:", format_number_with_period(round(numpy.sum(finished))))
print("Mean amount of crates opened to get 1 of 2 legendary collection items:", format_number_with_period(round(numpy.mean(finished))))
print(f"Amount of Lightforge Ingots used(limit: {format_number_with_period(ingots)}):", format_number_with_period(round(numpy.mean(ingotsBought))))
crystgin_amount = convertToCrystgin(round(numpy.mean(finished)), round(numpy.mean(ingotsBought)))
print("Crystgin spent on opening crates:", format_number_with_period(crystgin_amount))
cost, breakdown = convertToEuro(crystgin_amount)
print("Money spent on opening crates:", f"{format_number_with_period(cost)}€")
print("Packages Bought:")
for num, euro, crystgin in breakdown:
    print(f"{num} package(s) of {format_number_with_period(crystgin)} crystgin for {format_number_with_period(euro)} Euro each")