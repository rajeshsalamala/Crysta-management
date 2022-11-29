import streamlit as st
from gauth import insert_expenses_data,get_expenses_data
import pandas as pd
from PIL import Image





# Store the initial value of widgets in session state
if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"
    st.session_state.disabled = False



def add_expenses_data():

    with st.form("Expenses Data Updation",clear_on_submit=True):
        st.title('Expenses Data Updation')
        ## Location_Selection

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
        ## product Selection
        product = st.selectbox( "Please Select The Expenditure Item",
                                        ("Savings", "Utility Bills", "Household Expenditure","Personal Expenditure"),
                                        label_visibility=st.session_state.visibility,
                                        disabled=st.session_state.disabled)

        ## all other entries
        date                 = st.date_input('Date')
        amount        = st.number_input("Amount",value=3000,step=500)
        Reference            = st.text_input("Reference",value="NA")

        # Submit button.
        submitted = st.form_submit_button("SUBMIT")
        if submitted:
            date = date.strftime('%d/%m/%Y')
            data = {"date":date,
                    "month":month,
                    "product":product,
                    "amount":amount,
                    "Reference":Reference,
                    "payment_method":payment_method }
            st.write("Expenditure Data Successfully Uploaded")
            return data


def main_app():
    input_data = add_expenses_data()
    try:
        data = list(input_data.values())
        insert_expenses_data(data)
    except:
        pass
main_app()



# #########
## Reports
# #########




df = pd.DataFrame(get_expenses_data())


def expense_report(month,product):
    res = df[(df['month']==month) & (df['product']==product)]
    return res


def get_expense_report():

    with st.form("Expenditure Data Reports",clear_on_submit=True):
        st.title('Expenditure Data Reports')
        ## month Selection
        month = st.selectbox(
            "Please Select The Month",
            ("January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November",  "December"),
            label_visibility=st.session_state.visibility,
            disabled=st.session_state.disabled)
        ## product Selection
        product = st.selectbox( "Please Select The Expenditure Item",
                                        ("Savings", "Utility Bills", "Household Expenditure","Personal Expenditure"),
                                        label_visibility=st.session_state.visibility,
                                        disabled=st.session_state.disabled)
        # Submit button.
        submitted = st.form_submit_button("SUBMIT")
        if submitted:
            print('*'*100)
            rep_data = expense_report(month,product)
            if not rep_data.empty:
                st.dataframe(data=rep_data)
            else:
                image = Image.open("not-found.jpg")
                st.image(image)


a = get_expense_report()






