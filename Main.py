import Functions

un = "<s...>"
pw = "<password>"

academiejaar='0' # 0:huidig; 1:vorig; ...

(data, aantal_scores) = Functions.get_cijfers(un,pw,academiejaar)
#Functions.message(data, aantal_scores, un, pw)