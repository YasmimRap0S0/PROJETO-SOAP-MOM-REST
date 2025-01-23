const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const fs = require('fs');

const PROTO_PATH = './file_transfer.proto';
const packageDefinition = protoLoader.loadSync(PROTO_PATH);
const {FileTransfer} = grpc.loadPackageDefinition(packageDefinition);

const uploadFile = (call, callback) => {
    const { filename, content } = call.request;

    fs.writeFileSync(`./files/upload-${filename}`, content);
    callback(null, { message: `File upload-${generateId}-${filename} uploaded successfully!` });
};

const server = new grpc.Server();
server.addService(FileTransfer.service, { UploadFile: uploadFile });

const PORT = '50051';

server.bindAsync(`0.0.0.0:${PORT}`, grpc.ServerCredentials.createInsecure(), () => {
    console.log(`Server is running on port ${PORT}`);
    server.start();
});
