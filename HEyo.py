import numpy as np

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
    gra = [10,9,8,7,6,5,4]
    for i in arr1:
        if i >= aver:
            medd = i
            break

    indi = arr1.index(medd)
    return gra[indi], sum1

# Main Streamlit app
st.title("Grade Analysis from PDF")

pdf_url = "https://drive.google.com/uc?id=1uiPP4xEuTpyqPlKfgOZbhSk3DIbBRGLi&export=download"
reader = download_and_read_pdf(pdf_url)
if reader:
    papa = process_pdf(reader)
    hehe = st.text_input("Enter student name:")
    
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
            st.write(arr)
            plot_grades(arr)
            
            # Calculate average and median grade
            avg_grade, total_students = calculate_grades(arr)
            st.write(f"Grade given to >=50% of the batch: {avg_grade}")
            st.write(f"Total number of students: {total_students}")
        else:
            st.error("Student not found.")
