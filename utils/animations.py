import streamlit as st
import time

def loading_animation(message="Loading..."):
    """
    Display a simple loading animation with a progress bar
    
    Args:
        message (str): Message to display during loading
    """
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for i in range(100):
        # Update progress bar
        progress_bar.progress(i + 1)
        
        # Update status text
        status_text.text(f"{message} {i+1}%")
        
        # Sleep for a short time to create animation effect
        time.sleep(0.01)
    
    # Clear the progress bar and status text
    progress_bar.empty()
    status_text.empty()

def blockchain_mining_animation():
    """Display animation for blockchain mining process"""
    st.markdown("⛏️ **Mining Block...**")
    
    # Create placeholder for animation
    animation_placeholder = st.empty()
    
    # Define mining steps
    mining_steps = [
        "Collecting pending transactions...",
        "Computing block hash...",
        "Finding nonce value...",
        "Validating proof of work...",
        "Adding block to chain...",
        "Updating network nodes..."
    ]
    
    # Display each step with a delay
    for step in mining_steps:
        animation_placeholder.info(step)
        time.sleep(0.5)
    
    # Show completion message
    animation_placeholder.success("Block successfully mined! ✅")
    time.sleep(1)
    
    # Clear animation placeholder
    animation_placeholder.empty()

def transaction_animation():
    """Display animation for transaction processing"""
    st.markdown("💼 **Processing Transaction...**")
    
    # Create placeholder for animation
    animation_placeholder = st.empty()
    
    # Define transaction steps
    transaction_steps = [
        "Verifying digital signatures...",
        "Checking transaction validity...",
        "Encrypting medical data...",
        "Adding to pending transactions...",
        "Broadcasting to network nodes..."
    ]
    
    # Display each step with a delay
    for step in transaction_steps:
        animation_placeholder.info(step)
        time.sleep(0.4)
    
    # Show completion message
    animation_placeholder.success("Transaction processed successfully! ✅")
    time.sleep(1)
    
    # Clear animation placeholder
    animation_placeholder.empty()
