print("Loading Modules....", end='')

from utils.browsers import *
from utils.func import *
import warnings
from silence_tensorflow import silence_tensorflow
from colorama import init
import os
print('..completed')


sheet = import_excel("data/results.xlsx")
data = load_boid("data/boid.pkl")

print("Starting Browser...",end='')
url = "https://iporesult.cdsc.com.np"
silence_tensorflow()
warnings.filterwarnings("ignore", category=FutureWarning, module="numpy")
#logging.disable(logging.CRITICAL)
#logging.getLogger("cc").setLevel(logging.ERROR)
#os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['WDM_LOG_LEVEL'] = '0'

init(convert=True, autoreset=True)
browser_open(url) # Call browser_open function


p,count,iter = -1, 0, 1


while True:
    try:
        sel, option = list_company()    # List Company details
        while (int(p)<0 or int(p)>=len(option)):
            p = input("\nSelect company [or '0' to check all]:  ")
            clear_line(1)
            if p == '':
                close_all()
                exit()
            continue
        p = int(p)
        if int(p) == 0:
            check_all = range(1,len(option))
        elif int(p) == None:
            close_all()
            exit()  
        else: 
            check_all = range(p,p+1)
        for i in check_all:
            sel.select_by_index(i)
            selected_company = option[i].text
            print("\n\t" + Fore.BLUE + Style.BRIGHT + str(i) + ") " + selected_company + '\n')

            # Check Result
            for boid, name in data.items():
                if check_in_excel(sheet, boid, selected_company) == False :
                    result = check(boid, name, iter)
                    iter = 0
                    allotted = re_compile(result)   # Call re_compile function
                    print_result(allotted, name)  # Call print_result function
                    xl_write(allotted, name, boid, selected_company, sheet)  # Call xl_write function
                    
        if str(input("\npress 0 to check again  ")):
            p = -1
            continue
        break

    except Exception as e:
        print(e)
        close_all()  # Call close_all function
        exit()
