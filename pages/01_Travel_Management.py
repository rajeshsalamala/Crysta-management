# Contents of ~/my_app/pages/page_2.py
import streamlit as st
from gauth import get_data
from datetime import date, datetime,time
from PIL import Image
import pandas as pd
import jinja2
import pdfkit
import streamlit.components.v1 as components

import os

try:
    os.remove("output.html")
except:
    pass


df = pd.DataFrame(get_data())
st.set_page_config(layout="centered",initial_sidebar_state="expanded",)


# Store the initial value of widgets in session state
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False





def generate_slip(date,vehicle_number):

    res = df[(df['Booking_Date']==date) & (df['Vehicle_Number']==vehicle_number)]
    try:
        context = res.T.to_dict()[res.index[0]]
    except IndexError:
        image = Image.open("not-found.jpg")
        st.image(image)
    
    template_loader = jinja2.FileSystemLoader('./')
    template_env    = jinja2.Environment(loader=template_loader)
    template        = template_env.get_template('table.html')
    output_text     = template.render(context)

    # Creating an HTML file
    Func = open("output.html","w")
    # Adding input data to the HTML file
    Func.write(output_text)
    # Saving the data into the HTML file
    Func.close()


def generate_multi_slip(start_date,end_date,vehicle_number):
    context = []
    res = df[(df['Booking_Date']>=start_date) & (df['Booking_Date']<=end_date)& (df['Vehicle_Number']==vehicle_number)]
    res = res.reset_index(drop=True)
    if not res.empty:
        col = ['Booking_Date', 'Vehicle_Number', 'Driver_Name', 'Area_Reference', 'Start_Reading', 
            'End_Reading', 'Start_Time', 'End_Time', 'Extra_KMS', 'Extra_time', 'Tolls_Amount', 
            'Driver_Allowance', 'Advance', 'Balance_Bill_Amount']
        res = res[col]
        total_due = sum(res['Balance_Bill_Amount'].to_list())
        try:
            for x in res.index.to_list():
                dic = res.T.to_dict()[res.index[x]]
                context.append(dic)
        except IndexError:
            image = Image.open("not-found.jpg")
            st.image(image)
        
        template_loader = jinja2.FileSystemLoader('./')
        template_env    = jinja2.Environment(loader=template_loader)
        template        = template_env.get_template('multitable.html')
        output_text     = template.render(myArray=context,total_balance_Amount=total_due)    

        # Creating an HTML file
        Func = open("output.html","w")
        # Adding input data to the HTML file
        Func.write(output_text)
        # Saving the data into the HTML file
        Func.close()
    else:
        image = Image.open("not-found.jpg")
        st.image(image)

        

def get_report():

    with st.form("single_slip_app_form",clear_on_submit=True):
        st.title('Single Duty Slip Generation')
        ## Vehicle_Selection
        Vehicle_Number = st.selectbox(
            "Please Select The Vehicle",
            ("TS07GN5199", "TS07ES0693"),
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled)
        Booking_Date         = st.date_input('Booking Date')
        # Submit button.
        submitted = st.form_submit_button("SUBMIT")
        if submitted:
            Booking_Date = Booking_Date.strftime('%d/%m/%Y')
            data = { "Booking_Date": Booking_Date,'Vehicle_Number':Vehicle_Number}
            generate_slip(Booking_Date,Vehicle_Number)
            p = open("output.html")
            components.html(p.read(),height=600)
            return True


def get_multi_report():

    with st.form("multi_slip_app_form",clear_on_submit=True):
        st.title('Multi Date Duty Slip Generation')
        ## Vehicle_Selection
        Vehicle_Number = st.selectbox(
            "Please Select The Vehicle",
            ("TS07GN5199", "TS07ES0693"),
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled)

        start_date = st.date_input("Start Date", value=pd.to_datetime("today", format="%Y-%m-%d"))
        end_date   = st.date_input("End Date", value=pd.to_datetime("today", format="%Y-%m-%d"))


        date_format = "%d/%m/%Y"

        # convert the dates to string
        start = start_date.strftime(date_format)
        end   = end_date.strftime(date_format)

        # Submit button.
        submitted = st.form_submit_button("SUBMIT")
        if submitted:
            data = { "start": start,"end":end,'Vehicle_Number':Vehicle_Number}
            generate_multi_slip(start,end,Vehicle_Number)
            try:
                p = open("output.html")
                components.html(p.read(),height=600)
                return True
            except FileNotFoundError:
                pass



def download_image():
    try:
        with open("output.html", "rb") as file:
            btn = st.download_button(label="Download image",data=file,file_name="dutyslip.html" )
    except:
        pass


def main_app():
    try:
        input_data = get_report()
        if input_data:
            b = download_image()
            return input_data
    except UnboundLocalError:
        pass

def multi_slip_app():
    try:
        input_data = get_multi_report()
        if input_data:
            b = download_image()
            return input_data
    except UnboundLocalError:
        pass



main_app()
multi_slip_app()








