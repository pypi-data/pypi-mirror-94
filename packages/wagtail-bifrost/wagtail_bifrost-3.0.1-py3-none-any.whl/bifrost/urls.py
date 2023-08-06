from django.conf.urls import url
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from graphene_subscriptions.consumers import GraphqlSubscriptionConsumer

from .views import BifrostView

# Traditional URL routing
urlpatterns = [url(r"^graphql", csrf_exempt(BifrostView.as_view()))]

websocket_urlpatterns = [path("graphql/", GraphqlSubscriptionConsumer)]

# if SHOULD_EXPOSE_GRAPHIQL:
#     urlpatterns.append(url(r"^graphiql", graphiql))
