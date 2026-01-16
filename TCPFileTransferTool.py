import os, sys, argparse, socket, threading

parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers(dest="mode", required=True)
server_parser = subparsers.add_parser("server", help="Run in server mode.")
server_parser.add_argument("-p","--port", type=int, help="Port to listen on.", required=True)
client_parser = subparsers.add_parser("client", help="Run in client mode.")
client_parser.add_argument("-H", "--host", required=True, help="Target IP for server")
client_parser.add_argument("-p", "--port", type=int, required=True, help="Server port")
client_parser.add_argument("-fp", "--file_path", required=True, help="Path to file you want to send")
client_parser.add_argument("-fn", "--file_name", required=False, default="output", help="Path to file you want to send")


def run_server(port):
        host = "0.0.0.0"
        port = port
        srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv.bind((host, port))
        srv.settimeout(1.0)
        srv.listen()
        clients = []

        def recv_handler(client):
            data = b""
            while not data.endswith(b"\n"):
                chunk = client.recv(1)
                if not chunk:
                    break
                data += chunk
            return data.decode().strip()
        
        def clientHandler(client, address):
            try:
                mode = recv_handler(client)
                if mode == "FILE":
                    filename = recv_handler(client)
                    filesize = int(recv_handler(client))
                    with open(f"output_{filename}", "wb") as f:
                        received = 0
                        while received < filesize:
                            data = client.recv(4096)
                            if not data:
                                break
                            f.write(data)
                            received += len(data)
                            percent = (received / filesize) * 100
                            sys.stdout.write(f"\rReceiving from {address}: {percent:6.2f}%")
                            sys.stdout.flush()
                    recv_filename = f"output_{filename}"
                    print(f"\nReceived a file from {address}\nFilename: {recv_filename}\nSize: {filesize}")
            except Exception as e:
                print(f"Error: {e}")
            finally:
                if client in clients:
                    clients.remove(client)
                client.close()
        
        def receive():
            try:
                while True:
                    try:
                        client, address = srv.accept()
                        clients.append(client)
                        print(f"Connection established: {str(address)}")
                        thread = threading.Thread(target=clientHandler, args=(client,address), daemon=True)
                        thread.start()
                    except socket.timeout:
                        continue
            except KeyboardInterrupt:
                print("Goodbye")
                srv.close()   
        print(f"Server Broadcasting From {port}!")       
        receive()


def run_client(host, port, file_path, file_name):
        def sendFile():
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((str(host), port))
            file = file_path
            filename = file_name
            filesize = os.path.getsize(file)
            client.send(b"FILE\n")
            client.send(f"{filename}\n".encode())
            client.send(f"{filesize}\n".encode())
            with open(file, "rb") as f:
                sent = 0
                while True:
                    data = f.read(4096)
                    if not data:
                        break
                    client.send(data)
                    sent += len(data)
                    percent = (sent / filesize) * 100
                    sys.stdout.write(f"\rUploading: {percent:6.2f}%")
                    sys.stdout.flush()
            print("\nFile sent!")
            client.close()
        print(f"Initiating a client instance. Connecting to {host} on port {port}.")
        print("Sending file...")
        t1 = threading.Thread(target=sendFile)
        t1.start()
        t1.join()
        


def main():
    args = parser.parse_args()
    if args.mode == "server":
        run_server(port=args.port)
    elif args.mode == "client":
        run_client(host=args.host, port=args.port, file_path=args.file_path, file_name=args.file_name)
    else:
        print("Well... This is akward....")


if __name__ == "__main__":
    main()