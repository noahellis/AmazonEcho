from __future__ import print_function

ingredients = ['2 table spoons peanut butter', '1 table spoon jelly', 'two slices of bread']
directions = ['spread peanut butter on one side of bread', 'spread jelly on one side of other piece of bread',
              'press the pieces of bread together so the peanut butter and jelly sides are together', 'enjoy']
direction_index = 0
ingredient_index = 0
def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
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
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])


def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return get_welcome_response()


def on_intent(intent_request, session):


    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']



    if intent_name == "ReadNextIngredientIntent":
        return read_next_ingredient(intent, session)
    elif intent_name == "ReadAllIngredientsIntent":
        return read_all_ingredients(intent, session)
    elif intent_name == "ReadNextDirectionIntent":
        return read_next_direction(intent, session)
    elif intent_name == "ReadPreviousDirectionIntent":
        return read_previous_direction(intent, session)
    elif intent_name == "ReadPreviousIngredientIntent":
        return read_previous_ingredient(intent, session)
    # elif intent_name == "HowMuchIntent":
    #     return how_much_ingredient(intent, session, )
    elif intent_name == "EndIntent":
        return handle_session_end_request()
    # else:
    #     raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here

# --------------- Functions that control the skill's behavior ------------------


def get_welcome_response():
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """

    session_attributes = {}
    card_title = "Welcome"
    speech_output = "Welcome to Noah's Recipe Reader.  " \
                    "With this skill, you can hear ingredients or directions. "\
                    "You can ask for the next, previous or all ingredients, or get directions one at a time.  "\

    reprompt_text = None

    should_end_session = True
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Session Ended"
    speech_output = "Thank you for trying Noah's Recipe Reader. " \
                    "I hope you enjoyed this presentation of Noah's Amazon Echo Recipe Reader"\

    reprompt_text = None
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def read_next_ingredient(intent, session):

    card_title = intent['name']
    session_attributes = {}
    should_end_session = True

    global ingredient_index
    reprompt_text = None

    if ingredient_index == 0:
        speech_output = "The first ingredient is " + ingredients[0]
        ingredient_index += 1
    elif ingredient_index <= (len(ingredients) - 1):
        speech_output = "The next ingredient is " + ingredients[ingredient_index]
        ingredient_index += 1
    elif ingredient_index == (len(ingredients) - 1):
        speech_output = "The final ingredient is " + ingredients[ingredient_index]
    elif ingredient_index > (len(ingredients) - 1):
        ingredient_index = (len(ingredients) - 1)
        speech_output = "The final ingredient is " + ingredients[ingredient_index]
    else:
        speech_output = ingredients[ingredient_index]
        ingredient_index += 1
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def read_next_direction(intent, session):

    card_title = intent['name']
    session_attributes = {}
    should_end_session = True
    global direction_index
    reprompt_text = None

    if direction_index == 0:
        speech_output = "The first direction is " + directions[0]
        direction_index += 1
    elif direction_index <= (len(directions) - 1):
        speech_output = "The next direction is " + directions[direction_index]
        direction_index += 1
    elif direction_index == (len(directions) - 1):
        speech_output = "The final direction is " + directions[direction_index]
    elif direction_index > (len(directions) - 1):
        direction_index = (len(directions) - 1)
        speech_output = "The final direction is " + directions[direction_index]
    else:
        speech_output = directions[direction_index]
        direction_index += 1
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def read_all_ingredients(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = True
    reprompt_text = None
    speech_output_ingredients = []
    for i in ingredients:
        speech_output_ingredients.append(i)
    speech_output = "Here are all the ingredients, " + ','.join(speech_output_ingredients)
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def read_previous_ingredient(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = True
    reprompt_text = None
    global ingredient_index
    if ingredient_index == 0:
        speech_output= "The first ingredient is " + ingredients[0]
    elif ingredient_index < 0:
        ingredient_index = 0
        speech_output = "The first ingredient is " + ingredients[0]
    elif ingredient_index > 0 & ingredient_index <= len(ingredients):
        speech_output = "The previous ingredient was " + ingredients[ingredient_index - 1]
    else:
        speech_output = "The previous ingredient was " + ingredients[ingredient_index - 1]
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))

def read_previous_direction(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = True
    reprompt_text = None
    global direction_index
    if direction_index == 0:
        speech_output = "The first direction is " + directions[0]
    elif direction_index < 0:
        ingredient_index = 0
        speech_output = "The first direction is " + directions[0]
    elif direction_index > 0 & direction_index <= len(directions):
        speech_output = "The previous direction was " + directions[direction_index - 1]
    else:
        speech_output = "The previous direction was " + directions[direction_index - 1]

    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))
def how_much_ingredient(intent, session):
    intent_value = intent['slots']['value']
    card_title = intent['name']
    session_attributes = {}
    should_end_session = True
    reprompt_text = None
    if any(intent_value in ingredients):
        speech_output = "This recipe has " + intent_value
    else:
        speech_output = "This ingredient is not in the recipe"
    return build_response(session_attributes, build_speechlet_response(
		    card_title, speech_output, reprompt_text, should_end_session))
# --------------- Helpers that build all of the responses ----------------------


def build_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
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

