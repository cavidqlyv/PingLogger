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
    if "Maximum" in output:
        maxping=int(output.split()[output.split().index("Maximum")+2][:2])
        #Detailed information about the ping
        #print(' '.join([str(elem) for elem in packet_info])[:-1], "Maximum Ping :", maxping)
    else:
        maxping=0
    
    #Categorize the ping information
    if "Destination host unreachable." in output:
        return "Destination host unreachable;" +str(maxping) + "ms;" + str(time.ctime())+"\n"
    
    elif "General failure."  in output:
        return "General failure;" +str(maxping) + "ms;" + str(time.ctime())+"\n"
    
    elif "Request timed out." in output:
        return "Request timed out;" +str(maxping) + "ms;" + str(time.ctime())+"\n"

    elif "0% loss" not in output:
        percent_of_lost_packets=packet_info[10].split("(")[1]
        return percent_of_lost_packets+ " loss;" + str(maxping) + "ms;" + str(time.ctime())+"\n"

    elif maxping>250:
        return "high ping;"+ str(maxping) + "ms;" + str(time.ctime())+"\n"

    elif "time=" in output:
        return 0

    else:
        return output

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