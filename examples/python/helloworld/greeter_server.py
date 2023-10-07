from concurrent import futures
import logging

import grpc
import helloworld_pb2
import helloworld_pb2_grpc

class Greeter(helloworld_pb2_grpc.GreeterServicer):

    def SayHello(self, request, context):
        if request.language == "ENGLISH":
            return helloworld_pb2.HelloReply(message='Hello, %s!' % request.name)
        elif request.language == "FRENCH":
            return helloworld_pb2.HelloReply(message='Salut, %s!' % request.name)
        elif request.language == "ARABIC":
            return helloworld_pb2.HelloReply(message='Marhaba, %s!' % request.name)
        else:
            return helloworld_pb2.HelloReply(message='Invalid language')

    def SayHelloStream(self, request, context):
        message=""
        if request.language == "ENGLISH":
            helloworld_pb2.HelloReply(message=message+'Hello %s!' % request.name)
            helloworld_pb2.HelloReply(message=message+'How are you %s?' % request.name)
            return helloworld_pb2.HelloReply(message=message+'Have a good day %s!' % request.name)
        elif request.language == "FRENCH":
            helloworld_pb2.HelloReply(message=message+'Salut %s!' % request.name)
            helloworld_pb2.HelloReply(message=message+'Comment ça va %s?' % request.name)
            return helloworld_pb2.HelloReply(message=message+'Bonne journée %s!' % request.name)
        elif request.language == "ARABIC":
            helloworld_pb2.HelloReply(message=message+'Marhaba %s!' % request.name)
            helloworld_pb2.HelloReply(message=message+'Kaifa halouka %s?' % request.name)
            return helloworld_pb2.HelloReply(message=message+'Yom saeed %s!' % request.name)
        else:
            return helloworld_pb2.HelloReply(message='Invalid language')


def serve():
    port = '50051'
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    helloworld_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:' + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig()
    serve()

