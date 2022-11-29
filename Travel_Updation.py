# Contents of ~/my_app/main_page.py

import streamlit as st
from gauth import insert_data
import re
from json import dumps
from datetime import date, datetime,time
from functions import bill_reckoning
import datetime as dt


# https://levelup.gitconnected.com/how-to-add-a-background-image-to-your-streamlit-app-96001e0377b2#:~:text=To%20add%20a%20background%20image%20to%20your%20Streamlit%20app%2C%20you,to%20get%20the%20work%20done.
# def add_bg_from_url():
#     st.markdown(
#          f"""
#          <style>
#          .stApp {{
#              background-image: url("https://images.pexels.com/photos/531880/pexels-photo-531880.jpeg?cs=srgb&dl=pexels-pixabay-531880.jpg&fm=jpg");
#              background-attachment: fixed;
#              background-size: cover
#          }}
#          </style>
#          """,
#          unsafe_allow_html=True
#      )

# add_bg_from_url() 





def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""

    if isinstance(obj, (datetime, date,time)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))



st.sidebar.markdown("# Update Details in DataBase 🎈")


# Store the initial value of widgets in session state
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False



if 'End_Time' not in st.session_state:
    st.session_state['End_Time'] = dt.datetime.now().time()

if 'Start_Time' not in st.session_state:
    st.session_state['Start_Time'] = dt.datetime.now().time()

def add_data():

    date_pattern = r'(\d{4}\W\d{2}\W\d{2}).'
    time_pattern = r'.(\d{2}:\d{2}):'

    with st.form("my_form",clear_on_submit=True):

        ## Vehicle_Selection
        Vehicle_Number = st.selectbox(
            "Please Select The Vehicle",
            ("TS07GN5199", "TS07ES0693"),
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled)

        ## Booking_Type
        Buking_Type = st.radio(
            "Booking Type",
            ('local', 'outstation'))

        if Buking_Type == 'local':
            Booking_Type = 'local'
        else:
            Booking_Type = 'outstation'

        ## all other entries
        local_base_price     = st.number_input("local 8:80 price", value=2800,step=100)

        Booking_Date         = st.date_input('Booking Date')
        No_of_Days           = st.number_input("No Of Days", min_value=1)
        Start_Time           = st.time_input('Start Time', value=st.session_state['Start_Time'], key='Start_Time')
        End_Time             = st.time_input('End Time', value=st.session_state['End_Time'], key='End_Time')
        Start_Reading        = st.number_input("Start Reading",min_value=0)
        End_Reading_         = st.number_input("End Reading",min_value=0)
        garage_distance      = st.number_input("Garage Distance",min_value=0)
        Tolls_Amount         = st.number_input("Tolls Amount",value=0,step=10)
        Advance              = st.number_input("Advance",value=0,step=500)
        Driver_Allowance     = st.number_input("Driver_Allowance", min_value=0,step=100)
        Driver_Name          = st.text_input("Driver Name",value="Kondal")
        Reference            = st.text_input("Booking Reference",value="Local")
        Area_Reference       = st.text_input("Area Reference",value="HYD")
        driver_charges       = st.number_input("Mislinious Driver charges",value=0,step=100)
        Mislinious_Amount    = st.number_input("Mislinious Amount",value=0,step=100)
        Mislinious_Reference = st.text_input("Mislinious Reference",value="None")
        # Booking_Date         = re.findall(date_pattern,dumps(Booking_Date, default=json_serial))[0]
        Start_Time           = re.findall(time_pattern,dumps(Start_Time, default=json_serial))[0]
        End_Time             = re.findall(time_pattern,dumps(End_Time, default=json_serial))[0]
        hr_price             = st.number_input("Extra hr", min_value=150,step=10)
        km_price             = st.number_input("Extra km", min_value=18)
        # Submit button.
        submitted = st.form_submit_button("SUBMIT")
        if submitted:
            Booking_Date = Booking_Date.strftime('%d/%m/%Y')
            data = {"Vehicle_Number": Vehicle_Number,
                    "Booking_Date": Booking_Date,
                    "No_of_Days": No_of_Days,
                    "Driver_Name": Driver_Name,
                    "Reference": Reference,
                    "Booking_Type": Booking_Type,
                    "Area_Reference": Area_Reference,
                    "Start_Reading": Start_Reading,
                    "End_Reading": End_Reading_,
                    "Garage_Distance":garage_distance,
                    "Start_Time": Start_Time,
                    "End_Time": End_Time,
                    "Tolls_Amount": Tolls_Amount,
                    "Driver_Allowance": Driver_Allowance,
                    "Mislinious_Amount": Mislinious_Amount,
                    "Mislinious_Reference": Mislinious_Reference,
                    "Advance": Advance,
                    "Driver_Charges": driver_charges,
                    "Local_base_price":local_base_price,
                    "Extra_hr_price": hr_price,
                    "Km_price": km_price,

                    }
            st.write("Data Successfully Uploaded",data)
            return data


def main_app():
    input_data = add_data()
    final = bill_reckoning(input_data)
    new_data = list(final.values())
    a = insert_data(new_data)
    return new_data

fi =  main_app()


