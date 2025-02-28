from flask import Flask, request, jsonify
from database import db
from services import UsersServiceRest, AccountsServiceRest
from flask_restful import Api
from flasgger import Swagger
from soap import application
import pika
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///accounts.db'
db.init_app(app)

api = Api(app)
swagger = Swagger(app) 

with app.app_context():
    db.create_all()

api.add_resource(UsersServiceRest, '/users')
api.add_resource(AccountsServiceRest, '/accounts')

def start_response(status, response_headers, exc_info=None):
        pass
    
@app.route("/soap", methods=['POST'])
def soap_service():
    """
    Serviço SOAP para operações de usuário e conta
    ---
    post:
      summary: Endpoint SOAP para operações de usuário e conta
      consumes:
        - text/xml
      produces:
        - text/xml
      responses:
        200:
          description: Resposta do serviço SOAP
    """
    return application(request.environ, start_response)

# Conexão com RabbitMQ
def get_rabbitmq_channel():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="task_queue", durable=True)  # Fila persistente
    return channel, connection

@app.route("/publish", methods=["POST"])
def publish():
    """
    Publica uma mensagem na fila RabbitMQ
    ---
    post:
      summary: Publica uma mensagem na fila
      parameters:
        - name: body
          in: body
          required: True
          schema:
            properties:
              message:
                type: string
                example: "Nova tarefa para processar"
      responses:
        200:
          description: Mensagem publicada com sucesso
    """
    data = request.get_json()
    message = data.get("message", "Mensagem padrão")

    channel, connection = get_rabbitmq_channel()
    message_persistent = 2
    channel.basic_publish(
        exchange="",
        routing_key="task_queue",
        body=json.dumps({"message": message}),
        properties=pika.BasicProperties(
            delivery_mode=message_persistent,
        ),
    )

    connection.close()
    return jsonify({"status": "Mensagem publicada", "message": message})

if __name__ == '__main__':
    app.run(debug=True)
