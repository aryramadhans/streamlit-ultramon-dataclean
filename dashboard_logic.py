import pandas as pd
import io
import streamlit as st

def ultramon(content):
    # Read DataFrame from the uploaded file
    df_ultramon = pd.read_csv(content, skiprows=lambda x: x not in range(9, 400))

    nodes = 'R1.BLN.PE-MOBILE.1'
    ports = '0/1/0/1'

    df_ultramon.insert(0, 'Node', nodes)
    df_ultramon.insert(1, 'Port', ports)

    return df_ultramon


def genie_clean(content):
    # Read DataFrame from uploaded content
    df_genie = pd.read_csv(content, skiprows=list(range(1, 4)))

    # Drop the unused column
    df_genie = df_genie.drop(df_genie.columns[2], axis=1)

    # Rename the first column
    df_genie = df_genie.rename(columns={df_genie.columns[0]: 'nearend', df_genie.columns[1]: 'farend'})

    # Sort the values by farend column
    df_genie = df_genie.sort_values(by='farend', ascending=False)

    # Exclude unused values from column farend
    filtered = [
        'IANA',
        'ERX',
        'T-D',
        'P-D',
        'LAB-D',
        'TELKOM',
        'RR-TSEL',
        'AON',
        'DNIC-NET-030',
        'CHINANET-HB'
    ]
    df_genie = df_genie[~df_genie['farend'].str.upper().str.contains('|'.join(filtered))]
    df_genie['farend'] = df_genie['farend'].str.upper()
    df_genie['nearend'] = df_genie['nearend'].str.upper()
    df_genie = df_genie.sort_values(by='farend', ascending=True)

    # Split the column name
    def rename_columns(col):
        if 'to' in col:
            return col.split(' to ')[0]
        return col

    # Get the list of current columns
    columns = df_genie.columns.tolist()

    # Rename columns starting from index 3
    new_columns = columns[:1] + [rename_columns(col) for col in columns[1:]]
    df_genie.columns = new_columns

    # Melt the DataFrame
    melted_genie = df_genie.melt(id_vars=['nearend', 'farend'], var_name='time', value_name='util')
    melted_genie = melted_genie.sort_values(by=['farend', 'time'], ascending=True)

    return melted_genie

def genie_p95(content):
    df_p95 = pd.read_csv(content)

    # Calculate P95 for each combination of nearend and farend
    p95_values = df_p95.groupby(['nearend', 'farend'])['max'].quantile(0.95).reset_index()
    p95_values.columns = ['nearend', 'farend', 'p95_max']

    # Create a sorted pair column to handle nearend-farend and farend-nearend as the same
    p95_values['pair'] = p95_values.apply(lambda row: tuple(sorted([row['nearend'], row['farend']])), axis=1)

    # Select the row with the highest p95_max value for each unique pair
    result = p95_values.loc[p95_values.groupby('pair')['p95_max'].idxmax()]

    # Drop the auxiliary 'pair' column
    result = result.drop(columns=['pair'])

    return result

def genie_ref_clean(content):
    df_ref = pd.read_csv(content)
    df_ref = df_ref.drop(df_ref.columns[2:], axis=1)

    cat_atom = 'PE-MOBILE(ATOM)'
    df_ref.insert(2, 'kategori', cat_atom)
    filtered = [
        'IANA',
        'ERX',
        'T-D',
        'P-D',
        'TELKOM',
        'RR-TSEL',
        'ASBR',
        'AON',
        'HSI',
        'TRANSIT',
        'CHINANET-HB'
    ]

    # df_ref = df_ref[df_ref['nearend'].str.upper() == nearend]
    df_ref = df_ref[~df_ref['farend'].str.upper().str.contains('|'.join(filtered))]
    df_ref['farend'] = df_ref['farend'].str.upper()
    df_ref['nearend'] = df_ref['nearend'].str.upper()
    df_ref = df_ref.sort_values(by='farend', ascending=True)

    # Reformating the ASBR(ATOM)
    dfasbr_ref = pd.read_csv(content)
    dfasbr_ref = dfasbr_ref.drop(dfasbr_ref.columns[2:], axis=1)

    cat_atom = 'ASBR(ATOM)'
    dfasbr_ref.insert(2, 'kategori', cat_atom)

    # dfasbr_ref = dfasbr_ref.rename(columns={dfasbr_ref.columns[0]: 'nearend', dfasbr_ref.columns[1]: 'farend'})
    dfasbr_ref['farend'] = dfasbr_ref['farend'].str.upper()
    dfasbr_ref['nearend'] = dfasbr_ref['nearend'].str.upper()
    dfasbr_ref = dfasbr_ref[dfasbr_ref['farend'].str.upper().str.contains('ASBR', na=False)]

    merged_ref = pd.concat([df_ref, dfasbr_ref],ignore_index=True)

    cleaned_ref = merged_ref.drop_duplicates(subset=['nearend', 'farend'])

    return cleaned_ref


def zabbix_clean(content):
    df_zabbix = pd.read_csv(content)
    
    df_zabbix = df_zabbix.drop(columns=['ip','device_type','region','max_of_max_bits','avg_of_max_bits','insert_time_clickhouse','_kafka_timestamp'])
    
    df_zabbix = df_zabbix.rename(columns={
        df_zabbix.columns[0]: 'date',
        df_zabbix.columns[1]: 'node',
        df_zabbix.columns[2]: 'port',
        df_zabbix.columns[3]: 'util_in',
        df_zabbix.columns[4]: 'util_out'})
    
    df_zabbix['date'] = pd.to_datetime(df_zabbix['date'], format='mixed').dt.strftime('%Y-%m-%d %H:%M:%S')
    
    flt_node = [
        'EBR.AHZ.1-RE0',
        'EBR.BRN.1-RE0',
        'EBR.BRN.2-RE0',
        'EBR.DGO.1-RE0',
        'EBR.DGO.2-RE0',
        'EBR.DLD.1-RE0',
        'EBR.DLD.2-RE0',
        'EBR.KNG.1-RE0',
        'EBR.KNG.2-RE0',
        'EBR.MPY.1-RE0',
        'EBR.MPY.2-RE0',
        'EBR.SOE.1-RE0',
        'EBR.SOE.2-RE0',
        'EBR.TBS.1-RE0',
        'EBR.TBS.2-RE0',
        'EBR-AMB.2',
        'ebr-bjb.1',
        'ebr-bjb.2',
        'EBR-GAYUNGAN.1',
        'EBR-GAYUNGAN.2',
        'EBR-HRM.1-NEW',
        'EBR-HRM.2-NEW',
        'EBR-PTK.1',
        'EBR-PTK.2',
        'EBR-SLO.1',
        'EBR-SLO.2',
        'EBR-SMR.1',
        'EBR-SMR.2',
        'EBR-SUD.1-NEW',
        'EBR-SUD.2-NEW',
        'EBR-UPD.1-NEW',
        'EBR-UPD.2-NEW',
    ]

    flt_port = [
        'ae0.823',
        'ae0.716',
        'ae0.3010',
        'ae0.824',
        'ae0.1442',
        'ae0.1492',
        'ae0.3311',
        'ae0.706',
        'ae0.708',
        'ae0.717',
        'ae0.718',
        'ae0.711',
        'ae0.713',
        'ae0.710',
        'ae12.1463',
        'ae12.703',
        'ae12.704',
        'ae10.701',
        'ae10.798',
        'ae10.799',
        'ae10.702',
        'ae0.719',
        'ae0.720',
        'ae0.714',
        'ae0.712',
        'ae0.811',
        'ae0.715',
        'ae2.3011',
        'ae0.1441',
        'ae0.360',
        'Bundle-Ether2.851',
        'Bundle-Ether1.733',
        'Bundle-Ether1.735',
        'Bundle-Ether2.734',
        'Bundle-Ether2.736',
        'Bundle-Ether3.3010',
        'Bundle-Ether1.1557',
        'Bundle-Ether3.3011',
        'Bundle-Ether1.825',
        'Bundle-Ether1.821',
        'Bundle-Ether1.1493',
        'Bundle-Ether1.725',
        'Bundle-Ether1.1593',
        'Bundle-Ether2.822',
        'Bundle-Ether2.726',
        'Bundle-Ether2.361',
        'Bundle-Ether2.1558',
        'Bundle-Ether2.1494',
        'Bundle-Ether2.826',
        'Bundle-Ether2.1594',
        'Bundle-Ether1.769',
        'Bundle-Ether1.727',
        'Bundle-Ether1.723',
        'Bundle-Ether2.724',
        'Bundle-Ether2.770',
        'Bundle-Ether2.728',
        'Bundle-Ether1.837',
        'Bundle-Ether2.838',
        'Bundle-Ether1.745',
        'Bundle-Ether2.828',
        'Bundle-Ether2.746',
        'Bundle-Ether1.827',
        'Bundle-Ether1.743',
        'Bundle-Ether2.744',
        'Bundle-Ether1.765',
        'Bundle-Ether1.1563',
        'Bundle-Ether1.753',
        'Bundle-Ether1.731',
        'Bundle-Ether1.871',
        'Bundle-Ether1.846',
        'Bundle-Ether1.889',
        'Bundle-Ether2.890',
        'Bundle-Ether2.754',
        'Bundle-Ether2.766',
        'Bundle-Ether2.1564',
        'Bundle-Ether2.847',
        'Bundle-Ether2.872',
        'Bundle-Ether2.732',
        'Bundle-Ether1.1499',
        'Bundle-Ether1.1497',
        'Bundle-Ether1.751',
        'Bundle-Ether1.887',
        'Bundle-Ether1.869',
        'Bundle-Ether1.1591',
        'Bundle-Ether1.830',
        'Bundle-Ether1.850',
        'Bundle-Ether1.763',
        'Bundle-Ether2.1498',
        'Bundle-Ether2.752',
        'Bundle-Ether2.831',
        'Bundle-Ether2.870',
        'Bundle-Ether2.1500',
        'Bundle-Ether2.888',
        'Bundle-Ether2.764',
        'Bundle-Ether2.1592'
    ]

    df_zabbix = df_zabbix[df_zabbix['node'].str.upper().str.contains('|'.join(flt_node)) & (df_zabbix['port'].str.contains('|'.join(flt_port)))]    

    return df_zabbix


def display_data_cleaning_page(cleaning_function):
    # File uploader
    uploaded_files = st.file_uploader("Choose CSV files to cleaning the data",type="csv", accept_multiple_files=True)

    # Display the total number of files submitted
    if uploaded_files:
        st.write(f"Total number of files submitted: {len(uploaded_files)}")

    # Initialize an empty DataFrame for merging
    merged_cleaned_data = pd.DataFrame()

    # Process each file
    if uploaded_files:
        for uploaded_file in uploaded_files:
            # st.subheader(f"File: {uploaded_file.name}")

            # Read file content
            content = io.BytesIO(uploaded_file.read())

            # Clean data using the imported logic
            cleaned_data = cleaning_function(content)

            # Append cleaned data to the merged DataFrame
            merged_cleaned_data = pd.concat([merged_cleaned_data, cleaned_data], ignore_index=True)

        # Display merged cleaned data
        st.write("Merged Cleaned Data:")
        st.dataframe(merged_cleaned_data)

        # Download button
        csv = merged_cleaned_data.to_csv(index=False).encode('utf-8')
        
        file_name = st.text_input("Enter file name")
        st.download_button(
            label = "Download Cleaned Data",
            data = csv,
            file_name = file_name if file_name.endswith(".csv") else file_name + ".csv",
            mime = "text/csv"
            )

        # # Create two columns for download buttons
        # col1, col2 = st.columns(2)

        # # CSV Download Button
        # with col1:
        #     csv = merged_cleaned_data.to_csv(index=False).encode('utf-8')
        #     st.download_button(
        #         label="Download as CSV",
        #         data=csv,
        #         file_name="cleaned_data.csv",
        #         mime="text/csv",
        #         help="Download the cleaned data in CSV format"
        #     )

        # with col2:
        #     excel_buffer = io.BytesIO()
        #     with pd.ExcelWriter(excel_buffer, engine='xlsxwriter') as writer:
        #         merged_cleaned_data.to_excel(writer, index=False, sheet_name='CleanedData')
        #     excel_buffer.seek(0)

        # st.download_button(
        #     label="Download as Excel",
        #     data=excel_buffer,
        #     file_name="cleaned_data.xlsx",
        #     mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        #     help="Download the cleaned data in Excel format"
        # )