from selenium import webdriver 
from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui import WebDriverWait,Select
#from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (StaleElementReferenceException,ElementNotInteractableException,ElementClickInterceptedException,NoSuchElementException,WebDriverException,TimeoutException)
import time
import sqlite3
#import datetime 
import traceback
import sys 
print("Selenium script is running...")

conn=sqlite3.connect("details.db")
conn.row_factory=sqlite3.Row#Must come after connect 
cursor=conn.cursor()

#It tells SQLite to return rows as a special dictionary-like object, which as a tuple and a dictionary
#it's a special object of type sqlite3.Row 
#Index-based access like a tuple: row[0],Key-based access like a dict: row["email"]
                #conn = sqlite3.connect("db.sqlite3")
                #cursor = conn.cursor()  # ❌ This cursor uses default (tuple)
                #conn.row_factory = sqlite3.Row
#Row factory affects future cursors.If we want all cursors to give dictionary-style rows, set it before making any cursor.                

cursor.execute("SELECT * FROM customer_details ORDER BY id DESC ")
data=cursor.fetchone()
cursor.close()


#Setup webdriver and installing chrome webdriver 
options=webdriver.ChromeOptions() # options is an instance of ChromeOptions() and this helps us customize options of selenium's chrome
options.add_experimental_option("detach",True) # it is one of the options that we can customize, It keeps chrome open after the execution of script 

service=Service(ChromeDriverManager().install())
driver=webdriver.Chrome(service=service,options=options) # Launches Chrome with WebDriver.
#ChromeDriverManager().install(): installs required version of chromewebdriver 

driver.get("https://policy.haritaib.com/login")#navigates to login page of target website 

try:
    def safe_drop_down(id,text):
        while True:
            try:
                print("Hello",id)
                WebDriverWait(driver, 10).until(lambda d: len(Select(d.find_element(By.ID, id)).options) > 1)
                print(1)
                drop_down=driver.find_element(By.ID,id)
                print(2)
                dd=Select(drop_down)
                print(3)
                dd.select_by_visible_text(text)
                print(f"✅ Field {id} accepted value '{text}'")
                break 
            except StaleElementReferenceException:
                print("♻️ Dropdown refreshed, retrying...")
            except ( ElementNotInteractableException):
                print(f"🚫 Dropdown '{id}' not interactable yet. Retrying...")
            except(NoSuchElementException):
                print("No Such element present")
            except ValueError as ve:
                print(str(ve))
                break
            except WebDriverException as wde:
                print(f"🚨 WebDriverException: {wde}")
                break
            except Exception as e:
                print(f"❗️Unexpected Error: {e}")
                break
    def safe_entry(id,keys):
        while True:
            try:
                WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,id))) 
                driving=driver.find_element(By.ID,id)  
                driving.clear()          
                driving.send_keys(keys)
                time.sleep(0.5)  # Give JS time 

                # Confirm value stuck
                actual_value = driving.get_attribute("value").strip()
                if actual_value == keys:
                    print(f"✅ Field {id} accepted value '{keys}'")
                    return
                else:
                    print(f"⚠️ Field {id} got cleared or changed. Retrying...")
                    break 
            except StaleElementReferenceException:
                print("DOM refreshed, retrying...")
            except Exception as e:
                print(f"Unexpected error in {id}: {str(e)}")    

    print("Waiting for URL to match...")
    WebDriverWait(driver,300).until(EC.url_matches("https://policy.haritaib.com/quote-form"))
    print(driver.current_url)

    #Selecting policy type(radio button)
    if 'Renew'=='New':
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "policy_type_1")))
        driver.find_element(By.ID,"policy_type_1").click() 
    else:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "policy_type_2")))
        driver.find_element(By.ID,'policy_type_2').click()     
    
    #print(driver.page_source)    

    #Slecting policy subtype (Dynamic dropdown)  
    subtype_dropdown = driver.find_element(By.XPATH, "//label[contains(text(), 'Select Option')]/following-sibling::ng-select")
    #print(driver.find_element(By.XPATH, "//label[contains(text(), 'Select Option')]/following-sibling::ng-select"))
    subtype_dropdown.click()   
    option_to_select='SAOD'

    # panels = driver.find_elements(By.CLASS_NAME, "ng-dropdown-panel")
    # print("Dropdown panels found:", len(panels))
    # for i, panel in enumerate(panels):
    #     print(f"Panel {i+1}:")
    #     print(panel.text)  # prints the visible text inside the panel
    #     print(panel.get_attribute('outerHTML')) 
    # HTML of the dropdown <ng-dropdown-panel role="listbox" aria-label="Options list" class="ng-dropdown-panel ng-select-bottom" id="a22deba779d0" style="opacity: 1;"><!----><div class="ng-dropdown-panel-items scroll-host"><div></div><div><div class="ng-option ng-option-marked" role="option" id="a22deba779d0-0"><!----><span class="ng-option-label"><b _ngcontent-ewm-c88="" style="color: #114984;"> PACKAGE </b></span><!----></div><!----><!----><!----><!----><!----><!----></div></div><!----></ng-dropdown-panel>

    option = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class,'ng-dropdown-panel')]//div[contains(@class,'ng-option')]//b[contains(text(),'{option_to_select}')]")))
    option.click()
    print("Dropdown opened")

    #select tenure (dynamic dropdown)
    tenure_dropdown=driver.find_element(By.XPATH,"//label[contains(text(), 'Select Tenure')]/following-sibling::ng-select")
    tenure_dropdown.click()
    option_to_select='STANDALONEOD'
    option = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class,'ng-dropdown-panel')]//div[contains(@class,'ng-option')]//b[contains(text(),'{option_to_select}')]")))
    option.click()

    #VEHICLE INFO 

    #Insurance company 
    insu_dropdown=driver.find_element(By.XPATH,"//label[contains(text(), 'Insurance company')]/following-sibling::ng-select")
    insu_dropdown.click()
    option_to_select='TATA AIG GENERAL INSURANCE COMPANY LTD'
    panels = driver.find_elements(By.CLASS_NAME, "ng-dropdown-panel")
    print("Dropdown panels found:", len(panels))
    for i, panel in enumerate(panels):
        print(f"Panel {i+1}:")
        print(panel.text)  # prints the visible text inside the panel
        print(panel.get_attribute('outerHTML')) 
    option = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class,'ng-dropdown-panel')]//div[contains(@class,'ng-option')]//b[contains(text(),'{option_to_select}')]")))
    option.click()

    #Engine No.
    eng_no=driver.find_element(By.XPATH,"//label[contains(text(), 'Engine Number')]/preceding-sibling::input")
    eng_no.send_keys(data['Engine_no'])

    #Chassis No.
    chas_no=driver.find_element(By.XPATH,"//label[contains(text(),'Chassis Number')]/preceding-sibling::input")
    chas_no.send_keys(data['Chasis_no'])

    #Model 
    model_dropdown=driver.find_element(By.XPATH,"//label[contains(text(), 'Model')]/following-sibling::ng-select")
    model_dropdown.click()
    option_to_select='Apache KS Drum'
    option = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class,'ng-dropdown-panel')]//div[contains(@class,'ng-option')]//b[contains(text(),'{option_to_select}')]")))
    option.click()

    #Variant 
    vari_dropdown=driver.find_element(By.XPATH,"//label[contains(text(), 'Variant')]/following-sibling::ng-select")
    vari_dropdown.click()
    option_to_select='TVS APACHE KS APACHE RED ( PETROL  148cc ) '
    option = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class,'ng-dropdown-panel')]//div[contains(@class,'ng-option')]//b[contains(text(),'{option_to_select}')]")))
    option.click()

    #RTO
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,"//label[contains(text(), 'RTO')]/following-sibling::ng-select")))
    rto_dropdown=driver.find_element(By.XPATH,"//label[contains(text(), 'RTO')]/following-sibling::ng-select")
    rto_dropdown.click()
    option_to_select='TS-13'
    # panels = driver.find_elements(By.CLASS_NAME, "ng-dropdown-panel")
    # print("Dropdown panels found:", len(panels))
    # for i, panel in enumerate(panels):
    #     print(f"Panel {i+1}:")
    #     print(panel.text)  # prints the visible text inside the panel
    #     print(panel.get_attribute('outerHTML')) 
    option = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, f"//div[contains(@class,'ng-dropdown-panel')]//div[contains(@class,'ng-option')]//span[contains(text(),'{option_to_select}')]")))
    option.click()

    #Manufacture Year 
    year=driver.find_element(By.XPATH,"//label[contains(text(),'Manufacturing Year')]/following-sibling::select")
    year_sel=Select(year)
    year_sel.select_by_visible_text('2023')

    #manufacture Month
    month=driver.find_element(By.XPATH,"//label[contains(text(),'Manufacturing Month')]/following-sibling::select")
    month_sel=Select(month)
    month_sel.select_by_visible_text('March')

    #Registration Date 
    date_input = driver.find_element(By.XPATH, "//label[contains(text(),'Purchase/Registration Date')]/preceding::input[1]")
    date_input.click()

    # calendars = driver.find_elements(By.CLASS_NAME, "ngb-dp")
    # print("Calendars found:", len(calendars))
    # for i, cal in enumerate(calendars):
    #     print(f"Calendar {i+1}:")
    #     print(cal.get_attribute("outerHTML"))

    driver.execute_script(""" 
    arguments[0].value = '10-09-2025';
    arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
    arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
    """, date_input)
    #basically faking a real user typing + finishing the input, not just dumping text inside.
    #input → keeps the framework’s data model in sync with what you see.
    #change → triggers validation, saves, or dependent logic.

    #Policy Holder type(radio buttons)
    if ("Individual"=="Individual"):
        driver.find_element(By.ID,"policy_holder_type_1").click()
    else:
        driver.find_element(By.ID,"policy_holder_type_2").click()

    #OD Discount(dropdown) 
    od_dis=driver.find_element(By.XPATH,"//label[contains(text(),'OD Discount')]/following-sibling::select")
    Select(od_dis).select_by_visible_text("35")

    #Current IDV(textbox)
    idv=driver.find_element(By.XPATH,"//label[contains(text(),'Enter Current IDV')]/following-sibling::input")
    idv.send_keys("100800")

    #TP PD (checkbox)
    if ('yes'=='yes'):
        tp=driver.find_element(By.XPATH,"//label[contains(text(),'TP PD')]/preceding-sibling::input")    
        tp.click()

    #CKYC DETAILS 

    #KYC Docs(dd)
    kyc=driver.find_element(By.XPATH,"//label[contains(text(),'KYC Documents')]/following-sibling::select")
    Select(kyc).select_by_visible_text('Aadhaar Number')

    #Number on KYC docx(text)
    certificate = driver.find_element(By.XPATH, "//input[@formcontrolname='certificate_no']")
    certificate.send_keys("698312829484")

    #DOB(calendar)
    dob=driver.find_element(By.XPATH,"//label[contains(text(),'Date of Birth')]/preceding::input[1]")
    dob.click()
    driver.execute_script(""" 
    arguments[0].value = '09-07-1987';
    arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
    arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
    """, dob)

    #PEP(radio)
    if ('no'=='yes'):
        driver.find_element(By.ID,"pep_yes").click()
    else:
        driver.find_element(By.ID,"pep_no").click()

    #PREVIOUS POLICY DETAILS    

    #Change in ownership in the last year (radio)
    if('no'=='yes'):
        driver.find_element(By.ID,"change_owner_ship_yes").click()
    else:
        driver.find_element(By.ID,"change_owner_ship_no").click()

    #Do you have previous policy(radio)
    if ('no'=='yes'):
        driver.find_element(By.ID,"previous_policy_yes").click()
    else:
        driver.find_element(By.ID,"previous_policy_no").click()  






    
except Exception as e :
    print("❗ Exception class:", type(e).__name__)
    print("❗ repr(e):", repr(e))        # shows class + message
    print("❗ str(e):", str(e))          # may be empty
    print("❗ Full traceback:")
    traceback.print_exc(file=sys.stdout) 

