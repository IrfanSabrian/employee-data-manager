import streamlit as st
import pandas as pd
from modul import *

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "nickname" not in st.session_state:
    st.session_state.nickname = None

data = pd.read_excel('Employee Sample Data.xlsx')
data_list = data.to_dict('records')

def main():
    if not st.session_state.logged_in:
        st.title("Sistem Pengelola Data Karyawan")
        st.subheader("Silahkan Masuk")
        form = st.form(key='login-form')
        email = form.text_input("Email")
        password = form.text_input("Kata Sandi", type="password")

        login_button = form.form_submit_button("Masuk")

        if login_button:
            if check_login(email, password):
                st.session_state.logged_in = True
                st.experimental_rerun()
            else:
                st.error("Email atau kata sandi salah")
    else:
        menu()
        if st.session_state.logged_in:
            st.sidebar.success(f"Anda Masuk Sebagai: {st.session_state.nickname}")
            if st.sidebar.button("keluar"):
                st.sidebar.info("Anda Yakin Ingin Keluar?")
                st.session_state.logged_in = False
                st.session_state.nickname = None

def check_login(email, password):
    with open("admins.txt", "r") as file:
        lines = file.readlines()
        for line in lines:
            stored_email, stored_password, stored_nickname = line.strip().split(":")
            if email == stored_email and password == stored_password:
                st.session_state.nickname = stored_nickname
                return True
        return False

def menu():
    st.title("Sistem Pengelolaan Karyawan")
    option = st.sidebar.selectbox("Menu",
        ["Data Karyawan",
        "Laporan Analisis Karyawan",
        "Pengelolaan Karyawan"
    ])

    if option == "Data Karyawan":
        data_karyawan = st.sidebar.selectbox("Pilih Aksi", [
            "Filter Karyawan",
            "Pencarian Karyawan"
        ])

        if data_karyawan == "Filter Karyawan":
            filter_karyawan()
        elif data_karyawan == "Pencarian Karyawan":
            pencarian_karyawan()

    elif option == "Laporan Analisis Karyawan":
        laporan = st.sidebar.selectbox("Analisis", [
            "Analisis Demografi",
            "Analisis Gaji"
        ])

        if laporan == "Analisis Demografi":
            analisis_demografi()
        elif laporan == "Analisis Gaji":
            analisis_gaji()

    elif option == "Pengelolaan Karyawan":
        edit_option = st.sidebar.radio("Pilih Aksi", [
            "Tambah Karyawan",
            "Edit Data Karyawan",
            "Resign Karyawan",
            "Hapus Data Karyawan"
        ])

        if edit_option == "Tambah Karyawan":
            tambah_karyawan()
        elif edit_option == "Edit Data Karyawan":
            edit_karyawan()
        elif edit_option == "Resign Karyawan":
            resign_karyawan()
        elif edit_option == "Hapus Data Karyawan":
            hapus_karyawan()

if __name__ == '__main__':
    main()