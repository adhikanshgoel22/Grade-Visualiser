import streamlit as st
import matplotlib.pyplot as plt
from pypdf import PdfReader
import requests

# Function to download and read PDF
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

# Function to process PDF and extract data
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
            grades.append(parts[1] + " " + parts[2])
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

# Function to plot data
def plot_grades(arr):
    gra = ['AS', 'AA', 'AB', 'BB', 'BC', 'CC', 'CD', 'DD', 'FA', 'FD', 'FP', 'I', 'NP', 'PP']
    plt.bar(gra, arr, color='violet')
    plt.title('Grades')
    for index, value in enumerate(arr):
        plt.text(index, value, f"{value}", ha='center', va='bottom')
    plt.xlabel('Grade Awarded')
    plt.ylabel('Number of Students')
    st.pyplot(plt)

# Main Streamlit app
st.title("Grade Analysis from PDF")

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
        else:
            st.error("Student not found.")
