import socket
import pickle
import ssl
from tabulate import tabulate

# Updated menu for the restaurant
menu = {
    1: {"name": "South Indian Meal", "price": 60},
    2: {"name": "North Indian Meal", "price": 70},
    3: {"name": "Burger and Fries Combo", "price": 100},
    4: {"name": "Pizza and Soda Combo", "price": 120},
    5: {"name": "Ice Cream", "price": 50},
}

def send_menu(conn):
    # Send menu to client
    conn.send(pickle.dumps(menu))

def handle_order(conn, addr):
    print(f"Connected to {addr}")

    # Receive order
    order = conn.recv(1024)
    order = pickle.loads(order)

    total_price = 0
    ordered_items = []

    # Calculate total price and build ordered items list
    for item_id, quantity in order.items():
        if item_id in menu:
            item = menu[item_id]
            total_price += item["price"] * quantity
            ordered_items.append([item["name"], quantity, item["price"] * quantity])

    # Calculate GST (5%)
    gst_amount = total_price * 0.05
    total_price += gst_amount

    # Send total price with GST to client
    conn.send(pickle.dumps(total_price))

    # Print order details as a table
    headers = ["Item Name", "Quantity", "Total Price"]
    print("\nOrder Details:")
    print(tabulate(ordered_items, headers=headers, tablefmt="grid"))

    print(f"\nTotal Price (incl. 5% GST): ₹{total_price}")
    print(f"GST (5%): ₹{gst_amount}")

def main():
    host = "0.0.0.0"  # Listen on all available interfaces
    port = 8080

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)

    print("Restaurant Server is running...")
    print("Waiting for connections...")

    while True:
        conn, addr = server_socket.accept()

        # Create an SSL context
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        # Load server certificate and key (use relative paths if in the same directory)
        ssl_context.load_cert_chain(certfile="server.crt", keyfile="server.key")

        try:
            # Wrap the socket with SSL
            ssl_socket = ssl_context.wrap_socket(conn, server_side=True)
            print("SSL connection established!")
            
            while True:
                # Receive option from client
                option = ssl_socket.recv(1024)
                if not option:
                    break
                option = pickle.loads(option)

                if option == '1':
                    # Send menu
                    send_menu(ssl_socket)
                elif option == '2':
                    # Handle order
                    handle_order(ssl_socket, addr)
                elif option == '3':
                    # Client requested bill
                    total_price = pickle.loads(ssl_socket.recv(1024))
                    print("Client requested bill.")
                    print(f"Total Price: ₹{total_price}")
                    ssl_socket.send(pickle.dumps(total_price))
                elif option == '4':
                    # Receive and print feedback
                    feedback = pickle.loads(ssl_socket.recv(1024))
                    print("Client feedback:")
                    print(feedback)
                    print("Thank you for your feedback!")
                elif option == '5':
                    print("Client requested to exit.")
                    break
        finally:
            ssl_socket.close()

if __name__ == "__main__":
    main()
