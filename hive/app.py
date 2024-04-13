from flask import Flask
import flask
import json
from flask import jsonify, request
import requests
import google.generativeai as genai
import os

app = Flask(__name__)

with open('config.json') as f:
    app_config = json.load(f)


seatgeek_secret = app_config["seatgeek_secret"]
seatgeek_id = app_config["seatgeek_id"]

# Set up gemini models
gemini_key = app_config["gemini_key"]
genai.configure(api_key=gemini_key)

mixed_query_system_prompt = ("""T

""")
mixed_query_model = genai.GenerativeModel('gemini-1.5-pro-latest', system_instruction=mixed_query_system_prompt)

free_activity_model = genai.GenerativeModel('gemini-1.5-pro-latest')

processing_query_system_prompt = ("""Today's date is Sunday 4/14/2024.
In the following query by the user, do they mention anything specifying any of the following fields: when the event is, where the event they want to go to is, or what type of event they want to go to? Give response in the following format and do not send anything else: If not, just send "No". 
If so, send "[start of when (Default:today) yyyy-mm-dd], [end of when (Default:today)  yyyy-mm-dd], [where (Default:Detroit, MI) city, state], [event type]. Don't send the response with brackets and send the default value if the user doesn't specify the field. """)
query_processing_model = genai.GenerativeModel('gemini-1.5-pro-latest', system_instruction=processing_query_system_prompt)

general_activities = [
    "Go for a walk or hike in a local park or nature reserve",
    "Have a picnic in a park or by the beach",
    "Visit a museum or art gallery",
    "Explore a new neighborhood or part of town",
    "Go window shopping at local stores",
    "Have a movie marathon at home",
    "Play board games or card games",
    "Try a new recipe together",
    "Have a potluck dinner",
    "Go stargazing in a dark spot",
    "Volunteer at a local charity or community organization",
    "Attend a free concert or festival",
    "Visit a farmers market",
    "Have a bonfire or barbecue",
    "Go swimming at a local pool or beach",
    "Play sports together",
    "Go bowling or play mini golf",
    "Visit a local library",
    "Take a bike ride",
    "Go rollerblading or skateboarding",
    "Have a game night",
    "Do a puzzle together",
    "Read books together and discuss them",
    "Start a book club",
    "Learn a new skill together, like painting or knitting",
    "Take a dance class",
    "Go to a karaoke bar",
    "Have a spa day at home",
    "Do a DIY project together",
    "Go geocaching",
    "Play frisbee or catch",
    "People-watch in a busy area",
    "Visit a local historical landmark",
    "Go bird watching",
    "Have a philosophical discussion",
    "Take personality quizzes online",
    "Draw or paint together",
    "Write stories or poems together",
    "Learn a new language together",
    "Play charades or Pictionary",
    "Go to a comedy show",
    "Take a photography walk",
    "Visit an animal shelter",
    "Meditate or do yoga together",
    "Have a themed movie night",
    "Play video games together",
    "Go to an open mic night",
    "Volunteer at a soup kitchen",
    "Organize a clothing swap",
    "Have a game night with classic board games" 
]


interests = {
    "OJ": ["Football", "Gambling (legally)", "Driving", "Gardening", "country music"],
    "Ammad": ["Cooking", "Knitting", "EDM", "Fishing", "Biking"]
}

@app.route('/api')
def api():
    user_query = ""
    # Query SeatGeek API for events
    geoip= request.args.get('geoip')
    
    sg_events = get_seatgeek_results(user_query, geoip)


def get_seatgeek_events(datetime_min, datetime_max, geoip, city=None, state= None, query=None ):
    url = ""
    if query:
        if state and city:
            url = f'https://api.seatgeek.com/2/events?q={query}&datetime_utc.gte={datetime_min}&datetime_utc.lte={datetime_max}&venue.state={state}&venue.city={city}'
        else:
            url = f'https://api.seatgeek.com/2/events?q={query}&datetime_utc.gte={datetime_min}&datetime_utc.lte={datetime_max}'
    else:
        if state and city:
            url = f'https://api.seatgeek.com/2/events?geoip={geoip}&datetime_utc.gte={datetime_min}&datetime_utc.lte={datetime_max}&venue.state={state}&venue.city={city}'
        else:
            url = f'https://api.seatgeek.com/2/events?geoip={geoip}&datetime_utc.gte={datetime_min}&datetime_utc.lte={datetime_max}'
        
    events_response = requests.get(url) 
    if events_response.status_code == 200:
        data = events_response.json()
        return jsonify(data)
    else:
        return jsonify({'error': 'Failed to fetch data from SeatGeek API'}), events_response.status_code
        

# Convert user query into a simplified query for seatgeek
def get_seatgeek_results(query, geoip):
    prompt = query
    response = query_processing_model.generate_content(prompt)
    if response == "No": # User doesn't want a specific seatgeek query
        #TODO: Make current week 
        return get_seatgeek_events("2024-04-14", "2024-04-20", geoip, None)
    else:
        response= " " + response + " "
        segments = response.split(",")
        if len(segments) < 4:
            return get_seatgeek_events("2024-04-14", "2024-04-20", geoip, None)
        start_date = segments[0].strip()
        if not len(start_date): start_date = "2024-04-14"
        end_date = segments[1].strip()
        if not len(end_date): end_date = "2024-04-20"
        city = segments[2].strip()
        state= segments[3].strip()
        if len(segments) > 4:
            extra_info = segments[4].strip()
            extra_info = '+'.join(extra_info.split())
        
        return get_seatgeek_events(start_date, end_date, geoip, city=city, state=state, query=extra_info)
def generate_mixed_result(query, geoip): # Returns json
    event_response = get_seatgeek_results(query, geoip)

    # String of JSON of event data from query
    event_data = str(event_response.get_json())
    
    # Free events data 
    free_things_prompt = """List things to do for free in Ann Arbor today with no additional text"""
    free_activity_response = free_activity_model.generate_content(free_things_prompt)

    # Put calendar information and seat geek response into a singular prompt for context
    friend_free_times = []
    friend_interests = []
    gemini_input = ""
    delimiter = "**********"
    # Add user Free time
    gemini_input += delimiter
    gemini_input += str(interests["OJ"]) # User interests
    gemini_input += delimiter
    for free_time in friend_free_times: # Add friend free_times
        gemini_input += str(free_time)
        gemini_input += "----------"
    gemini_input += delimiter
    for interests in friend_interests: # Friend interests
        gemini_input += str(interests)
        gemini_input += "----------"
    gemini_input += delimiter
    gemini_input += event_data # Seat geek events
    gemini_input += delimiter
    gemini_input += free_activity_response # Free things to do around town
    gemini_input += delimiter
    gemini_input += general_activities # General things to do

    gemini_suggestion_text = mixed_query_model.generate_content(gemini_input)
    gemini_suggestions = json.loads(gemini_suggestion_text)
    return gemini_suggestions






#for the ids, pretty sure its just their primary email for the calendar
def get_free_busy_info(timeMin, timeMax, ids, timeZone='UTC', groupExpansionMax=100, calendarExpansionMax=50):
    url = 'https://www.googleapis.com/calendar/v3/freeBusy'
    headers = {'Content-Type': 'application/json'}
    data = {
        "timeMin": timeMin,
        "timeMax": timeMax,
        "timeZone": timeZone,
        "groupExpansionMax": groupExpansionMax,
        "calendarExpansionMax": calendarExpansionMax,
        "items": [{"id": id} for id in ids]
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

@app.route('/')
def index():
    context = {'name': "OJ Simpson"}
    return flask.render_template("index.html", **context)

if __name__ == '__main__':
    app.run(debug=True)