from gauth import get_data,get_tenent_data


def calculate_totalhrs(start_time,end_time):
    round_ = lambda x: .25 * round(x/.25)    
    Start_Time = [int(x) for x in start_time.split(':')]
    End_Time   = [int(x) for x in end_time.split(':')]
    
    if End_Time[1]<Start_Time[1]:
        End_Time[1] = End_Time[1]+60
        End_Time[0] = End_Time[0]-1
        
    if End_Time[0]<Start_Time[0]:
        End_Time[0] = End_Time[0]+24
        
    time_diff = [y-x for x,y in zip(Start_Time,End_Time)]
    num_timediff = round_(round(time_diff[0]+time_diff[1]/60,2))
    actual_timediff = '.'.join([str(x) for x in time_diff]).split('.')
    actual_timediff = actual_timediff[0]+'hrs'+actual_timediff[1]+'mins'
    return [actual_timediff,num_timediff]


# gsheets_order = list(get_data[0].keys())
# print(gsheets_order)


gsheets_order =['Vehicle_Number', 'Booking_Date', 'No_of_Days', 'Driver_Name', 'Reference',
                 'Booking_Type', 'Local_base_price', 'Extra_hr_price', 'Km_price', 'Area_Reference',
                 'Start_Reading', 'End_Reading','Garage_Distance', 'Start_Time', 'End_Time', 'Total_Kms', 'Total_Time',
                 'Extra_KMS', 'Extra_time', 'Extra_km_amount', 'Extra_hr_amount', 'Tolls_Amount',
                 'Driver_Allowance', 'Mislinious_Amount', 'Mislinious_Reference', 'Total_BIll_Amount',
                 'Advance', 'Balance_Bill_Amount', 'Driver_Charges', 'Fuel_Charges', 'Total_Balance_Amount']


def bill_reckoning(data):
    data = data
    reordered_dict = {}
    try:
        totalkms = 0
        if data['End_Reading'] == data['Start_Reading']:
            totalkms = 0
        if data['End_Reading']>data['Start_Reading']:
            totalkms = data['End_Reading']-data['Start_Reading']
            totalkms = totalkms + data['Garage_Distance']

        # totalkms = data['End_Reading']-data['Start_Reading'] if data['End_Reading']>data['Start_Reading'] elif data['End_Reading'] == data['Start_Reading'] else 0
        if data['Booking_Type'] == 'local':
            totalhrs = calculate_totalhrs(data['Start_Time'],data['End_Time'])
            extrahrs = totalhrs[1]-8 if totalhrs[1] >8 else 0
            extrakms = totalkms-80 if totalkms >80 else 0
            extrahr_charges = extrahrs * data['Extra_hr_price']
            extrakm_charges = extrakms * data['Km_price']
            total_bill_amount = data['Local_base_price'] + extrahr_charges + extrakm_charges +data['Tolls_Amount']+ data['Mislinious_Amount']
            balance_bill_amount = total_bill_amount-data['Advance']
            fuel_charges = totalkms*10
            Total_Balance_Amount = total_bill_amount - data['Tolls_Amount'] -data['Mislinious_Amount'] - fuel_charges - data['Driver_Charges']- data['Driver_Allowance']
            data['Total_BIll_Amount']    = total_bill_amount
            data['Balance_Bill_Amount']  = balance_bill_amount
            data['Total_Time']           = totalhrs[0]
            data['Total_Kms']            = totalkms
            data['Extra_time']           = extrahrs
            data['Extra_KMS']            = extrakms
            data['Extra_hr_amount']      = extrahr_charges
            data['Extra_km_amount']      = extrakm_charges
            data['Fuel_Charges']         = fuel_charges
            data['Total_Balance_Amount'] = Total_Balance_Amount

        if data['Booking_Type'] == 'outstation':
            outstn_round             = lambda x,y: 300 if x*y<300 else 300*y
            totalkms                 = outstn_round(totalkms,data['No_of_Days'])
            totalkms                 = totalkms + data['Garage_Distance']
            km_charges               = totalkms * data['Km_price']
            allowance_charges        = data['Driver_Allowance'] * data['No_of_Days']                         
            total_bill_amount        = km_charges+ allowance_charges+data['Tolls_Amount']+data['Mislinious_Amount']
            balance_bill_amount        = total_bill_amount-data['Advance']
            fuel_charges = totalkms*10
            Total_Balance_Amount = total_bill_amount - data['Tolls_Amount'] -data['Mislinious_Amount'] - fuel_charges - data['Driver_Charges']- data['Driver_Allowance']
            data['Total_BIll_Amount'] = total_bill_amount
            data['Balance_Bill_Amount'] = balance_bill_amount
            data['Total_Time']        = totalhrs[0]
            data['Total_Kms']         = totalkms
            data['Extra_time']        = extrahrs
            data['Extra_KMS']         = extrakms
            data['Extra_hr_amount']   = extrahr_charges
            data['Extra_km_amount']   = extrakm_charges
            data['Fuel_Charges']         = fuel_charges
            data['Total_Balance_Amount'] = Total_Balance_Amount
    except Exception as e:
        pass
    try:
        reordered_dict = {k: data[k] for k in gsheets_order}
        # print(reordered_dict)
    except Exception as e:
        pass
    return reordered_dict

# def update_tenet_data()