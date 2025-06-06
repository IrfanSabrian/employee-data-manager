import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
from tabulate import tabulate

data = pd.read_excel('Employee Sample Data.xlsx')
data_list = data.to_dict('records')


def sublist_search(data_list, sublist, field):
    n = len(data_list)
    m = len(sublist)
    for i in range(n - m + 1):
        found = True
        for j in range(m):
            if str(data_list[i + j][field]).lower() != str(sublist[j]).lower():
                found = False
                break
        if found:
            return data_list[i:i + m]
    return []

def pencarian_karyawan():
    st.subheader("Pencarian Karyawan")

    menu = st.sidebar.radio('Menu:', ['Cari berdasarkan EEID', 'Cari berdasarkan Full Name'])
    search_key = st.text_input('Masukkan kata kunci pencarian:')
    results = []

    if menu == 'Cari berdasarkan EEID':
        data_list = data.to_dict('records')
        search_algorithm = 'Substring Search'
        if search_algorithm == 'Substring Search':
            results = sublist_search(data_list, [search_key], 'EEID')

    elif menu == 'Cari berdasarkan Full Name':
        data_list = data.to_dict('records')
        search_algorithm = 'Substring Search'
        if search_algorithm == 'Substring Search':
            search_words = search_key.lower().split()
            results = [record for record in data_list if all(word in record['Full Name'].lower().split() for word in search_words)]

    if st.button("Cari"):
        if len(results) > 0:
            st.subheader("Hasil Pencarian:")
            for result in results:
                col1, col2 = st.columns(2)

                with col1:
                    st.write(f"**EEID           :** {result['EEID']}")
                    st.write(f"**Full Name      :** {result['Full Name']}")
                    st.write(f"**Job Title      :** {result['Job Title']}")
                    st.write(f"**Department     :** {result['Department']}")
                    st.write(f"**Business Unit  :** {result['Business Unit']}")
                    st.write(f"**Gender         :** {result['Gender']}")

                with col2:
                    st.write(f"**Ethnicity      :** {result['Ethnicity']}")
                    st.write(f"**Age            :** {result['Age']}")
                    st.write(f"**Hire Date      :** {result['Hire Date'].strftime('%Y-%m-%d')}")
                    st.write(f"**Annual Salary $:** {result['Annual Salary']:.2f}")
                    st.write(f"**Bonus %        :** {result['Bonus %']:.2f}")
                    st.write(f"**Country        :** {result['Country']}")

        else:
            if search_key:
                st.write('Data yang Anda cari tidak ditemukan. Silakan ulangi pencarian.')


def analisis_demografi():
    st.subheader("Analisis Demografi")
    
    # Kolom yang ingin ditampilkan dalam grafik pie
    selected_column = st.sidebar.radio("Pilih Kolom Untuk Grafik Pie", ["Department", "Business Unit", "Gender", "Ethnicity", "Country"])
    
    st.write(f"Menampilkan grafik pie untuk kolom: {selected_column}")
    create_pie_plotly(data, selected_column)

def create_pie_plotly(data, column):
    fig = go.Figure(data=[go.Pie(labels=data[column].value_counts().index, values=data[column].value_counts().values)])
    st.plotly_chart(fig)

def analisis_gaji():
    st.subheader("Analisis Gaji Berdasarkan Department")

    # Daftar Departemen
    departments = ["Accounting", "Engineering", "Finance", "Human Resources", "IT", "Marketing", "Sales"]

    # Pilih grafik yang ingin ditampilkan
    selected_graph = st.sidebar.radio("Grafik Gaji Berdasarkan Department", departments)

    # Ambil data Departemen yang dipilih
    gaji_department = data[data["Department"] == selected_graph]
    gaji_department["Total Annual Salary"] = gaji_department["Annual Salary"] + (gaji_department["Annual Salary"] * gaji_department["Bonus %"] / 100)

    # Buat grafik batang dengan warna yang berbeda
    create_salary_plotly(gaji_department, selected_graph)

def create_salary_plotly(data, department):
    # Jumlahkan Total Annual Salary dengan sesama Department
    data_grouped = data.groupby("Business Unit")["Total Annual Salary"].sum().reset_index()

    # Definisikan list warna yang berbeda untuk setiap batang
    colors = ["blue", "green", "red", "orange", "purple", "pink", "brown"]

    fig = go.Figure()
    fig.add_trace(go.Bar(x=data_grouped["Business Unit"], y=data_grouped["Total Annual Salary"], name='Total Annual Salary', marker_color=colors))
    fig.update_layout(title=f"Grafik Total Annual Salary untuk Department {department}",
                      xaxis_title="Business Unit",
                      yaxis_title="Total Annual Salary")
    st.plotly_chart(fig)

def filter_karyawan():
    st.subheader("Filter Karyawan")
    pilihan = st.sidebar.radio("Filter Berdasarkan Kolom:", ["Job Title","Department", "Business Unit", "Ethnicity", "Country"])

    if pilihan == "Job Title":
        department_options = st.sidebar.selectbox("Pilih Job Title:", data["Job Title"].unique())
        filtered_data = data[data["Job Title"] == department_options]
    elif pilihan == "Department":
        department_options = st.sidebar.selectbox("Pilih Department:", data["Department"].unique())
        filtered_data = data[data["Department"] == department_options]
    elif pilihan == "Business Unit":
        business_options = st.sidebar.selectbox("Pilih Business Unit:", data["Business Unit"].unique())
        filtered_data = data[data["Business Unit"] == business_options]
    elif pilihan == "Ethnicity":
        ethnicity_options = st.sidebar.selectbox("Pilih Ethnicity:", data["Ethnicity"].unique())
        filtered_data = data[data["Ethnicity"] == ethnicity_options]
    elif pilihan == "Country":
        country_options = st.sidebar.selectbox("Pilih Country:", data["Country"].unique())
        filtered_data = data[data["Country"] == country_options]

    st.subheader("Data Karyawan yang Difilter")
    st.dataframe(filtered_data)

def tambah_karyawan():
    global data
    st.subheader("Tambah Karyawan Baru")

    # Inisialisasi kolom yang sesuai dengan kolom data Anda
    kolom = ['EEID', 'Full Name', 'Job Title', 'Department', 'Business Unit',
             'Gender', 'Ethnicity', 'Age', 'Hire Date', 'Annual Salary',
             'Bonus %', 'Country', 'City', 'Exit Date']

    data_baru = {}

    # Tampilkan 14 textbox atau selectbox untuk mengisi data
    for col in kolom:
        
        if col == 'Business Unit':
            # Menampilkan selectbox dengan pilihan Business Unit
            business_units = ["Speciality Products", "Corporate", "Manufacturing", "Research & Development"]
            data_baru[col] = st.selectbox(col, business_units)
        elif col == 'Gender':
            # Menampilkan selectbox dengan pilihan Gender
            genders = ["Male", "Female"]
            data_baru[col] = st.selectbox(col, genders)
        elif col == 'Job Title':
            # Menampilkan selectbox dengan pilihan Job Title
            title = ["Account Representative", "Analyst", "Analyst II", "Automation Engineer", 
                     "Business Partner", "Cloud Infrastructure Architect", "Computer Systems Manager", 
                     "Controls Engineer", "Development Engineer", "Director", "Engineering Manager", 
                     "Enterprise Architect", "Field Engineer", "HRIS Analyst", "IT Coordinator", 
                     "IT Systems Architect", "Manager", "Network Administrator", "Network Architect", 
                     "Network Engineer", "Operations Engineer", "Quality Engineer", "Solutions Architect", 
                     "Sr. Account Representative", "Sr. Analyst", "Sr. Business Partner", "Sr. Manager", 
                     "Systems Analyst", "System Administrator", "Service Desk Analyst", "Technical Architect", 
                     "Test Engineer", "Vice President"]
            data_baru[col] = st.selectbox(col, title)
        elif col == 'Department':
            # Menampilkan selectbox dengan pilihan Department
            department = ["Accounting",
                        "Engineering",
                        "Finance",
                        "Human Resources",
                        "IT",
                        "Marketing",
                        "Sales"]
            data_baru[col] = st.selectbox(col, department)
        elif col == 'Age':
            # Menampilkan input field untuk angka keuangan (Age)
            data_baru[col] = st.number_input(col,0)
        elif col == 'Hire Date':
            # Menggunakan pd.Timestamp.now() untuk mendapatkan tanggal dan waktu saat ini
            data_baru[col] = pd.Timestamp.now()
        elif col == 'Annual Salary':
            # Menampilkan input field untuk angka keuangan (Annual Salary)
            data_baru[col] = st.number_input(col)
        elif col == 'Bonus %':
            # Menampilkan input field untuk persentase bonus (Bonus %)
            data_baru[col] = st.number_input(col, step=0.01, format='%f')
        elif col == 'Exit Date':
            pass
        else:
            data_baru[col] = st.text_input(col)

    if st.button("Simpan Data"):
        # Tambahkan data baru ke DataFrame
        df_baru = pd.DataFrame([data_baru])
        data = pd.concat([data, df_baru], ignore_index=True)

        # Simpan DataFrame ke file Excel
        data.to_excel('Employee Sample Data.xlsx', index=False)

        st.success("Data berhasil disimpan.")

def edit_karyawan():
    global data

    st.subheader("Edit Karyawan")

    search_key = st.text_input('Masukkan EEID untuk mencari karyawan:')
    search_key = search_key.strip()

    if search_key:
        # Cari indeks baris berdasarkan EEID
        found_index = data[data['EEID'] == search_key].index
        if len(found_index) > 0:
            st.write("Data yang ditemukan:")
            st.write(data.loc[found_index])

            # Tampilkan input field untuk mengubah data karyawan
            data_baru = {}
            for col in data.columns:
                if col == 'Business Unit':
                    business_units = ["Speciality Products", "Corporate", "Manufacturing", "Research & Development"]
                    data_baru[col] = st.selectbox(col, business_units, index=business_units.index(data.loc[found_index[0], col]))
                elif col == 'Gender':
                    genders = ["Male", "Female"]
                    data_baru[col] = st.selectbox(col, genders, index=genders.index(data.loc[found_index[0], col]))
                elif col == 'Job Title':
                    # Menampilkan selectbox dengan pilihan Job Title
                    title = ["Account Representative", "Analyst", "Analyst II", "Automation Engineer", "Business Partner", 
                            "Cloud Infrastructure Architect", "Computer Systems Manager", "Controls Engineer", 
                            "Development Engineer", "Director", "Engineering Manager", "Enterprise Architect", 
                            "Field Engineer", "HRIS Analyst", "IT Coordinator", "IT Systems Architect", "Manager", 
                            "Network Administrator", "Network Architect", "Network Engineer", "Operations Engineer", 
                            "Quality Engineer", "Solutions Architect", "Sr. Account Representative", "Sr. Analyst", 
                            "Sr. Business Partner", "Sr. Manager", "Systems Analyst", "System Administrator", 
                            "Service Desk Analyst", "Technical Architect", "Test Engineer", "Vice President"]

                    data_baru[col] = st.selectbox(col, title, index=title.index(data.loc[found_index[0], col]))
                elif col == 'Department':
                    # Menampilkan selectbox dengan pilihan Department
                    department = ["Accounting", "Engineering", "Finance",
                                "Human Resources","IT","Marketing","Sales"]
                    data_baru[col] = st.selectbox(col, department, index=department.index(data.loc[found_index[0], col]))
                elif col == 'Age':
                    data_baru[col] = st.number_input(col, value=data.loc[found_index[0], col])
                elif col == 'Annual Salary':
                    data_baru[col] = st.number_input(col, value=data.loc[found_index[0], col])
                elif col == 'Bonus %':
                    data_baru[col] = st.number_input(col, step=0.01, format='%f', value=data.loc[found_index[0], col])
                elif col == 'Hire Date':
                    # Tampilkan Hire Date sebagai teks biasa (bukan input field) dan simpan nilai Hire Date saat menekan tombol "Simpan Perubahan"
                    st.write(data.loc[found_index, col].values[0])
                    data_baru[col] = data.loc[found_index[0], col]
                elif col == 'Exit Date':
                    exit_date = data.loc[found_index[0], col]
                    data_baru[col] = st.date_input(col, value=pd.Timestamp(exit_date)) if pd.notna(exit_date) else None
                elif col == 'Job Title':
                    job_titles = data["Job Title"].unique()
                    data_baru[col] = st.selectbox("Pilih Job Title:", job_titles, index=job_titles.tolist().index(data.loc[found_index[0], col]))
                else:
                    data_baru[col] = st.text_input(col, value=data.loc[found_index[0], col])

            # Tambahkan tombol "Simpan Perubahan"
            if st.button("Simpan Perubahan"):
                # Update data karyawan yang telah diubah
                data.loc[found_index[0]] = data_baru

                # Simpan DataFrame ke file Excel
                data.to_excel('Employee Sample Data.xlsx', index=False)

                st.success("Perubahan berhasil disimpan.")
        else:
            st.warning("Data tidak ditemukan. Silakan coba lagi.")
            
def resign_karyawan():
    global data

    st.subheader("Resign Karyawan")

    search_key = st.text_input('Masukkan EEID untuk mencari karyawan:')
    search_key = search_key.strip()

    if search_key:
        # Cari indeks baris berdasarkan EEID
        found_index = data[data['EEID'] == search_key].index
        if len(found_index) > 0:
            st.write("Data yang ditemukan:")
            st.write(data.loc[found_index])

            if st.button("Resign"):
                # Ambil tanggal saat ini
                today_date = datetime.today().strftime('%Y-%m-%d %H:%M:%S')

                # Update kolom Exit Date dengan tanggal saat ini
                data.at[found_index[0], 'Exit Date'] = today_date

                # Simpan DataFrame ke file Excel
                data.to_excel('Employee Sample Data.xlsx', index=False)

                st.success("Karyawan telah direseign dengan sukses. Exit Date telah diisi dengan tanggal saat ini.")
        else:
            st.warning("Data tidak ditemukan. Silakan coba lagi.")

def hapus_karyawan():
    global data

    st.subheader("Hapus Karyawan")

    search_key = st.text_input('Masukkan EEID untuk mencari karyawan:')
    search_key = search_key.strip()

    if search_key:
        # Cari indeks baris berdasarkan EEID
        found_index = data[data['EEID'] == search_key].index
        if len(found_index) > 0:
            st.write("Data yang ditemukan:")
            st.write(data.loc[found_index])

            if st.button("Hapus Data"):
                # Hapus baris berdasarkan indeks
                data = data.drop(found_index)

                # Simpan DataFrame ke file Excel tanpa baris yang dihapus
                data.to_excel('Employee Sample Data.xlsx', index=False)

                st.success("Data berhasil dihapus.")
        else:
            st.warning("Data tidak ditemukan. Silakan coba lagi.")
        