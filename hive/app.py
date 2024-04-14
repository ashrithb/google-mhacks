from flask import Flask, redirect, url_for
import flask
import json
import logging
from flask import jsonify, request
import requests
import google.generativeai as genai
import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from flask_cors import CORS
import threading

app = Flask(__name__)
app.config['DEBUG'] = True

CORS(app)  # This applies CORS to all routes and all origins
logging.basicConfig(filename='flask.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

with open('config.json') as f:
    app_config = json.load(f)




# Set up gemini models
gemini_key = app_config["gemini_key"]
genai.configure(api_key=gemini_key)

mixed_query_system_prompt = ("""The prompts that follow will contain the following components delimited by 10 * in a row: the busy time slots given by the calendar of the user, interests of the user, busy time slots of the friends of the user where each friend's free times are delimited by 10 dashes in a row,   
interests of each friend delimited by 10 dashes in a row, paid events in json format generated from the user prompt, free events available in the users area, and a list of general activities.

Based on the availability of the user, generate a list of 10 potential group activities containing a set or subset of the friends in the group that are from events listed in the prompt. An example input will be pasted below for clarity and input should be expected in the specified format. The potential group activities will also outputed in a json in the format listed below.
Prompt:
(Free Time Slots of the User)
**********
(User interests)
**********
(Friend 1 Free Time Slots)
----------
(Friend 2 Free Time Slots)
**********
(Friend 1 Interests)
----------
(Friend 2 Interests)
**********
(Json of Paid Events)
**********
(Free Events in User Area)
**********
(List of General Activites)

Response:
{
events = [
    {
        "event_id": 1,
        "event_description": "(Title of event or activites)",
        "friends": "(Set of Friends involved in activity)"
        "time": (Date and Time of Event, Format: Day of Week, HH:MM; Example: Sunday, 10:30PM)
    },
    (up to 10 events)
]
}
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





from requests.auth import HTTPBasicAuth


def get_seatgeek_events(datetime_min, datetime_max, geoip, city=None, state= None, query=None ):
    url = ""
    # if query:
    #     if state and city:
    #         url = f'https://api.seatgeek.com/2/events?q={query}&datetime_utc.gte={datetime_min}&datetime_utc.lte={datetime_max}&venue.state={state}&venue.city={city} -u {seatgeek_id}:{seatgeek_secret}'
    #     else:
    #         url = f'https://api.seatgeek.com/2/events?q={query}&datetime_utc.gte={datetime_min}&datetime_utc.lte={datetime_max} -u {seatgeek_id}:{seatgeek_secret}'
    # else:
    #     if state and city:
    #         url = f'https://api.seatgeek.com/2/events?geoip={geoip}&datetime_utc.gte={datetime_min}&datetime_utc.lte={datetime_max}&venue.state={state}&venue.city={city} -u {seatgeek_id}:{seatgeek_secret}'
    #     else:
    #         url = f'https://api.seatgeek.com/2/events?geoip={geoip}&datetime_utc.gte={datetime_min}&datetime_utc.lte={datetime_max} -u {seatgeek_id}:{seatgeek_secret}'
    # print(url)
    # API endpoint
    url = "https://api.seatgeek.com/2/events"
    params = {
        "geoip": 'true',
        "datetime_utc.gte": datetime_min,
        "datetime_utc.lte": datetime_max
    }
    if city and state:
        params['venue.city'] = city
        params['venue.state'] = state
    if query:
        params['q'] = query
    events_response = requests.get(url) 
        # Authentication credentials

    password = app_config["seatgeek_secret"]
    username = app_config["seatgeek_id"]
    print(params, username, password)
    events_response = requests.get(url, params=params, auth=HTTPBasicAuth(username, password))
    print(events_response.json())
    if events_response.status_code == 200:
        data = events_response.json()
        print(data)
        return jsonify(data)
    else:
        print("Failed querying SeatGeek API")
        return jsonify({'error': 'Failed to fetch data from SeatGeek API'})
        

# Convert user query into a simplified query for seatgeek
def get_seatgeek_results(query, geoip):
    prompt = query
    # print("Prompt:" + prompt)
    response = query_processing_model.generate_content(prompt)
    if response.text == "No": # User doesn't want a specific seatgeek query
        #TODO: Make current week 
        print("Doing default Seatgeek API query")
        return get_seatgeek_events("2024-04-14", "2024-04-20", geoip, None)
    else:
        response= " " + response.text + " "
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
        print("Doing custom Seatgeek API query where city = " + city + ", state = " + state + ", extra info = " + extra_info)
        return get_seatgeek_events(start_date, end_date, geoip, city=city, state=state, query=extra_info)
def generate_mixed_result(query, geoip): # Returns json
    interests = {
        "OJ": ["Football", "Gambling (legally)", "Driving", "Gardening", "country music"],
        "Ammad": ["Cooking", "Knitting", "EDM", "Fishing", "Biking"]
    }
    event_response = get_seatgeek_results(query, geoip)
    print(event_response)

    # String of JSON of event data from query
    event_data = str(event_response)
    
    # Free events data 
    free_things_prompt = """List things to do for free in Ann Arbor today with no additional text"""
    free_activity_response = free_activity_model.generate_content(free_things_prompt)

    # Put calendar information and seat geek response into a singular prompt for context
    friend_free_times = []
    friend_interests = ["Playing Basketball", "Playing soccer", "Watching Football"],["Cooking", "Baking", "Watching Football"]
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
    gemini_input += free_activity_response.text # Free things to do around town
    gemini_input += delimiter
    gemini_input += str(general_activities) # General things to do

    #for our gcal service
    service = create_service()
    if service is None:
        print("Failed to create service")
        return None

    # Define the time range for the free/busy query
    #using a fixed range, but should replace this with the actual range you want to check
    timeMin = "2024-04-14T00:00:00Z"
    timeMax = "2024-04-20T23:59:59Z"  

    free_busy_info = get_free_busy_info(timeMin, timeMax)

    busy_times = free_busy_info.get('calendars', {}).values()

    for busyTime in busy_times:
        busyTimeStr= json.dumps(busyTime)
        friend_free_times.append(busyTimeStr)# this will input only the busy times, not free times

    # result['free_busy_info'] = free_busy_info
    # resultStr= json.dumps(result)
    # gemini_input += delimiter
    # gemini_input += resultStr

    gemini_suggestion_text = mixed_query_model.generate_content(gemini_input)
    print(gemini_input)
    try:
        gemini_suggestions = json.loads(gemini_suggestion_text)
        return gemini_suggestions
    
    except Exception as e:
        print("Invalid activity suggestions")
        return None
    

def create_service():
    SCOPES = 'https://www.googleapis.com/auth/calendar.readonly';
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json')
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json',SCOPES)
            print("Post Flow")
            creds = flow.run_local_server(port=5000)
        # Save the credentials for next ime
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        print("Attempted to creat service")
        service = build('calendar', 'v3', credentials=creds)
    except Exception as e:
        print(e)
        return None
    print("returned form creation")
    return service

#for the ids, pretty sure its just their primary email for the calendar
def get_free_busy_info(timeMin, timeMax, timeZone='UTC', groupExpansionMax=100, calendarExpansionMax=50):#not passing in ids anymore
    ids=["ashrithlb@gmail.com", "nadipellipratik@gmail.com", "aditkk29@gmail.com"]
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


######################################################################
#                       ROUTING                                      #                    
######################################################################
@app.route('/api')
def api():
    
    user_query = request.args.get('user_query')
    # Query SeatGeek API for events
    geoip= request.args.get('geoip')
    # [ user_query = "I want to golfing", geoip = "48.29234.32432"]
    
    suggestions = generate_mixed_result(user_query, geoip) # JSON of results
    print(suggestions)
    response = flask.jsonify({'results': suggestions})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/oauth2callback')
def oauth2callback():
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secrets.json',
        scopes=['https://www.googleapis.com/auth/calendar.readonly'],
        redirect_uri='http://localhost:8000/oauth2callback'  # This line must be updated
    )
    flow.fetch_token(authorization_response=request.url)
    # Proceed with fetching user data
    return 'Authentication successful!'

@app.route('/')
def index():
    context = {'name': "OJ Simpson"}
    response = flask.render_template("index.html", **context)
    # response.headers.add('Access-Control-Allow-Origin', '*')
    return response

def initiate_auth():
    SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
    creds = flow.run_local_server(port=2000)
    # Save credentials logic here
    
@app.route('/login')
def login():
    """Route to start the OAuth flow."""
    thread = threading.Thread(target=initiate_auth)
    thread.start()
    thread.join()
    return redirect(url_for('home'))
if __name__ == '__main__':
    app.run(debug=True)
