from django.shortcuts import render_to_response


def profile(request):
    return render_to_response('users/profile.html')
