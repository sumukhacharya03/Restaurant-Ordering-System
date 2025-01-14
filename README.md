# Restaurant-Ordering-System
Restaurant Ordering System using Socket Programming

# About the Project:

I have implemented socket programming to create a client-server architecture. The client represents the person placing the food order, while the server collects the client's order information. It then displays the order details to the client, such as the items ordered with their respective quantities in a tabular form. Additionally, the server calculates and presents the bill, including GST tax. The system also allows the client to provide feedback, which the server displays. Once the client finishes the order, they can exit the system. Furthermore, we've integrated SSL as an extra layer of security to enhance the system's safety.

# What is Socket Programming?
Socket programming enables communication between different computers over a network. It works like a two-way telephone connection, where one computer (the server) listens for incoming connections while another computer (the client) initiates the connection to establish communication. Once connected, both computers can send and receive data through these sockets, making it possible to build networked applications like chat programs, web servers, or in this case, a restaurant ordering system.

# What is SSL(Secure Sockets Layer)?
SSL (Secure Sockets Layer) is a security protocol that creates an encrypted connection between a client and server to protect sensitive data during transmission. It uses digital certificates to verify the server's identity and establish a secure channel, preventing attackers from intercepting or tampering with the data. In this restaurant ordering system, SSL ensures that customer orders, menu prices, and feedback are transmitted securely between the client and restaurant server.

# How to run the Project:

<li>
  First, clone the repo into a new folder using this command:

  
  ```git bash
  git clone https://github.com/sumukhacharya03/Restaurant-Ordering-System.git
```
</li>

<li>
  Then, open 2 terminals in that folder and run these 2 commands on the 2 terminals separately:


  ```git bash
  python server.py
  ```

```git bash
python client.py
  ```
</li>

<li>
  To run it across two devices:
  
  1. Don't change the server.py code.
    
  2. In the client code change the host from "localhost" to the server's device IP address
  
 ```git bash
  # Change this line in client.py
  host = "192.168.x.x"  # Replace with server's actual IP address
  ```

  3. To run the systems on separate devices:
     
       1. Find the server's IP address:
          1. On Windows:
             ```git bash
             ipconfig
             ```
             
          2. On Linux/Mac:
             ```git bash
             ifconfig
             ```

      Look for an IPv4 address in your local network(usually starts with 192.168.x.x)
     
     2. Run the systems:

        On the server's system:
        
        ```git bash
        python server.py
        ```

        On the client's system:

        ```git bash
        python client.py
        ```
</li>

<li>
  Then, you can use the client terminal to browse menus, order food, view bills, and provide feedback like this:
  
  <img width="376" alt="image" src="https://github.com/user-attachments/assets/26a8e396-7850-4ce8-a903-a584445cec62" />

</li>

<li>
  And simultaneously you can see the server terminal collecting the order details from client and display the bills and feedback like this:
  
  <img width="632" alt="image" src="https://github.com/user-attachments/assets/93f6687a-6644-4a75-8b34-2e26e4772c20" />

</li>
