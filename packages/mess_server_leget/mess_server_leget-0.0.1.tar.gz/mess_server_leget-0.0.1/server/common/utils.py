import json

from common import settings


def get_message(sock):
    """
    Функция принимает байты, возвращает словарь, если примет не байты, выкинет исключение
    :param sock:
    :return:

    """
    encode_response = sock.recv(settings.MAX_PACKAGE_LENGTH)
    if isinstance(encode_response, bytes):
        json_response = encode_response.decode(settings.ENCODING)
        response = json.loads(json_response)
        if isinstance(response, dict):
            return response
        raise ValueError
    raise ValueError


def send_message(sock, message):
    """
    Функция принимает словарь, кодирует его и отправляет
    :param sock:
    :param message:
    :return:
    """
    json_message = json.dumps(message)
    encoding_message = json_message.encode(settings.ENCODING)
    sock.send(encoding_message)
