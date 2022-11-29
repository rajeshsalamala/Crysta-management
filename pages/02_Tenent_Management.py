import streamlit as st
import pandas as pd
from gauth import insert_tenent_data,get_tenent_data


df = pd.DataFrame(get_tenent_data())



# Store the initial value of widgets in session state
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False



def add_data():

    with st.form("Tenent Data Updation",clear_on_submit=True):
        st.title('Tenent Data Updation')
        ## Location_Selection
        location = st.selectbox(
            "Please Select The Location",
            ("Hyderabad", "Jadcherla"),
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled)
        ## month Selection
        month = st.selectbox(
            "Please Select The Month",
            ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",  "December"),
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled)
        ## payment method Selection
        payment_method = st.selectbox( "Please Select The Payment Method",
                                        ("Cash", "Gpay", "Phonepay", "Account Transfer"),
                                        label_visibility=st.session_state.visibility,
                                        disabled=st.session_state.disabled)
        ## flat Selection
        flat = st.selectbox( "Please Select The Flat Number",
                                        ("HYD_G_1Bed", "HYD_G_1Rm", "HYD_1_1Bed", "HYD_1_2Bed",
                                         "HYD_2_1Bed", "HYD_2_2Bed", "HYD_3_1Bed", "HYD_3_1Rm",
                                         "JCL_Front", "JCL_Middle", "JCL_Last"),
                                        label_visibility=st.session_state.visibility,
                                        disabled=st.session_state.disabled)

        ## all other entries
        date                 = st.date_input('Date')
        rental_amount        = st.number_input("Rental Amount",value=3000,step=500)
        previous_balance     = st.number_input("Previous Balance",value=0,step=100)
        total_balance        = st.number_input("Total Balance",value=0,step=1000)
        tenent_name          = st.text_input("Tenent Name",value="NA")
        Reference            = st.text_input("Reference",value="NA")
        # Submit button.
        submitted = st.form_submit_button("SUBMIT")
        if submitted:
            date = date.strftime('%d/%m/%Y')
            data = {"date":date,
                    "location":location,
                    "flat":flat,
                    "tenent_name":tenent_name,
                    "month":month,
                    "rental_amount":rental_amount,
                    "previous_balance":previous_balance,
                    "total_balance":total_balance,
                    "Reference":Reference,
                    "payment_method":payment_method }
            st.write("Tenent Data Successfully Uploaded")
            return data
def main_app():
    input_data = add_data()
    try:
        data = list(input_data.values())
        insert_tenent_data(data)
    except:
        pass


def tenent_report(month,location):
    res = df[(df['month']==month) & (df['location']==location)]
    return res

def get_report():

    with st.form("my_form",clear_on_submit=True):
        st.title('Tenent Data Reports')
        ## Location_Selection
        location = st.selectbox(
            "Please Select The Location",
            ("Hyderabad", "Jadcherla"),
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled)
        ## month Selection
        month = st.selectbox(
            "Please Select The Month",
            ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",  "December"),
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled)
        # Submit button.
        submitted = st.form_submit_button("SUBMIT")
        if submitted:
            print('*'*100)
            rep_data = tenent_report(month,location)
            print(rep_data)
            st.dataframe(data=rep_data)



main_app()
get_report()






