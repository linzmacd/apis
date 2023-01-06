
from flask import Flask, render_template, request

from pprint import pformat
import os
import requests


app = Flask(__name__)
app.secret_key = 'SECRETSECRETSECRET'

# This configuration option makes the Flask interactive debugger
# more useful (you should remove this line in production though)
app.config['PRESERVE_CONTEXT_ON_EXCEPTION'] = True


API_KEY = os.environ['TICKETMASTER_KEY']


@app.route('/')
def homepage():
    """Show homepage."""

    return render_template('homepage.html')


@app.route('/afterparty')
def show_afterparty_form():
    """Show event search form"""

    return render_template('search-form.html')


@app.route('/afterparty/search')
def find_afterparties():
    """Search for afterparties on Eventbrite"""

    keyword = request.args.get('keyword', '')
    postalcode = request.args.get('zipcode', '')
    radius = request.args.get('radius', '')
    unit = request.args.get('unit', '')
    sort = request.args.get('sort', '')

    url = 'https://app.ticketmaster.com/discovery/v2/events'
    payload = {'apikey': API_KEY, 
               'keyword': keyword, 
               'postalCode': postalcode, 
               'radius': radius, 
               'unit': unit, 
               'sort': sort}

    res = requests.get(url, params=payload)


    # TODO: Make a request to the Event Search endpoint to search for events
    #
    # - Use form data from the user to populate any search parameters
    #
    # - Make sure to save the JSON data from the response to the `data`
    #   variable so that it can display on the page. This is useful for
    #   debugging purposes!
    #
    # - Replace the empty list in `events` with the list of events from your
    #   search results

    # data = {'Test': ['This is just some test data'],
    #         'page': {'totalElements': 1}}
    # events = [] 

    data = res.json()
    try:
        events = data['_embedded']['events']
    except:
        events = []
         
    return render_template('search-results.html',
                           pformat=pformat,
                           data=data,
                           results=events)


# ===========================================================================
# FURTHER STUDY
# ===========================================================================


@app.route('/event/<id>')
def get_event_details(id):
    """View the details of an event."""

    # TODO: Finish implementing this view function

    url = f'https://app.ticketmaster.com/discovery/v2/events/{id}'
    
    payload = {'apikey': API_KEY}

    res = requests.get(url, params=payload)
    data = res.json()
    
    name = data['name']
    # description =  
    image = data['images'][0]['url']
    url = data['url']
    start_date = data['dates']['start']['localDate']
    list_venues = data['_embedded']['venues']
    clean_list_venues = []
    for venue in list_venues:
        clean_list_venues += [venue['name']]
    # list_classification = 
    # venue['city']['name']

    return render_template('event-details.html',
                           name=name,
                           image=image, 
                           url=url,
                           start_date=start_date,
                           list_venues=clean_list_venues
                           )


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
