from django.shortcuts import render
import requests


def view_home(request):
    return render(request, 'ticketMasterKnockOff.html')

def view_results(request):
    response = requests.get('https://randomuser.me/api/')
    print(response.json())

    return render(request, 'ticketMasterKnockOff.html')

def get_random_users(results, gender):
    try:
    # Construct the URL with parameters
    url = "https://randomuser.me/api/"
    params = {
    "results": results,
    "gender": gender
    }
    response = requests.get(url, params=params)
    response.raise_for_status() # Raise an exception for 4xx and 5xx status codes
    data = response.json()
    return data
 except requests.exceptions.RequestException as e:
     print(f"Request failed: {e}")
     return None
random_female_users = get_random_users(results=5, gender="female")
if random_female_users:
    # do something with the data




# Renders page with the response coming from API
 def index(request):
     # if the request method is a post
     if request.method == 'POST':
         # get the search term and location
         number_of_users = request.POST['number-of-users']
         gender = request.POST['gender’]
         # call get_random_users function() to get the data from the API
         random_female_users = get_random_users(number_of_users, gender)
         # If the request to fetch data from randomuser was unsuccessful or returned None
         if random_female_users:
         # Store each user's information in a variable
             users = random_female_users['results’]
         # Create a context dictionary send the data to 'index.html' template
         context = {'users': users}
         return render(request, 'randomuser/index.html', context)


 # all other cases, just render the page without sending/passing any context to the template
 return render(request, 'randomuser/index.html')


