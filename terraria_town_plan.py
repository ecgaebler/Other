import datetime

class NPC:
    def __init__(self, name, biomes, npcs):
        self.name = name
        self.liked_biome = biomes[0]
        self.disliked_biome = biomes[1]
        self.loved_npcs = npcs[0]
        self.liked_npcs = npcs[1]
        self.disliked_npcs = npcs[2]
        self.hated_npcs = npcs[3]

class Best:
    def __init__(self):
        self.score = float("inf")
        self.states = []


angl = NPC( "Angl", ("Ocean","Desert"), ([],["Demo","PaGi","TaCo"],[],["Tave"]) )
arde = NPC( "ArDe", ("Desert","Snow"), (["Nurs"],["Stea"],["Golf"],["Demo"]) )
clot = NPC( "Clot", ("Cavern","Hallow"), (["Truf"],["TaCo"],["Nurs"],["Mech"]) )
cybo = NPC( "Cybo", ("Snow","Jungle"), ([],["Stea","Pira","Styl"],["Zool"],["Wiza"]) )
demo = NPC( "Demo", ("Cavern","Ocean"), (["Tave"],["Mech"],["ArDe","GoTi"],[]) )
drya = NPC( "Drya", ("Jungle","Desert"), ([],["WiDo","Truf"],["Angl"],["Golf"]) )
dytr = NPC( "DyTr", ("Desert","Forest"), ([],["ArDe","Pain"],["Stea"],["Pira"]) )
golf = NPC( "Golf", ("Forest","Cavern"), (["Angl"],["Pain","Zool"],["Pira"],["Merc"]) )
goti = NPC( "GoTi", ("Cavern","Jungle"), (["Mech"],["DyTr"],["Clot"],["Styl"]) )
guid = NPC( "Guid", ("Forest","Ocean"), ([],["Clot","Zool"],["Stea"],["Pain"]) )
mech = NPC( "Mech", ("Snow","Cavern"), ([goti],["Cybo"],["ArDe"],["Clot"]) )
merc = NPC( "Merc", ("Forest","Desert"), ([],["Golf","Nurs"],["TaCo"],["Angl"]) )
nurs = NPC( "Nurs", ("Hallow","Snow"), (["ArDe"],["Wiza"],["Drya","PaGi"],["Zool"]) )
pain = NPC( "Pain", ("Jungle","Forest"), (["Drya"],["PaGi"],["Truf","Cybo"],[]) )
pagi = NPC( "PaGi", ("Hallow","Cavern"), (["Wiza","Zool"],["Styl"],["Merc"],["TaCo"]) )
pira = NPC( "Pira", ("Ocean","Cavern"), (["Angl"],["Tave"],["Styl"],["Guid"]) )
stea = NPC( "Stea", ("Desert","Jungle"), (["Cybo"],["Pain"],["Drya","Wiza","PaGi"],[]) )
styl = NPC( "Styl", ("Ocean","Snow"), (["DyTr"],["Pira"],["Tave"],["GoTi"]) )
tave = NPC( "Tave", ("Hallow","Snow"), (["Demo"],["GoTi"],["Guid"],["DyTr"]) )
taco = NPC( "TaCo", ("Snow","Hallow"), (["Merc"],["PaGi"],["Demo","Mech"],[]) )
truf = NPC( "Truf", ("Mushroom","*"), (["Guid"],["Drya"],["Clot"],["WiDo"]) )
wido = NPC( "WiDo", ("Jungle","Hallow"), ([],["Drya","Guid"],["Nurs"],["Truf"]) )
wiza = NPC( "Wiza", ("Hallow","Ocean"), (["Golf"],["Merc"],["WiDo"],["Cybo"]) )
zool = NPC( "Zool", ("Forest","Desert"), (["WiDo"],["Golf"],["Angl"],["ArDe"]) )

early_npcs = [wido,guid,angl,arde,clot,demo,drya,dytr,golf,goti,
                    mech,merc,nurs,pain,pagi,styl,tave,zool]
late_npcs = [truf,cybo,pira,stea,taco,wiza]

all_biomes = ["Forest","Jungle","Desert","Ocean","Snow","Cavern","Hallow","Mushroom"]
early_biomes = ["Forest","Jungle","Desert","Ocean","Snow","Cavern"]
late_biomes = ["Mushroom","Hallow"]

crowded_modifier = 1.04 # NPCs > 3 within 25 tiles (for each additional NPC)
sparce_modifier = 0.90 # NPCs < 3 within 25 tiles and NPCs < 4 within 120 tiles
biome_like_modifier = 0.95
biome_hate_modifier = 1.05
npc_love_modifier = 0.90
npc_like_modifier = 0.95
npc_dislike_modifier = 1.05
npc_hate_modifier = 1.10

npc_dict = {}
for npc in early_npcs:
    npc_dict[npc.name] = npc
npc_list = list(npc_dict.keys())
    
best = Best()
best.states = []
best.score = float("inf")

ignore_set = set()
for npc in ["Guid","Nurs","Angl"]:
    ignore_set.add(npc)
    
start_state = [[], #Forest
               ["WiDo"], #Jungle
               [], #Desert
               [], #Snow
               [], #Cavern
               []] #Ocean
               #[], #Hallow
               #[], #Ocean
               #["Truf"]] #Mushroom
'''
start_state = [["Truf"], #Mushroom
               []] #Hallow
'''

def biome_score(biome, npcs):
    """" Given a biome and list of NPC names, calculate the happiest score """
    result = 100.0
    if len(npc_list) < 2:
        return result

    for npc in npcs:
        if npc in ignore_set: #ignore non-vendor npcs
            continue
        npc_score = 1.0
        
        #check town size
        if len(npcs) > 3:
            npc_score *= pow(crowded_modifier, len(npcs) - 3)
        elif len(npcs) < 3:
            npc_score *= sparce_modifier

        #check biome
        if biome == npc_dict[npc].liked_biome:
            npc_score *= biome_like_modifier
        elif biome == npc_dict[npc].disliked_biome:
            npc_score *= biome_hate_modifier

        #check neighbors
        for neighbor in npcs:
            if neighbor != npc:
                if neighbor in npc_dict[npc].loved_npcs:
                    npc_score *= npc_love_modifier
                elif neighbor in npc_dict[npc].liked_npcs:
                    npc_score *= npc_like_modifier
                elif neighbor in npc_dict[npc].disliked_npcs:
                    npc_score *= npc_dislike_modifier
                elif neighbor in npc_dict[npc].hated_npcs:
                    npc_score *= npc_hate_modifier

        npc_score = npc_score
        if npc_score < result:
            result = npc_score

    #print(f"{town_biome}: {result}")
    return result


def permutations(state, npc_idx, biome_list):
    """
    state is a list of string lists, where the strings are NPC names.
    best is a Best object because I don't know how to side effect in Python. /:
    ignore_set is a list of NPC names to ignore, such as for nonvendors.
    """
    result = []
    npc_names = list(npc_dict.keys())
    if npc_idx >= len(npc_names): #no npcs left to add
        current_score = 0
        for i in range(len(state)): #loop through each biome town, adding its score.
            current_score += biome_score(biome_list[i], state[i])
            #print(f"{biome_list[i]} score: {current_score}")
        if current_score < best.score: #found new best score!
            best.score = current_score
            best.states = [state]
            d=datetime.datetime.now()
            if best.score <= 0.85*len(biome_list):
                temp_str = str([round(biome_score(biome_list[_], state[_]), 3)
                                for _ in range(len(state))])
                print(f"[{d.strftime('%b %d %H:%M')}] "
                      f"best combined score: {round(best.score,3)} "
                      f"(scores: {temp_str})")
            elif best.score <= len(biome_list):
                print(f"[{d.strftime('%b %d %H:%M')}] "
                      f"best combined score: {round(best.score,3)} "
                      f"(average score: {round(best.score/len(biome_list),3)})")
            else:
                print(f"Best combined score: {round(best.score,3)}")
        elif current_score == best.score: #same score as best
            best.states.append(state)
    else:
        for i in range(len(state)):
            if npc_idx <= 7:
                print(f"{'-'*(npc_idx//2)}Placing NPC #{npc_idx+1} in {biome_list[i]}...")
            if len(state[i]) > 2 * len(npc_dict)/len(biome_list): #don't place in already crowded town
                continue
            updated_town = state[i] + [npc_names[npc_idx]]
            new_state = state[:i] + [updated_town] + state[i+1:]
            permutations(new_state, npc_idx + 1, biome_list)

print("Witch Doctor preplaced in Jungle.")
permutations(start_state, 1, early_biomes)
print(f"best score: {best.score}")
print(f"{len(best.states)} best permutations")
