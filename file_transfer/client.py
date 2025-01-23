import grpc
import file_transfer_pb2
import file_transfer_pb2_grpc

def upload_file(stub, file_path):
    with open(file_path, 'rb') as f:
        content = f.read()
        filename = file_path.split('/')[-1]
        request = file_transfer_pb2.FileRequest(filename=filename, content=content)
        response = stub.UploadFile(request)
        print(response.message)

def main():
    channel = grpc.insecure_channel('localhost:50051')
    stub = file_transfer_pb2_grpc.FileTransferStub(channel)
    file_path = input("Entre com o nome do arquivo .txt para fazer o upload: ")
    upload_file(stub, f"files/{file_path}")

if __name__ == "__main__":
    main()
