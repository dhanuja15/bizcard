#IMPORTING REQUIRED PACKAGES
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_option_menu import option_menu
import easyocr
from PIL import Image
import re
import io
import sqlite3

#READ TEXT FROM IMAGE 
def text_from_img(path):
  inp_img=Image.open(path)
  inp_img_array=np.array(inp_img)
  read=easyocr.Reader(['en'])
  txt_img=read.readtext(inp_img_array,detail=0)
 
  return txt_img,inp_img

#EXTRACTION OF TEXT FROM IMAGE
def text_extraction(text):
  dict={"NAME":[],"DESIGNATION":[],"COMPANY NAME":[],"CONTACT":[],"EMAIL_ID":[],"WEBSITE":[],
        "ADDRESS":[],"PINCODE":[]}
  
  for ind,i in enumerate(text):

    #CARD HOLDER NAME
    if ind == 0:
      dict["NAME"].append(i)

    #DESIGNATION
    elif ind == 1:
      dict["DESIGNATION"].append(i)

    #CONTACT NUMBER
    elif "-" in i:
      dict["CONTACT"].append(i)
    if len(dict["CONTACT"]) == 2:
      dict["CONTACT"] = " & ".join(dict["CONTACT"])

    #EMAIL_ID
    elif '@' in i and '.com' in i:
      dict["EMAIL_ID"].append(i)

    # WEBSITE_URL
    website_pattern = re.compile(r'(www\.[^\s]+)')
    if re.search(website_pattern, i):
      dict["WEBSITE"].append(i)

    #PINCODE
    pincode_pattern = re.compile(r'\b\d{6}\b')
    if re.search(pincode_pattern, i):
      dict["PINCODE"].append(i)

    #COMPANY NAME
    elif ind == len(text) - 1:
      dict["COMPANY NAME"].append(i)

    #ADDRESS
    else:
      rem=re.sub(r'[,;]','',i)
      dict["ADDRESS"].append(rem)

  for key,value in dict.items():
    if len(value)>0:
      concadenate= " ".join(value)
      dict[key]=[concadenate]
    else:
      value="NA"
      dict[key]=[value]

  return dict


#STREAMLIT APP PART

st.set_page_config(layout="wide")
st.markdown("<h1 style=color:blue><center>BizCardX: Extracting Business Card Data with OCR</center></h1>",unsafe_allow_html=True)

with st.sidebar:
  st.markdown("**Navigation**")
  select=st.radio("MENU",["HOME","UPLOAD","VIEW AND MODIFY","DELETE"])

if select=="HOME":
  st.subheader(":violet[Welcome to the BizCardX App!]")
  st.markdown('### Bizcard is a Python application designed to extract information from business cards. It utilizes various technologies such as :blue[Streamlit, Python, EasyOCR , PIL and SQLite] database to achieve this functionality.')
  st.write("")
  st.write("")
  st.write("")
  st.write('### The main purpose of Bizcard is to automate the process of extracting key details from business card images, such as the name, designation, company, contact information, and other relevant data. By leveraging the power of OCR (Optical Character Recognition) provided by EasyOCR, Bizcard is able to extract text from the images.')
  st.write("")
  st.write("")
  st.write("")
  st.subheader(':violet[Technologies Used]')
  st.write('### :white[Python]  :white[Streamlit] :white[EasyOCR]  :white[PIL(Python Imaging Library)]  :white[SQLite3]')
  st.write("EasyOCR is an open-source optical character recognition (OCR) library that enables developers to easily extract text from images."
  "EasyOCR uses deep learning techniques to accurately recognize text in images, making it a powerful tool for tasks such as document processing, image captioning, and text extraction from scanned documents.")

if select=="UPLOAD":
  st.subheader("Upload Business Card Image")
  img=st.file_uploader("Upload the image",type=["jpg","jpeg","png"])

  if img is not None:
    st.image(img,width=500)
    text_image,input_image=text_from_img(img)
    text_data=text_extraction(text_image)

    if text_data:
      st.success("TEXT IS EXTRACTED SUCCESSFULLY FROM IMAGE")

    text_df=pd.DataFrame(text_data)

    #Image to bytes conversion
    img_bytes=io.BytesIO()
    input_image.save(img_bytes,format="PNG")
    data=img_bytes.getvalue()

    img_data={"IMAGE":[data]}
    img_df=pd.DataFrame(img_data)

    con_df=pd.concat([text_df,img_df],axis=1)
    st.dataframe(con_df)

    button=st.button("Save",use_container_width=True)
    if button:
      mydb=sqlite3.connect("bizcard.db")
      cursor=mydb.cursor()

      #create table

      table_query='''create table if  not exists bizcard_data (name varchar(255),designation varchar(255),company_name varchar(255),
                    contact varchar(30),email varchar(255),website text,address text,pincode varchar(255),image text)'''
      cursor.execute(table_query)
      mydb.commit()

      mydb = sqlite3.connect("bizcard.db")
      cursor = mydb.cursor()
      select_query = "SELECT * FROM bizcard_data WHERE name = ?"
      cursor.execute(select_query, (text_data["NAME"][0],))
      existing_data = cursor.fetchone()

      if existing_data:
        # Display the existing data
        st.write("This card holder's information already exists in the database:")
        existing_df = pd.DataFrame([existing_data], columns=("NAME", "DESIGNATION", "COMPANY NAME", "CONTACT", "EMAIL", "WEBSITE", "ADDRESS", "PINCODE", "IMAGE"))
        st.dataframe(existing_df)
      else:
        # Save the new data
        insert_query = '''insert into bizcard_data(name, designation, company_name, contact, email, website, address, pincode, image)
                          values(?,?,?,?,?,?,?,?,?)'''
        datas = con_df.values.tolist()[0]
        cursor.execute(insert_query, datas)
        mydb.commit()
        st.success("Table is saved successfully")

if select == "VIEW AND MODIFY":

  st.subheader("View and Modify Business Card Data")
  method=st.radio("Select the method",["None","Preview","Modify"])

  if method=="None":
    st.write("")

  if method == "Preview":
    mydb=sqlite3.connect("bizcard.db")
    cursor=mydb.cursor()

    select_query="select * from bizcard_data"
    cursor.execute(select_query)
    table=cursor.fetchall()
    tab_df=pd.DataFrame(table,columns=("NAME","DESIGNATION","COMPANY NAME", "CONTACT", "EMAIL", "WEBSITE", 
                                      "ADDRESS","PINCODE", "IMAGE"))
    st.dataframe(tab_df)

  if method == "Modify":
    mydb=sqlite3.connect("bizcard.db")
    cursor=mydb.cursor()

    select_query="select * from bizcard_data"
    cursor.execute(select_query)
    table=cursor.fetchall()
    tab_df=pd.DataFrame(table,columns=("NAME","DESIGNATION","COMPANY NAME", "CONTACT", "EMAIL", "WEBSITE", 
                                              "ADDRESS","PINCODE", "IMAGE"))

    col1,col2=st.columns(2)
    with col1:
      name_selected=st.selectbox("Select the name_",tab_df["NAME"])

    df=tab_df[tab_df["NAME"]==name_selected]

    copy_df=df.copy()


    col1,col2=st.columns(2)
    with col1:
      name_modified=st.text_input("Name",df["NAME"].unique()[0])
      designation_modified=st.text_input("Designation",df["DESIGNATION"].unique()[0])
      comp_name_modified=st.text_input("Company Name",df["COMPANY NAME"].unique()[0])
      contact_modified=st.text_input("Contact",df["CONTACT"].unique()[0])
      copy_df["NAME"]=name_modified
      copy_df["DESIGNATION"]=designation_modified
      copy_df["COMPANY NAME"]=comp_name_modified
      copy_df["CONTACT"]=contact_modified

    with col2:
      email_modified=st.text_input("Email",df["EMAIL"].unique()[0])
      website_modified=st.text_input("Website",df["WEBSITE"].unique()[0])
      address_modified=st.text_input("Address",df["ADDRESS"].unique()[0])
      pincode_modified=st.text_input("Pincode",df["PINCODE"].unique()[0])
      image_modified=st.text_input("Image",df["IMAGE"].unique()[0])
      copy_df["EMAIL"]=email_modified
      copy_df["WEBSITE"]=website_modified
      copy_df["ADDRESS"]=address_modified
      copy_df["PINCODE"]=pincode_modified
      copy_df["IMAGE"]=image_modified

    st.dataframe(copy_df)
    col1,col2=st.columns(2)
    with col1:
      click=st.button("Modify",use_container_width=True)

    if click:
      mydb=sqlite3.connect("bizcard.db")
      cursor=mydb.cursor()

      cursor.execute(f"delete from bizcard_data where name='{name_selected}'")
      mydb.commit()

      insert_query='''insert into bizcard_data(name, designation, company_name, contact, email, website, address, pincode, image)
                                          values(?,?,?,?,?,?,?,?,?)'''

      datas=copy_df.values.tolist()[0]
      cursor.execute(insert_query,datas)
      mydb.commit()

      st.success("Table is modified succesfully")


if select=="DELETE":

  st.subheader("Delete Business Card Data")
  mydb=sqlite3.connect("bizcard.db")
  cursor=mydb.cursor()

  col1,col2=st.columns(2)
  with col1:

    select_query = "SELECT DISTINCT name FROM bizcard_data"
    cursor.execute(select_query)
    unique_names = [i[0] for i in cursor.fetchall()]
    
    if not unique_names:
        st.warning("No names to delete.")
    else:
        name_ = st.selectbox("Select the name", unique_names)
        st.write(f"Selected name: {name_}")

  with col2:
    select_query=f"select designation from bizcard_data where name='{name_}'"
    cursor.execute(select_query)
    table1=cursor.fetchall()
    mydb.commit()
    designation=[]
    for j in table1:
      designation.append(j[0])
      dsgn=st.selectbox("Select the designation",designation)
      st.write(f"selected designation: {dsgn}")

  remove=st.button("DELETE",use_container_width=True)
  if remove:
    cursor.execute(f"delete from bizcard_data where NAME='{name_}' and DESIGNATION='{dsgn}'")
    mydb.commit()
    st.warning("Deleted")
