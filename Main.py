import Functions
import json


    # Get username and password from dict from json file
with open('login_info.json') as json_file:
    data = json.load(json_file)
    un = data['un']
    pw = data['pw']

#un = "<s...>"
#pw = "<password>"


academiejaar='0' # 0:huidig; 1:vorig; ...

(data, aantal_scores) = Functions.get_cijfers(un,pw,academiejaar)
#Functions.message(data, aantal_scores, un, pw)