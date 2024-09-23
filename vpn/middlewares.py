from bs4 import BeautifulSoup
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from vpn.models import Site
from vpn import settings


class ProxyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, *args, **kwargs):

        if view_func.__name__ == "dynamic_proxy_view":
            if not getattr(request, "processed_base_tag", False):
                request.processed_base_tag = True
                original_site_url = self.get_original_site_url(request)

                response = self.get_response(request)

                if "text/html" in response.get("Content-Type", ""):
                    soup = BeautifulSoup(response.content, "html.parser")
                    if not soup.head.find("base"):
                        base_tag = soup.new_tag("base", href=original_site_url)
                        soup.head.insert(0, base_tag)

                    for tag in soup.find_all("a"):
                        original_href_url = tag.get("href")

                        # Change only internal links
                        if original_href_url and "www" not in original_href_url:
                            new_url = self.get_internal_url(
                                request.path, original_href_url
                            )
                            tag["href"] = new_url

                    response = HttpResponse(soup.prettify(), content_type="text/html")

                return response

    def get_internal_url(self, internal_route, original_href_url):
        return f"{settings.BASE_URL}{internal_route}{original_href_url}"

    def get_original_site_url(self, request):
        path_parts = request.path.split("/")
        site_title = path_parts[1] if len(path_parts) > 1 else None
        user = request.user
        site = get_object_or_404(Site, user=user, title=site_title)
        return site.original_url
