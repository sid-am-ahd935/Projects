import json
from difflib import get_close_matches

dict = {}
Dict = {}
with open("dictionary.json" , "r", encoding = "utf-8") as f:
    Dict = json.load(f)

dict = {k.lower(): v for k, v in Dict.items()}
    

search = input ("Enter Word To Search: ")
word = search
search = search.lower()

if search in dict:
    word = dict[search]
    
    count = 0
    for i in word:
        count +=1
        print("%d)" %count,i)
                
else:
    closelist = get_close_matches(search, dict.keys(), cutoff = 0.7)
    #cutoff Is The Accuracy Of Search Results
    
    if len(closelist) != 0:
        print("\nMaybe You Were Looking For This:")
        for i in closelist:
            print("\n>>",i, ":\n\t")
            word = dict[i]
            count = 0
            for i in word:
                count +=1
                print("%d)" %count,i, "\n")


    else: print("Your word", word, "is not found. Please try again.")
    
'''
Or You Can Use Multiple if and else statements to what i did with two for loops.
And you can decorate this program by using functions and another input statement asking whether the closest match is the one you are looking for and letting them chose from the given closest matches
'''