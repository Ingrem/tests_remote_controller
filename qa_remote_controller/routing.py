# routing.py
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.conf.urls import url
from qa_remote_controller.apps.integration.consumer import Consumer
from qa_remote_controller.apps.bc_mock_controller.consumer import MockConsumer
from qa_remote_controller.apps.simple_web_socket.consumer import Consumer_simple_socket
from qa_remote_controller.apps.reports_controller.consumer import ConsumerReports
from qa_remote_controller.apps.documentation_controller.consumer import ConsumerDocumentation
from qa_remote_controller.apps.manual_match_generator.manual_match_generator import ManualMatchGeneratorConsumer

websocket_urlpatterns = [
    url(r'^$', Consumer),
    url(r'^11_mock$', MockConsumer),
    url(r'^simple_web_socket', Consumer_simple_socket),
    url(r'^reports', ConsumerReports),
    url(r'^documentation', ConsumerDocumentation),
    url(r'^generators', ManualMatchGeneratorConsumer),
]

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': AuthMiddlewareStack(
        URLRouter(
            websocket_urlpatterns
        )
    ),
})