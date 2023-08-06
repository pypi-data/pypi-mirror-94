from django.conf import settings

from .utils import add_query_strings_to_links

EXCLUDE_PATHS_LIST = getattr(settings, "GLOBAL_QUERY_STRINGS_EXCLUDE_PATHS_LIST", [])


class GlobalQueryStringsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if self._exclude_paths(request):
            return response

        if "Content-Type" in response and "text/html" in response["Content-Type"]:
            response.content = add_query_strings_to_links(response.content)

        return response

    @staticmethod
    def _exclude_paths(request):
        """
        Check if the current path match a value of the GLOBAL_QUERY_STRINGS_EXCLUDE_PATHS_LIST settings.

        Returns a boolean: True if the requested path should bypass the middleware False otherwise.
        """
        return any(bool(request.path.startswith(path)) for path in EXCLUDE_PATHS_LIST)
