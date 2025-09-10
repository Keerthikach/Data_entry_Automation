import tkinter as tk 
import sqlite3
from tkinter import messagebox
#import os 
from bs4 import BeautifulSoup 
import datetime 


conn=sqlite3.connect("details.db")
cursor=conn.cursor()

#to get a db with update schema all the time because i am still developing it.
cursor.execute("DROP TABLE IF EXISTS customer_details;")

cursor.execute("""
      CREATE TABLE IF NOT EXISTS customer_details(
               id INTEGER PRIMARY KEY AUTOINCREMENT,
               f_name TEXT,
               l_name TEXT,
               email TEXT,
               phone TEXT,
               DOB TEXT,
               is_veh_fin TEXT,
               is_phy_chal TEXT,
               is_sec_veh TEXT,
               rep_name TEXT,
               qualification TEXT,
               aadhar_no TEXT,
               nationality TEXT,
               gender TEXT,
               address_proof TEXT,
               sel_op TEXT,
               Engine_no TEXT,
               Chasis_no TEXT,
               Colour TEXT,
               Invoice_no TEXT,
               Price NUMBER,
               manu_date TEXT,   
               District TEXT,
               Mandal TEXT,
               Location TEXT,
               Pincode TEXT,
               House_no TEXT,
               Street TEXT,
               Landmark TEXT,
               City TEXT,
               Company TEXT,
               Insurance_Type TEXT,
               Policy_No TEXT,
               Insu_from TEXT,
               Insu_to TEXT,
               fin_name TEXT,
               fin_add TEXT,
               fin_dis TEXT,
               fin_Man TEXT,
               fin_city TEXT,
               fin_date TEXT    
               );
""")
conn.commit()
conn.close()

def contents():
    conn=sqlite3.connect("details.db")
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM customer_details ")
    print(cursor.fetchall()) 


def option_finder():
    html1="""
        <select name="ctl00$OnlineDealerContent$ddlMakerClass" onchange="javascript:setTimeout('__doPostBack(\'ctl00$OnlineDealerContent$ddlMakerClass\',\'\')', 0)" id="ctl00_OnlineDealerContent_ddlMakerClass" tabindex="7" class="ddl" style="font-weight:normal;width:250px;position: static">
        <option selected="selected" value="0" title="Select">Select</option>
        <option value="APACHE RR 310 BSVI" title="APACHE RR 310 BSVI">APACHE RR 310 BSVI</option>
        <option value="APACHE RR 310 BSVI-PH2" title="APACHE RR 310 BSVI-PH2">APACHE RR 310 BSVI-PH2</option>
        <option value="APACHE RTR 310 BSVI-PH2" title="APACHE RTR 310 BSVI-PH2">APACHE RTR 310 BSVI-PH2</option>
        <option value="JUPITER 125  SMW BSVI" title="JUPITER 125  SMW BSVI">JUPITER 125  SMW BSVI</option>
        <option value="JUPITER 125 FAW DISC &amp; REAR AW DBM BSVI" title="JUPITER 125 FAW DISC &amp; REAR AW DBM BSVI">JUPITER 125 FAW DISC &amp; REAR AW DBM BSVI</option>
        <option value="JUPITER 125 FAW DRUM &amp; REAR AW DBM BSVI" title="JUPITER 125 FAW DRUM &amp; REAR AW DBM BSVI">JUPITER 125 FAW DRUM &amp; REAR AW DBM BSVI</option>
        <option value="TVS - IQUBE ELECTRIC SMARTXONNECT9 BOV" title="TVS - IQUBE ELECTRIC SMARTXONNECT9 BOV">TVS - IQUBE ELECTRIC SMARTXONNECT9 BOV</option>
        <option value="TVS - JUPITER 125 BSVI-PH2" title="TVS - JUPITER 125 BSVI-PH2">TVS - JUPITER 125 BSVI-PH2</option>
        <option value="TVS - SPORT BSVI-PH2" title="TVS - SPORT BSVI-PH2">TVS - SPORT BSVI-PH2</option>
        <option value="TVS APACHE RTR 160 4V (WITH RIDE MODE) BSVI-PH2" title="TVS APACHE RTR 160 4V (WITH RIDE MODE) BSVI-PH2">TVS APACHE RTR 160 4V (WITH RIDE MODE) BSVI-PH2</option>
        <option value="TVS APACHE RTR 160 4V DISC BSVI" title="TVS APACHE RTR 160 4V DISC BSVI">TVS APACHE RTR 160 4V DISC BSVI</option>
        <option value="TVS APACHE RTR 160 4V DRUM BSVI" title="TVS APACHE RTR 160 4V DRUM BSVI">TVS APACHE RTR 160 4V DRUM BSVI</option>
        <option value="TVS APACHE RTR 160 4V HIGH POWER DISC BSVI" title="TVS APACHE RTR 160 4V HIGH POWER DISC BSVI">TVS APACHE RTR 160 4V HIGH POWER DISC BSVI</option>
        <option value="TVS APACHE RTR 160 4V HIGH POWER DRUM BSVI" title="TVS APACHE RTR 160 4V HIGH POWER DRUM BSVI">TVS APACHE RTR 160 4V HIGH POWER DRUM BSVI</option>
        <option value="TVS APACHE RTR 160 4V WITH RIDE MODE DISC BSVI" title="TVS APACHE RTR 160 4V WITH RIDE MODE DISC BSVI">TVS APACHE RTR 160 4V WITH RIDE MODE DISC BSVI</option>
        <option value="TVS APACHE RTR 160 4V WITH RIDER MODE DRUM BSVI" title="TVS APACHE RTR 160 4V WITH RIDER MODE DRUM BSVI">TVS APACHE RTR 160 4V WITH RIDER MODE DRUM BSVI</option>
        <option value="TVS APACHE RTR 160 DISC BSVI" title="TVS APACHE RTR 160 DISC BSVI">TVS APACHE RTR 160 DISC BSVI</option>
        <option value="TVS APACHE RTR 160 DRUM" title="TVS APACHE RTR 160 DRUM">TVS APACHE RTR 160 DRUM</option>
        <option value="TVS APACHE RTR 160(WITH RIDE MODE) BSVI-PH2" title="TVS APACHE RTR 160(WITH RIDE MODE) BSVI-PH2">TVS APACHE RTR 160(WITH RIDE MODE) BSVI-PH2</option>
        <option value="TVS APACHE RTR 165 RP BSVI" title="TVS APACHE RTR 165 RP BSVI">TVS APACHE RTR 165 RP BSVI</option>
        <option value="TVS APACHE RTR 180 BSVI" title="TVS APACHE RTR 180 BSVI">TVS APACHE RTR 180 BSVI</option>
        <option value="TVS APACHE RTR 180(WITH RIDE MODE) BSVI-PH2" title="TVS APACHE RTR 180(WITH RIDE MODE) BSVI-PH2">TVS APACHE RTR 180(WITH RIDE MODE) BSVI-PH2</option>
        <option value="TVS APACHE RTR 200 4V BSVI" title="TVS APACHE RTR 200 4V BSVI">TVS APACHE RTR 200 4V BSVI</option>
        <option value="TVS APACHE RTR 200 4V WITH RIDE MODE BSVI-PH2" title="TVS APACHE RTR 200 4V WITH RIDE MODE BSVI-PH2">TVS APACHE RTR 200 4V WITH RIDE MODE BSVI-PH2</option>
        <option value="TVS IQUBE ELECTRIC BOV" title="TVS IQUBE ELECTRIC BOV">TVS IQUBE ELECTRIC BOV</option>
        <option value="TVS IQUBE ELECTRIC S BOV" title="TVS IQUBE ELECTRIC S BOV">TVS IQUBE ELECTRIC S BOV</option>
        <option value="TVS IQUBE ELECTRIC SMARTXONNECT BOV" title="TVS IQUBE ELECTRIC SMARTXONNECT BOV">TVS IQUBE ELECTRIC SMARTXONNECT BOV</option>
        <option value="TVS IQUBE ELECTRIC ST 12 BOV" title="TVS IQUBE ELECTRIC ST 12 BOV">TVS IQUBE ELECTRIC ST 12 BOV</option>
        <option value="TVS IQUBE ELECTRIC ST 17 BOV" title="TVS IQUBE ELECTRIC ST 17 BOV">TVS IQUBE ELECTRIC ST 17 BOV</option>
        <option value="TVS JUPETER BSVI-PH2" title="TVS JUPETER BSVI-PH2">TVS JUPETER BSVI-PH2</option>
        <option value="TVS JUPETER CLASSIC BSVI-PH2" title="TVS JUPETER CLASSIC BSVI-PH2">TVS JUPETER CLASSIC BSVI-PH2</option>
        <option value="TVS JUPETER ZX BSVI-PH2" title="TVS JUPETER ZX BSVI-PH2">TVS JUPETER ZX BSVI-PH2</option>
        <option value="TVS JUPETER ZX INTELLIGO BSVI-PH2" title="TVS JUPETER ZX INTELLIGO BSVI-PH2">TVS JUPETER ZX INTELLIGO BSVI-PH2</option>
        <option value="TVS JUPITER 113 BSVI-PH2" title="TVS JUPITER 113 BSVI-PH2">TVS JUPITER 113 BSVI-PH2</option>
        <option value="TVS JUPITER 125 BSVI-PH2" title="TVS JUPITER 125 BSVI-PH2">TVS JUPITER 125 BSVI-PH2</option>
        <option value="TVS JUPITER BSVI" title="TVS JUPITER BSVI">TVS JUPITER BSVI</option>
        <option value="TVS JUPITER BSVI-PH2" title="TVS JUPITER BSVI-PH2">TVS JUPITER BSVI-PH2</option>
        <option value="TVS JUPITER CLASSIC BSVI" title="TVS JUPITER CLASSIC BSVI">TVS JUPITER CLASSIC BSVI</option>
        <option value="TVS JUPITER CLASSIC BSVI-PH2" title="TVS JUPITER CLASSIC BSVI-PH2">TVS JUPITER CLASSIC BSVI-PH2</option>
        <option value="TVS JUPITER ZX BSVI" title="TVS JUPITER ZX BSVI">TVS JUPITER ZX BSVI</option>
        <option value="TVS JUPITER ZX BSVI-PH2" title="TVS JUPITER ZX BSVI-PH2">TVS JUPITER ZX BSVI-PH2</option>
        <option value="TVS KING LS+FI BSVI" title="TVS KING LS+FI BSVI">TVS KING LS+FI BSVI</option>
        <option value="TVS NTORQ 125 - SUPER SQUAD EDITION BSVI-PH2" title="TVS NTORQ 125 - SUPER SQUAD EDITION BSVI-PH2">TVS NTORQ 125 - SUPER SQUAD EDITION BSVI-PH2</option>
        <option value="TVS NTORQ 125 BSVI" title="TVS NTORQ 125 BSVI">TVS NTORQ 125 BSVI</option>
        <option value="TVS NTORQ 125 BSVI-PH2" title="TVS NTORQ 125 BSVI-PH2">TVS NTORQ 125 BSVI-PH2</option>
        <option value="TVS NTORQ 125 RACE EDITION BSVI" title="TVS NTORQ 125 RACE EDITION BSVI">TVS NTORQ 125 RACE EDITION BSVI</option>
        <option value="TVS NTORQ 125 RACE EDITION BSVI-PH2" title="TVS NTORQ 125 RACE EDITION BSVI-PH2">TVS NTORQ 125 RACE EDITION BSVI-PH2</option>
        <option value="TVS NTORQ 125 RACE XP BSVI" title="TVS NTORQ 125 RACE XP BSVI">TVS NTORQ 125 RACE XP BSVI</option>
        <option value="TVS NTORQ 125 RACE XP BSVI-PH2" title="TVS NTORQ 125 RACE XP BSVI-PH2">TVS NTORQ 125 RACE XP BSVI-PH2</option>
        <option value="TVS NTORQ 125 XT BSVI-PH2" title="TVS NTORQ 125 XT BSVI-PH2">TVS NTORQ 125 XT BSVI-PH2</option>
        <option value="TVS NTORQ 125XT BSVI" title="TVS NTORQ 125XT BSVI">TVS NTORQ 125XT BSVI</option>
        <option value="TVS RADEON BSVI-PH2" title="TVS RADEON BSVI-PH2">TVS RADEON BSVI-PH2</option>
        <option value="TVS RADEON DISC BSVI" title="TVS RADEON DISC BSVI">TVS RADEON DISC BSVI</option>
        <option value="TVS RADEON DRUM BSVI" title="TVS RADEON DRUM BSVI">TVS RADEON DRUM BSVI</option>
        <option value="TVS RAIDER BSVI" title="TVS RAIDER BSVI">TVS RAIDER BSVI</option>
        <option value="TVS RAIDER BSVI-PH2" title="TVS RAIDER BSVI-PH2">TVS RAIDER BSVI-PH2</option>
        <option value="TVS RAIDER SUPER SQUAD EDITION BSVI-PH2" title="TVS RAIDER SUPER SQUAD EDITION BSVI-PH2">TVS RAIDER SUPER SQUAD EDITION BSVI-PH2</option>
        <option value="TVS RONIN 2CH BSVI" title="TVS RONIN 2CH BSVI">TVS RONIN 2CH BSVI</option>
        <option value="TVS RONIN BSVI-PH2" title="TVS RONIN BSVI-PH2">TVS RONIN BSVI-PH2</option>
        <option value="TVS SCOOTY PEP+ BSVI" title="TVS SCOOTY PEP+ BSVI">TVS SCOOTY PEP+ BSVI</option>
        <option value="TVS SCOOTY ZEST BSVI" title="TVS SCOOTY ZEST BSVI">TVS SCOOTY ZEST BSVI</option>
        <option value="TVS SPORT DURALIFE BSVI" title="TVS SPORT DURALIFE BSVI">TVS SPORT DURALIFE BSVI</option>
        <option value="TVS SPORT DURALIFE BSVI-PH2" title="TVS SPORT DURALIFE BSVI-PH2">TVS SPORT DURALIFE BSVI-PH2</option>
        <option value="TVS SPORT ELS BSVI" title="TVS SPORT ELS BSVI">TVS SPORT ELS BSVI</option>
        <option value="TVS SPORT ELS BSVI-PH2" title="TVS SPORT ELS BSVI-PH2">TVS SPORT ELS BSVI-PH2</option>
        <option value="TVS SPORT KLS BSVI" title="TVS SPORT KLS BSVI">TVS SPORT KLS BSVI</option>
        <option value="TVS STAR CITY+ BSVI" title="TVS STAR CITY+ BSVI">TVS STAR CITY+ BSVI</option>
        <option value="TVS XL 100 BSVI" title="TVS XL 100 BSVI">TVS XL 100 BSVI</option>
        <option value="TVS XL 100 BSVI-PH2" title="TVS XL 100 BSVI-PH2">TVS XL 100 BSVI-PH2</option>
        <option value="TVS XL 100 COMFORT BSVI" title="TVS XL 100 COMFORT BSVI">TVS XL 100 COMFORT BSVI</option>
        <option value="TVS XL 100 COMFORT I-TOUCH START BSVI" title="TVS XL 100 COMFORT I-TOUCH START BSVI">TVS XL 100 COMFORT I-TOUCH START BSVI</option>
        <option value="TVS XL 100 COMFORT I-TOUCH START BSVI-PH2" title="TVS XL 100 COMFORT I-TOUCH START BSVI-PH2">TVS XL 100 COMFORT I-TOUCH START BSVI-PH2</option>
        <option value="TVS XL 100 HEAVY DUTY BSVI" title="TVS XL 100 HEAVY DUTY BSVI">TVS XL 100 HEAVY DUTY BSVI</option>
        <option value="TVS XL 100 HEAVY DUTY BSVI-PH2" title="TVS XL 100 HEAVY DUTY BSVI-PH2">TVS XL 100 HEAVY DUTY BSVI-PH2</option>
        <option value="TVS XL 100 HEAVY DUTY I-TOUCH START BSVI" title="TVS XL 100 HEAVY DUTY I-TOUCH START BSVI">TVS XL 100 HEAVY DUTY I-TOUCH START BSVI</option>
        <option value="TVS XL100 COMFORT I-TOUCH START BSVI" title="TVS XL100 COMFORT I-TOUCH START BSVI">TVS XL100 COMFORT I-TOUCH START BSVI</option>
        <option value="TVS XL100 HEAVY DUTY I-TOUCH START BSVI-PH2" title="TVS XL100 HEAVY DUTY I-TOUCH START BSVI-PH2">TVS XL100 HEAVY DUTY I-TOUCH START BSVI-PH2</option>
        <option value="TVS ZEST BSVI-PH2" title="TVS ZEST BSVI-PH2">TVS ZEST BSVI-PH2</option>
        <option value="tvs-apache rtr 180 (with ride mode) BSVI-PH2" title="tvs-apache rtr 180 (with ride mode) BSVI-PH2">tvs-apache rtr 180 (with ride mode) BSVI-PH2</option>
        <option value="TVS-RONIN 1CH BSVI" title="TVS-RONIN 1CH BSVI">TVS-RONIN 1CH BSVI</option>
        <option value="TVS-STAR CITY + BSVI-PH2" title="TVS-STAR CITY + BSVI-PH2">TVS-STAR CITY + BSVI-PH2</option>
        </select>"""
    soup=BeautifulSoup(html1,"html.parser")
    titles=[options.text.strip() for options in soup.find_all("option")] 
    return titles 

def op_finder2():
    html1="""
        <select name="ctl00$OnlineDealerContent$ddlBusinessDistrict" onchange="javascript:setTimeout('__doPostBack(\'ctl00$OnlineDealerContent$ddlBusinessDistrict\',\'\')', 0)" id="ctl00_OnlineDealerContent_ddlBusinessDistrict" tabindex="43" class="ddl" style="width:179px;">
        <option selected="selected" value="0" title="Select">Select</option>
        <option value="1" title="ADILABAD">ADILABAD</option>
        <option value="29" title="BHADRADRI">BHADRADRI</option>
        <option value="22" title="HANUMAKONDA">HANUMAKONDA</option>
        <option value="7" title="HYDERABAD">HYDERABAD</option>
        <option value="27" title="JAGITYAL">JAGITYAL</option>
        <option value="44" title="JANGOAN">JANGOAN</option>
        <option value="40" title="JAYASHANKAR">JAYASHANKAR</option>
        <option value="45" title="JOGULAMBA">JOGULAMBA</option>
        <option value="36" title="KAMAREDDY">KAMAREDDY</option>
        <option value="8" title="KARIMNAGAR">KARIMNAGAR</option>
        <option value="9" title="KHAMMAM">KHAMMAM</option>
        <option value="42" title="KOMRAMBHEEM">KOMRAMBHEEM</option>
        <option value="12" title="MAHABOOBNAGAR">MAHABOOBNAGAR</option>
        <option value="41" title="MAHABUBABAD">MAHABUBABAD</option>
        <option value="26" title="MANCHERIYAL">MANCHERIYAL</option>
        <option value="13" title="MEDAK">MEDAK</option>
        <option value="37" title="MEDCHAL M-GIRI">MEDCHAL M-GIRI</option>
        <option value="51" title="MULUGU">MULUGU</option>
        <option value="30" title="NAGARKURNOOL">NAGARKURNOOL</option>
        <option value="14" title="NALGONDA">NALGONDA</option>
        <option value="49" title="NARAYANPET">NARAYANPET</option>
        <option value="25" title="NIRMAL">NIRMAL</option>
        <option value="16" title="NIZAMABAD">NIZAMABAD</option>
        <option value="28" title="PEDDAPALLI">PEDDAPALLI</option>
        <option value="43" title="RAJANNA">RAJANNA</option>
        <option value="18" title="RANGA REDDY">RANGA REDDY</option>
        <option value="33" title="SANGAREDDY">SANGAREDDY</option>
        <option value="32" title="SIDDIPET">SIDDIPET</option>
        <option value="34" title="SURYAPET">SURYAPET</option>
        <option value="38" title="VIKARABAD">VIKARABAD</option>
        <option value="31" title="WANAPARTHY">WANAPARTHY</option>
        <option value="39" title="WARANGAL">WARANGAL</option>
        <option value="35" title="YADADRI">YADADRI</option>

        </select>
           """
    soup=BeautifulSoup(html1,"html.parser")
    titles=[option.text.strip() for option in soup.find_all("option")]
    return titles 

def op_finder3():
    html_code="""
<select name="ctl00$OnlineDealerContent$ddlInsCmpyName" onchange="javascript:setTimeout('__doPostBack(\'ctl00$OnlineDealerContent$ddlInsCmpyName\',\'\')', 0)" id="ctl00_OnlineDealerContent_ddlInsCmpyName" tabindex="69" class="ddl" style="width:250px;">
	<option selected="selected" value="0" title="Select">Select</option>
	<option value="58" title="National Insurance Company Ltd">National Insurance Company Ltd</option>
	<option value="90" title="The New India Assurance  Company Ltd.">The New India Assurance  Company Ltd.</option>
	<option value="102" title="Royal Sundaram Alliance Insurance Company Ltd.">Royal Sundaram Alliance Insurance Company Ltd.</option>
	<option value="103" title="Reliance General Insurance Company Ltd.">Reliance General Insurance Company Ltd.</option>
	<option value="106" title="IFFCO Tokio General Insurance Company Ltd.">IFFCO Tokio General Insurance Company Ltd.</option>
	<option value="108" title="Tata AIG General Insurance Company Ltd.">Tata AIG General Insurance Company Ltd.</option>
	<option value="113" title="Bajaj Allianz General Insurance Company Ltd. ">Bajaj Allianz General Insurance Company Ltd. </option>
	<option value="115" title="ICICI Lombard General Insurance Company Ltd. ">ICICI Lombard General Insurance Company Ltd. </option>
	<option value="123" title="Cholamandalam MS General Insurance Company Ltd.">Cholamandalam MS General Insurance Company Ltd.</option>
	<option value="125" title="HDFC-ERGO General Insurance Company Ltd.">HDFC-ERGO General Insurance Company Ltd.</option>
	<option value="132" title="Future Generali Insurance Company Ltd.">Future Generali Insurance Company Ltd.</option>
	<option value="134" title="Universal Sompo General Insurance Company Ltd.">Universal Sompo General Insurance Company Ltd.</option>
	<option value="137" title="Shriram General Insurance  Company Ltd.">Shriram General Insurance  Company Ltd.</option>
	<option value="139" title="Bharati AXA General Insurance Company Ltd.">Bharati AXA General Insurance Company Ltd.</option>
	<option value="141" title="Raheja QBE General Insurance Company Ltd.">Raheja QBE General Insurance Company Ltd.</option>
	<option value="144" title="SBI General Insurance  Company Ltd.">SBI General Insurance  Company Ltd.</option>
	<option value="146" title="L&amp;T General Insurance  Company Ltd.">L&amp;T General Insurance  Company Ltd.</option>
	<option value="149" title="Magma HDI General Insurance  Company Ltd.">Magma HDI General Insurance  Company Ltd.</option>
	<option value="150" title="Liberty Videocon General Insurance  Company Ltd.">Liberty Videocon General Insurance  Company Ltd.</option>
	<option value="152" title="Kotak Mahindra General Insurance">Kotak Mahindra General Insurance</option>
	<option value="157" title="Acko General Insurance Limited">Acko General Insurance Limited</option>
	<option value="158" title="Go Digit General Insurance Limited">Go Digit General Insurance Limited</option>
	<option value="159" title="Zuno General Insurance Limited">Zuno General Insurance Limited</option>
	<option value="545" title="United India Insurance Company Ltd.">United India Insurance Company Ltd.</option>
	<option value="556" title="The Oriental Insurance Company Ltd.">The Oriental Insurance Company Ltd.</option>

</select>
"""
    soup=BeautifulSoup(html_code,"html.parser")
    titles=[option.text.strip() for option in soup.find_all("option")]
    return titles 

def save_changes():
    date=datetime.date(int(yy_entry.get()),int(mm_entry.get()),1)  
    DOB_date=datetime.date(int(y_entry.get()),int(m_entry.get()),int(d_entry.get())) 
    infrom_date=datetime.date(int(yyyy_inf_entry.get()),int(mm_inf_entry.get()),int(dd_inf_entry.get()))
    into_date=datetime.date(int(yyyy_int_entry.get()),int(mm_int_entry.get()),int(dd_int_entry.get()))
    fin_date=datetime.date(int(yyyy_fin_entry.get()),int(mm_fin_entry.get()),int(dd_fin_entry.get()))

    form_data = {
    "f_name": f_name_entry.get(),
    "l_name": l_name_entry.get(),
    "email": email_entry.get(),
    "phone": phone_entry.get(),
    "DOB": DOB_date,
    "is_veh_fin": var1.get(),
    "is_phy_chal":var2.get(),
    "is_sec_veh": var3.get(),
    "rep_name":rep_name.get(),
    "qualification":var4.get(),
    "aadhar_no":aad_entry.get(),
    "nationality":var5.get(),
    "gender":var6.get(),
    "address_proof":add_pro.get(),
    "sel_op": selected_option.get(),
    "Engine_no": eng_entry.get(),
    "Chasis_no": cha_entry.get(),
    "Colour": col_entry.get(),
    "Invoice_no": in_entry.get(),
    "Price": pr_entry.get(),
    "manu_date":date,
    "District":dis.get(),
    "Mandal":man_entry.get(),
    "Location":loc_entry.get(),
    "Pincode": pin_entry.get(),
    "House_no":hou_entry.get(),
    "Street": stre_entry.get(),
    "Landmark":lan_entry.get(),
    "City":cit_entry.get(),
    "Company":comp.get(),
    "Insurance_Type":insu.get(),
    "Policy_No":pol_entry.get(),
    "Insu_from":infrom_date,
    "Insu_to":into_date,
    "fin_name":finn_entry.get(),
    "fin_add":fina_entry.get(),
    "fin_dis":dis_fin.get(),
    "fin_Man":man_entry_fin.get(),
    "fin_city":cit_entry_fin.get(),
    "fin_date":fin_date 
    }
    
    conn=sqlite3.connect("details.db")
    cursor=conn.cursor()


    query=f"INSERT INTO customer_details ({','.join(form_data.keys())}) VALUES({','.join([':'+key for key in form_data.keys()])})" 
    #for columns-Output: "name, email, phone" for values-[':name', ':email', ':phone'];  
    cursor.execute(query,form_data)
    
    cursor.execute("SELECT * FROM customer_details ")
    print(cursor.fetchall())
    messagebox.showinfo("Success","updated in the db")

    conn.commit()
    conn.close()



#to create a window
root=tk.Tk()
root.title("Customer Entry Form")

#entry fields 
#First name field
tk.Label(root,text=" First Name: ").grid(row=0,column=0)
f_name_entry=tk.Entry(root)
f_name_entry.grid(row=0,column=1) 

#last name field
tk.Label(root,text="Last name: ").grid(row=0,column=2)
l_name_entry=tk.Entry(root)
l_name_entry.grid(row=0,column=3)

#email field 
tk.Label(root,text="Email: ").grid(row=0,column=4)
email_entry=tk.Entry(root)
email_entry.grid(row=0,column=5)

#phone field 
tk.Label(root,text="Phone: ").grid(row=0,column=6)
phone_entry=tk.Entry(root)
phone_entry.grid(row=0,column=7)

#DOB 
tk.Label(root,text="DOB").grid(row=1,column=0)
d_entry=tk.Entry(root)
m_entry=tk.Entry(root)
y_entry=tk.Entry(root)
d_entry.grid(row=1,column=1)
m_entry.grid(row=1,column=2)
y_entry.grid(row=1,column=3) 

#Creating radiobuttons for taking in a choice 
var1=tk.StringVar(value="")
tk.Label(root,text="Is Vehicle Financed?").grid(row=2,column=0)

options=["Yes","No"]
for i,op in enumerate(options):
    tk.Radiobutton(root,text=op,variable=var1,value=op).grid(row=2,column=i+1) 

#physically challenged(radio buttons) 
var2=tk.StringVar(value="")    
tk.Label(root,text="Physically Challenged? ").grid(row=3,column=0)
options=["Yes","No"]
for i,op in enumerate(options):
    tk.Radiobutton(root,text=op,variable=var2,value=op).grid(row=3,column=i+1)

#is second vehicle
var3=tk.StringVar(value="")    
tk.Label(root,text="Second Vehicle? ").grid(row=4,column=0)
options=["YES","NO"]
for i,op in enumerate(options):
    tk.Radiobutton(root,text=op,variable=var3,value=op).grid(row=4,column=i+1) 

#father's or husband's name    
tk.Label(root,text="Father's/Husband's Name").grid(row=1,column=4) 
rep_name=tk.Entry(root)
rep_name.grid(row=1,column=5)

#qualification 
tk.Label(root,text="Qualification:").grid(row=5,column=0)
var4=tk.StringVar(value="")
options=["POST GRADUATE","GRADUATE","10th Pass","8th Pass","Below 8th Class","Illiterate"]
for i,op in enumerate(options):
    tk.Radiobutton(root,text=op,variable=var4,value=op).grid(row=5,column=i+1)

#aadhar number 
tk.Label(root,text="Aadhar No.").grid(row=6,column=0)
aad_entry=tk.Entry(root)
aad_entry.grid(row=6,column=1) 

#nationality
tk.Label(root,text="Nationality").grid(row=7,column=0)
var5=tk.StringVar(value="")
options=["Indian","NRI","Foreigner"]
for i,op in enumerate(options):
    tk.Radiobutton(root,text=op,variable=var5,value=op).grid(row=7,column=i+1)

#gender 
tk.Label(root,text="Gender").grid(row=8,column=0)
var6=tk.StringVar()
options=["Male","Female"]
for i,op in enumerate(options):
    tk.Radiobutton(root,text=op,variable=var6,value=op).grid(row=8,column=i+1)

#address proof
tk.Label(root,text="Address Proof ").grid(row=9,column=0) 
add_pro=tk.StringVar()
add_pro.set("Select an Item") 
options=["Passport","Telephone bill (LANDLINE/MOBILE)","ELECTRICITY BILL ISSUED BY DISCOMS"
         ,"Voter's ID Card","Ration Card","MULTI PURPOSE HOUSEHOLD CARD","PAYSLIP"
         ,"MUNICIPAL TAX (NOTICE/RECEIPT)","BANK PASSBOOK (PUBLIC/PRIVATE SECTOR/BANKING INSTITUTION IN RBI 2ND SCHEDULE 1934)"
         ,"GAS ALLOTMENT ORDER","DRIVING LICENCE","REGISTRATION CERTIFICATE","WATER BILL(MUNICIPAL/WATER WORKS DEPT)"
         ,"LIC","VOTER ID","Driving License","ADHAR CARD"] 
add_pro_ops=tk.OptionMenu(root,add_pro,*options)
add_pro_ops.grid(row=9,column=1)

#select Maker's_class 
tk.Label(root,text="Maker's Class").grid(row=9,column=2) 
selected_option=tk.StringVar()
selected_option.set("Select an option") 
options=option_finder()
drop_down=tk.OptionMenu(root,selected_option,*options)
drop_down.grid(row=9,column=3)

#engine number 
tk.Label(root,text="Engine number").grid(row=10,column=0)
eng_entry=tk.Entry(root)
eng_entry.grid(row=10,column=1)

#Chasis no.
tk.Label(root,text="Chasis no.").grid(row=10,column=2)
cha_entry=tk.Entry(root)
cha_entry.grid(row=10,column=3)

#Colour 
tk.Label(root,text="Colour").grid(row=10,column=4)
col_entry=tk.Entry(root)
col_entry.grid(row=10,column=5)

#Invoice no.
tk.Label(root,text="Invoice no.").grid(row=11,column=0)
in_entry=tk.Entry(root)
in_entry.grid(row=11,column=1)

#price
tk.Label(root,text="Price").grid(row=11,column=2)
pr_entry=tk.Entry(root)
pr_entry.grid(row=11,column=3)

#manu date
tk.Label(root,text="Manufacture Date").grid(row=11,column=4)
mm_entry=tk.Entry(root)
yy_entry=tk.Entry(root)
mm_entry.grid(row=11,column=5)
yy_entry.grid(row=11,column=6)

#District 
tk.Label(root,text="Add District").grid(row=12,column=0)
dis=tk.StringVar()
dis.set("Select an Item") 
options=op_finder2()
dis_selector=tk.OptionMenu(root,dis,*options)
dis_selector.grid(row=12,column=1)

#mandal
tk.Label(root,text="Mandal").grid(row=12,column=2)
man_entry=tk.Entry(root)
man_entry.grid(row=12,column=3)

#Location(ONly for hyderabad)
tk.Label(root,text="Location").grid(row=12,column=4)
loc_entry=tk.Entry(root)
loc_entry.grid(row=12,column=5)

#pincode
tk.Label(root,text="Pincode").grid(row=13,column=0)
pin_entry=tk.Entry(root)
pin_entry.grid(row=13,column=1)

#House_no
tk.Label(root,text="House No").grid(row=13,column=2)
hou_entry=tk.Entry(root)
hou_entry.grid(row=13,column=3)

#Street
tk.Label(root,text="Street Name").grid(row=13,column=4)
stre_entry=tk.Entry(root)
stre_entry.grid(row=13,column=5)

#Landmark
tk.Label(root,text="Landmark").grid(row=14,column=0)
lan_entry=tk.Entry(root)
lan_entry.grid(row=14,column=1)

#City
tk.Label(root,text="City").grid(row=14,column=2)
cit_entry=tk.Entry(root)
cit_entry.grid(row=14,column=3)

#company
tk.Label(root,text="Insurance Company name").grid(row=15,column=0)
comp=tk.StringVar()
comp.set("Select an option")
options=op_finder3()
drop_down=tk.OptionMenu(root,comp,*options)
drop_down.grid(row=15,column=1)

#Insurance Type
tk.Label(root,text="Isurance Type").grid(row=15,column=2)
insu=tk.StringVar()
insu.set("Select an option")
options=["COMPREHENSIVE","PUBLIC LIABILITY","THIRD PARTY LIABILITY","OTHER"]
drop_down=tk.OptionMenu(root,insu,*options)
drop_down.grid(row=15,column=3) 

#policy no
tk.Label(root,text="Policy No.").grid(row=16,column=0)
pol_entry=tk.Entry(root)
pol_entry.grid(row=16,column=1)

#Insurance From
tk.Label(root,text="Insurance from").grid(row=17,column=0)
dd_inf_entry=tk.Entry(root)
mm_inf_entry=tk.Entry(root)
yyyy_inf_entry=tk.Entry(root)
dd_inf_entry.grid(row=17,column=1)
mm_inf_entry.grid(row=17,column=2)
yyyy_inf_entry.grid(row=17,column=3)

#Insurance to
tk.Label(root,text="Insurance to").grid(row=17,column=5)
dd_int_entry=tk.Entry(root)
mm_int_entry=tk.Entry(root)
yyyy_int_entry=tk.Entry(root)
dd_int_entry.grid(row=17,column=6)
mm_int_entry.grid(row=17,column=7)
yyyy_int_entry.grid(row=17,column=8) 

#Fin Name 
tk.Label(root,text="Financer's Name").grid(row=18,column=0)
finn_entry=tk.Entry(root)
finn_entry.grid(row=18,column=1)

#Address 1
tk.Label(root,text="Financer's Address1").grid(row=18,column=2)
fina_entry=tk.Entry(root)
fina_entry.grid(row=18,column=3)

#distrcit(dd)
tk.Label(root,text="Add District").grid(row=18,column=4)
dis_fin=tk.StringVar()
dis_fin.set("Select an Item") 
options=op_finder2()
dis_selector_fin=tk.OptionMenu(root,dis_fin,*options)
dis_selector_fin.grid(row=18,column=5)

#Mandal(dd)
tk.Label(root,text="Mandal").grid(row=19,column=0)
man_entry_fin=tk.Entry(root)
man_entry_fin.grid(row=19,column=1)

#City 
tk.Label(root,text="City").grid(row=19,column=2)
cit_entry_fin=tk.Entry(root)
cit_entry_fin.grid(row=19,column=3)

#Aggregate date 
tk.Label(root,text="Aggregate Date").grid(row=19,column=4)
dd_fin_entry=tk.Entry(root)
mm_fin_entry=tk.Entry(root)
yyyy_fin_entry=tk.Entry(root)
dd_fin_entry.grid(row=19,column=5)
mm_fin_entry.grid(row=19,column=6)
yyyy_fin_entry.grid(row=19,column=7) 

#submit button 
submit_btn=tk.Button(root,text="SUBMIT",command=save_changes)
submit_btn.grid(row=21,column=2) 
 
#button to see all the values in db
sub=tk.Button(root,text="Contents of DB",command=contents)
sub.grid(row=21,column=3) 

root.mainloop()



