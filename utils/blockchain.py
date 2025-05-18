import hashlib
import json
import time
import pickle
import os
from datetime import datetime

class Block:
    """
    A class representing a block in the blockchain
    
    Attributes:
        index (int): Position of the block in the chain
        timestamp (float): Time when the block was created
        records (list): Medical records contained in this block
        previous_hash (str): Hash of the previous block
        hash (str): Hash of the current block
        nonce (int): Number used for mining/proof-of-work
    """
    
    def __init__(self, index, timestamp, records, previous_hash=''):
        """
        Initialize a new block
        
        Args:
            index (int): Position of the block in the chain
            timestamp (float): Time when the block was created
            records (list): Medical records to store in this block
            previous_hash (str, optional): Hash of the previous block
        """
        self.index = index
        self.timestamp = timestamp
        self.records = records
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash()
    
    def calculate_hash(self):
        """
        Calculate the hash of this block using SHA-256
        
        Returns:
            str: The hash value as a hexadecimal string
        """
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "records": self.records,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        
        return hashlib.sha256(block_string).hexdigest()
    
    def mine_block(self, difficulty):
        """
        Mine a block (Proof of Work)
        
        Args:
            difficulty (int): Number of leading zeros required in hash
        """
        target = '0' * difficulty
        
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
            
        print(f"Block mined: {self.hash}")
    
    def to_dict(self):
        """Convert block to dictionary for serialization"""
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "records": self.records,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }
    
    @classmethod
    def from_dict(cls, block_dict):
        """Create block instance from dictionary"""
        block = cls(
            block_dict["index"],
            block_dict["timestamp"],
            block_dict["records"],
            block_dict["previous_hash"]
        )
        block.nonce = block_dict["nonce"]
        block.hash = block_dict["hash"]
        return block

class Blockchain:
    """
    A class representing the blockchain for medical records
    
    Attributes:
        chain (list): List of blocks in the chain
        difficulty (int): Mining difficulty (# of leading zeros)
        pending_records (list): Records waiting to be added to a block
    """
    
    def __init__(self):
        """Initialize a new blockchain with a genesis block"""
        self.chain = []
        self.difficulty = 2  # Mining difficulty
        self.pending_records = []
        
        # Create genesis block if the chain is empty
        if not self.chain:
            self.add_genesis_block()
    
    def add_genesis_block(self):
        """Create and add the genesis (first) block to the chain"""
        genesis_block = Block(0, time.time(), ["Genesis Block - EHR Blockchain System"], "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)
        self.save()
    
    def get_latest_block(self):
        """Get the most recent block in the chain"""
        return self.chain[-1]
    
    def add_record(self, record):
        """
        Add a medical record to pending records
        
        Args:
            record (dict): Medical record to add
        """
        # Add timestamp to record
        record['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.pending_records.append(record)
        return len(self.pending_records)
    
    def mine_pending_records(self, mining_reward_address=None):
        """
        Mine pending records into a new block
        
        Args:
            mining_reward_address (str, optional): Address to receive mining reward
        """
        if not self.pending_records:
            return False
            
        new_block = Block(
            len(self.chain),
            time.time(),
            self.pending_records.copy(),
            self.get_latest_block().hash
        )
        
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        
        # Clear pending records
        self.pending_records = []
        
        # Save blockchain to file
        self.save()
        return True
    
    def is_chain_valid(self):
        """
        Validate the blockchain integrity
        
        Returns:
            bool: True if valid, False otherwise
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            # Check if current block hash is valid
            if current_block.hash != current_block.calculate_hash():
                print("Invalid hash")
                return False
                
            # Check if previous hash reference is correct
            if current_block.previous_hash != previous_block.hash:
                print("Invalid previous hash reference")
                return False
                
        return True
    
    def get_records_for_patient(self, patient_id):
        """
        Get all records for a specific patient
        
        Args:
            patient_id: ID of the patient
            
        Returns:
            list: List of medical records for the patient
        """
        patient_records = []
        
        # Check each block for records belonging to the patient
        for block in self.chain:
            for record in block.records:
                if isinstance(record, dict) and record.get('patient_id') == patient_id:
                    # Add block info to the record
                    record_with_block = record.copy()
                    record_with_block['block_index'] = block.index
                    record_with_block['block_hash'] = block.hash
                    record_with_block['block_timestamp'] = block.timestamp
                    patient_records.append(record_with_block)
        
        return patient_records
    
    def get_records_for_doctor(self, doctor_id):
        """
        Get all records created by a specific doctor
        
        Args:
            doctor_id: ID of the doctor
            
        Returns:
            list: List of medical records created by the doctor
        """
        doctor_records = []
        
        # Check each block for records created by the doctor
        for block in self.chain:
            for record in block.records:
                if isinstance(record, dict) and record.get('doctor_id') == doctor_id:
                    # Add block info to the record
                    record_with_block = record.copy()
                    record_with_block['block_index'] = block.index
                    record_with_block['block_hash'] = block.hash
                    record_with_block['block_timestamp'] = block.timestamp
                    doctor_records.append(record_with_block)
        
        return doctor_records
    
    def save(self):
        """Save blockchain to file"""
        # Create data directory if it doesn't exist
        os.makedirs("data", exist_ok=True)
        
        # Save to pickle file
        with open("data/blockchain.pkl", "wb") as f:
            pickle.dump(self, f)
    
    @staticmethod
    def load():
        """Load blockchain from file"""
        try:
            with open("data/blockchain.pkl", "rb") as f:
                return pickle.load(f)
        except (FileNotFoundError, EOFError):
            return Blockchain()  # Return new blockchain if file doesn't exist
    
    def to_dict(self):
        """Convert blockchain to dictionary for serialization"""
        return {
            "chain": [block.to_dict() for block in self.chain],
            "difficulty": self.difficulty,
            "pending_records": self.pending_records
        }
    
    @classmethod
    def from_dict(cls, blockchain_dict):
        """Create blockchain instance from dictionary"""
        blockchain = cls()
        blockchain.chain = [Block.from_dict(block_dict) for block_dict in blockchain_dict["chain"]]
        blockchain.difficulty = blockchain_dict["difficulty"]
        blockchain.pending_records = blockchain_dict["pending_records"]
        return blockchain
