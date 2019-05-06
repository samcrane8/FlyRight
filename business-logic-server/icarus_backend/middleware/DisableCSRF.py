from django.utils.deprecation import MiddlewareMixin


class DisableCSRF(MiddlewareMixin):
    def process_request(self, request):
        setattr(request, '_dont_enforce_csrf_checks', True)

    # def __call__(self, request):
    #     response = self.get_response(request)
    #     response['Access-Control-Allow-Origin'] = '*'
    #     #response['Access-Control-Allow-Origin'] = 'http://localhost:8080 http://devapi.icarusmap.com'
    #     return response