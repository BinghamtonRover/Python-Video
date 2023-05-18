from lib.server import VideoServer

if __name__ == '__main__':
	print("Initializing...")
	data_socket = VideoServer(port=8002)
	while True: 
		try: data_socket.listen()
		except KeyboardInterrupt: quit()
		except OSError as error: 
			if error.errno == 10054: continue
			else: raise error
