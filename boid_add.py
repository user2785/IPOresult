import pickle
import pprint
import re
from utils.func import load_boid, clear_line


VALID_BOID = re.compile(r'^130\d{13}$')
FILENAME = 'data/boid.pkl'

try:
    data = load_boid(FILENAME)
except (FileNotFoundError, EOFError):
    data = {}
    with open(FILENAME, 'wb') as f:
        pickle.dump(data, f)

pprint.pprint(data)

while True:
    yn = input("\nAdd more (y/[n]) ")
    if yn.lower() == 'n' or yn == '':
        clear_line(1)
        break
    elif yn.lower() == 'y':
        while True:
            boid = input("Enter BOID: ")
            if VALID_BOID.match(boid):
                if boid in data:
                    clear_line(2)
                    print("BOID already exists. Please enter a different BOID.")
                else:
                    break
            else:
                clear_line(2)
                print("Invalid BOID. BOID should have 16 digits starting with '130'.")
        while True:
            name = input("Enter Name: ")
            if name.strip() != '':
                if name.title() in data.values():
                    print("Name already exists. Please enter a different name.")
                else:
                    data[boid] = name.title()
                    break
            else:
                print("Name cannot be empty.")
        with open(FILENAME, 'wb') as f:
            pickle.dump(data, f)
    else:
        clear_line(1)

while True:
    yn = input("Remove some (y/[n]) ")
    if yn.lower() == 'n' or yn == '':
        clear_line(1)
        break
    elif yn.lower() == 'y':
        name_to_remove = input("Enter name to remove: ")
        found = False
        for k, v in data.items():
            if v.lower() == name_to_remove.lower():
                del data[k]
                clear_line(2)
                print(f"Removed {v}: {k}")
                found = True
                break
        if not found:
            clear_line(2)
            print("Name not found.")
        with open(FILENAME, 'wb') as f:
            pickle.dump(data, f)
    else:
        clear_line(1)

print("\n\nTask Completed Successfully\n")
pprint.pprint(data)