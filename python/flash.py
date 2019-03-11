import subprocess
import sys
import glob
import serial
import os

baud_rate = "115200"
platform = "esp32"

# Get path of exe file running and cd to it

path = getattr(sys, '_MEIPASS', os.getcwd())
os.chdir(path)


# Scan for COM ports

def scan_serial_ports():
    
    # Thanks to @Thomas for parts of this function code :)
    # https://stackoverflow.com/questions/12090503/listing-available-com-ports-with-python

    ports = ['COM%s' % (i + 1) for i in range(20)]

    result = []
    
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result


# Detect changes in COM ports

input("Please make sure your device in unplugged, then press enter")

list_a = scan_serial_ports()

input("Now plug in your device, then press enter")

list_b = scan_serial_ports()


# Return new COM port as esp32 port

def returnNonMatches(li1, li2): 
    return (list(set(li1) - set(li2))) 

com_port = (returnNonMatches(list_b, list_a)[0])
#com_port = COM6 # Use this as a override

print("Your device is running on:")
print(com_port)


# Flash binaries

binary_files = {
    "bootloader" : ["0x1000", ".\\bootloader.bin"],
    "partitions" : ["0x8000", ".\\partitions_mgos.bin"],
    "otadata" : ["0xd000", ".\\otadata.bin"],
    "app" : ["0x10000", ".\\app1.bin"],
    "fs" : ["0x190000", ".\\fs.img"]
}

def flash_mongoose():
    for binary in binary_files:
        subprocess.Popen([".\esptool.exe", "-p", com_port, "-b", baud_rate, "-c", platform, "write_flash", binary_files[binary][0], binary_files[binary][1]]).wait()

flash_mongoose()


# Configure wifi

wifi = input("Would you like to configure MDash and Wifi? (y for yes, anything else for no)")

if str(wifi).lower() == "y":
    input("Your board has brand new firmware on it. In order to configure settings, please unplug and plug the board back in, then press ENTER")

    print("Configuring wifi with MOS tool to allow for MDASH integration. Please get your access key from: ")
    print("https://mongoose-os.com/docs/mongoose-os/quickstart/setup.md#8-add-device-to-the-mdash-management-dashboard")

    wifi_ssid = input("Please enter your wifi SSID: ")
    wifi_pass = input("Please enter your wifi PASS: ")
    mdash_token = input("Please enter your MDASH access token: ")    

    print("Configuring wifi...")
    subprocess.Popen([".\mos.exe", "--port", com_port, "wifi", str(wifi_ssid), str(wifi_pass)]).wait()
    
    print("Configuring MDASH")
    subprocess.Popen([".\mos.exe", "--port", com_port, "config-set", "dash.enable=true", ("dash.token=" + str(mdash_token))]).wait()
        
else:
    input("All done - press ENTER to quit")
    sys.exit() 

input("All done - press ENTER to quit")