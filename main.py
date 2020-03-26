# Author: Matthew Manning
# Student ID: #000967779

import sys
import time
from datetime import datetime

from hashtable import HashTable
from packageDelivery import hashTable, Package

# This is used to find the computational time of the program, time is started at beginning of program and ended
# when all packages are delivered
time_elapsed = time.process_time()


# This functions starts the interface for users to retrieve info on packages
def main():
    print('''Welcome to Western Governors University Parcel Service's Daily Local Deliveries package lookup system.''')
    print('The following commands can be used to look up information on packages: \n')
    print('1. Enter 1 in order to look up information on a single package.')
    print('2. Enter 2 in order to look up information of all packages at a specific time.')
    print('3. Enter 3 in order to exit program')
    while True:
        try:
            command = int(input('Enter command: '))
        except ValueError:
            print('Not a valid integer!')
            continue
        if command == 1:
            package_lookup()
            continue
        elif command == 2:
            all_packages()
            continue
        elif command == 3:
            print('Goodbye')
            sys.exit()
        else:
            print('Not a valid command!')
            continue


# Function for user to look up a specific package and it's information
# O(1) time complexity
def package_lookup():
    single_com = input('''Enter package ID or 'Back' to return to command list: ''')
    try:
        if single_com.lower() == 'back':
            return None
        elif isinstance(int(single_com), int):
            temp_pckg = hashTable.search(int(single_com))
            if temp_pckg is None:
                print('Package not found')
            else:
                print('Package ID: %s' % temp_pckg.packageID)
                print("Destination Address: %s %s %s %s" % (temp_pckg.address, temp_pckg.city, temp_pckg.state, temp_pckg.zip_code))
                print('Deadline for delivery: %s' % temp_pckg.deadline)
                print('Package weight: %d' % temp_pckg.weight)
                print('Special notes: %s' % temp_pckg.special_notes)
                print('Delivery status %s ' % temp_pckg.status)
                print('Loaded on truck at : %s' % temp_pckg.timestamp_start)
                print('Delivered to destination at : %s' % temp_pckg.timestamp_delivered)
        else:
            print('Not a valid command!')
    except ValueError:
        print('Not a valid command!')


# Function to look up all packages in a certain timeframe, creates temporary hash table
# to not affect packages in original hash table
# O(N) space time complexity
def all_packages():
    time_command = input('Enter time to see status of all packages at that time (Format: 00:00 AM or PM): ')
    temp_hashtable = HashTable()

    try:
        for j in range(len(hashTable.table)):
            for i in hashTable.table[j]:
                # Package at entered time is not yet loaded on to a truck,
                # changes start timestamp to entered time command
                if datetime.strptime(i[1].timestamp_start, '%I:%M %p') > datetime.strptime(time_command, '%I:%M %p'):
                    temp_package_timestamp_delivered = ''
                    temp_package_timestamp_start = time_command
                    temp_package_status = 'At Hub'
                    temp_package = Package(i[1].packageID, i[1].address, i[1].city, i[1].state, i[1].zip_code,
                                           i[1].deadline, i[1].weight, i[1].special_notes, temp_package_status,
                                           temp_package_timestamp_start, temp_package_timestamp_delivered)
                    temp_hashtable.add(i[0], temp_package)
                # Package at entered time is not yet delivered, changes start timestamp to entered time command
                elif datetime.strptime(i[1].timestamp_delivered, '%I:%M %p') > datetime.strptime(time_command,
                                                                                                 '%I:%M %p'):
                    temp_package_timestamp_delivered = ''
                    temp_package_timestamp_start = time_command
                    temp_package_status = 'On-Route'
                    temp_package = Package(i[1].packageID, i[1].address, i[1].city, i[1].state, i[1].zip_code,
                                           i[1].deadline, i[1].weight, i[1].special_notes, temp_package_status,
                                           temp_package_timestamp_start, temp_package_timestamp_delivered)
                    temp_hashtable.add(i[0], temp_package)
                # Package was delivered, uses start timestamp as time loaded on truck
                # and delivered timestamp as time delivered
                else:
                    temp_package = Package(i[1].packageID, i[1].address, i[1].city, i[1].state, i[1].zip_code,
                                           i[1].deadline, i[1].weight, i[1].special_notes, i[1].status,
                                           i[1].timestamp_start, i[1].timestamp_delivered)
                    temp_hashtable.add(i[0], temp_package)

    except ValueError:
        print('Enter time in correct format!')
    print(
        'Package ID | Address | City | State | Zip Code | Delivery Deadline | Weight | Special Notes | Timestamp for '
        'at hub or when loaded on truck | Delivery Timestamp')
    for package in temp_hashtable.sort_keys():
        print(temp_hashtable.search(package).all_details)
    temp_hashtable.table.clear()


print("{} {}".format('Total computational time: ', time_elapsed))
if __name__ == "__main__":
    main()
