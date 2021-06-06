class CORSMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Headers"] = "X-Requested-With, X-HTTP-Method-Override, Content-Type, Accept"
        response["Access-Control-Allow-Credentials"] = True
        response["Access-Control-Allow-Methods"] = "GET,PUT,POST,DELETE"

        return response
