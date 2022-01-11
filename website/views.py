from django.shortcuts import render


def privacy_policy(request):
    return render(request, 'website/privacy_policy.html')
