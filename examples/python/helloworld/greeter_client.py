from __future__ import print_function

import logging

import grpc
import helloworld_pb2
import helloworld_pb2_grpc


def run():
    print("Will try to greet world ...")
    with grpc.insecure_channel('localhost:50051') as channel:
        stub = helloworld_pb2_grpc.GreeterStub(channel)
        method = input("Which method do you want to call? (1 for SayHello, 2 for SayHelloStream): ")
        name = input("What's your name? ")
        while True:
            lang_input = input("What's your preferred language? (ENGLISH, FRENCH, ARABIC): ")
            if lang_input in ['ENGLISH', 'FRENCH', 'ARABIC']:
                break
            else:
                print("Invalid language. Please enter one of ENGLISH, FRENCH, or ARABIC.")

        if method == '1':
            # Create a request message for SayHello
            request = helloworld_pb2.HelloRequest(
                name=name,
                language=lang_input
            )

            # Call the server's SayHello method
            response = stub.SayHello(request)
            print(response.message)
        elif method == '2':
            # Create a request message for SayHelloStream
            request = helloworld_pb2.HelloRequest(
                name=name,
                language=lang_input
            )
            for response in stub.SayHelloStream(request):
                print(response.message)
        else:
            print("Invalid choice. Please enter 1 or 2.")


if __name__ == '__main__':
    logging.basicConfig()
    run()

