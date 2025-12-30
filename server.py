import socket
import json
import time
from datetime import datetime
import threading
import sys

class RemoteServer:
    def __init__(self, host='0.0.0.0', port=6000):
        self.host = host
        self.port = port
        self.running = True
        self.functions = {
            'sum_values': self._sum_values,
            'server_time': self._server_time,
            'invert_text': self._invert_text,
            'multiply_values': self._multiply_values
        }
    
    def _sum_values(self, val1, val2):
        return float(val1) + float(val2)
    
    def _multiply_values(self, val1, val2):
        return float(val1) * float(val2)
    
    def _server_time(self):
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
    
    def _invert_text(self, text):
        return text[::-1]
    
    def _handle_connection(self, connection, address):
        try:
            data = connection.recv(1024)
            if data:
                request = json.loads(data.decode('utf-8'))
                
                req_id = request.get('id', 'unknown')
                func_name = request.get('function', '')
                parameters = request.get('parameters', {})
                
                if func_name in self.functions:
                    func = self.functions[func_name]
                    
                    if isinstance(parameters, dict):
                        result = func(**parameters)
                    elif isinstance(parameters, list):
                        result = func(*parameters)
                    else:
                        result = func(parameters)
                    
                    response = {
                        'id': req_id,
                        'output': result,
                        'status': 'completed',
                        'timestamp': datetime.now().isoformat()
                    }
                else:
                    response = {
                        'id': req_id,
                        'error': f'Function {func_name} not found',
                        'status': 'failed'
                    }
                
                connection.send(json.dumps(response).encode('utf-8'))
        
        except Exception as e:
            error_response = {
                'id': 'error',
                'error': str(e),
                'status': 'error'
            }
            connection.send(json.dumps(error_response).encode('utf-8'))
        
        finally:
            connection.close()
    
    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            server_socket.bind((self.host, self.port))
            server_socket.listen(10)
            
            print(f"Server active on port {self.port}")
            print("Available functions:", list(self.functions.keys()))
            
            while self.running:
                connection, address = server_socket.accept()
                
                thread = threading.Thread(
                    target=self._handle_connection,
                    args=(connection, address)
                )
                thread.daemon = True
                thread.start()
        
        except KeyboardInterrupt:
            print("\nServer termination requested")
        except Exception as e:
            print(f"Server error: {e}")
        finally:
            server_socket.close()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='RPC Server')
    parser.add_argument('--port', type=int, default=6000, help='Server port')
    parser.add_argument('--delay', type=int, default=0, help='Artificial delay in seconds')
    
    args = parser.parse_args()
    
    server = RemoteServer(port=args.port)
    
    if args.delay > 0:
        print(f"Applying delay of {args.delay} seconds")
        time.sleep(args.delay)
    
    server.start()