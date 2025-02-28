import pika
import json

def get_rabbitmq_channel():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    channel.queue_declare(queue="task_queue", durable=True)
    return channel, connection

def callback(ch, method, properties, body):
    message = json.loads(body)
    print(f"📥 Mensagem recebida: {message['message']}")

    # Confirmação de que a mensagem foi processada
    ch.basic_ack(delivery_tag=method.delivery_tag)

if __name__ == "__main__":
    channel, connection = get_rabbitmq_channel()
    print("🟢 Aguardando mensagens. Pressione CTRL+C para sair.")

    # Consumindo mensagens da fila
    channel.basic_qos(prefetch_count=1)  # Garante processamento de uma mensagem por vez
    channel.basic_consume(queue="task_queue", on_message_callback=callback)

    channel.start_consuming()
