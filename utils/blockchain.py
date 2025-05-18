"""
Simple blockchain implementation for the EHR Chain application.
"""

import hashlib
import json
import time
from datetime import datetime

class Block:
    """A class representing a block in the blockchain."""
    
    def __init__(self, index, timestamp, data, previous_hash):
        """
        Initialize a new block.
        
        Args:
            index (int): The position of the block in the chain
            timestamp (float): The time when the block was created
            data (dict): The data stored in the block
            previous_hash (str): The hash of the previous block
        """
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """
        Calculate the hash of the block using SHA-256.
        
        Returns:
            str: The hash value as a hexadecimal string
        """
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    
    def mine_block(self, difficulty=2):
        """
        Mine the block by finding a hash with a specific number of leading zeros.
        
        Args:
            difficulty (int): The number of leading zeros required
        """
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
    
    def get_formatted_time(self):
        """
        Get a human-readable timestamp.
        
        Returns:
            str: Formatted date and time
        """
        return datetime.fromtimestamp(self.timestamp).strftime('%Y-%m-%d %H:%M:%S')
    
    def to_dict(self):
        """
        Convert the block to a dictionary.
        
        Returns:
            dict: A dictionary representation of the block
        """
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "formatted_time": self.get_formatted_time(),
            "data": self.data,
            "previous_hash": self.previous_hash,
            "hash": self.hash,
            "nonce": self.nonce
        }

class Blockchain:
    """A class representing a blockchain."""
    
    def __init__(self):
        """Initialize a new blockchain with a genesis block."""
        self.chain = [self.create_genesis_block()]
        self.difficulty = 2
    
    def create_genesis_block(self):
        """
        Create the first block in the chain.
        
        Returns:
            Block: The genesis block
        """
        return Block(0, time.time(), {"message": "Genesis Block"}, "0")
    
    def get_latest_block(self):
        """
        Get the most recent block in the chain.
        
        Returns:
            Block: The latest block
        """
        return self.chain[-1]
    
    def add_block(self, data):
        """
        Add a new block to the chain.
        
        Args:
            data (dict): The data to be stored in the block
            
        Returns:
            Block: The newly added block
        """
        previous_block = self.get_latest_block()
        new_index = previous_block.index + 1
        new_block = Block(new_index, time.time(), data, previous_block.hash)
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        return new_block
    
    def is_chain_valid(self):
        """
        Validate the integrity of the blockchain.
        
        Returns:
            bool: True if the chain is valid, False otherwise
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            # Check if the hash is correctly calculated
            if current_block.hash != current_block.calculate_hash():
                return False
            
            # Check if the chain is linked correctly
            if current_block.previous_hash != previous_block.hash:
                return False
        
        return True
    
    def get_chain_data(self):
        """
        Get all blocks in the chain as dictionaries.
        
        Returns:
            list: A list of block dictionaries
        """
        return [block.to_dict() for block in self.chain]
