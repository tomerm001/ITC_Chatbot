"""
This is the template server side for ChatBot
"""
from bottle import route, run, template, static_file, request
import json
from urllib.request import urlopen


# Global variable for holding msg info
analyze = {}
analyze['firstresponse'] = False


@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg')

    user_message = main_analyze(user_message)

    return json.dumps({"animation": "inlove", "msg": user_message})


@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7070)



# ANALYZE MSG SECTION


def main_analyze(msg):

    global analyze

    # split message into list
    msg_list = msg.lower().split()


    if(not(analyze['firstresponse'])):
        analyze['name'] = msg_list[0]
        analyze['firstresponse'] = True
        return "Hi {0}, it is nice to meet you.".format(analyze['name'])

    if(check_swearwords(msg_list)):
        return "Yo, next insult and you are dead!!"

    if(check_word(msg_list,"weather")):
        return get_weather_query("tel aviv israel")

    else:
        return "Sorry, I don't know."


# check if insults in message
def check_swearwords (input_list):

    insult_found = False

    insults = ('idiot', 'fuck')

    if any(x in insults for x in input_list):
        insult_found = True

    return  insult_found

#check if word in list
def check_word (input_list, word):

    word_found = False

    insults = ('idiot', 'fuck')

    for x in input_list:
        if(x == word):
            word_found = True

    return  word_found

# call in case exact city country is unknown
def get_weather_query(search):

    key = "1459f7ce080b9446"

    search = str(search)
    search = search.replace(" ", "%20")

    f = urlopen('http://api.wunderground.com/api/1459f7ce080b9446/geolookup/forecast/q/{0}.json'.format(search))

    json_string = f.read()
    parsed_json = json.loads(json_string.decode("utf-8"))

    current_weather = parsed_json["forecast"]["txt_forecast"]["forecastday"][0]['fcttext']

    print(current_weather)

    f.close()

    return current_weather

# weather API if location syntax is known
def get_weather(country, city):

    key= "1459f7ce080b9446"

    f = urlopen('http://api.wunderground.com/api/1459f7ce080b9446/forecast/q/{0}/{1}.json'.format(country, city))

    # Code for current conditions
    # f = urlopen('http://api.wunderground.com/api/1459f7ce080b9446/conditions/q/Israel/Jerusalem.json')

    json_string = f.read()
    parsed_json = json.loads(json_string.decode("utf-8"))

    # print(parsed_json)
    current_weather = parsed_json["forecast"]["txt_forecast"]["forecastday"][0]['fcttext']

    print(current_weather)

    f.close()

    return current_weather

# Serch for a city or country and get options
def get_city_country(query_text):

    f = urlopen('http://autocomplete.wunderground.com/aq?query={0}'.format(query_text))
    json_string = f.read()
    parsed_json = json.loads(json_string.decode("utf-8"))

    city = parsed_json
    print(city)


if __name__ == '__main__':
    main()
