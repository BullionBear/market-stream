import signal
import grpc
import asyncio
from concurrent import futures
from generated import greeter_pb2
from generated import greeter_pb2_grpc


class GreeterServicer(greeter_pb2_grpc.GreeterServicer):
    async def SayHello(self, request, context):
        return greeter_pb2.HelloReply(message=f'Hello, {request.name}')


async def serve():
    server = grpc.aio.server()
    greeter_pb2_grpc.add_GreeterServicer_to_server(GreeterServicer(), server)
    listen_addr = '[::]:50051'
    server.add_insecure_port(listen_addr)
    print(f'Starting server on {listen_addr}')
    await server.start()
    # Setup graceful shutdown
    loop = asyncio.get_running_loop()

    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)
    loop.add_signal_handler(signal.SIGINT, stop.set_result, None)

    await stop
    await server.stop(30)  # Wait up to 30 seconds for the server to shut down

if __name__ == '__main__':
    asyncio.run(serve())