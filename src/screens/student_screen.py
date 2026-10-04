import numpy as np
from  PIL import Image
import streamlit as st
from src.components.header import header_dashboard, header_home
from src.ui.base_layout import  style_background_dashboard , style_base_layout
from src.components.footer import footer_dashboard
from src.pipelines.face_pipeline import predict_attendance , get_face_embeddings,train_classifier
from src.pipelines.voice_pipeline import get_voice_embedding 
from src.database.db import get_all_students,create_students
import time
    
def student_dashboard():
    st.header("Dashboard")


def student_screen():

    style_background_dashboard()
    style_base_layout()

    if 'student_data' in st.session_state:
        student_dashboard()
        return


    c1,c2 = st.columns(2,vertical_alignment="center",gap="large")
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to home",type='secondary',key='loginbackbtn',shortcut="control+backspace"):
            st.session_state['login_type']=None
            st.rerun()
    st.space()
    st.space()

    st.header("Login With FaceID",text_alignment='center')

    if "show_registration" not in st.session_state:
        st.session_state.show_registration = False

    photo_shoot =st.camera_input("position your face in the centre")
    if photo_shoot:
       img = np.array(Image.open(photo_shoot))

       with st.spinner("AI is scanning..."):
           detected,all_ids,num_faces = predict_attendance(img)

           if num_faces ==0:
               st.warning("Face Not found!")

           elif num_faces >1:
               st.warning("Mulitple face found")
           else:
               if detected:
                   student_id = list(detected.keys())[0]
                   all_students = get_all_students()
                   student = next((s for s in all_students if  s['student_id']==student_id),None)

                   if student:
                       st.session_state.is_logged_in = True
                       st.session_state.user_role = 'student'
                       st.session_state.student_data = student
                       st.toast(f"welcome back {student['name']}")
                       time.sleep(1)
                       st.rerun()
               else:
                       st.info("face not recognized: you might be new student")
                       st.session_state.show_registration = True
    if st.session_state.show_registration:
        with st.container(border=True):
            st.header("Register new Profile")
            new_name = st.text_input("Enter your name",placeholder="Name")

            st.subheader("optional : voice Enrollment")
            st.info("Enroll you for voice only attendance")


            audio_data = None

            try:
                audio_data = st.audio_input("Record a short pharse like  i am Name, name is:")
            except Exception:
                st.error("Audio data failed:")

            if st.button("Create Account",type='primary'):
                if new_name:
                    with st.spinner("creating profile .."):
                        encodings = get_face_embeddings(img)
                        if len(encodings)>0:
                            face_emb = encodings[0].tolist()

                            voice_emb = None
                            if audio_data:
                                voice_emb = get_voice_embedding(audio_data.read())

                            response_data = create_students(new_name,face_embedding = face_emb,voice_embedding = voice_emb)

                            if response_data:
                                train_classifier()
                                st.session_state.is_logged_in = True
                                st.session_state.user_role = 'student'
                                st.session_state.student_data = response_data[0]
                                st.toast(f"Profile  Created! Hi {new_name}")
                                time.sleep(1)
                                st.rerun()
                            else:
                                st.error("couldnt capture your facial features for registrations")
                else:
                    st.warning("please enter your name!")           

                 


           


    footer_dashboard()
    


