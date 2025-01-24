const grpc = require('@grpc/grpc-js');
const protoLoader = require('@grpc/proto-loader');
const fs = require('fs');

const PROTO_PATH = './file_transfer.proto';
const packageDefinition = protoLoader.loadSync(PROTO_PATH);
const { FileTransfer } = grpc.loadPackageDefinition(packageDefinition);

// Função para gerar um ID único
const generateId = () => {
    return Date.now();  // Você pode usar um UUID aqui também, se preferir
};

const uploadFile = (call, callback) => {
    const { filename, content } = call.request;

    // Salva o arquivo
    fs.writeFileSync(`./files/upload-${filename}`, content);

    // Retorna uma resposta com o ID gerado e o nome do arquivo
    callback(null, { message: `Arquivo upload-${generateId()}-${filename} carregado com sucesso!` });
};

const server = new grpc.Server();
server.addService(FileTransfer.service, { UploadFile: uploadFile });

const PORT = '50051';

server.bindAsync(`0.0.0.0:${PORT}`, grpc.ServerCredentials.createInsecure(), () => {
    console.log(`Servidor executando na porta ${PORT}`);
    server.start();
});
