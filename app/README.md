rodando a api: `python main.py run`
SOAP
chamar: `localhost:5000/soap`
### GET USER ID
```xml
<?xml version="1.0" encoding="utf-8"?>
<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:tns="soap_wsgi_app">
  <soapenv:Body>
    <tns:get_user>
      <tns:user_id>2</tns:user_id>
    </tns:get_user>
  </soapenv:Body>
</soapenv:Envelope>
```

RabbitMQ rodando localmenteo servidor de mensagens: `docker run -d --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:management
`
rodando o consumidor: ``python consumer.py`