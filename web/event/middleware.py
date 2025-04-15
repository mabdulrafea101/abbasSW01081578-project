from .signals import event_view_accessed


class EventStatusUpdateMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the request is for an event-related view
        if request.path.startswith('/event'):
            # Send the signal to update event statuses
            event_view_accessed.send(sender=self.__class__)
        
        response = self.get_response(request)
        return response
