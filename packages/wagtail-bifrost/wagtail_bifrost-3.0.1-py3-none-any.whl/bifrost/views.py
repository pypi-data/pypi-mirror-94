from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie
from graphene_file_upload.django import FileUploadGraphQLView

SHOULD_EXPOSE_GRAPHIQL = settings.DEBUG or getattr(
    settings, "BIFROST_EXPOSE_GRAPHIQL", False
)


class BifrostView(View):
    playground = SHOULD_EXPOSE_GRAPHIQL

    @method_decorator(ensure_csrf_cookie)
    def get(self, request):
        if self.playground:
            return render(
                request,
                "bifrost/playground.html",
                {"url": request.build_absolute_uri()},
            )

        raise Http404()

    @method_decorator(ensure_csrf_cookie)
    def post(self, request):
        return FileUploadGraphQLView.as_view(graphiql=False)(request)
