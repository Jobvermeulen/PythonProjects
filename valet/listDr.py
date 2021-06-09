import psutil
import os


def disk_usage():
    obj_Disk = psutil.disk_usage('/')

    print ("Total: " + str(int(obj_Disk.total / 1024000000)) + "gb")
    print ("Uses by system: " + str(int(obj_Disk.used / 1024000000)) + "gb")
    print ("Free: " + str(int(obj_Disk.free / 1024000000)) + "gb")

def valet_routes():
    target_dir = '/Users/jobvermeulen/.config/valet/sites'

    all_routes = []
    for f in os.listdir(target_dir):
        all_routes.append(f)

    for g in all_routes:
        print('http://'+g+'.test');

def temperatures():
    print(psutil.sensors_temperatures())


def main():
    print(psutil.sensors_temperatures(fahrenheit=False))

    print('1. disk_usage \n2. valet_routes \n3. temperatures')
    try:
        integer = int(input())

        if(integer == 1):
            print("\n Disk usage:")
            disk_usage()
        elif(integer == 2):
            print("\n Valet routes:")
            valet_routes()
        elif(integer == 3):
            print("\n temperatures of your pc:")
            temperatures()
    
    except:
        print("there was an error")

if __name__ == "__main__":
    main()