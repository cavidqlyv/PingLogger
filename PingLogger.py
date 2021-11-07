# create fuction that sends ping every second to google dns
# if ping is not successful write to file

import subprocess
import time

def maxping():
    """This function Checks the ping and categorizes ping information"""
    #Ping google dns
    result = subprocess.run(["ping", "-c", "1", "8.8.8.8"], stdout=subprocess.PIPE)
    
    #Get ping result
    output = result.stdout.decode("utf-8")
    
    #Find the line that contains the Packet informations
    packets_transmited_start_index=output.split().index("Packets:")
    packet_info=output.split()[packets_transmited_start_index:packets_transmited_start_index+12]
    
    #Find the line that contains the Maximum ping time
    maxping=int(output.split()[output.split().index("Maximum")+2][:2])
    
    #Detailed information about the ping
    print(' '.join([str(elem) for elem in packet_info])[:-1], "MaxPing :", maxping)


    #Categorize the ping information
    if "0% loss" in output:
        return 0
    elif "100% loss" in output:
        return "0 packet sent;"+ str(maxping) + "ms;" + str(time.ctime())+"\n"
    elif maxping>250:
        return "high ping;"+ str(maxping) + "ms;" + str(time.ctime())+"\n"
    else:
        return "packet lost;" + str(maxping) + "ms;" + str(time.ctime())+"\n"


def write_to_file(info,filename="ping.csv"):
    """This file writes information to the created file"""
    f = open(filename, "a")
    f.write(info)
    f.close()


def main():
    while True:
        pingobj=maxping()
        if pingobj!=0:
            print(pingobj)
            write_to_file(pingobj,filename="ping.csv")
        time.sleep(0.01)

if __name__=="__main__":
    main()