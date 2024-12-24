import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from pypdf import PdfReader
import requests

# Function to download and read the PDF
def download_and_read_pdf(pdf_url):
    response = requests.get(pdf_url)
    if response.status_code == 200:
        with open("downloaded_file.pdf", "wb") as f:
            f.write(response.content)
        reader = PdfReader("downloaded_file.pdf")
        return reader
    else:
        st.error(f"Failed to download PDF. Status code: {response.status_code}")
        return None

# Function to process the PDF and extract data
def process_pdf(reader):
    papa = []
    for i in range(6, len(reader.pages)):
        pagee = reader.pages[i]
        textt = pagee.extract_text().split("\n")
        for line in textt:
            grades = []
            name = []
            parts = line.split(" ")
            if len(parts) < 3:
                continue
            grades.append(parts[1] + parts[2])
            for j in range(3, len(parts) - 3):
                if len(parts[j]) == 0:
                    grades.append(0)
                elif parts[j].isdigit():
                    grades.append(int(parts[j]))
                else:
                    name.append(parts[j])
            papa.append(name)
            papa.append(grades)
    return papa

# Function to plot grades
def plot_grades(arr):
    gra = ['AS', 'AA', 'AB', 'BB', 'BC', 'CC', 'CD', 'DD', 'FA', 'FD', 'FP', 'I', 'NP', 'PP']
    plt.bar(gra, arr, color='violet')
    plt.title('Grades')
    for index, value in enumerate(arr):
        plt.text(index, value, f"{value}", ha='center', va='bottom')
    plt.xlabel('Grade Awarded')
    plt.ylabel('Number of Students')
    st.pyplot(plt)

# Function to calculate average and median grade
def calculate_grades(arr):
    arr1 = []
    arr1.append(arr[0])
    for j in range(1, 14):
        arr1.append(arr1[j - 1] + arr[j])
    arr1.remove(arr1[0])  # Remove the first element as it is a cumulative sum

    sum1 = arr1[-1]
    aver = np.ceil(sum1 / 2)

    medd = 0
    gra = [10,9,7,6,5,4]
    for i in arr1:
        if i >= aver:
            medd = i
            break

    indi = arr1.index(medd)
    return gra[indi], sum1

# Main Streamlit app
st.title("Grade Analysis")

# PDF URL
pdf_url = "https://drive.google.com/uc?id=1uiPP4xEuTpyqPlKfgOZbhSk3DIbBRGLi&export=download"
reader = download_and_read_pdf(pdf_url)
if reader:
    papa = process_pdf(reader)
    hehe = st.text_input("Enter Course Code:")
    
    if hehe:
        arr = []
        stri = ""
        for i in range(1, len(papa)):
            if len(papa[i]) >= 1 and papa[i][0] == hehe:
                for num in range(1, 15):
                    arr.append(papa[i][num])
                for j in range(len(papa[i - 1])):
                    stri += papa[i - 1][j] + " "
        if arr:
            st.write(f"Grades for {stri.strip()}:")
            # st.write(arr)
            plot_grades(arr)
            
            # Calculate average and median grade
            avg_grade, total_students = calculate_grades(arr)
            st.write(f"Grade given to >=50% of the batch: {avg_grade}")
            st.write(f"Total number of students: {total_students}")
        else:
            st.error("Student not found.")
