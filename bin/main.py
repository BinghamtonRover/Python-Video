from lib.server import VideoServer

if __name__ == '__main__':
	print("Initializing...")
	data_socket = VideoServer(port=8002)
	while True: 
		try: data_socket.listen()
		except KeyboardInterrupt: quit()
		except OSError as error: 
			# UDP error when a socket is closed during use. Ignore and try again.
			if error.errno == 10054 or error.errno == 101: continue
			else: raise error
