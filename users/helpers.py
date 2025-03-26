from django.db import ProgrammingError
from django.urls import URLResolver, URLPattern
from users.models import ViewPermission

def reg_urls_to_rule(urlpatterns):
    try:
        views = get_all_views(urlpatterns)
        for url in urlpatterns:
            if isinstance(url, URLResolver):
                if url.namespace in ['admin', 'accounts']:
                    continue
                reg_urls_to_rule(url.url_patterns)

            elif isinstance(url, URLPattern):
                view = views.get(url.lookup_str)
                if view:
                    for method in view.http_method_names:
                        if method not in ('head', 'options', 'trace'):
                            ViewPermission.objects.get_or_create(
                                view_name=url.lookup_str,
                                path_name=url.name,
                                method=method
                            )
    except ProgrammingError:
        pass

def get_all_views(urlpatterns, views=None):
    views = views or {}
    for pattern in urlpatterns:
        if hasattr(pattern, 'url_patterns'):
            get_all_views(pattern.url_patterns, views=views)
        else:
            callback = getattr(pattern, 'callback', None)
            if hasattr(callback, 'cls'):
                view = callback.cls
            elif hasattr(callback, 'view_class'):
                view = callback.view_class
            else:
                view = callback
            views[pattern.lookup_str] = view
    return views
