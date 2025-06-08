# Challenge Solution

1. Export https objects, containing an image “`image.jpg`" with `CTF{5tAnd02d_` 
2. Base64 decode `f0reNs_F-R-E-E_` from DNS. Get a script to decode the domain names of queries or responses, then change it to remove all the actual domains and keep the remaining base64 parts. (Script below)
3. Find `flag_piece!}` in the (very random and unrealistic) payload of packets 510 and 511.
- Script for part 2:
    
    ```python
    import base64
    from scapy.all import rdpcap, DNSQR, DNSRR
    
    def base64_decode(domain_name):
        try:
            decoded_name = base64.b64decode(domain_name).decode('utf-8')
            return decoded_name
        except Exception as e:
            return f"Error decoding {domain_name}: {e}"
    
    def extract_domain_names(pcap_file):
        packets = rdpcap(pcap_file)
        domain_names = set()
    
        for packet in packets:
            if packet.haslayer(DNSQR):
                query_name = packet[DNSQR].qname.decode('utf-8').strip('.')
                domain_names.add(query_name)
            if packet.haslayer(DNSRR):
                response_name = packet[DNSRR].rrname.decode('utf-8').strip('.')
                domain_names.add(response_name)
    
        return domain_names
    
    def main(pcap_file):
        domain_names = extract_domain_names(pcap_file)
        for domain_name in domain_names:
            decoded_name = base64_decode(domain_name.replace("fakegrifflesctfwebsite.com", ""))
            print(f"Original: {domain_name}, Decoded: {decoded_name}")
    
    if __name__ == "__main__":
        pcap_file = "ctf_challenge.pcap"
        main(pcap_file)
    ```
    

# Comments

*While this challenge should be trivial to an experienced CTF player, those who have just installed Wireshark may face difficulties and might attempt more brute-force-like approaches to solve this challenge.*

*The intention of this challenge is for experienced players to breeze through this challenge as they would have seen each indicator before and should pick up on them — (1) Many HTTP packets ⇒ export HTTP objects, (2) Lots of base64, clearly DNS tunnelling ⇒ Write/generate a script to decode all of it, and (3) A bunch of plaintext payloads ⇒ just scroll through quickly and eyeball it, or search for a curly brace, or write a script to consolidate all the payloads.* 

*Setting this, I also hope for it not to be too annoying to guess the solution, like an odd way of obfuscating the flag in the payloads etc. I also hope for it to have some similarities with real-world interesting traffic like the DNS tunnelling.* 

*For less-experienced players hopefully it could be a good starting point to learn about these three low-hanging fruits commonly found in the easiest network capture analysis challenges.* 

*Note that parts 2 and 3 can also be trivially solved with the strings command, but it could depend on how good your eyeballs are.* 

# The Flag

Flag: `grifflesCTF{5tAnd02d_f0reNs_F-R-E-E_flag_piece!}`