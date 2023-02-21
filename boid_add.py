import pickle
import pprint
import re

clear_line = '\033[A                                                                                                  ' \
             '\033[A '
valid = re.compile(r'\d+')
filename = 'boid.pkl'
try:
    rfile = open(filename, 'rb')
    data = pickle.load(rfile)
    pprint.pprint(data)
    rfile.close()
except EOFError:
    data = {}
    wfile = open(filename, 'wb')
    pickle.dump(data, wfile)
    wfile.close()
except FileNotFoundError:
    data = {}
    wfile = open(filename, 'wb')
    pickle.dump(data, wfile)
    wfile.close()
    
yn = input("\nAdd more (y/[n]) ")   
while True:
    if yn.lower() == 'n' or yn == '':
        print(clear_line)
        break
    elif yn.lower() == 'y':
        boid = input("Enter Boid: ")
        match = valid.search(boid)
        try:
            num = match.group()
            if len(num) != 16 or num is None or int(num)//(10**13) != 130:
                print(clear_line)
                print(clear_line)
                print("boid should have 16 digits starting with '130'  ")
                continue
        except AttributeError:
            print(clear_line)
            print(clear_line)
            print("invalid.....")
            continue
        while True:
            name = input("Enter Name: ")
            if name != '':
                pass
            if name.title() in data.values():
                print("Name already there... Choose different name")
            else:
                break
        data.setdefault(boid, name.title())
        yn = input("Add more (y/[n]) ")
    else:
        print(clear_line)
        yn = input("Add more (y/[n]) ")
    wfile = open(filename, 'wb')
    pickle.dump(data, wfile)
    wfile.close()
    
yn = input("Remove some (y/[n]) ")
while True:
    if yn.lower() == 'n' or yn == '':
        print(clear_line)
        break
    elif yn.lower() == 'y':
        print(clear_line)
        rem = input("Enter name to remove: ")
        not_found = True
        for k, v in data.items():
            if v.lower() == rem.lower():
                del data[k]
                print("-----Removed----- " + v + " : " + k)
                not_found = False
                break
        if not_found:
            print(clear_line)
            print("Sorry, Not in there......\n")
            continue
        yn = input("Remove some (y/[n]) ")
    else:
        yn = input("Remove some (y/[n]) ")
        print(clear_line)
    wfile = open(filename, 'wb')
    pickle.dump(data, wfile)
    wfile.close()

print("\n\nTask Completed Successfully\n")
pprint.pprint(data)
