from spyne.application import Application
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from services import AccountServiceSOAP

# Configuração do serviço SOAP
soap_app = Application(
    [AccountServiceSOAP],
    tns="soap_wsgi_app",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(),
)

application = WsgiApplication(soap_app)