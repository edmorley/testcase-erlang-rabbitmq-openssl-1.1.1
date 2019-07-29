# OpenSSL 1.1.1 incompatibility with RabbitMQ on Erlang 17

This test-case demonstrates the TLS connection errors seen when a client
using [OpenSSL 1.1.1](https://www.openssl.org/blog/blog/2018/09/11/release111/)
attempts to connect to a RabbitMQ server when it is running on Erlang/OTP 17.x.

I believe the errors are due to OpenSSL 1.1.1's revised cypher suite list
triggering a bug in Erlang 17's TLS implementation.

This issue affects clients connecting from:
* Ubuntu 18.04 (since OpenSSL 1.1.1 has recently been backported to `bionic-updates`)
* Debian Buster
* (likely many more)

In addition to the test-case below, servers can be checked for compatibility by
upgrading to OpenSSL 1.1.1 on a local machine and then running:
`echo 'Q' | openssl s_client -connect HOSTNAME:5671 || echo 'Failed!'`

## STR

1. Ensure latest Docker/Docker Compose is installed.
2. Git clone this repository.
3. From the root of the repository, run: `docker-compose up --build`

## Expected

The Celery worker is successfully able to connect to the RabbitMQ server,
and no errors appear in either the app or server logs.

## Actual

The app fails to connect, with errors of form:

```
consumer: Cannot connect to amqps://guest:**@rabbitmq:5671//: [Errno 104] Connection reset by peer.
```

The RabbitMQ server logs show:

```
=ERROR REPORT==== 29-Jul-2019::11:02:21 ===
Error on AMQP connection <0.321.0>:
{ssl_upgrade_failure,
    {{function_clause,
         [{ssl_cipher,hash_algorithm,"\b",
              [{file,"ssl_cipher.erl"},{line,1199}]},
          {ssl_handshake,'-dec_hello_extensions/2-lc$^0/1-1-',1,
              [{file,"ssl_handshake.erl"},{line,1706}]},
          {ssl_handshake,'-dec_hello_extensions/2-lc$^0/1-1-',1,
              [{file,"ssl_handshake.erl"},{line,1707}]},
          {ssl_handshake,dec_hello_extensions,2,
              [{file,"ssl_handshake.erl"},{line,1706}]},
          {tls_handshake,decode_handshake,3,
              [{file,"tls_handshake.erl"},{line,206}]},
          {tls_handshake,get_tls_handshake_aux,3,
              [{file,"tls_handshake.erl"},{line,177}]},
          {tls_connection,next_state,4,
              [{file,"tls_connection.erl"},{line,433}]},
          {gen_fsm,handle_msg,7,[{file,"gen_fsm.erl"},{line,503}]}]},
     {gen_fsm,sync_send_all_state_event,[<0.322.0>,{start,5000},infinity]}}}
```

## Solutions/workarounds

* Ideally upgrade the RabbitMQ server's Erlang to 18 or newer, since Erlang 17
  is EOL/insecure. To try this out here, modify `docker-compose.yml` to use the
  `rabbitmq:3.5.5` image (which bundles Erlang 18.1 instead).
* Run the client from a distro/release that is running OpenSSL <1.1.1 (such as
  Ubuntu 16.04 or Debian Strech, which are still on OpenSSL 1.1.0). To try this,
  modify `Dockerfile` to instead use the base image `python:3.7.4-slim-stretch`.
* Adjust the client configuration to force it to use TLS 1.1 instead of TLS 1.2.
  To try this, uncomment the `FORCE_TLS_1_1` env var in `docker-compose.yml`.
