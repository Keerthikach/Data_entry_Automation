
from selenium import webdriver 
from selenium.webdriver.common.by import By
#from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.support.ui import WebDriverWait,Select
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import (StaleElementReferenceException,ElementNotInteractableException,ElementClickInterceptedException,NoSuchElementException,WebDriverException,TimeoutException)
import time
import sqlite3
import datetime 
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

driver.get("https://tgtransport.net/TGCFSTONLINE/Registration/DealerLogin.aspx")#navigates to login page of target website 


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

    #login credentials 
    username=driver.find_element(By.ID,"ctl00_OnlineContent_txtUserName")
    password=driver.find_element(By.ID,"ctl00_OnlineContent_txtPassword")
    username.send_keys("TG710553659") 
    password.send_keys("Rmpl@2017")

    print("Enter captcha manually and click on the login button.")
    current_url=driver.current_url
    WebDriverWait(driver,60).until(EC.url_changes((current_url)))


    #waiting until the main dash board appears 
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,"ctl00_NewVeh"))) #EC stands for expected_conditions, which is a module from Selenium that provides pre-defined conditions for waiting until a certain state is met.
    #the argument given to visibility_of_element_located is a tuple because, in Selenium, you specify elements using locators, which are always written as a tuple of (By.<METHOD>, "value")


    #For NEW vehicle tab 
    menu=driver.find_element(By.ID,"ctl00_NewVeh")
    #creating an actions object 
    action=ActionChains(driver)
    #using actions to hover over the new vehicles part 
    action.move_to_element(menu).perform()

    time.sleep(0.5)
    
    #search for non-transport 
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,"ctl00_lbtnNonTransport")))
    non_transport=driver.find_element(By.ID,"ctl00_lbtnNonTransport")
    non_transport.click()

    #drop down for is vehicle financed ctl00_OnlineDealerContent_ddlIsvehfin
    safe_drop_down("ctl00_OnlineDealerContent_ddlIsvehfin",data["is_veh_fin"])

    #drop down selection for class_of_vehicle ctl00_OnlineDealerContent_ddlVehClass MOTOR CYCLE
    safe_drop_down("ctl00_OnlineDealerContent_ddlVehClass","MOTOR CYCLE")
    
    #drop down for maker's_name  ctl00_OnlineDealerContent_ddlMakerName TVS MOTOR COMPANY LTD
    safe_drop_down("ctl00_OnlineDealerContent_ddlMakerName","TVS MOTOR COMPANY LTD")

    #drop down for maker's class ctl00_OnlineDealerContent_ddlMakerClass
    safe_drop_down("ctl00_OnlineDealerContent_ddlMakerClass",data["sel_op"])    

    #drop down for ownership_type ctl00_OnlineDealerContent_ddlOwnerType Individual
    safe_drop_down("ctl00_OnlineDealerContent_ddlOwnerType","Individual")   

    #engine no. ctl00_OnlineDealerContent_txtEngine
    safe_entry("ctl00_OnlineDealerContent_txtEngine",data["Engine_no"])

    #Chasis_no ctl00_OnlineDealerContent_txtChassis
    safe_entry("ctl00_OnlineDealerContent_txtChassis",data["Chasis_no"])
    

    #color ctl00_OnlineDealerContent_txtColour
    safe_entry("ctl00_OnlineDealerContent_txtColour",data["Colour"])
      # give time for JS to clear it if it wants to

    #invoice number ctl00_OnlineDealerContent_txtInvoiceNo
    safe_entry("ctl00_OnlineDealerContent_txtInvoiceNo",data["Invoice_no"])
    

    #price ctl00_OnlineDealerContent_txtInvoiceAmt ctl00_OnlineDealerContent_txtConfirmInvoiceAmt
    safe_entry("ctl00_OnlineDealerContent_txtInvoiceAmt",data["Price"])
     
    safe_entry("ctl00_OnlineDealerContent_txtConfirmInvoiceAmt",data["Price"])

    #manufacture year&month 
    try:
        mm_find=driver.find_element(By.ID,"ctl00_OnlineDealerContent_txtMfgMM") 
        yyyy_find=driver.find_element(By.ID,"ctl00_OnlineDealerContent_txtMfgYYYY")

        if (not mm_find.get_attribute("value") and not yyyy_find.get_attribute("value")) and mm_find.is_enabled() and mm_find.is_displayed():
            mm=datetime.datetime.strptime(data["manu_date"],"%Y-%m-%d").strftime("%m")
            yyyy=datetime.datetime.strptime(data["manu_date"],"%Y-%m-%d").strftime('%Y')
            safe_entry("ctl00_OnlineDealerContent_txtMfgMM",mm)
            safe_entry("ctl00_OnlineDealerContent_txtMfgYYYY",yyyy) 
        else:
            print("Field exists but is not interactable (disabled or hidden)")   
    except (ElementClickInterceptedException,ElementNotInteractableException)as e:
        print(f"Skipping field because it's not interactable: {e}")


    # APPLICANT DETAILS 

    #moving to applicant details tab 
    appli=driver.find_element(By.ID,"ctl00_OnlineDealerContent_lbtnApplicantDetails")
    action=ActionChains(driver) 
    action.move_to_element(appli).click().perform() 
    time.sleep(0.5)
    
    #Radio buttons for is pysically challenged 
    if data["is_phy_chal"]=="Yes":
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,"ctl00_OnlineDealerContent_rbtnlstPH_0"))).click()
    else:
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,"ctl00_OnlineDealerContent_rbtnlstPH_1"))).click()

    # For Name on RC Card Max 20 chars
    safe_entry("ctl00_OnlineDealerContent_txtDisplayName",data["f_name"]+" "+data["l_name"])

    #First Name 
    safe_entry("ctl00_OnlineDealerContent_txtFirstName",data["f_name"])

    #Last name
    safe_entry("ctl00_OnlineDealerContent_txtSurName",data["l_name"])

    #date of birth 
    date_obj=datetime.datetime.strptime(data["DOB"],"%Y-%m-%d")
    dd=date_obj.strftime("%d")
    mm=date_obj.strftime("%m")
    yyyy=date_obj.strftime("%Y")
    safe_entry("ctl00_OnlineDealerContent_txtDDdob",dd)
    safe_entry("ctl00_OnlineDealerContent_txtMMdob",mm)
    safe_entry("ctl00_OnlineDealerContent_txtYYYYdob",yyyy)

    #second vehicle drop down 
    safe_drop_down("ctl00_OnlineDealerContent_ddlIsSecondVehicle",data["is_sec_veh"])

    #Fathers's/Husband's Name 
    safe_entry("ctl00_OnlineDealerContent_txtFatherName",data["rep_name"])

    #Qualification
    safe_drop_down("ctl00_OnlineDealerContent_ddlEduQual",data["qualification"])

    #Aadhar number
    adhar1=data["aadhar_no"][:4]
    adhar2=data["aadhar_no"][4:8]
    adhar3=data["aadhar_no"][8:]
    safe_entry("ctl00_OnlineDealerContent_txtadhar1",adhar1)
    safe_entry("ctl00_OnlineDealerContent_txtadhar2",adhar2)
    safe_entry("ctl00_OnlineDealerContent_txtadhar3",adhar3)

    #Nationality
    safe_drop_down("ctl00_OnlineDealerContent_ddlNationality",data["nationality"])

    #Gender 
    if data["gender"]=="Male":
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,"ctl00_OnlineDealerContent_rdoMale"))).click()
    else:
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,"ctl00_OnlineDealerContent_rdoFemale"))).click()

    #Address Proof
    safe_drop_down("ctl00_OnlineDealerContent_ddlAddressProof",data["address_proof"]) 

    #District 
    print(data['District']) 
    safe_drop_down("ctl00_OnlineDealerContent_ddlBusinessDistrict",data["District"].strip())

    #Mandal    
    db_val=data["Mandal"].strip().lower()
    id="ctl00_OnlineDealerContent_ddlBusinessMandal"
    selected = False
    while True :
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ctl00_OnlineDealerContent_ddlBusinessMandal")))
            WebDriverWait(driver, 10).until(lambda d: len(Select(d.find_element(By.ID, "ctl00_OnlineDealerContent_ddlBusinessMandal")).options) > 1)
    
            drop=Select(driver.find_element(By.ID,"ctl00_OnlineDealerContent_ddlBusinessMandal"))
            for option in drop.options:
                title = option.get_attribute("title").strip().lower()
                val = option.get_attribute("value")
                if title==db_val:
                    drop = Select(driver.find_element(By.ID, "ctl00_OnlineDealerContent_ddlBusinessMandal"))
                    print(val) 
                    drop.select_by_value(val) 
                    selected = True
                    break 
            if selected:
                break     
            else:
                print(f"⚠️ Could not find a matching state for: {db_val}")    
        except StaleElementReferenceException:
            # the element was swapped out again — wait a bit and retry
            print("♻️ Dropdown reloaded, retrying…")
            time.sleep(0.5)
        except (NoSuchElementException):
            print(f"🚫 '{id}' no such element  yet, retrying…")
            time.sleep(2) 
        except ElementNotInteractableException:
             print(f"🚫 '{id}' not interactable yet, retrying…")
             time.sleep(2)
        except TimeoutException:
            print(f"⏱️ Timed out waiting for '{id}'.")
            break 

    #Location 
    db_val=data["Location"].lower().strip()
    id="ctl00_OnlineDealerContent_ddlBusinessLocation"
    selected=False 
    while True :
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ctl00_OnlineDealerContent_ddlBusinessLocation")))
            WebDriverWait(driver, 10).until(lambda d: len(Select(d.find_element(By.ID, "ctl00_OnlineDealerContent_ddlBusinessLocation")).options) > 1)

            drop=Select(driver.find_element(By.ID,"ctl00_OnlineDealerContent_ddlBusinessLocation"))
            for option in drop.options:
                title=option.get_attribute("title").lower().strip()
                val=option.get_attribute("value")
                if title==db_val:
                    drop=Select(driver.find_element(By.ID,"ctl00_OnlineDealerContent_ddlBusinessLocation"))
                    drop.select_by_value(val)
                    selected=True 
                    break
            if selected:
                break 
            else:
                print(f"⚠️ Could not find a matching state for: {db_val}")   
        except StaleElementReferenceException:
            # the element was swapped out again — wait a bit and retry
            print("♻️ Dropdown reloaded, retrying…")
            time.sleep(0.5)
        except (NoSuchElementException):
            print(f"🚫 '{id}' no such element  yet, retrying…")
            time.sleep(2) 
        except ElementNotInteractableException:
             print(f"🚫 '{id}' not interactable yet, retrying…")
             time.sleep(2)
        except TimeoutException:
            print(f"⏱️ Timed out waiting for '{id}'.")
            break         
    
    #Pincode
    safe_drop_down("ctl00_OnlineDealerContent_ddlPresentPinCode",data["Pincode"]) 

    #House No
    safe_entry("ctl00_OnlineDealerContent_txtBusinessAddress1",data["House_no"])

    #Street
    safe_entry("ctl00_OnlineDealerContent_txtBusinessAddress2",data["Street"])

    #landmark
    safe_entry("ctl00_OnlineDealerContent_txtBusinessAddress3",data["Landmark"])

    #City
    safe_entry("ctl00_OnlineDealerContent_txtBusinessCity",data["City"])

    #Phone 
    safe_entry("ctl00_OnlineDealerContent_txtBusinessMobileNumber",data["phone"])

    #email
    safe_entry("ctl00_OnlineDealerContent_txtBusinessEmail",data["email"])

    #copy button 
    button=WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID,"ctl00_OnlineDealerContent_btnCopyAddress"))) 
    print(button.is_enabled())
    try:
        driver.execute_script("arguments[0].scrollIntoView({block:'center'});", button)
        button.click()
    except ElementClickInterceptedException:
        driver.execute_script("arguments[0].click();",button)
    time.sleep(0.5) 


    #INSURANCE DETAILS  
    while True:
        try:
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"ctl00_OnlineDealerContent_lbtnInsurance")))
            insu = driver.find_element(By.ID, "ctl00_OnlineDealerContent_lbtnInsurance")
            driver.execute_script("arguments[0].click();", insu)
            action=ActionChains(driver)
            action.move_to_element(insu).click().perform()
            time.sleep(0.5)
            break 
        except StaleElementReferenceException:
            print("Dom refreshed retrying ")  
            time.sleep(0.5)  

    #company
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.ID, "ctl00_OnlineDealerContent_ddlInsCmpyName")))
    safe_drop_down("ctl00_OnlineDealerContent_ddlInsCmpyName",data['Company'])

    #insurance type
    safe_drop_down("ctl00_OnlineDealerContent_ddlInsuranceType",data['Insurance_Type'])

    #policy no
    safe_entry("ctl00_OnlineDealerContent_txtPolicyNo",data['Policy_No'])

    #insurance from date
    date_obj=datetime.datetime.strptime(data['Insu_from'],"%Y-%m-%d")
    dd=date_obj.strftime("%d")
    mm=date_obj.strftime("%m")
    yyyy=date_obj.strftime("%Y")
    safe_entry("ctl00_OnlineDealerContent_txtDDIncFrom",dd)
    safe_entry("ctl00_OnlineDealerContent_txtMMIncFrom",mm)
    safe_entry("ctl00_OnlineDealerContent_txtYYYYIncFrom",yyyy)

    #insurance to date 
    date_obj=datetime.datetime.strptime(data['Insu_to'],"%Y-%m-%d")
    dd=date_obj.strftime("%d")
    mm=date_obj.strftime("%m")
    yyyy=date_obj.strftime("%Y")
    safe_entry("ctl00_OnlineDealerContent_txtDDIncTo",dd)
    safe_entry("ctl00_OnlineDealerContent_txtMMIncTo",mm)
    safe_entry("ctl00_OnlineDealerContent_txtYYYYIncTo",yyyy)

    #FINANCE DETAILS 
    while True:
        try:
            WebDriverWait(driver,10).until(EC.presence_of_element_located((By.ID,"ctl00_OnlineDealerContent_lbtnFinance")))
            insu = driver.find_element(By.ID, "ctl00_OnlineDealerContent_lbtnFinance")
            driver.execute_script("arguments[0].click();", insu)
            action=ActionChains(driver)
            action.move_to_element(insu).click().perform()
            time.sleep(0.5)
            break 
        except StaleElementReferenceException:
            print("Dom refreshed retrying ")  
            time.sleep(0.5)  

    #Finanacer's Name 
    safe_entry("ctl00_OnlineDealerContent_txtFicName",data['fin_name'])      

    #Financer's address 
    safe_entry("ctl00_OnlineDealerContent_txtFicAddress1",data['fin_add'])

    #Financer's District
    safe_drop_down("ctl00_OnlineDealerContent_ddlDistrict",data['fin_dis'])

    #Financer's Mandal
    db_val=data["fin_Man"].strip().lower()
    id="ctl00_OnlineDealerContent_ddlMandal"
    selected = False
    while True :
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "ctl00_OnlineDealerContent_ddlMandal")))
            WebDriverWait(driver, 10).until(lambda d: len(Select(d.find_element(By.ID, "ctl00_OnlineDealerContent_ddlMandal")).options) > 1)
    
            drop=Select(driver.find_element(By.ID,"ctl00_OnlineDealerContent_ddlMandal"))
            for option in drop.options:
                title = option.get_attribute("title").strip().lower()
                val = option.get_attribute("value")
                if title==db_val:
                    drop = Select(driver.find_element(By.ID, "ctl00_OnlineDealerContent_ddlMandal"))
                    print(val) 
                    drop.select_by_value(val) 
                    selected = True
                    break 
            if selected:
                break     
            else:
                print(f"⚠️ Could not find a matching state for: {db_val}")    
        except StaleElementReferenceException:
            # the element was swapped out again — wait a bit and retry
            print("♻️ Dropdown reloaded, retrying…")
            time.sleep(0.5)
        except (NoSuchElementException):
            print(f"🚫 '{id}' no such element  yet, retrying…")
            time.sleep(2) 
        except ElementNotInteractableException:
             print(f"🚫 '{id}' not interactable yet, retrying…")
             time.sleep(2)
        except TimeoutException:
            print(f"⏱️ Timed out waiting for '{id}'.")
            break 

    #Finacer's City 
    safe_entry("ctl00_OnlineDealerContent_txtcity",data['fin_city'])    

    #Agreement Date 
    date_obj=datetime.datetime.strptime(data['fin_date'],"%Y-%m-%d")
    dd=date_obj.strftime("%d")
    mm=date_obj.strftime("%m")
    yyyy=date_obj.strftime("%Y")
    safe_entry("ctl00_OnlineDealerContent_txtDDAggrement",dd)
    safe_entry("ctl00_OnlineDealerContent_txtMMAggrement",mm)
    safe_entry("ctl00_OnlineDealerContent_txtYYYYAggrement",yyyy)

    


    #-----------------------------------------------------------------------------------------
    driver.execute_script("window.open('');") #open a new tab
    driver.switch_to.window(driver.window_handles[-1]) #go to the new tab
    driver.get("https://policy.haritaib.com/login")# navigate to login page of target website 






















    
        

    
    
   
    
    

    
    


    







    
except Exception as e:
    print("❗ Exception class:", type(e).__name__)
    print("❗ repr(e):", repr(e))        # shows class + message
    print("❗ str(e):", str(e))          # may be empty
    print("❗ Full traceback:")
    traceback.print_exc(file=sys.stdout) 

