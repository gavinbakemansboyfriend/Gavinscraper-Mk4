import sys, json, re, requests, configparser, os
from bs4 import BeautifulSoup
from time import localtime, ctime, sleep
from pprint import pprint

headers = {
        "User-Agent":"Greysec-Scraper-v1.2",
        "Cookie":""
        }
now = localtime()
start_time = "{}-{}_{}-{}-{}".format(now.tm_hour, now.tm_min, now.tm_year, now.tm_mon, now.tm_mday)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BRIGHTWHITE = '\033[97m'
    
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    PURPLE = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    GREY = '\033[90m'
    DEFAULT = '\033[39m'
    
    BIGHTRED = '\033[38;5;196m'
    CRIMSON = '\033[38;5;160m'
    ORANGE = '\033[38;5;202m'
    BRIGHTORANGE = '\033[38;5;208m'
    MAGENTA = '\033[38;5;129m'
    
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ITALIC = '\033[3m'
    INVERSE = '\033[7m'


def banner():
    os.system('color')
    print(f"""{bcolors.BIGHTRED}                #################
              #######################
            #####*######################
          ###############################
         ###################r#############
        ###################################
        ###################################
        ###           #######           ###
        #              #####              #
        #              #####              #
        ##            #######            ##
        ####        ###########        ####
        ###################################
          ##############   ##p###########
        ######$########     ###############
        #  ############################# ##
        ## #############00############# ###
        #############################  ####
         ####  ## ###   #### #### ## ##### 
          ##### ######## ### #  ## # ####  
           #### ###  #  #### ### #######
            ########## #  ### ## ######
             #################    # ##
                ##################
                 ################
{bcolors.MAGENTA}
                GAVINSCRAPER MARK 4{bcolors.DEFAULT}""")
    sleep(2)

def get_profile(uid=None):
    if uid == None:
        print("Error: function get_profile uid parameter not set")
        return False
    try:
        profile = BeautifulSoup(requests.get(f"https://www2.nwrdc.wa-k12.net/pictures/tahomas/{uid}265.JPG?rev=0", headers=headers).text, "html.parser")
        print(f"https://www2.nwrdc.wa-k12.net/pictures/tahomas/{uid}650.JPG?rev=0")
    except Exception as error:
        print(f"Exception in function get_profile: {error}")
        return False

    return profile

def parse_data(data):
    # data - BeautifulSoup object to scrape <bs4>
    username = "NULL"
    postcount = "NULL"
    threadcount = "NULL"
    # Find username
    try:
        username = data.title.text
        
    except:
        username = "IMGFOUND"

    # Find post count
    #for trow in data.find_all(class_="trow1"):
    #    if "posts per" in trow.text:
    #        try:
    #            postcount = re.search("^\d{1,10}", trow.text.replace(",","")).group().strip()
    #        except:
    #            postcount = "PARSING_ERROR"
    #
    #        break

    # Find thread count
    #for trow in data.find_all(class_="trow2"):
    #    if "threads per" in trow.text:
    #        try:
    #            threadcount = re.search("^\d{1,10}", trow.text.replace(",","")).group().strip()
    #        except:
    #            threadcount = "PARSING_ERROR"
    #            
    #        break
    userdata = {
            "username":f"{username}",
            }

    return userdata

## Main ##
##########################

banner()

# Load configuration from file
try:
    config = configparser.ConfigParser()
    config.read("scraper.conf")
    user_range = [ int(config["MAIN"]["uid_start"]), int(config["MAIN"]["uid_end"]) ]
    version = "greysec_scraper_v1.3"
    datafile = config["MAIN"]["outfile"]
    verbose = config["MAIN"]["verbose"]
except Exception as error:
    print(f"Error: {error}")
    sys.exit(1)

print("Starting GreySec Data Scraper at {}".format(ctime()))

data_output = {
        "starttime": start_time,
        "endtime": "ENDTIME",
        "data": {}
        }
try:
    for user in range(user_range[0],user_range[1] + 1):
        if user < 1000000:
            uid = "0" + str(user)
        else:
            uid = str(user)
    
        if verbose == "true":
            print(f"[*] Getting data on uid {uid}")

        html = get_profile(uid)
        if html == False: # If an error occurred in the get_profile function
            continue
        
        parsedinfo = parse_data(html)
        if parsedinfo['username'] == "IMGFOUND":
            data_output["data"][uid] = parsedinfo
            
            data = json.dumps(parse_data(html))
            with open(datafile, "a") as outfile:
                outfile.write(f"https://www2.nwrdc.wa-k12.net/pictures/tahomas/{uid}265.JPG?rev=0\n")
                outfile.close()
                
            if verbose == "true":
                print(bcolors.ORANGE + str(data_output["data"][uid]) + bcolors.DEFAULT + "\n")
        elif verbose == "true":
            print(bcolors.BIGHTRED + parsedinfo['username'] + bcolors.DEFAULT + "\n")
            

    end_time = "{}-{}_{}-{}-{}".format(localtime().tm_hour, localtime().tm_min, localtime().tm_year, localtime().tm_mon, localtime().tm_mday)
    data_output["endtime"] = end_time

except KeyboardInterrupt:
    print("\nUser interrupt. Finishing up...")

finally:
    print(f"{bcolors.OKBLUE}GreySec Data Scraper Complete at {bcolors.MAGENTA}" + ctime() + bcolors.DEFAULT)
    # Write results to file

    #with open(datafile, "w") as out:
        #json.dump(data_output, out, indent="\t")
        #out.close()