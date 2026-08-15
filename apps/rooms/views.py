from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import RoomForm
from .models import Room
from django.http import HttpResponseForbidden
from apps.wishlist.models import Wishlist
from django.db.models import Avg
from apps.reviews.models import Review
from django.db.models import Q

@login_required
def create_room(request):
    if request.method=="POST":
        form=RoomForm(request.POST,request.FILES,)
        
        if form.is_valid():
            room= form.save(commit=False)
            room.owner=request.user
            room.save()
            
            return redirect ("rooms:room_list")
    
    else:
        form=RoomForm()
        
    return render(request,"rooms/create_room.html",{"form":form})



def room_list(request):
    rooms=Room.objects.all()
    search=request.GET.get("search")
    location=request.GET.get("location")
    min_rent=request.GET.get("min_rent")
    max_rent=request.GET.get("max_rent")
    available=request.GET.get("available")
    room_type=request.GET.get("room_type")
    gender = request.GET.get("gender")
    
    if search:
        rooms=rooms.filter(
            Q(title__icontains=search)|
            Q(location__icontains=search)
        )
        
    if location:
        rooms=rooms.filter(
            location__icontains=location
        )
        
    if min_rent:
        rooms=rooms.filter(
            rent__gte=min_rent
        )
        
    if max_rent:
        rooms=rooms.filter(
            rent__lte=max_rent
        )
        
    if available:
        rooms=rooms.filter(
            is_available=True
        )
        
    if room_type:
        rooms=rooms.filter(
            room_type=room_type
        )
        
    if gender:
        rooms=rooms.filter(
            gender_preference=gender
        )
        
    sort=request.GET.get("sort")
    
    if sort =="rent_low":
        rooms=rooms.order_by("rent")
    elif sort=="rent_high":
        rooms=rooms.order_by("-rent")
    elif sort=="newest":
        rooms=rooms.order_by("-created_at")
        
    
    context={
        "rooms":rooms,
    }
    
    return render(request,"rooms/room_list.html",context)



def room_detail(request,id):
    room=get_object_or_404(Room,id=id)
    
    reviews=room.reviews.select_related("user").order_by("-created_at")
    average_rating=reviews.aggregate(Avg("rating"))["rating__avg"]
    
    is_in_wishlist=False
    
    if request.user.is_authenticated:
        is_in_wishlist=Wishlist.objects.filter(
            user=request.user,
            room=room,
        ).exists()
    
    context={
        "room":room,
        "is_in_wishlist":is_in_wishlist,
        "reviews":reviews,
        "average_rating":average_rating,
    }
    
    return render (request,"rooms/room_detail.html",context,)


@login_required
def edit_room(request,id):
    room = get_object_or_404(Room,id=id)
    
    if room.owner!=request.user:
        return HttpResponseForbidden("You are not allowed to edit this room.")
    
    if request.method=="POST":
        form=RoomForm(request.POST,instance=room)
        
        if form.is_valid():
            form.save()
            return redirect("rooms:room_detail",id=room.id)
        
    else:
        form=RoomForm(instance=room)
    return render(request,"rooms/edit_room.html",{"form":form,"room":room},)


@login_required
def delete_room(request,id):
    room=get_object_or_404(Room,id=id)
    
    if room.owner!=request.user:
        return HttpResponseForbidden("You are not allowed to delete this room.")
    
    if request.method=="POST":
        room.delete()
        return redirect("rooms:room_list")
    
    return render(request,"rooms/delete_room.html",{"room":room},)
    