The contents of this folder are shared between your host computer and all the running containers of kathara.

You can find this folder in the network containers in the path: 
/shared

This folder contains a .pcap file, which contains some captured packet.
To generate these packets we have launched netcat in server mode on s1 and netcat in client mode on pc1.
Then we have launched tcpdump on interface eth0 of r1.
You can open the .pcap file on your computer with wireshark, for example

We first sent a packet from pc1 to s1 containing the string "hey, how are you?" to s1 (can you spot it in the .pcap file?).
Then from s1 to pc1 we sent the string "fine thanks".


