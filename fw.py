#!/usr/bin/env python3

# IMPORTANT: Change your adapter name to correct one in line 175
# Add 2 files to directory "blocked.log" and "notifications.log"
# Program will block IP for 10 minutes after 3 packets from same IP. You can extend blocking time if you will.

import subprocess
from collections import defaultdict
from datetime import datetime, timedelta
import threading
import time
import logging
import os


# Configure logging to display output in the terminal
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")

# Global variables
scan_tracker = defaultdict(lambda: {"count": 0, "timestamp": None})
BLOCK_DURATION = timedelta(minutes=10)  # Duration to block an IP
SCAN_LIMIT = 2  # Number of scans allowed before blocking
logged_blocked_ips = set()  # Track logged blocked IPs
blocked_ips_log = {}  # Track blocked IPs and their block counts

def block_icmp(ip):
    """Block ICMP (ping) requests from the given IP."""
    try:
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-p", "icmp", "--icmp-type", "echo-request", "-j", "DROP"], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error blocking ICMP for IP {ip}: {e}")

def is_ip_blocked(ip):
    """Check if the IP is already blocked in iptables."""
    try:
        result = subprocess.run(["sudo", "iptables", "-L", "-n"], stdout=subprocess.PIPE, text=True)
        return ip in result.stdout
    except subprocess.CalledProcessError as e:
        logging.error(f"Error checking IP {ip}: {e}")
        return False
    
def update_blocked_log(ip):
    """Update the blocked.log file with the given IP and its block count."""
    log_file = "blocked.log"
    blocked_ips = {}

    # Read existing blocked IPs from the log file
    try:
        with open(log_file, "r") as file:
            for line in file:
                parts = line.strip().split(" - ")
                if len(parts) == 2:
                    blocked_ip, count = parts
                    blocked_ips[blocked_ip] = int(count)
    except FileNotFoundError:
        pass  # If the file doesn't exist, we'll create it

    # Update the count for the given IP
    if ip in blocked_ips:
        blocked_ips[ip] += 1
    else:
        blocked_ips[ip] = 1

    # Write the updated blocked IPs back to the log file
    with open(log_file, "w") as file:
        for blocked_ip, count in blocked_ips.items():
            file.write(f"{blocked_ip} - {count}\n")
            
def block_nmap_scans():
    """Block Nmap scans."""
    try:
        # Block ICMP echo requests
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-p", "icmp", "--icmp-type", "echo-request", "-j", "DROP"], check=True)
        # Block TCP SYN scans
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-p", "tcp", "--tcp-flags", "SYN,ACK,FIN,RST", "SYN", "-j", "DROP"], check=True)
        # Block UDP scans
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-p", "udp", "-j", "DROP"], check=True)
        # Block IP protocol scans
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-p", "ip", "-j", "DROP"], check=True)
        # Block all incoming traffic
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-j", "DROP"], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error blocking Nmap scans: {e}")

if __name__ == "__main__":
    block_nmap_scans()
    
            
def block_icmp(ip):
    """Block ICMP (ping) requests from the given IP."""
    try:
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-p", "icmp", "--icmp-type", "echo-request", "-j", "DROP"], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error blocking ICMP for IP {ip}: {e}")
            
def redirect_suspicious_traffic(ip):
    """Redirect suspicious traffic to a non-existent service."""
    try:
        subprocess.run(["sudo", "iptables", "-t", "nat", "-A", "PREROUTING", "-s", ip, "-p", "tcp", "--dport", " 9999", "-j", "REDIRECT", "--to-port", "9999"], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error redirecting traffic for IP {ip}: {e}")
        
def limit_connection_rate(ip):
    """Limit the number of connection attempts from a single IP."""
    try:
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-p", "tcp", "--dport", "22", "-m", "connlimit", "--connlimit-above", "1", "-j", "REJECT"], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error limiting connection rate for IP {ip}: {e}")
        
def send_notification(title, message):
    """Log a notification to a file."""
    with open("notifications.log", "a") as file:
        file.write(f"{title}: {message}\n")
            

def block_ip(ip):
    """Block the given IP using iptables and log it in blocked.log."""
    if is_ip_blocked(ip):
        logging.info(f"IP {ip} is already blocked. Skipping...")
        return

    logging.info(f"Blocking IP: {ip}")
    try:
        # Block all traffic from the IP
        if ":" in ip:  # IPv6 address
            subprocess.run(["sudo", "ip6tables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
        else:  # IPv4 address
            subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
        # Block ICMP Echo Requests (ping) from the IP
        block_icmp(ip)
        # Redirect suspicious traffic
        redirect_suspicious_traffic(ip)
        # Limit connection rate
        limit_connection_rate(ip)
        # Update the blocked.log file
        update_blocked_log(ip)
        # Send a notification
        send_notification("IP Blocked", f"The IP {ip} has been blocked.")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error blocking IP {ip}: {e}")

def unblock_ip(ip):
    """Unblock the given IP using iptables."""
    logging.info(f"Unblocking IP: {ip}")
    try:
        # Check if the rule to block the IP address exists
        result = subprocess.run(["sudo", "iptables", "-n", "-L", "INPUT"], stdout=subprocess.PIPE, text=True)
        if ip in result.stdout:
            # Remove the DROP rule for the IP
            subprocess.run(["sudo", "iptables", "-D", "INPUT", "-s", ip, "-j", "DROP"], check=True)
            # Remove the ICMP Echo Request block for the IP
            subprocess.run(["sudo", "iptables", "-D", "INPUT", "-s", ip, "-p", "icmp", "--icmp-type", "echo-request", "-j", "DROP"], check=True)
            # Send a desktop notification # DOES NOT WORK PROPERLY CURRENTLY
            send_notification("Unblocked IP", f"IP {ip} has been unblocked.")
        else:
            logging.info(f"Rule to block IP {ip} does not exist. Skipping...")
    except subprocess.CalledProcessError as e:
        logging.error(f"Error unblocking IP {ip}: {e}")
        
        
def unblock_expired_ips():
    """Unblock IPs whose block duration has expired."""
    current_time = datetime.now()
    for ip, data in list(scan_tracker.items()):
        if data["timestamp"] and current_time - data["timestamp"] > BLOCK_DURATION:
            unblock_ip(ip)
            del scan_tracker[ip]  # Remove from tracker
            logged_blocked_ips.discard(ip)  # Remove from logged blocked IPs set

def monitor_traffic():
    """Monitor network traffic for suspicious activity."""
    try:
        # Use tcpdump to capture SYN, UDP, and ICMP traffic
        tcpdump_process = subprocess.Popen(
            ["sudo", "tcpdump", "-i", "enp42s0", "-l", "-n", "(tcp[tcpflags] & (tcp-syn) != 0) or udp or icmp"],
            stdout=subprocess.PIPE, text=True
        )
        logging.info("tcpdump started successfully.")

        for line in tcpdump_process.stdout:
            # Parse tcpdump output to extract source IP
            parts = line.split()
            src_ip = parts[2].split(".")[0:4]  # Extract the first 4 parts of the IP
            src_ip = ".".join(src_ip)  # Join into a full IP address

            # Skip processing if the IP is already blocked
            if is_ip_blocked(src_ip):
                if src_ip not in logged_blocked_ips:
                    logging.info(f"IP {src_ip} is already blocked. Skipping...")
                    logged_blocked_ips.add(src_ip)  # Add to the set of logged blocked IPs
                continue  # Skip to the next packet

            logging.info(f"Detected packet from IP: {src_ip}")

            # Update scan count and timestamp
            current_time = datetime.now()
            if scan_tracker[src_ip]["timestamp"] and current_time - scan_tracker[src_ip]["timestamp"] > BLOCK_DURATION:
                # Reset tracker if the block duration has expired
                scan_tracker[src_ip] = {"count": 0, "timestamp": None}
                logging.info(f"Reset tracker for IP: {src_ip}")

            scan_tracker[src_ip]["count"] += 1
            scan_tracker[src_ip]["timestamp"] = current_time
            logging.info(f"Updated scan count for IP {src_ip}: {scan_tracker[src_ip]['count']}")

            # Check if the IP has exceeded the scan limit
            if scan_tracker[src_ip]["count"] > SCAN_LIMIT:
                logging.info(f"IP {src_ip} exceeded scan limit, blocking for {BLOCK_DURATION}...")
                block_ip(src_ip)
                logged_blocked_ips.add(src_ip)  # Log the blocked IP
                blocked_ips_log[src_ip] = scan_tracker[src_ip]["count"]  # Log the count of blocks
                # Schedule unblock in a separate thread after BLOCK_DURATION
                unblock_time = current_time + BLOCK_DURATION
                logging.info(f"IP {src_ip} will be unblocked at {unblock_time.strftime('%Y-%m-%d %H:%M:%S')}")
                threading.Timer(BLOCK_DURATION.total_seconds(), unblock_ip, args=(src_ip,)).start()
                # Reset the scan count after blocking
                scan_tracker[src_ip]["count"] = 0

                # Block incoming traffic on all ports, except for SSH, HTTP, and HTTPS
                block_all_ports(src_ip)

    except Exception as e:
        logging.error(f"Error monitoring traffic: {e}")

def block_all_ports(ip):
    """Block incoming traffic on all ports, except for SSH, HTTP, and HTTPS."""
    try:
        # Block all incoming traffic on all ports
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
        # Allow incoming traffic on SSH, HTTP, and HTTPS ports
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-p", "tcp", "--dport", "22", "-j", "ACCEPT"], check=True)
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-p", "tcp", "--dport", "80", "-j", "ACCEPT"], check=True)
        subprocess.run(["sudo", "iptables", "-A", "INPUT", "-s", ip, "-p", "tcp", "--dport", "443", "-j", "ACCEPT"], check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Error blocking all ports for IP {ip}: {e}")

if __name__ == "__main__":
    # Start monitoring traffic in a separate thread
    threading.Thread(target=monitor_traffic, daemon=True).start()

    # Periodically unblock expired IPs
    while True:
        unblock_expired_ips()
        time.sleep(60)  # Check every minute
