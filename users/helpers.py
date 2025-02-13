from django.db import ProgrammingError
from django.urls import URLResolver, URLPattern

from users.models import ViewPermission


def reg_urls_to_rule(urlpatterns):
    try:
        views = get_all_views(urlpatterns)
        for url in urlpatterns:
            if isinstance(url, URLResolver):
                if url.namespace == 'admin' or url.namespace == 'accounts':
                    continue
                reg_urls_to_rule(url.url_patterns)

            elif isinstance(url, URLPattern):
                view = views[url.lookup_str]
                for method in view.http_method_names:
                    if method in ('head', 'options', 'option', 'trace'):
                        continue
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
            if hasattr(pattern.callback, 'cls'):
                view = pattern.callback.cls
            elif hasattr(pattern.callback, 'view_class'):
                view = pattern.callback.view_class
            else:
                view = pattern.callback
            views[pattern.lookup_str] = view

    return views