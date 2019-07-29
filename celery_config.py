import os
import ssl

broker_url = os.environ.get('BROKER_URL')

if os.environ.get('FORCE_TLS_1_1', '').lower() in ('true', '1'):
    # Work around a Kombu bug where using amqps:// clobbers broker_use_ssl, thanks to:
    # https://github.com/celery/kombu/blob/aa8ea28f50c4605fda0a3b1cea4ca1b3a5e80598/kombu/transport/__init__.py#L22
    # https://github.com/celery/kombu/blob/080502fd5c4736c0063daa08f5bbd672c3975a68/kombu/transport/pyamqp.py#L179
    # Since we're setting broker_use_ssl, the amqps:// form is redundant anyway.
    broker_url = broker_url.replace('amqps://', 'amqp://')
    # Force TLS 1.1 to be used instead of 1.2, to work around bugs in old Erlang's TLS 1.2 implementation.
    broker_use_ssl = {
        'ssl_version': ssl.PROTOCOL_TLSv1_1,
    }
