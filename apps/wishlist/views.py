from django.shortcuts import get_object_or_404,redirect,render
from django.contrib.auth.decorators import login_required
from apps.rooms.models import Room
from .models import Wishlist

@login_required
def toggle_wishlist(request,room_id):
    room=get_object_or_404(Room,id=room_id)
    
    wishlist_item=Wishlist.objects.filter(
        user=request.user,
        room=room,
    ).first()
    
    if wishlist_item:
        wishlist_item.delete()
    else:
        Wishlist.objects.create(
            user=request.user,
            room=room,
        )
    return redirect("rooms:room_detail",id=room_id)


@login_required
def wishlist_list(request):
    wishlist=Wishlist.objects.filter(
        user=request.user
    ).select_related("room")
    
    context={
        "wishlist":wishlist,
    }
    
    return render(request,"wishlist/wishlist_list.html",context)


