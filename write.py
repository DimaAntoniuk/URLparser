import requests
import re

string = "k href='fjdlglknfd'"
string = string[string.find('href'):]
print(string[string.find("'")+1:])
