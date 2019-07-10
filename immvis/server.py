from concurrent import futures
from time import sleep
import grpc
import immvis_pb2
import immvis_pb2_grpc
from grpc_server import ImmVisGrpcServer
from discovery import ImmVisDiscoveryService

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class ImmVisServer():

    _server = None
    _discovery_service = None

    def __init__(self, grpc_server_port=50051, discovery_port=5000, data_frame=None):
        self._server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
        immvis_pb2_grpc.add_ImmVisServicer_to_server(ImmVisGrpcServer(data_frame), self._server)
        self._server.add_insecure_port('[::]:' + str(grpc_server_port))
        self._discovery_service = ImmVisDiscoveryService(port=discovery_port)

    def start(self):
        self._server.start()
        self._discovery_service.start()

    def stop(self):
        self._server.stop(0)
        self._discovery_service.stop()

_immvis_server = ImmVisServer()

def start_server(data_frame=None):
    print("Server has started!")
    _immvis_server.start()

    try:
        while True:
            sleep(_ONE_DAY_IN_SECONDS)
    except (KeyboardInterrupt, SystemExit):
        stop_server()

def stop_server():
    print("Server has stoped!")
    _immvis_server.stop()

if __name__ == '__main__':
    print("Running server...")
    start_server()
