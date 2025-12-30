import socket
import json
import time
import sys

class RemoteClient:
    def __init__(self, server_address, server_port=6000):
        self.server_address = '172.31.1.134'
        self.server_port = server_port
        self.response_timeout = 3
        self.max_retries = 3
    
    def execute_function(self, func_name, parameters=None):
        if parameters is None:
            parameters = {}
        
        request_id = f"{int(time.time()*1000)}"
        
        request_data = {
            'id': request_id,
            'function': func_name,
            'parameters': parameters
        }
        
        for attempt in range(1, self.max_retries + 1):
            print(f"Attempt {attempt} for function {func_name}")
            
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.settimeout(self.response_timeout)
                
                start_time = time.time()
                client_socket.connect((self.server_address, self.server_port))
                
                client_socket.send(json.dumps(request_data).encode('utf-8'))
                
                response = client_socket.recv(1024)
                end_time = time.time()
                
                if response:
                    result = json.loads(response.decode('utf-8'))
                    
                    if result.get('status') == 'completed':
                        print(f"Success. Response time: {end_time - start_time:.3f}s")
                        print(f"Result: {result.get('output')}")
                        client_socket.close()
                        return result
                    else:
                        print(f"Error: {result.get('error')}")
                
                client_socket.close()
                
            except socket.timeout:
                print(f"Timeout after {self.response_timeout} seconds")
            except ConnectionRefusedError:
                print("Connection refused - server unavailable")
            except Exception as e:
                print(f"Communication error: {e}")
            
            if attempt < self.max_retries:
                print(f"Waiting 1 second before retry {attempt + 1}")
                time.sleep(1)
        
        print(f"All {self.max_retries} attempts failed")
        return None
    
    def check_connection(self):
        try:
            test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            test_socket.settimeout(2)
            test_socket.connect((self.server_address, self.server_port))
            test_socket.close()
            return True
        except:
            return False

def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='RPC Client')
    parser.add_argument('--server', required=True, help='Server IP address')
    parser.add_argument('--port', type=int, default=6000, help='Server port')
    parser.add_argument('--function', default='server_time', help='Function to execute')
    parser.add_argument('--param1', help='First parameter')
    parser.add_argument('--param2', help='Second parameter')
    
    args = parser.parse_args()
    
    client = RemoteClient(args.server, args.port)
    
    print(f"Connecting to server: {args.server}:{args.port}")
    
    if not client.check_connection():
        print("Cannot establish connection with server")
        sys.exit(1)
    
    parameters = {}
    
    if args.param1 and args.param2:
        try:
            parameters = {'val1': float(args.param1), 'val2': float(args.param2)}
        except ValueError:
            parameters = {'val1': args.param1, 'val2': args.param2}
    elif args.param1:
        parameters = {'text': args.param1}
    
    result = client.execute_function(args.function, parameters)
    
    if result:
        print("\nFinal response received")
        print(f"Request ID: {result.get('id')}")
        print(f"Status: {result.get('status')}")
        if 'output' in result:
            print(f"Output: {result.get('output')}")

if __name__ == "__main__":
    main()