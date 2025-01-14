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
    host = "192.168.4.145"  # Change this to the server's IP address
    port = 8080

    # Establish a regular TCP connection
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Create an SSL context
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS)
    # Wrap the socket with SSL
    ssl_socket = ssl_context.wrap_socket(client_socket, server_hostname=host)

    try:
        # Connect to the server
        ssl_socket.connect((host, port))

        while True:
            print("\nOptions:")
            print("1. Show Menu")
            print("2. Order Food")
            print("3. Show Bill")
            print("4. Feedback")
            print("5. Exit")

            option = input("Select an option: ")

            if option == '1':
                # Send option 1 to server to request menu
                ssl_socket.send(pickle.dumps(option))
                # Receive and display menu
                menu = pickle.loads(ssl_socket.recv(1024))
                display_menu(menu)
            elif option == '2':
                # Send option 2 to server to place order
                ssl_socket.send(pickle.dumps(option))
                # Place order
                order = place_order()
                # Send order to server
                ssl_socket.send(pickle.dumps(order))
                # Receive total price
                total_price = pickle.loads(ssl_socket.recv(1024))
                print(f"Total Price: ₹{total_price}")
            elif option == '3':
                # Send option 3 to server to request bill
                ssl_socket.send(pickle.dumps(option))
                # Send total price
                ssl_socket.send(pickle.dumps(total_price))
                # Receive total price
                total_price = pickle.loads(ssl_socket.recv(1024))
                show_bill(total_price)  # This will display the total price
            elif option == '4':
                # Send option 4 to server to request feedback
                ssl_socket.send(pickle.dumps(option))
                feedback = input("Enter your feedback: ")
                ssl_socket.send(pickle.dumps(feedback))
                print("Thank you for your feedback!")
            elif option == '5':
                # Send option 5 to server to request exit
                ssl_socket.send(pickle.dumps(option))
                print("Exiting...")
                break
            else:
                print("Invalid option. Please try again.")

    finally:
        ssl_socket.close()

if __name__ == "__main__":
    main()
