import grpc

from concurrent import futures
from protopython import check_pb2, check_pb2_grpc

class Greeter(check_pb2_grpc.GreeterServicer):
    def greet(self, request, context):
        print("Got Request From " + str(request))
        return check_pb2.ServerResponse(message='{0} {1}'.format(request.from_client, request.name))

def server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    check_pb2_grpc.add_GreeterServicer_to_server(Greeter(), server)
    server.add_insecure_port('[::]:50051')
    print('gRPC Started')
    server.start()
    server.wait_for_termination()
server()