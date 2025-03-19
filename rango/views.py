from django.shortcuts import render
from django.http import HttpResponse
from rango.forms import *
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from datetime import datetime

@login_required
def restricted(request):
    return render(request, 'rango/restricted.html')

# Use the login_required() decorator to ensure only those logged in can
# access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)
    # Take the user back to the homepage.
    return redirect(reverse('rango:index'))

def index(request):

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    

    visitor_cookie_handler(request)

    response = render(request, 'rango/tNindex.html', context=context_dict)

    return response

def tNindex(request):
    courses = Courses.objects.all()
    notes = Note.objects.all()

    return render(request, 'rango/tNindex.html', {'courses' : courses, 'notes':notes})

def tNcourse(request):
    courses = Courses.objects.all()
    
    return render(request, 'rango/tNcourse.html', {'courses': courses})

def tNlogin(request):
     # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

       
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return redirect(reverse('rango:tNindex'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your ThinkNote account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
    
        return render(request, 'rango/tNlogin.html')
   

def tNnote(request):
    return render(request, 'rango/tNnote.html')

def tNregister(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        students_form = StudentForm(request.POST)

        if user_form.is_valid() and students_form.is_valid():
            # Save the User data
            user = user_form.save(commit=False)
            password = user_form.cleaned_data['password']
            
            user.set_password(password)  
            user.save()

            # Save the Students data
            student = students_form.save(commit=False)
            student.user = user  
            student.save()

            registered = True
            return redirect('login')  # Redirect to the login page after successful registration
       
        else:
            print(user_form.errors, students_form.errors)  # Print form errors for debugging
    else:
        user_form = UserForm()
        students_form = StudentForm()

    return render(request,
                  'rango/tNregister.html',
                  context={'user_form': user_form,
                           'students_form': students_form,
                           'registered': registered})
def tNsearch(request):
    return render(request, 'rango/tNsearch.html')

@login_required
def tNupload(request):
    if request.method == 'POST':
        form = NoteForm(request.POST, request.FILES)  # Include request.FILES for file uploads
        if form.is_valid():

            form.save(commit = False) 
            form.UserID = request.user
            form.save()
            return redirect('success_url')  
        
    else:
        form = NoteForm()  # Render an empty form for GET requests

    #return render(request, 'upload_note.html', {'form': form})
    return render(request, 'rango/tNupload.html', {'form': form})

def tNuser(request):
    notes = Note.objects.all()

    return render(request, 'rango/tNuser.html', {'notes':notes})



def about(request):
    context_dict = {}
    visitor_cookie_handler(request)
    context_dict['visits'] = request.session['visits']
    return render(request, 'rango/about.html', context=context_dict)



def register(request):
    # A boolean value for telling the template
    # whether the registration was successful.
    # Set to False initially. Code changes value to
    # True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves,
            # we set commit=False. This delays saving the model
            # until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and
            # put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to indicate that the template
            # registration was successful.
            registered = True
        else:
            # Invalid form or forms - mistakes or something else?
            # Print problems to the terminal.
            print(user_form.errors, profile_form.errors)
    else:
        # Not a HTTP POST, so we render our form using two ModelForm instances.
        # These forms will be blank, ready for user input.
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
                  'rango/register.html',
                  context={'user_form': user_form,
                           'profile_form': profile_form,
                           'registered': registered})

def user_login(request):
    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        
        user = authenticate(username=username, password=password)

       
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print(f"Invalid login details: {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
    
        return render(request, 'rango/login.html')

# A helper method
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val

def visitor_cookie_handler(request):
    # Get the number of visits from the server-side cookie
    visits = int(get_server_side_cookie(request, 'visits', '1'))

    # Get the last visit time from the server-side cookie or set it to the current time if it doesn't exist
    last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

    # If it's been more than a day since the last visit...
    if (datetime.now() - last_visit_time).days > 0:
        visits = visits + 1
        # Update the last visit cookie with the current time
        request.session['last_visit'] = str(datetime.now())
    else:
        # Keep the last visit cookie unchanged
        request.session['last_visit'] = last_visit_cookie

    # Update/set the visits cookie
    request.session['visits'] = visits
