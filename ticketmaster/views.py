from django.shortcuts import render, redirect
# Make sure to install requests using 'pip install requests' on your terminal, otherwise 'requests' will not work
import requests
from datetime import datetime
from django.contrib import messages


def view_home(request):
    response = requests.get(
        'https://app.ticketmaster.com/discovery/v2/events.json?sort=date,asc&tIrapX2vWcsnEvoKHUkI25bDu0lTcYVT')
    print(response.json())

    return render(request, 'index.html')


def view_results(request):
    return render(request, 'index.html')


def index(request):
    # Initialize searchEvent with a default value
    # searchEvent = 'default_event_type'

    # if the request method is a post
    if request.method == 'POST':
        # get the search term and location

        # searchEvent = request.POST['pick-me']
        # searchState = request.POST['searchbar']

        search_term = request.POST.get('term')
        search_city = request.POST.get('city')

        print(search_term)
        print(search_city)

        # Check if searchState is empty
        if not search_term:
            # Set up an error message using Django's message utility to inform the user
            messages.info(request, 'Both event and state are required fields.')
            #     # redirect user to the index page
            return redirect('index')

        # Add code to handle or display the error_message as needed.

        # call get_tickets function() to get the data from the API
        eventTickets = get_tickets(search_term, search_city)
        print(eventTickets)

        # If the request to fetch data from randomuser was unsuccessful or returned None
        if eventTickets is None:
            # Set up an error message using Django's message utility to inform the user
            messages.info(request, 'The server encountered an issue while fetching data. Please try again later.')
            # redirect user to the index page
            return redirect('index')

        else:

            # print the response for testing purpose (open "Run" at the bottom to see what is printed)
            # print(eventTickets.encode('utf-8'))
            # Store each event information in a variable
            events = eventTickets['_embedded']['events']

            # Initialize an empty list to store user data
            event_list = []

            # Iterate through each user in the 'users' list coming from the api
            # Rather than directly passing the "users" array to the template,
            # the following approach allows server-side processing and formatting of specific data (e.g., date).
            # So, the template only needs to plug in the preprocessed information.
            for event in events:
                # Extract relevant information from the user dictionary
                event_name = event['name']
                image = event['images'][0]['url']
                venueAddress = event['_embedded']['venues'][0]['address']['line1']
                # venueAddress = event['_embedded']['venues'][0]['address']['line1']
                # venueCity = event['images'][0]['url']
                # email = user['email']
                # phone = user['phone']
                # picture = user['picture']['large']
                # registration_date = user['registered']['date']

                # Format the registration date from "2004-03-12T17:05:44.193Z" to "2004"
                # Extract the first 10 characters to get the date portion, then convert to a datetime object
                # date_object = datetime.strptime(registration_date[:10], "%Y-%m-%d")

                # Format the date object to a more readable format, e.g., "Sat Nov 03 2023"
                # registration_date = date_object.strftime("%a %b %d %Y")

                # Create a new dictionary to store user details
                event_details = {
                    'eventName': event_name,
                    'image': image,
                    'Address': venueAddress
                    # 'email': email,
                    # 'phone': phone,
                    # 'picture': picture,
                    # 'registration_date': registration_date
                }

                # Append the user details dictionary to the user_list
                event_list.append(event_details)

        # Create a context dictionary with the user_list and render the 'index.html' template
        context = {'events': event_list}
        return render(request, 'index.html', context)

        # all other cases, just render the page without sending/passing any context to the template

    return render(request, 'index.html')


def get_tickets(search_term, search_city):
    try:
        # API key
        api_key = "tIrapX2vWcsnEvoKHUkI25bDu0lTcYVT"
        # Construct the URL with parameters
        url = 'https://app.ticketmaster.com/discovery/v2/events.json&sort=date,asc'

        # The query parameters will be appended to the url such as https://randomuser.me/api/?results=5&gender=female&nat=us
        params = {
            "apikey": api_key,
            "keyword": search_term,
            "city": search_city
        }

        # Send a GET request to the specified URL with parameters
        response = requests.get(url, params=params)

        # Raise an exception for 4xx and 5xx status codes
        response.raise_for_status()

        # Parse the JSON data from the response
        data = response.json()

        # Return the parsed data
        return data
    except requests.exceptions.RequestException as e:
        # Handle request exceptions (e.g., network issues, timeouts)
        print(f"Request failed: {e}")

        # Return None to indicate failure
        return None


def logIn(request):
    return render(request, 'logInPage.html')


def cart(request):
    return render(request, 'cart.html')


def results(request):
    return render(request, 'results.html')
