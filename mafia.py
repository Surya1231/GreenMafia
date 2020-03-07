from __future__ import print_function
import random 

# --------------- Helpers that build all of the responses ----------------------



def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------
def get_welcome_response():
    session_attributes = {"state":0 , "current_player" : 0 , "no_of_players" : 0 , "players" : [] , "roles" : []}
    card_title = "Welcome"
    speech_output = "Welcome to Green Mafia Game! Do you want to here the rules?"
    reprompt_text = "I don't know if you heard me, welcome to your Green mafia!"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
        
def get_rules_response(intent , session):
    session_attributes = session['attributes']
    card_title = "Rules"
    if intent["slots"]["yn"].get("value")==None:
        speech_output = "Sorry I am unable to catch that please respond in yes or no."
    else :
        session_attributes["state"] = 1
        if intent["slots"]["yn"].get("value") == "yes":
            rulles = " Green Mafia is a social deduction game modeling a conflict between the two groups: an informed minority (the woodcutters), and an uninformed majority (the trees). At the start of the game, each player is secretly assigned a role affiliated with one of these teams. The game has two alternating phases: first, a night role, during which those with night killing powers may covertly kill other players, and second, a day role, in which surviving players debate the identities of players and vote to eliminate a suspect. The game continues until a faction achieves its win condition; for the tress, this means eliminating all wood cutters, while for woodcutters, this usually means reaching numerical parity with the tree and eliminating any rival evil groups"
            speech_output = rulles + " These are the rules. So Let's start the game. How many players are playing ?"
        else:
            speech_output = "So Let's start the game. How many players are playing ?"
    reprompt_text = "I don't know if you heard me, Please tell me do you want to here rules?"
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

        
def get_total_players_response(intent,session):
    session_attributes = session['attributes']
    card_title = "Total Players Count"
    n = ""
    if intent["slots"]["int"].get("value")!=None:
        n = intent["slots"]["int"].get("value")
    elif intent["slots"]["name"].get("value")!=None:
        n = intent["slots"]["name"].get("value") 
    if n.isdigit():
        n = int(n)
        session_attributes["state"] = 2
        session_attributes["no_of_players"] = n
        session_attributes["current_player"] = 0
        speech_output = "OK. Tell the name of first player"
    else:
        speech_output = "Sorry I am unable to catch that. Please tell me a valid number"
    reprompt_text = "You never responded to the first test message. Sending another one."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

        
def get_player_names_response(intent , session):
    session_attributes = session['attributes']
    card_title = "Getting Players Names"
    nam= intent ["slots"]["name"]["value"]
    session_attributes["players"].append(nam)
    session_attributes["current_player"]+=1
    speech_output="Ok got that.Tell me the name of next player"
    if session_attributes["current_player"] >= session_attributes["no_of_players"]:
        speech_output="I have got the names of all the players. So are you ready to continue the game?"
        p = []
        n = session_attributes["no_of_players"]
        p.append("Wood Cutter")
        p.append("ranger")
        p.append("arborist")
        while len(p)<n:
            p.append("Tree")
        random.shuffle(p)
        wi=p.index("Wood Cutter")
        session_attributes["woodcutter"]=session_attributes["players"][wi]
        session_attributes["roles"] = p[::]
        session_attributes["state"] = 3
        session_attributes["current_player"] = 0
    reprompt_text = "You never responded to the first test message. Sending another one."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def give_role_response(intent,session):
    session_attributes = session['attributes']
    card_title = "Your Role: "
    speech_output = "Role"
    i = session_attributes["current_player"]
    if intent["slots"]["yn"].get("value")==None:
        speech_output = "Sorry I am unable to catch that please respond in yes or no."
    elif session_attributes["state"] == 3:
        if intent["slots"]["yn"].get("value") == "yes":
            if i == session_attributes["no_of_players"]:
                speech_output = "I have assigned roles to all the players. So starting the game. Are you ready?"
                session_attributes["state"] = 5
            else:
                speech_output = "So assigning the role to " + session_attributes["players"][i] +" .Tell me yes when smartphone is in your hand?"
                session_attributes["state"] = 4
        else:
            speech_output = "Get ready I am waiting for your yes."
    else:
        if intent["slots"]["yn"].get("value") == "yes":
            speech_output = "Your role is displayed above. Tell me yes when you have seen it."
            session_attributes["current_player"]+=1
            session_attributes["state"] = 3
            card_title += session_attributes["roles"][i] 
        else:
            speech_output = "Get ready I am waiting for your yes."
    reprompt_text = "Waiting for your response."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def night_time_start(intent,session):
    session_attributes = session['attributes']
    card_title = "Night Time"
    if intent["slots"]["yn"].get("value")==None:
        speech_output = "Sorry I am unable to catch that please respond in yes or no."
    else :
        if intent["slots"]["yn"].get("value") == "yes":
            speech_output = "Night has started . I request all the players to take position and go to sleep. Tell me yes when you are ready."
            session_attributes["state"] = 6
        else:
            speech_output = "Waiting for your response in yes"
    reprompt_text = "You never responded to the first test message. Sending another one."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def call_mafia(intent,session):
    session_attributes = session['attributes']
    card_title = "Calling Woodcutter"
    speech_output = "hello"
    if session_attributes["state"] == 6:
        if intent["slots"]["yn"].get("value")==None or  intent["slots"]["yn"].get("value") == "no":
            speech_output = "Please get ready I am waiting for your yes"
        else:
            speech_output = " Woodcutter Wakeup and type the name of the tree you want to cut down"
            session_attributes["state"] = 7
    else:
        if intent["slots"]["name"].get("value") == None or intent["slots"]["name"].get("value") not in session_attributes["players"] :
            speech_output = "Invalid playername"
            card_title = "invalid playername"
        else:
            session_attributes["mafia"] = intent["slots"]["name"].get("value")
            card_title = "Successful"
            speech_output = "I request woodcutter to take back his/her position.  Woodcutter go to Sleep.  I request arborist to come and play his role. Enter the name of tree you want to protect"
            session_attributes["state"] = 8
    reprompt_text = "You never responded to the first test message. Sending another one."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def call_arborist(intent,session):
    session_attributes = session['attributes']
    card_title = "Calling Arborist"
    speech_output = "hello"
    if intent["slots"]["name"].get("value") == None or intent["slots"]["name"].get("value") not in session_attributes["players"] :
        speech_output = "Invalid playername"
        card_title = "invalid playername"
    else:
        if "arborist" not in session_attributes["roles"]:
            session_attributes["arborist"] =""
            card_title="arborist you are dead"
        else:
            session_attributes["arborist"] = intent["slots"]["name"].get("value")
            card_title = "Successful"
        speech_output = "I request arborist to take back his/her position.  Arborist go to Sleep.  I request ranger to come and play his role. Enter the name of tree you suspect to be a the disguised woodcutter"
        session_attributes["state"] = 9
    reprompt_text = "You never responded to the first test message. Sending another one."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def call_ranger(intent,session):
    session_attributes = session['attributes']
    card_title = "Result of your guess : "
    speech_output = "hello"
    if intent["slots"]["name"].get("value") == None or intent["slots"]["name"].get("value") not in session_attributes["players"] :
        speech_output = "Invalid playername"
        card_title = "invalid playername"
    else:
        if "ranger" not in session_attributes["roles"]:
            card_title+="ranger you are dead"
        elif (session_attributes["woodcutter"] == intent["slots"]["name"].get("value")):
            card_title+= "Yeah you caught him"
        else:
            card_title += "No he is not"
        speech_output = "I request ranger to take back his/her position.  Ranger go to sleep. Everyone wake up. Tell me yes when you all are ready."
        session_attributes["state"] = 10
    reprompt_text = "You never responded to the first test message. Sending another one."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def make_verdict(intent,session):
    session_attributes = session['attributes']
    card_title = "Verdict Time"
    speech_output = "hello"
    if intent["slots"]["yn"].get("value")==None or  intent["slots"]["yn"].get("value") == "no":
        speech_output = "Please get ready I am waiting for your yes"
    else:
        speech_output="So I am giving my verdict."
        if session_attributes["mafia"]!=session_attributes["arborist"]:
            speech_output+="Sorry! You have lost one of the trees."+session_attributes["mafia"]+" is dead. Arborist could not save him from being cut down by the cunning woodcutter"
            ki=session_attributes["players"].index(session_attributes["mafia"])
            session_attributes["players"].pop(ki)
            session_attributes["roles"].pop(ki)
            session_attributes["no_of_players"]-=1
        else:
            speech_output+="Mafia tried to cut down a tree but arborist saved it."
        speech_output+="Now discussion begins. When you are ready for voting tell me yes."
        session_attributes["state"] = 11
        session_attributes["current_player"]=0
    reprompt_text = "You never responded to the first test message. Sending another one."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def start_voting(intent,session):
    session_attributes = session['attributes']
    card_title = "Voting Starts"
    if intent["slots"]["yn"].get("value")==None:
        speech_output = "Sorry I am unable to catch that please respond in yes or no."
    else :
        if intent["slots"]["yn"].get("value") == "yes":
            session_attributes["state"] = 12
            speech_output = "Ok! Lets start the voting. "+session_attributes["players"][0]+ " come forward and tell the name of the tree you suspect to be the woodcutter."
            session_attributes["current_player"]=1
            session_attributes["votes"]=[0 for i in range(session_attributes["no_of_players"])]
        else:
            speech_output = "Waiting for your yes."
    reprompt_text = "You never responded to the first test message. Sending another one."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def take_votes(intent,session):
    session_attributes = session['attributes']
    card_title = "Taking Votes"
    i = session_attributes["current_player"]
    if intent["slots"]["name"].get("value")==None or intent["slots"]["name"].get("value") not in session_attributes["players"]:
        speech_output = "Sorry invalid name."
    else:
        speech_output = "I have noted your vote. You can go back to your position."
        idx=session_attributes["players"].index(intent["slots"]["name"].get("value"))
        session_attributes["votes"][idx]+=1
        if i == session_attributes["no_of_players"]:
            speech_output += "I have taken everyone's votes and will announce the results of voting. Are you ready?"
            session_attributes["state"] = 13
        else:
            speech_output += "I request " + session_attributes["players"][i] + " to come forward and tell the name of the tree he suspects. "
            session_attributes["current_player"]+=1
    reprompt_text = "Waiting for your response."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
        
def voting_verdict(intent,session):
    session_attributes = session['attributes']
    card_title = "Voting Verdict"
    mx=max(session_attributes["votes"])
    idx=session_attributes["votes"].index(mx)
    if intent["slots"]["yn"].get("value")==None:
        speech_output="Sorry coud not get that"
    elif intent["slots"]["yn"].get("value") == "yes":
        speech_output="Ok. So according to your votes, " + session_attributes["players"][idx] + " has been killed. "
        if session_attributes["players"][idx]==session_attributes["woodcutter"]:
            speech_output+="You have guessed the right woodcutter. The woodcutter has failed and the forest has been saved. Game ends."
            session_attributes["state"]=14
        else:
            session_attributes["players"].pop(idx)
            session_attributes["roles"].pop(idx)
            session_attributes["no_of_players"]-=1
            if session_attributes["no_of_players"]<=3:
                speech_output+="Since only 3 or less trees are left in the forest, the woodcutter has successfully accomplished his mission and has won. Game ends."
                session_attributes["state"]=14
            else:
                speech_output+="You have guessed the wrong tree to be disguised as woodcutter. Game will continue. Tell me yes when you are ready."
                session_attributes["state"]=5
    else:
        speech_output="Waiting for your yes"
    reprompt_text = "Waiting for your response."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))



def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you Playing Green Mafia " \
                    "Have a nice day! "
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    session["state"] = 0
    session["current_player"] = 0
    session["no_of_players"] = 0
    session["players"] = []
    session["roles"] = []
    

def on_launch(launch_request, session):
    return get_welcome_response()


def on_intent(intent_request, session):
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']
    if intent_name == "FirstIntent":
        if session["attributes"]["state"] == 0:
            #return call_mafia(intent,session)
            return get_rules_response(intent , session)
        elif session["attributes"]["state"] == 1:
            return get_total_players_response(intent , session)
        elif session["attributes"]["state"] == 2:
            return get_player_names_response(intent , session)
        elif session["attributes"]["state"] == 3 or session["attributes"]["state"] == 4 :
            return give_role_response(intent,session)
        elif session["attributes"]["state"] == 5:
            return night_time_start(intent,session)
        elif session["attributes"]["state"]==6 or session["attributes"]["state"]==7:
            return call_mafia(intent,session)
        elif session["attributes"]["state"]==8:
            return call_arborist(intent,session)
        elif session["attributes"]["state"]==9:
            return call_ranger(intent,session)
        elif session["attributes"]["state"]==10:
            return make_verdict(intent,session)
        elif session["attributes"]["state"]==11:
            return start_voting(intent,session)
        elif session["attributes"]["state"]==12:
            return take_votes(intent,session)
        elif session["attributes"]["state"]==13:
            return voting_verdict(intent,session)
        else:
            return handle_session_end_request()
    elif intent_name == "AMAZON.HelpIntent":
        return get_welcome_response()
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_session_end_request()
    else:
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):

    # if (event['session']['application']['applicationId'] !=
    #         "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        #return on_session_ended(event['request'], event['session'])
        return handle_session_end_request()
