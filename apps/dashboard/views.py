from django.contrib.auth.decorators import login_required
from apps.services.dashboard_service import get_provider_dashboard_data
from django.shortcuts import render
from apps.common.decorators import provider_required

@login_required
@provider_required
def provider_dashboard(request):
    context=get_provider_dashboard_data(request.user)
    
    
    
    return render(request,
                  "dashboard/provider_dashboard.html",
                  context,)
    
    

