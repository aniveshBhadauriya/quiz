
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    print("===========>>"*10)
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):

    # print("===================="*10)

    if not current_question_id:
        return False , "No Current Question"
    
    session[current_question_id] = answer
    session.save()
    
    '''
    Validates and stores the answer for the current question to django session.
    '''
    return True, ""


def get_next_question(current_question_id):
    
    if not current_question_id:

        return PYTHON_QUESTION_LIST[0] , 0
    
    if current_question_id > len(PYTHON_QUESTION_LIST):
        return 'All Questions are completed ! Thankyou ' , None
    
    return PYTHON_QUESTION_LIST[current_question_id+1] , current_question_id+1    

    # return "dummy question", -1


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    c=0
    for i,v in session.items():
        if BOT_WELCOME_MESSAGE[i]['answer'] == v:
            c+=1
    
    l = str(len(session.keys()))
    c = str(c)

    
    return c+'/'+l
