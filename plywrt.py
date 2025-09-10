from playwright.sync_api import Playwright, sync_playwright
import sqlite3
import datetime

con=sqlite3.connect("details.db")
con.row_factory=sqlite3.Row
cursor=con.cursor()

cursor.execute("SELECT * FROM customer_details ORDER BY id DESC ")
data=cursor.fetchone()
cursor.close()

#playwright codegen --target python https://example.com This is the command for codegen 

def run(playwright: Playwright) -> None:

    browser = playwright.chromium.launch(headless=False,slow_mo=300,args=["--start-maximized"])
    context = browser.new_context(no_viewport=True )
    page = context.new_page()
    page.goto("https://tgtransport.net/TGCFSTONLINE/Registration/DealerLogin.aspx")

    def safe_fill_field(page, selector, value, max_retries=3):
        # Safely fill a field with verification
        for attempt in range(max_retries):
            try:
                # Wait for field to be ready
                field = page.locator(selector)
                field.wait_for(state="visible")
                field.wait_for(state="attached")
                
                # Clear and fill
                field.clear()
                field.fill(value)
                
                # Verify the value was set
                actual_value = field.input_value()
                if actual_value == value:
                    print(f"Successfully filled {selector} with '{value}'")
                    return True
                else:
                    print(f"Attempt {attempt + 1}: Expected '{value}', got '{actual_value}'")
                    page.wait_for_timeout(1000)  # Wait before retry
                    
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                page.wait_for_timeout(1000)
        
        return False
    
    def handle_multiple_modals(page, max_modals=5):
        """Handle multiple modals that appear one after another"""
        modals_handled = 0
        
        for i in range(max_modals):
            try:
                # Check for modal background
                modal_background = page.locator("#ctl00_OnlineDealerContent_ModalPopupExtender1_backgroundElement")
                modal_background.wait_for(state="visible", timeout=2000)
                
                print(f"Modal #{i+1} detected")
                
                # Try different close button patterns
                close_buttons = [
                    "input[value*='OK']",
                    "input[value*='Close']", 
                    "input[value*='Cancel']",
                    "button:has-text('OK')",
                    "button:has-text('Close')",
                    "button:has-text('Cancel')",
                    "[id*='btnOK']",
                    "[id*='btnClose']"
                ]
                
                button_clicked = False
                for button_selector in close_buttons:
                    close_button = page.locator(button_selector)
                    if close_button.count() > 0:
                        close_button.click()
                        button_clicked = True
                        print(f"Closed modal #{i+1} with: {button_selector}")
                        break
                
                if not button_clicked:
                    print(f"No close button found for modal #{i+1}, trying ESC key")
                    page.keyboard.press("Escape")
                
                # Wait for modal to disappear
                modal_background.wait_for(state="hidden", timeout=3000)
                modals_handled += 1
                
                # Small delay before checking for next modal
                page.wait_for_timeout(500)
                
            except Exception as e:
                print(f"No more modals found after handling {modals_handled}",e)
                break
        
        return modals_handled

    page.locator("#ctl00_OnlineContent_txtUserName").click()
    page.locator("#ctl00_OnlineContent_txtUserName").fill("TG710553659")

    page.get_by_role("row", name="Password", exact=True).get_by_role("cell").nth(1).click()
    page.locator("#ctl00_OnlineContent_txtPassword").fill("Rmpl@2017") 

    page.get_by_role("textbox", name="Enter Captcha").click()
    old_url=page.url
    page.wait_for_function("window.location.href !== '{}'".format(old_url),timeout=60000)
    print("Donzo")

 
    page.hover("#ctl00_NewVeh") 
    page.wait_for_selector("text=Non Transport", timeout=60000)
    page.get_by_role("link", name="Non Transport").click()

    #is_vehicle_financed
    page.locator("#ctl00_OnlineDealerContent_ddlIsvehfin").select_option("Y")

    #vehicle class
    page.locator("#ctl00_OnlineDealerContent_ddlVehClass").select_option("MCYN")

    #Maker class
    page.locator("#ctl00_OnlineDealerContent_ddlMakerName").select_option("363")

    #Maker class (vehicle name)
    dropdown = page.locator('[id$="_ddlMakerClass"]')  # ends-with match
    dropdown.wait_for(state="attached", timeout=10000)
    dropdown.locator("option").nth(1).wait_for(state="attached", timeout=10000)
    page.locator('ctl00_OnlineDealerContent_ddlMakerClass').select_option(label=data['sel_op'])

    #Ownership Type
    page.locator("#ctl00_OnlineDealerContent_ddlOwnerType").select_option("INV")

    #Engine number
    page.locator("#ctl00_OnlineDealerContent_txtEngine").click()
    page.locator("#ctl00_OnlineDealerContent_txtEngine").fill(data['Engine_no'])

    #Chassis number
    page.locator("#ctl00_OnlineDealerContent_txtChassis").click()
    page.locator("#ctl00_OnlineDealerContent_txtChassis").fill(data["Chasis_no"])

    #Colour
    page.locator("#ctl00_OnlineDealerContent_txtColour").click()
    page.locator("#ctl00_OnlineDealerContent_txtColour").fill(data['Colour'])

    #Invoice number
    page.locator("#ctl00_OnlineDealerContent_txtInvoiceNo").click()
    page.locator("#ctl00_OnlineDealerContent_txtInvoiceNo").fill(data["Invoice_no"])

    #Price
    page.locator("#ctl00_OnlineDealerContent_txtInvoiceAmt").click()
    page.locator("#ctl00_OnlineDealerContent_txtInvoiceAmt").fill(str(data["Price"]))

    #Confirm Price
    page.locator("#ctl00_OnlineDealerContent_txtConfirmInvoiceAmt").click()
    page.locator("#ctl00_OnlineDealerContent_txtConfirmInvoiceAmt").fill(str(data["Price"]))

    #Click Applicant deyails
    page.get_by_role("link", name="APPLICANT DETAILS").click()
    
    #Is physically challenged
    page.locator('#ctl00_OnlineDealerContent_trPH').get_by_label(data["is_phy_chal"]).click() 

    #Display Name
    page.locator("#ctl00_OnlineDealerContent_txtDisplayName").click()
    page.locator("#ctl00_OnlineDealerContent_txtDisplayName").fill(data["f_name"]+" "+data["l_name"])

    #First Name
    page.locator("#ctl00_OnlineDealerContent_txtFirstName").click()
    page.locator("#ctl00_OnlineDealerContent_txtFirstName").fill(data["f_name"])

    #Surname
    page.locator("#ctl00_OnlineDealerContent_txtSurName").click()
    page.locator("#ctl00_OnlineDealerContent_txtSurName").fill(data["l_name"])

    #Date of birth 
    date_obj=datetime.datetime.strptime(data["DOB"],"%Y-%m-%d")
    dd=date_obj.strftime("%d")
    mm=date_obj.strftime("%m")
    yyyy=date_obj.strftime("%Y")

    #date
    page.locator("#ctl00_OnlineDealerContent_txtDDdob").click()
    page.locator("#ctl00_OnlineDealerContent_txtDDdob").fill(dd)

    #Month
    page.locator("#ctl00_OnlineDealerContent_txtMMdob").click()
    page.locator("#ctl00_OnlineDealerContent_txtMMdob").fill(mm)

    #Year
    page.locator("#ctl00_OnlineDealerContent_txtYYYYdob").click()
    page.locator("#ctl00_OnlineDealerContent_txtYYYYdob").fill(yyyy)

    #Is_sec_veh
    page.locator("#ctl00_OnlineDealerContent_ddlIsSecondVehicle").select_option(label=data["is_sec_veh"])

    #Father Name
    page.locator("#ctl00_OnlineDealerContent_txtFatherName").click()
    page.locator("#ctl00_OnlineDealerContent_txtFatherName").fill(data["rep_name"])

    #Education Qualification
    page.locator("#ctl00_OnlineDealerContent_ddlEduQual").select_option(label=data["qualification"])

    #aadhar
    aadhar1=str(data["aadhar_no"][:4])
    aadhar2=str(data["aadhar_no"][4:8])
    aadhar3=str(data["aadhar_no"][8:])

    page.locator("#ctl00_OnlineDealerContent_txtadhar1").click()
    page.locator("#ctl00_OnlineDealerContent_txtadhar1").fill(aadhar1)
    page.locator("#ctl00_OnlineDealerContent_txtadhar2").click()
    page.locator("#ctl00_OnlineDealerContent_txtadhar2").fill(aadhar2)
    page.locator("#ctl00_OnlineDealerContent_txtadhar3").click()
    page.locator("#ctl00_OnlineDealerContent_txtadhar3").fill(aadhar3)

    #Nationality
    page.locator("#ctl00_OnlineDealerContent_ddlNationality").select_option(label=data["nationality"])
    print("Done Nat")

    #gender 
    gender_row = page.locator("tr:has(td:has-text('Gender'))") # Locate the <tr> that has a <td> with text 'Gender' (using :has-text pseudo-class)
    gender_row.get_by_label(data['gender'],exact=True).check()
    print("Done Gender")

    #Address Proof
    page.locator("#ctl00_OnlineDealerContent_ddlAddressProof").select_option(label=data["address_proof"])
    print("Done Address")

    #is vehicle scraped 
    if ("No"=="Yes"):
        page.locator("#ctl00_OnlineDealerContent_rbtnIsScrapped_0").click()
    else:
        page.locator("#ctl00_OnlineDealerContent_rbtnIsScrapped_1").click()
    print("Done scrap")

    #District Mandal Location 

    #District
    page.locator("#ctl00_OnlineDealerContent_ddlBusinessDistrict").select_option(label=data["District"])

    #Mandal
    page.wait_for_function(
    """() => {
        const dropdown = document.querySelector('#ctl00_OnlineDealerContent_ddlMakerClass');
        return dropdown && dropdown.options.length > 1;
    }""",
    timeout=10000
    )

    page.select_option("#ctl00_OnlineDealerContent_ddlBusinessMandal", label=data['Mandal'])

    #Location
    if (data['Mandal']=='Hyderabad'):
        page.wait_for_function(
        """() => {
            const dropdown = document.querySelector('#ctl00_OnlineDealerContent_ddlBusinessLocation');
            return dropdown && dropdown.options.length > 1;
        }""",
        timeout=10000
        )

        page.select_option("#ctl00_OnlineDealerContent_ddlBusinessLocation", label=data['Location'])

    #Pincode 
    page.wait_for_function(
        """()=>{
        const dropdown=document.querySelector('#ctl00_OnlineDealerContent_ddlPresentPinCode');
        return dropdown && dropdown.options.length>1;
        }""",
        timeout=10000
    )
    page.select_option("#ctl00_OnlineDealerContent_ddlPresentPinCode",label=data['Pincode'])

    #House No.
    handle_multiple_modals(page) 
    page.locator("#ctl00_OnlineDealerContent_txtBusinessAddress1").click()
    page.locator("#ctl00_OnlineDealerContent_txtBusinessAddress1").fill(data['House_no'])

    #Street 
    handle_multiple_modals(page) 
    page.locator("#ctl00_OnlineDealerContent_txtBusinessAddress2").click()
    page.locator("#ctl00_OnlineDealerContent_txtBusinessAddress2").fill(data['Street'])

    #Landmark
    handle_multiple_modals(page) 
    page.locator("#ctl00_OnlineDealerContent_txtBusinessAddress3").click()
    page.locator("#ctl00_OnlineDealerContent_txtBusinessAddress3").fill(data['Landmark'])

    #city 
    handle_multiple_modals(page) 
    page.locator("#ctl00_OnlineDealerContent_txtBusinessCity").click()
    page.locator("#ctl00_OnlineDealerContent_txtBusinessCity").fill(data['City'])

    #Phone
    page.locator("#ctl00_OnlineDealerContent_txtBusinessMobileNumber").click()
    page.locator("#ctl00_OnlineDealerContent_txtBusinessMobileNumber").fill(data['phone'])

    #email 
    page.locator("#ctl00_OnlineDealerContent_txtBusinessEmail").click()
    page.locator("#ctl00_OnlineDealerContent_txtBusinessEmail").fill(data['email'])

    #copy button 
    page.locator("#ctl00_OnlineDealerContent_btnCopyAddress").click()
    

    #Insurace Details 
    page.get_by_role("link", name="INSURANCE DETAILS").click()

    #Company Name
    page.locator("#ctl00_OnlineDealerContent_ddlInsCmpyName").select_option(label=data['Company'])

    #Insurance Type
    page.locator("#ctl00_OnlineDealerContent_ddlInsuranceType").select_option(label=data['Insurance_Type'])

    #Policy No.
    page.locator("#ctl00_OnlineDealerContent_txtPolicyNo").click()
    page.locator("#ctl00_OnlineDealerContent_txtPolicyNo").fill(data['Policy_No'])

    #Insurance from 
    date_obj=datetime.datetime.strptime(data['Insu_from'],"%Y-%m-%d")
    dd=date_obj.strftime("%d")
    mm=date_obj.strftime("%m")
    yyyy=date_obj.strftime("%Y")
    page.locator("#ctl00_OnlineDealerContent_txtDDIncFrom").fill(dd)
    page.locator("#ctl00_OnlineDealerContent_txtMMIncFrom").fill(mm)
    page.locator("#ctl00_OnlineDealerContent_txtYYYYIncFrom").fill(yyyy)

    #Insurance To
    date_obj=datetime.datetime.strptime(data['Insu_to'],"%Y-%m-%d")
    dd=date_obj.strftime("%d")
    mm=date_obj.strftime("%m")
    yyyy=date_obj.strftime("%Y")
    page.locator("#ctl00_OnlineDealerContent_txtDDIncTo").fill(dd)
    page.locator("#ctl00_OnlineDealerContent_txtMMIncTo").fill(mm)
    page.locator("#ctl00_OnlineDealerContent_txtYYYYIncTo").fill(yyyy)

    #Finance details 
    page.get_by_role("link", name="FINANCE DETAILS").click()

    #Financer's Name
    page.locator("#ctl00_OnlineDealerContent_txtFicName").fill(label=data['fin_name'])

    #Financer's Address 1
    page.locator("#ctl00_OnlineDealerContent_txtFicAddress1").fill(label=data['fin_add'])

    #District 
    page.locator("#ctl00_OnlineDealerContent_ddlDistrict").select_option(label=data["fin_dis"])

    #Mandal 
    page.wait_for_function(
    """() => {
        const dropdown = document.querySelector('#ctl00_OnlineDealerContent_ddlMandal');
        return dropdown && dropdown.options.length > 1;
    }""",
    timeout=10000
    )
    page.select_option("#ctl00_OnlineDealerContent_ddlMandal", label=data['fin_Man'])

    #City 
    page.locator("#ctl00_OnlineDealerContent_txtcity").fill(data['fin_city'])

    #Agreement date
    date_obj=datetime.datetime.strptime(data['fin_date'],"%Y-%m-%d")
    dd=date_obj.strftime("%d")
    mm=date_obj.strftime("%m")
    yyyy=date_obj.strftime("%Y")
    page.locator("#ctl00_OnlineDealerContent_txtDDAggrement").fill(dd)
    page.locator("#ctl00_OnlineDealerContent_txtMMAggrement").fill(mm)
    page.locator("#ctl00_OnlineDealerContent_txtYYYYAggrement").fill(yyyy)



    input("Press Enter to close browser...")
    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
