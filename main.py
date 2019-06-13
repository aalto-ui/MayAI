__author__ = 'Janin Koch'

import bandit
from ast import literal_eval
VectorList = []



# initiating bandits

def initiateBandit(name):
    # 0: bandit dimensions
    context_dimension = (6, 2, 2, 2, 2)  # H = 60
    decision_dimension = (3, 2, 2, 2, 3)  # H = 20
    arm_dimensions = (4, 1, 1, 1, 1)  # H = 5

    # 1: Get prior data
    # prior_data = get_prior_data()
    prior_data = []

    # 2: Get user history
    #user_data = get_user_data(name)
    user_data = []

    # 3: set up bandit and context space
    cBandit = bandit.ContextualBandit(arm_dimensions, decision_dimension, context_dimension, user_data, prior_data)

    return cBandit

def addVector(Vector,cBandit):
    # Vector: (H (0-360), S (0-1), L (0-1), O (0,1), Dist (0,60,120))
    VectorList.append(Vector)
    
    #If key_selected in Empty
    if not cBandit.key_selected:
        cBandit.key_selected.append(Vector)

def newVector(cBandit):
    #receive new image vector based on VectorList
    cBandit, context, next_image, expected_reward = cBandit.suggest_images()
    return next_image


if __name__ == "__main__":
    banditObj = initiateBandit('Janin')


#Input Image after processing
currentVector = raw_input("What is your initial image (H:0-360, S:0-1, L:0-1, O:0,1, Dist:0-180) => e.g (123,0.6,0.3,0,178): ")

#Add image to bandit Object
addVector(literal_eval(currentVector),banditObj)

#Keep Suggesting images until decision == 'quit'
while (True):
    nextImage = newVector(banditObj)
    print "New image characteristics: ", nextImage

    decision = raw_input("would you like to use this image? (y/n/quit) ")
    if (decision=="y"):
        addVector(nextImage,banditObj)
        bandit.update_bandit(banditObj, 1, VectorList )

    elif (decision=="n"):
        addVector(nextImage,banditObj)
        bandit.update_bandit(banditObj, 0, VectorList )
    
    elif (decision=="quit"):
        print "Thank you"
        break #Ending the session
    

