import socket
import pickle
import ssl

def display_menu(menu):
    print("Menu:")
    for item_id, item in menu.items():
        print(f"{item_id}: {item['name']} - ₹{item['price']}")

def place_order():
    order = {}
    while True:
        item_id = input("Enter item ID to order (0 to finish): ")
        if item_id == '0':
            break
        
        quantity = int(input("Enter quantity: "))
        order[int(item_id)] = quantity

    return order

def show_bill(total_price):
    print(f"Total Price: ₹{total_price}")

def main():
    # Use localhost if testing on same machine
    host = "localhost"  # or "127.0.0.1"
    port = 8080

    # Create a regular TCP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Set a timeout for the connection attempt
    client_socket.settimeout(10)

    # Create an SSL context with modern protocol
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    # Don't verify certificate for testing
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    # Wrap the socket with SSL
    ssl_socket = ssl_context.wrap_socket(client_socket, server_hostname=host)

    try:
        # Connect to the server
        print(f"Attempting to connect to {host}:{port}...")
        ssl_socket.connect((host, port))
        print("Connected successfully!")

        while True:
            print("\nOptions:")
            print("1. Show Menu")
            print("2. Order Food")
            print("3. Show Bill")
            print("4. Feedback")
            print("5. Exit")

            option = input("Select an option: ")

            if option == '1':
                ssl_socket.send(pickle.dumps(option))
                menu = pickle.loads(ssl_socket.recv(1024))
                display_menu(menu)
            elif option == '2':
                ssl_socket.send(pickle.dumps(option))
                order = place_order()
                ssl_socket.send(pickle.dumps(order))
                total_price = pickle.loads(ssl_socket.recv(1024))
                print(f"Total Price: ₹{total_price}")
            elif option == '3':
                ssl_socket.send(pickle.dumps(option))
                ssl_socket.send(pickle.dumps(total_price))
                total_price = pickle.loads(ssl_socket.recv(1024))
                show_bill(total_price)
            elif option == '4':
                ssl_socket.send(pickle.dumps(option))
                feedback = input("Enter your feedback: ")
                ssl_socket.send(pickle.dumps(feedback))
                print("Thank you for your feedback!")
            elif option == '5':
                ssl_socket.send(pickle.dumps(option))
                print("Exiting...")
                break
            else:
                print("Invalid option. Please try again.")

    except socket.timeout:
        print("Connection timed out. Please check if the server is running and the address is correct.")
    except ConnectionRefusedError:
        print("Connection refused. Please check if the server is running.")
    except ssl.SSLError as e:
        print(f"SSL Error: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        try:
            ssl_socket.close()
        except Exception:
            pass

if __name__ == "__main__":
    main()