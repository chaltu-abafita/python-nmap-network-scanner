from nmap import manage_nmap_scans

#Show the menu and let the user run the Nmap scanner or quit the program.
while True:
    print("\nNmap Automation Menu")
    print("1. Run Nmap scan")
    print("2. Quit")

    choice = input("\nEnter your choice (1 or 2): ")

    if choice == "1":
        manage_nmap_scans()
    elif choice == "2":
        print("Thank you for using the Nmap automation program!")
        break
    else:
        print("Invalid choice. Please enter 1 or 2.")
