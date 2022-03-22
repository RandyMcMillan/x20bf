import time
import json
import hashlib

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5 as PKCS1_v1_5_Cipher
from Crypto.Signature import PKCS1_v1_5 as PKCS1_v1_5_Signature
from Crypto.Hash import SHA512
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto import Random
from base64 import b64decode, b64encode

from p2pnetwork.node import Node
from p2psecure.blockchain import Blockchain

"""
Author : Maurice Snoeren <macsnoeren(at)gmail.com>
Version: 0.2 beta (use at your own risk!)

Python package p2psecure for implementing secure decentralized peer-to-peer network applications based
on the package p2pnetwork that provides a framework to create decentralized peer-to-peer network
applications with.
"""


class SecureNode(Node):
    """This class is a concrete implementation of the Node class and communicates with JSON between the nodes.
    It implements a secure communication between the nodes. Not that the communication is encrypted, but
    more on the tampering aspect. Messages are checked on the integrity (due to signing). A public/private
    RSA key infrastructure is used to implement this. Furthermore, it implements a basic ping/pong system and
    discovery. Using this node, you are able to implement your own protocol on top. All messages that are send
    (make sure you use create_message method) are signed and checked when received.

    Instantiates a SecureNode that extends the Node class by secure functionality.
      host: The host name or ip address that is used to bind the TCP/IP server to.
      port: The port number that is used to bind the TCP/IP server to.

    After instantiation, you nee to load or generate a public/private key for this node to be able to send and/or
    connect to the decentralized peer-to-peer network. This secure node is packed with all kinds of hasing and
    encryption algorithms."""

    # Python class constructor
    def __init__(self, host, port):
        """Create instance of a Node. If you want to implement the Node functionality with a callback, you should
        provide a callback method. It is preferred to implement a new node by extending this Node class.
          host: The host name or ip address that is used to bind the TCP/IP server to.
          port: The port number that is used to bind the TCP/IP server to."""
        super(SecureNode, self).__init__(host, port, None)

        # Track the discovery message that are recieved, so we know when to stop!
        self.discovery_messages = {}

        # The RSA public/private key from this node
        self.rsa_key = None

        self.blockchain = Blockchain()

    def node_message(self, connected_node, message):
        """node_message is overridden to provide secure communication using hashing and signing. The message has been
        send by using a dict data structure. The NodeConnection class already converts this back to a dict structure
        in this method.
        The check is performed by check_message, see the documentation there. When the message is valid, it will be
        processed. The field '_type' determines the packet type. Currently the following packets are implemented:
          ping: The ping packet is send by a node to check the connection and latency.
          pong: The pong packet is the reply that is send based an a ping packet.
          discovery: The discovery packet is send to discover the connection list of a connecting node.
          discovery_answer: The answer of a node to a discovery packet that holds its list of connecting nodes."""
        # try:
        print("node_message from " + connected_node.id + ": " + str(message))

        if self.check_message(message):
            if "_type" in message:
                if message["_type"] == "ping":
                    self.received_ping(connected_node, message)

                elif message["_type"] == "pong":
                    self.received_pong(connected_node, message)

                elif message["_type"] == "discovery":
                    self.received_discovery(connected_node, message)

                elif message["_type"] == "discovery_answer":
                    self.received_discovery_answer(connected_node, message)

                else:
                    self.debug_print(
                        "node_message: message type unknown: "
                        + connected_node.id
                        + ": "
                        + str(message)
                    )

        else:
            print("Received message is corrupted and cannot be processed!")

    def create_message(self, data):
        """This method creates the message based on the Python dict data variable to be sent to other nodes. Some data
        is added to the data, like the id, timestamp, message is and hash of the message. In order to check the
        message validity when a node receives it, the message is hashed and signed. The method returns a string
        of the data in JSON format, so it can be send immediatly to the node. The public key is also part of the
        communication packet."""
        for el in [
            "_id",
            "_timestamp",
            "_message_id",
            "_hash",
            "_signature",
            "_public_key",
        ]:  # Clean up the data, to make sure we calculatie the right things!
            if el in data:
                del data[el]

        try:
            data["_mcs"] = self.message_count_send
            data["_mcr"] = self.message_count_recv
            data["_id"] = self.id
            data["_timestamp"] = time.time()
            data["_message_id"] = self.get_hash(data)

            self.debug_print("Message creation:")
            self.debug_print(
                "Message hash based on: " + self.get_data_uniq_string(data)
            )

            data["_hash"] = self.get_hash(data)

            self.debug_print(
                "Message signature based on: " + self.get_data_uniq_string(data)
            )

            data["_signature"] = self.sign_data(data)
            data["_public_key"] = self.get_public_key().decode("utf-8")

            self.debug_print("_hash: " + data["_hash"])
            self.debug_print("_signature: " + data["_signature"])
            self.debug_print("_public_key: " + data["_public_key"])

            return data

        except Exception as e:
            self.debug_print("SecureNode: Failed to create message " + str(e))

    def check_message(self, data):
        """When a message is received it is hashed and signed by the sending node. This method checks the hash
        and signature of the message. When the signature, data hash and message id is correct, the method
        returns True otherwise False.
        TODO: if a node is known, the public key should be stored, so this could not be changed by the
        node in the future. That is more safe. Maybe the public key should be exchanged prior."""
        self.debug_print("Incoming message information:")
        self.debug_print("_hash: " + data["_hash"])
        self.debug_print("_signature: " + data["_signature"])

        signature = data["_signature"]
        public_key = data["_public_key"]
        data_hash = data["_hash"]
        message_id = data["_message_id"]
        timestamp = data["_timestamp"]

        # 1. Check the signature!
        del data["_public_key"]
        del data["_signature"]
        checkSignature = self.verify_data(data, public_key, signature)

        # 2. Check the hash of the data
        del data["_hash"]
        checkDataHash = self.get_hash(data) == data_hash

        # 3. Check the message id
        del data["_message_id"]
        checkMessageId = self.get_hash(data) == message_id

        # 4. Restore the data
        data["_signature"] = signature
        data["_public_key"] = public_key
        data["_hash"] = data_hash
        data["_message_id"] = message_id
        data["_timestamp"] = timestamp

        self.debug_print("Checking incoming message:")
        self.debug_print(" signature : " + str(checkSignature))
        self.debug_print(" data hash : " + str(checkDataHash))
        self.debug_print(" message id: " + str(checkMessageId))

        return checkSignature and checkDataHash and checkMessageId

    def send_message(self, message):
        """This method sends a string to all the nodes in the format {"message": message}. It uses also
        the create_message method in order to hash and sign the message as well."""
        self.send_to_nodes(
            self.create_message({"_type": "message", "message": message})
        )

    #######################################################
    # Hashing of Python variables methods                 #
    #######################################################

    def get_data_uniq_string(self, data):
        """This function makes sure that a complex dict variable (consisting of other dicts and lists,
        is converted to a unique string that can be hashed. Every data object that contains the same
        values, should result into the dame unique string."""
        return json.dumps(data, sort_keys=True)

    def get_hash(self, data):
        """Returns the hased version of the data dict. The dict can contain lists and dicts, but it must
        be based as dict."""
        try:
            h = hashlib.sha512()
            message = self.get_data_uniq_string(data)

            self.debug_print("Hashing the data:")
            self.debug_print("Message: " + message)

            h.update(message.encode("utf-8"))

            self.debug_print("Hash of the message: " + h.hexdigest())

            return h.hexdigest()

        except Exception as e:
            print("Failed to hash the message: " + str(e))

    #######################################################
    # RSA En-Decryption methods                           #
    #######################################################

    def get_public_key(self):
        """Return the public key that is generated or loaded for this node."""
        return self.rsa_key.publickey().exportKey("PEM")

    def get_private_key(self):
        """Get the private key that is generated or loaded for this node."""
        return self.rsa_key.exportKey("PEM")

    def encrypt(self, message, public_key):
        """Encrypt a message using a public key, most of the time from someone else."""
        try:
            key = RSA.importKey(public_key)
            cipher = PKCS1_v1_5_Cipher.new(key)
            return b64encode(cipher.encrypt(message))

        except Exception as e:
            print("Failed to encrypt the message: " + str(e))

    def decrypt(self, ciphertext):
        """Decrypt a ciphertext message that has been encrypted with our public key by someone else."""
        try:
            ciphertext = b64decode(ciphertext)
            cipher = PKCS1_v1_5_Cipher.new(self.rsa_key)
            sentinal = "sentinal"  # What is this again?
            return cipher.decrypt(ciphertext, sentinal)

        except Exception as e:
            print("Failed to decrypt the message: " + str(e))

    def sign(self, message):
        """Sign the message using our private key based on the SHA512 hash."""
        try:
            message_hash = SHA512.new(message.encode("utf-8"))

            self.debug_print("Signing the message:")
            self.debug_print("Message to be hashed: " + message)
            self.debug_print("Hash of the message: " + message_hash.hexdigest())

            signer = PKCS1_v1_5_Signature.new(self.rsa_key)
            signature = b64encode(signer.sign(message_hash))
            return signature.decode("utf-8")

        except Exception as e:
            print("Failed to sign the message: " + str(e))

    def sign_data(self, data):
        """Sign the data (a Python dict), that is hashed, with our private key. It is converted
        to a string, so the method sign can be used."""
        message = self.get_data_uniq_string(data)
        return self.sign(message)

    def verify(self, message, public_key, signature):
        """Verify the signature, based on the message, public key and signature."""
        try:
            signature = b64decode(signature.encode("utf-8"))
            key = RSA.importKey(public_key)
            h = SHA512.new(message.encode("utf-8"))
            verifier = PKCS1_v1_5_Signature.new(key)

            self.debug_print("Message to verify: " + message)
            self.debug_print("Hash of the message: " + h.hexdigest())

            return verifier.verify(h, signature)

        except Exception as e:
            self.debug_print("verify: " + str(e))

    def verify_data(self, data, public_key, signature):
        """Verify the signature, based on the data, public key and signature. The data is converted
        to a string, so the method verify can be used."""
        message = self.get_data_uniq_string(data)
        return self.verify(message, public_key, signature)

    #######################################################
    # AES En-Decryption methods                           #
    #######################################################

    def encryption_key_from_password(self, salt, password, total_bytes_key):
        """Creates a key to be used for encryption, based on PBKDF version 2, and returns the key.
        It uses a salt to make sure it is really unguessable."""
        key = PBKDF2(password, salt, total_bytes_key)
        self.debug_print("encryption_key_from_password salt: " + str(salt))
        self.debug_print("encryption_key_from_password  key: " + str(key))
        return key

    def encrypt_aes_pad(self, s):
        """AES requires data to be in multiples of 16 bytes. If this is not the case, it is required
        to add extra bytes to the data."""
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    def encrypt_aes(self, plaintext, key, key_size=256):
        """Encrypt the plaintext with the given key. Make sure the key contains the required key size."""
        plaintext = self.encrypt_aes_pad(plaintext)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(plaintext)

    def encrypt_aes_pw(self, plaintext, password):
        """Encrypt the plaintext with the given key. Make sure the key contains the required key size."""
        plaintext = self.encrypt_aes_pad(plaintext)
        salt = Random.new().read(16)
        key = self.encryption_key_from_password(salt, password, 32)  # 256-bit key
        return salt + self.encrypt_aes(plaintext, key)

    def decrypt_aes(self, ciphertext, key):
        """Decrypt the ciphertext using the key. Return the plaintext."""
        iv = ciphertext[: AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size :])
        return plaintext.rstrip(b"\0")

    def decrypt_aes_pw(self, ciphertext, password):
        """Decrypt the ciphertext using the key. Return the plaintext."""
        salt = ciphertext[:16]
        key = self.encryption_key_from_password(salt, password, 32)  # 256-bit key
        return self.decrypt_aes(ciphertext[16:], key)

    def encrypt_aes_file(self, file_name, plaintext, key):
        """Encrypt the plaintext and put it into a file with file_name."""
        enc = self.encrypt_aes(plaintext, key)
        with open(file_name, "wb") as fo:
            fo.write(enc)

    def decrypt_aes_file(self, file_name, key):
        """Read a file and decrypt the content. Plaintext from the file is returned."""
        with open(file_name, "rb") as fo:
            ciphertext = fo.read()
        return self.decrypt_aes(ciphertext, key)

    def encrypt_aes_file_pw(self, file_name, plaintext, password):
        """Encrypt the plaintext and put it into a file with file_name using a password."""
        enc = self.encrypt_aes_pw(plaintext, password)
        with open(file_name, "wb") as fo:
            fo.write(enc)

    def decrypt_aes_file_pw(self, file_name, password):
        """Read a file and decrypt the content using a password. Plaintext from the file is returned."""
        with open(file_name, "rb") as fo:
            ciphertext = fo.read()
        return self.decrypt_aes_pw(ciphertext, password)

    #######################################################
    # Public and private key storage and retrieval        #
    #######################################################

    def key_pair_generate(self):
        self.rsa_key = RSA.generate(4096)

    def key_pair_save(self, file_name, password):
        try:
            key_string = self.rsa_key.exportKey("PEM", password)
            key_string = self.encrypt_aes_pw(key_string, password)
            with open(file_name, "wb") as fo:
                fo.write(key_string)

        except Exception as e:
            self.debug_print("key_pair_generate: " + str(e))

    def key_pair_load(self, file_name, password):
        try:
            with open(file_name, "rb") as fo:
                key_string = self.decrypt_aes_pw(fo.read(), password)
                self.rsa_key = RSA.importKey(key_string, password)

        except Exception as e:
            self.debug_print("key_pair_generate: " + str(e))

    #######################################################
    # PING / PONG Message packets                         #
    #######################################################

    def send_ping(self):
        """A ping request is send to all the nodes that are connected."""
        self.send_to_nodes(
            self.create_message(
                {"_type": "ping", "timestamp": time.time(), "id": self.id}
            )
        )

    def send_pong(self, node, timestamp):
        """A pong request is only send to the node that has send the ping request."""
        node.send(
            self.create_message(
                {
                    "_type": "pong",
                    "timestamp": timestamp,
                    "timestamp_node": time.time(),
                    "id": self.id,
                }
            )
        )

    def received_ping(self, node, data):
        """With a ping message, return a pong message to the node."""
        self.send_pong(node, data["timestamp"])

    def received_pong(self, node, data):
        """Got message back based on our ping message, check the latency of the node!"""
        latency = time.time() - data["timestamp"]
        node.set_info("ping", latency)
        self.debug_print("Received pong message with latency " + str(latency))

    #######################################################
    # DISCOVERY                                           #
    #######################################################

    def send_discovery(self):
        """Send the discovery packet to all the connected nodes.
        TODO: Improve discovery information that is send back by the nodes."""
        self.send_to_nodes(
            self.create_message(
                {"_type": "discovery", "id": self.id, "timestamp": time.time()}
            )
        )

    def send_discovery_answer(self, node, data):
        """Send the discovery_answer packet to a specific node (mostly were we received a discovery packet
        from). This packet contains a list of all the nodes with which we have a connection with."""
        nodes = []
        for n in self.nodes_inbound:
            nodes.append(
                {
                    "id": n.id,
                    "ip": n.host,
                    "port": n.main_node.port,
                    "connection": "inbound",
                }
            )
        for n in self.nodes_outbound:
            nodes.append(
                {"id": n.id, "ip": n.host, "port": n.port, "connection": "outbound"}
            )

        node.send(
            self.create_message(
                {
                    "id": data["id"],
                    "_type": "discovery_answer",
                    "timestamp": data["timestamp"],
                    "nodes": nodes,
                }
            )
        )

    def received_discovery(self, node, data):
        """This method processes the discovery packet and send back a discover_anwser_message with the details
        and relay it to the other hosts, when I got the answers from them  send it through. This means i
        need to administer these messages as well to relay it back."""
        if data["id"] in self.discovery_messages:
            self.debug_print(
                "discovery_message: message already received, so not sending it"
            )

        else:
            self.debug_print("discovery_message: process message")
            self.discovery_messages[data["id"]] = node
            self.send_discovery_answer(node, data)
            self.send_to_nodes(
                self.create_message(
                    {
                        "_type": "discovery",
                        "id": data["id"],
                        "timestamp": data["timestamp"],
                    }
                ),
                [node],
            )

    def received_discovery_answer(self, node, data):
        """This method processes the discovery_answer packet. In the case it is not mine, the packet is relayed
        to the correct node. Nothing is done with this information.
        TODO: A method to process this information should be invoked."""
        if data["id"] in self.discovery_messages:  # needs to be relayed
            self.send_discovery_answer(self.discovery_messages[data["id"]], data)

        else:
            if data["id"] == self.id:
                self.debug_print(
                    "discovery_message_answer: This is for me!: "
                    + str(data)
                    + ":"
                    + str(time.time() - data["timestamp"])
                )

            else:
                self.debug_print("unknwon state!")
