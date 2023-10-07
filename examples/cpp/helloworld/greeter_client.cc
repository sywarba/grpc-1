#include <iostream>
#include <memory>
#include <string>

#include <grpcpp/grpcpp.h>

#include "helloworld.grpc.pb.h"

using grpc::Channel;
using grpc::ClientContext;
using grpc::Status;
using helloworld::Greeter;
using helloworld::HelloReply;
using helloworld::HelloRequest;


class GreeterClient {
 public:
  GreeterClient(std::shared_ptr<Channel> channel)
      : stub_(Greeter::NewStub(channel)) {}

  std::string SayHello(const std::string& name, const std::string& language) {
    HelloRequest request;
    request.set_name(name);
    request.set_language(language);

    HelloReply reply;
    ClientContext context;

    Status status = stub_->SayHello(&context, request, &reply);

    if (status.ok()) {
      return reply.message();
    } else {
      std::cout << "RPC failed with error code: " << status.error_code()
                << ", message: " << status.error_message() << std::endl;
      return "";
    }
  }

  void SayHelloStream(const std::string& name, const std::string& language) {
    HelloRequest request;
    request.set_name(name);
    request.set_language(language);

    ClientContext context;
    std::unique_ptr<grpc::ClientReader<HelloReply> > reader(
        stub_->SayHelloStream(&context, request));

    HelloReply reply;
    while (reader->Read(&reply)) {
      std::cout << reply.message() << std::endl;
    }

    Status status = reader->Finish();
    if (!status.ok()) {
      std::cout << "RPC failed with error code: " << status.error_code()
                << ", message: " << status.error_message() << std::endl;
    }
  }

 private:
  std::unique_ptr<Greeter::Stub> stub_;
};

void Run() {
  std::string target_str = "localhost:50051";
  GreeterClient greeter(
      grpc::CreateChannel(target_str, grpc::InsecureChannelCredentials()));

  std::cout << "Will try to greet world ..." << std::endl;

  std::string method;
  std::cout << "Which method do you want to call? (1 for SayHello, 2 for SayHelloStream): ";
  std::cin >> method;

  std::string name;
  std::cout << "What's your name? ";
  std::cin >> name;

  std::string language;
  while (true) {
    std::cout << "What's your preferred language? (ENGLISH, FRENCH, ARABIC): ";
    std::cin >> language;

    if (language == "ENGLISH" || language == "FRENCH" || language == "ARABIC") {
      break;
    } else {
      std::cout << "Invalid language. Please enter one of ENGLISH, FRENCH, or ARABIC." << std::endl;
    }
  }

  if (method == "1") {
    std::string message = greeter.SayHello(name, language);
    std::cout << message << std::endl;
  } else if (method == "2") {
    greeter.SayHelloStream(name, language);
  } else {
    std::cout << "Invalid choice. Please enter 1 or 2." << std::endl;
  }
}

int main(int argc, char** argv) {
  Run();
  return 0;
}
