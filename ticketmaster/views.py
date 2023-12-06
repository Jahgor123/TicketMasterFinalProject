from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
# Make sure to install requests using 'pip install requests' on your terminal, otherwise 'requests' will not work
import requests
from datetime import datetime
from django.contrib import messages

from ticketmaster.models import Ticket
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm


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
        event_tickets = get_tickets(search_term, search_city)
        print(event_tickets)

        # If the request to fetch data from randomuser was unsuccessful or returned None
        if event_tickets is None:
            # Set up an error message using Django's message utility to inform the user
            messages.info(request, 'The server encountered an issue while fetching data. Please try again later.')
            # redirect user to the index page
            return redirect('index')

        else:

            # print the response for testing purpose (open "Run" at the bottom to see what is printed)
            # print(eventTickets.encode('utf-8'))
            # Store each event information in a variable
            events = event_tickets['_embedded']['events']

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
                venue_address = event['_embedded']['venues'][0]['address']['line1']
                event_date = event['dates']['start']['localDate']
                event_formal_start_time = event['dates']['start']['localTime']
                # event_ticket_link = event['outlets'][0]['url']
                event_price = 60  # default value for ticket prices if they don't exist
                if 'priceRanges' in event:
                    if event['priceRanges']:
                        event_price = event['priceRanges'][0]['min']

                event_ticket_link = event['url']
                # if 'outlets' in event:
                #     if event['outlets']:
                #         event_ticket_link = event['url']
                # else:
                #     event_ticket_link = event['_links']['self']['href']

                # Format the registration date from "2004-03-12T17:05:44.193Z" to "2004"
                # Extract the first 10 characters to get the date portion, then convert to a datetime object
                # date_object = datetime.strptime(registration_date[:10], "%Y-%m-%d")

                # Format the date object to a more readable format, e.g., "Sat Nov 03 2023"
                # registration_date = date_object.strftime("%a %b %d %Y")

                # Create a new dictionary to store user details
                event_details = {
                    'eventName': event_name,
                    'image': image,
                    'Address': venue_address,
                    'Date': event_date,
                    'Time': event_formal_start_time,
                    'event_ticket_link': event_ticket_link,
                    'price': event_price
                }

                # Append the user details dictionary to the user_list
                event_list.append(event_details)
                # store tickets into database for requirement 3 lol
                Ticket.objects.create(Name=event_name, quantity=1, price=event_price)

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


def store_tickets_to_database(request, ticket):
    context = {}  # empty dictionary
    for ticket in ticket:
        context = ticket

    return render(request, 'cart.html', context)


def clear_tickets_from_database(request, ticket):
    clear_all_tickets = Ticket.objects.all().delete()
    return


# To implement wish_list I can create all the attributes needed and store them in the ticket
# then each person can have a wishlist id which stores an array of tickets

def add_wish_list(request, context):
    event_list = []
    # for something in something
    #
    return render(request, 'logInPage.html')



def cart_pull(request):
    # open cart / view
    # user presses add to cart (needs quantity)
    # asks for the quantity (drop down limit 10 tickets or text field)
    # data is saved to the structure
    # user has a ticket cart field
    # if authentic then cart icon appears (top right) and once pressed
    # comes to this method which will take you to cart.html and load all your tickets

    return render(request, 'cart.html')


def register_view(request):
    # This function renders the registration form page and create a new user based on the form data
    if request.method == 'POST':
        # We use Django's UserCreationForm which is a model created by Django to create a new user.
        # UserCreationForm has three fields by default: username (from the user model), password1, and password2.
        form = UserCreationForm(request.POST)
        # check whether it's valid: for example it verifies that password1 and password2 match
        if form.is_valid():
            form.save()
            # redirect the user to login page so that after registration the user can enter the credentials
            return redirect('login')
    else:
        # Create an empty instance of Django's UserCreationForm to generate the necessary html on the template.
        form = UserCreationForm()
    # return render(request, 'accounts/register.html', {'form': form})
    return render(request, 'register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('Username')
        password = request.POST.get('Password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # User was authenticated
            # redirect to the index page upon successful login

            # login in the user
            login(request, user)
            return redirect('index')
        else:
            # User was not authenticated
            form = AuthenticationForm()
            return render(request, 'noUserFound.html')

    return render(request, 'logInPage.html')


def logout_view(request):
    # Log out user
    logout(request)
    # Redirect to index with user logged out
    return redirect('index')

    # # to restrict user from reaching this page if not login
    # @login_required(login_url='login')
    # def my_view(request):
    #     Tickets = Ticket.objects.filter(user=request.user)
    #     context = {'tickets':'tickets'}

