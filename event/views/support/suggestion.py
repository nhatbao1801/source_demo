from event.models.event import Event


def get_event_near_user(request):
    # Based on city
    # Get city of current loggon user
    city_id = request.user.city_id
    # Get cities_event
    return Event.objects.filter(city_id__exact=city_id)
