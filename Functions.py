from selenium import webdriver
import tkinter as tk
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from tabulate import tabulate


def get_cijfers(un,pw,academiejaar):
    options = Options()
    options.add_argument("--headless")
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    delay = 5 # time before it stops waiting to load, may need to increase with slow internet
    driver = webdriver.Chrome(options=options)

    url = "https://ssologin.uantwerpen.be/"
    driver.get(url)

    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, '_shib_idp_revokeConsent')))
    except TimeoutException:
        print("Loading took too much time!")

    username = driver.find_element("id","username")
    password = driver.find_element("id","password")

    username.send_keys(un)
    password.send_keys(pw)
    password.send_keys(Keys.RETURN)

    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'div_maintenancemsg')))
    except TimeoutException:
        print("Loading took too much time!")

    url = "https://app.sisastudent.uantwerpen.be/psc/studweb/EMPLOYEE/SA/c/NUI_FRAMEWORK.PT_AGSTARTPAGE_NUI.?CONTEXTIDPARAMS=TEMPLATE_ID:PTPPNAVCOL&scname=ADMN_QQ_TL_SSS_CIJFERS&PTPPB_GROUPLET_ID=QQ_TL_SSS_CIJFERS&CRefName=QQ_ADMN_NAVCOLL_SSS_1&AJAXTransfer=y"
    driver.get(url)

    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'TERM_GRID$0_row_0')))
    except TimeoutException:
        print("Loading took too much time!")

    time.sleep(0.1)
    element_to_click = driver.find_element("id","TERM_GRID$0_row_"+academiejaar)
    element_to_click.click()
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.ID, 'ACAD_PROG_TBL_DESCR$0')))
    except TimeoutException:
        print("Loading took too much time!")
    html = driver.page_source
    driver.quit()

    '''text_file = open("soup.txt", "w")
    n = text_file.write(str(html))
    text_file.close()'''

    posities_vakken = [i for i in range(len(html)) if html.startswith('id="CLASS_TBL_VW_DESCR', i)]
    vakken=[]
    for i in range(len(posities_vakken)):
        vak=""
        j=1
        while html[posities_vakken[i]+25+j] != "<":
            vak+=html[posities_vakken[i]+25+j]
            j+=1
        vakken.append(vak)

    posities_scores = [i for i in range(len(html)) if html.startswith('id="STDNT_ENRL_SSV1_CRSE_GRADE_OFF', i)]
    scores=[]
    aantal_scores=0
    for i in range(len(posities_scores)):
        score=""
        if html[posities_scores[i]+38] != "&":
            score+=html[posities_scores[i]+38]
            aantal_scores+=1
            if html[posities_scores[i]+39] != "&":
                score+=html[posities_scores[i]+39]
            scores.append(score)
        else:
            scores.append("/")

    data = list(zip(vakken, scores))
    print(f"\nEr zijn {aantal_scores} scores online geplaatst dit academiejaar:\n")
    print(tabulate(data, headers=["Vak", "Cijfer"])+'\n')

    return (data, aantal_scores)

def message(data, aantal_scores, un, pw):
    if aantal_scores!=0:
        title = 'Er zijn cijfers!'
    else:
        title = 'Nog geen cijfers...'

    message = tk.Tk()
    message.geometry("500x300")
    message.title(title)
    message.lift()

    label = tk.Label(message, text=tabulate(data, headers=["Vak", "Cijfer"]), font='Courier')
    label.pack(pady=20)

    ok_button = tk.Button(message, text="OK", command=message.destroy)
    ok_button.pack(side="right", padx=5, pady=5)

    retry_button = tk.Button(message, text="Retry", command=lambda:retry(message, un, pw))
    retry_button.pack(side="left", padx=5, pady=5)
    message.mainloop()


def retry(m, un, pw):
    m.destroy()
    data, aantal_scores = get_cijfers(un, pw)
    message(data, aantal_scores, un, pw)