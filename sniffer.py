from scapy.all import sniff, IP, TCP, UDP, ICMP, Raw
from datetime import datetime

packet_count = 0

def process_packet(packet):
    global packet_count

    # Sirf IP packets dekhenge
    if IP not in packet:
        return

    packet_count += 1
    src_ip = packet[IP].src
    dst_ip = packet[IP].dst

    # Protocol pehchanen
    if TCP in packet:
        protocol = "TCP"
        src_port = packet[TCP].sport
        dst_port = packet[TCP].dport
    elif UDP in packet:
        protocol = "UDP"
        src_port = packet[UDP].sport
        dst_port = packet[UDP].dport
    elif ICMP in packet:
        protocol = "ICMP"
        src_port = "-"
        dst_port = "-"
    else:
        protocol = "Other"
        src_port = "-"
        dst_port = "-"

    # Payload (data) nikalein, pehle 50 bytes
    if Raw in packet:
        payload = packet[Raw].load[:50]
    else:
        payload = "No payload"

    time_now = datetime.now().strftime("%H:%M:%S")

    print("=" * 60)
    print(f"Packet #{packet_count}  Time: {time_now}")
    print(f"Source IP      : {src_ip}:{src_port}")
    print(f"Destination IP : {dst_ip}:{dst_port}")
    print(f"Protocol       : {protocol}")
    print(f"Payload        : {payload}")

    # Log file mein bhi save karein
    with open("packets_log.txt", "a") as f:
        f.write(f"{time_now} | {src_ip} -> {dst_ip} | {protocol} | {src_port}->{dst_port}\n")


print("Sniffer start ho gaya... band karne ke liye Ctrl+C dabayen")

# count=0 ka matlab jab tak band na karein capture chalta rahe
sniff(prn=process_packet, store=False, count=0)