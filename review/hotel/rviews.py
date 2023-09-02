from django.shortcuts import render
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import get_object_or_404
def signup(request):
    if request.method == 'POST':
        username23 = request.POST.get('username')
        password23 = request.POST.get('password')
        email23 = request.POST.get('email')
        file = request.FILES.get('file')
        if not password23 or not email23 or not username23:
            return render(request, "form1.html", {'error': True})
        if User1.objects.filter(username1=username23).exists():
            return render(request, "form1.html", {'error1': True})
        if User1.objects.filter(email1=email23).exists():
            return render(request, "form1.html", {'error3': True})
        # Create the User object
        user = User.objects.create_user(username=username23, password=password23, email=email23)
        # Create the User1 object and associate it with the User object
        user1 = User1.objects.create(user=user, username1=username23, password1=password23, email1=email23, file=file)
        if file:
            file_name = file.name
            file_content = file.read()
            file = ContentFile(file_content, name=file_name)
            user1.file = file
        user1.save()
        # users=UserRegisterForm(request.POST)
        # print(users)
        return redirect('/login/')
    return render(request, "signup.html")
def login(request):
    if request.method == 'POST':
        dataemail = User.objects.all().values('email', 'password')
        dataemail1 = User1.objects.all().values('email1', 'password1','file')
        print("The email, password, and picture of all data respectively are:", dataemail)
        print("The email, password, and picture of all data respectively are:", dataemail1)
        password = request.POST.get('password')
        email = request.POST.get('email')
        print(email, password)
        
        if not password:
            return render(request, "login.html", {'error': True})
        elif not email:
            return render(request, "login.html", {'error1': True})
        # Find the matching email in the dataemail queryset
        matching_user = next((user for user in dataemail if user['email'] == email), None)
        if matching_user  and check_password(password, matching_user['password']):
            # Password matches
            user = User.objects.get(email=email)
            auth_login(request, user)
            return redirect('/home/')
        # Invalid credentials
        return render(request, "login.html", {'error2': True})
    return render(request, "login.html")
def home(request):
    user = request.user
    username = user.username
    email = user.email
    file = None
    # Retrieve the User1 instance for the current user
    user1 = User1.objects.filter(email1=email).first()
    hotel = Hotel.objects.all().values('id', 'hotel_name', 'city', 'state', 'description', 'price', 'image', 'video')
    if user1:
        file = user1.file
    # Update the hotel queryset to include the image and video URLs
    hotel = list(hotel)  # Convert the queryset to a list
    for item in hotel:
        if item['image']:
            item['image_url'] = settings.MEDIA_URL + str(item['image'])
        if item['video']:
            item['video_url'] = settings.MEDIA_URL + str(item['video'])
    context = {
        'email': email,
        'username': username,
        'file': file,
        'hotel': hotel
    }
    return render(request, "home.html", context)
def hotel(request):
    user = request.user
    username = user.username
    email = user.email
    if request.method == 'POST':
        hotel_name = request.POST.get('hotelName')
        city = request.POST.get('city')
        state = request.POST.get('state')
        price = request.POST.get('price')
        description = request.POST.get('description')
        image_file = request.FILES.get('image')
        video_file = request.FILES.get('video')
        user1 = Hotel.objects.create(username=username, email=email, hotel_name=hotel_name, city=city, state=state, price=price, description=description)
        if image_file:
            image_name = image_file.name
            image_content = image_file.read()
            image = ContentFile(image_content, name=image_name)
            user1.image = image
        if video_file:
            video_name = video_file.name
            video_content = video_file.read()
            video = ContentFile(video_content, name=video_name)
            user1.video = video
        user1.save()
        print("the user 1 is",user1)
        return redirect('/home/')
    return render(request, "create.html")
def hotel1(request):
    error = False
    review_saved = False
    review_exists = False
    context = {}  # Initialize context as an empty dictionary
    hotel = None

    if request.method == "POST":
        review_text1 = request.POST.get('review')
        hotel_id = request.POST.get('hotel_id')
        hotel_id1 = request.POST.get('number')
        hotel = get_object_or_404(Hotel, id=hotel_id)
        hotel_data = {
            'id': hotel.id,
            'hotel_name': hotel.hotel_name,
            'city': hotel.city,
            'state': hotel.state,
            'description': hotel.description,
            'price': hotel.price,
            'image': hotel.image,
            'video': hotel.video,
            'image_url': settings.MEDIA_URL + str(hotel.image),
            'video_url': settings.MEDIA_URL + str(hotel.video)
        }
        print("the hotel_data is", hotel_data)
        context = {
            'hotel': hotel_data
        }
        print("the context", context)
        review = HotelReview(
            hotel=hotel,
            username=request.user.username,
            email=request.user.email,
            review_text=review_text1
        )
        review.save()
        review_saved = True
    return render(request, "Hreview.html", {
        'error': error,
        'review_saved': review_saved,
        'review_exists': review_exists,
        'hotel': hotel,
        **context
    })
    
def reply(request):
    reply1 = None
    review_id1 = None
    error = False  # Initialize error flag
    if request.method == "POST":
        reply_text = request.POST.get('reply')  # Retrieve the reply from form data
        review_id1 = request.POST.get('review_id')

        if reply_text.strip() == "":
            error = True  # Set the error flag if the reply is empty
            # error(request, "Reply cannot be empty.")  # Add an error message
        else:
            try:
                review1 = HotelReview.objects.get(id=review_id1)
                print("the review are",review1)
                reply1 = Reply( review=review1,username=request.user.username, email=request.user.email, reply=reply_text)
                reply1.save()
                print(reply1)
            except HotelReview.DoesNotExist:
                pass  # Handle the case when the review does not exist
    replies = Reply.objects.filter(review__id=review_id1)  # Retrieve replies for a specific review
    print("the replies are",replies)
    return render(request, "Hreplay.html", {'reply': reply1, 'replies': replies, 'review_id': review_id1, 'error': error})
def r12(request):
    user = request.user
    username = user.username
    email = user.email
    hotel_id1 = request.POST.get('hotel_id')
    # Retrieve the review for the current user excluding None values
    review = HotelReview.objects.filter(
        hotel_id=hotel_id1,
        username=username,
        email=email,
        review_text__isnull=False
    ).values('id','hotel_id', 'username', 'email', 'review_text')
    print(review)
    context = {
        'email': email,
        'username': username,
        'review': review
    }
    return render(request, "reviewdisplay.html", context)