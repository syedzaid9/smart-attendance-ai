import streamlit as st
from src.components.header import header_dashboard, header_home
from src.ui.base_layout import  style_background_dashboard , style_base_layout
from src.components.footer import footer_dashboard
from src.database.db import check_teacher_exists,create_teacher,teacher_login
from src.pipelines.face_pipeline import predict_attendance
import numpy as np

def teacher_screen():
    style_background_dashboard()
    style_base_layout()
    
    
    if "teacher_data" in st.session_state:
         teacher_dashboard()
    elif  'teacher_login_type' not in st.session_state or st.session_state.teacher_login_type=='login':
            teacher_screen_login()
    elif st.session_state.teacher_login_type=='Rigster':
            teacher_screen_register()

def teacher_dashboard():
     teacher_data = st.session_state.teacher_data
     c1,c2 = st.columns(2,vertical_alignment="center",gap="large")
     with c1:
             header_dashboard()
     with c2:
             st.subheader(f""""Well come,{teacher_data['name']}""")
             if st.button("Logout",type='secondary',key='teacher_logout_btn',shortcut="control+backspace"):
                 st.session_state['login_type']=None
                 del st.session_state.teacher_data  
                 st.rerun()
     st.space()


     if "current_teacher_tab" not in st.session_state:
          st.session_state.current_teacher_tab = 'take_attendance'
     tab1,tab2,tab3 = st.columns(3)

     with tab1:
          type1 = 'primary' if st.session_state.current_teacher_tab == 'take_attendance' else 'tertiary'
          if st.button("Take Attendance",width='stretch',type=type1,icon=':material/ar_on_you:'):
               st.session_state.current_teacher_tab = 'take_attendance'
               st.rerun()

     with tab2:
               type2 = 'primary' if st.session_state.current_teacher_tab == 'manage_subject' else 'tertiary'
               if st.button("Manage Subject",width='stretch',type=type2,icon=':material/book_ribbon:'):
                    st.session_state.current_teacher_tab = 'manage_subject'
                    st.rerun()

     with tab3:
               type3 = 'primary' if st.session_state.current_teacher_tab == 'attendance_records' else 'tertiary'
               if st.button("Attendance records",width='stretch',type=type3,icon=':material/cards_stack:'):
                    st.session_state.current_teacher_tab = 'attendance_records'
                    st.rerun()

     st.divider()
     if st.session_state.current_teacher_tab =='take_attendance':
          teacher_tab_take_attendance()
     if st.session_state.current_teacher_tab =='manage_subject':
          teacher_tab_take_manage_subject()
     if st.session_state.current_teacher_tab =='attendance_records':
          teacher_tab_take_attendance_records()

     

     footer_dashboard()
def login_teacher(teacher_username,teacher_password):
     if not teacher_username or not teacher_password:
          return False,"Please fill all the fields"
     teacher = teacher_login(teacher_username,teacher_password)

     if teacher:
          st.session_state.user_role='teacher'
          st.session_state.teacher_data = teacher
          st.session_state.is_logged_in = True
          return True
     return False

       


def teacher_screen_login():
    c1,c2 = st.columns(2,vertical_alignment="center",gap="large")
    with c1:
        header_dashboard()
    with c2:
        if st.button("Go back to home",type='secondary',key='teacher_login_back_btn',shortcut="control+backspace"):
            st.session_state['login_type']=None
            st.rerun()
    
    st.header("Login using password",text_alignment='center')
    st.space()
    st.space()
    teacher_username = st.text_input("Enter username",placeholder="name")
    teacher_password =st.text_input("Enter password",placeholder="password",type='password')
    st.divider()

    btn1,btn2 = st.columns(2)

    with btn1:
        if st.button("Login",icon=':material/passkey:',shortcut="control+enter",width='stretch'):
            if login_teacher(teacher_username,teacher_password):
                st.toast("welcome back!",icon="👋")
                st.rerun()
            else:
                st.error("Incorrect username or password")

    with btn2:
        if st.button("Rigster",type='primary',icon=':material/passkey:',width='stretch'):
             st.session_state.teacher_login_type='Rigster'
    footer_dashboard()

def register_teacher(teacher_username,teacher_name,teacher_pass,teacher_pass_confirm):
     if not teacher_username or not teacher_name or not teacher_pass or not teacher_pass_confirm:
          return False,"Please fill all the fields"
     if check_teacher_exists(teacher_username):
            return False,"Username already exists"
     if teacher_pass != teacher_pass_confirm:
            return False,"Passwords do not match"
     try:
          create_teacher(teacher_username,teacher_pass,teacher_name)
          return True,"Teacher registered successfully"
     except Exception as e:
          return False,print(e)
          
def teacher_screen_register():
      
      c1,c2 = st.columns(2,vertical_alignment="center",gap="xxlarge")
      with c1:
           header_dashboard() 
      with c2:
        if st.button("Go back to home",type='secondary',key='teacher_register_back_btn',shortcut="control+backspace"):
             st.session_state['login_type']=None
             st.rerun()
    
      st.header("Register your teacher profile")

      st.space()
      st.space()
      teacher_username = st.text_input("Enter username",placeholder="name")
      teacher_name = st.text_input("Enter name",placeholder="zaid")
      teacher_password =st.text_input("Enter password",placeholder="password",type='password')
      conforn_password =st.text_input("Enter password",placeholder="conform it",type='password')
      st.divider()

      btn1,btn2 = st.columns(2)
      
      with btn2:
            if st.button("Login",icon=':material/passkey:',shortcut="control+enter",width='stretch'):
                 st.session_state.teacher_login_type='login'

      with btn1:
            if st.button("Rigster",type='primary',icon=':material/passkey:',width='stretch'):
                 success,message = register_teacher(teacher_username,teacher_name,teacher_password,conforn_password)
                 if success:
                      st.success(message)
                      import time
                      time.sleep(2)
                      st.session_state.teacher_login_type='login'
                      st.rerun()
                 else:
                      st.error(message)
    
    
   
                
      footer_dashboard()

def teacher_tab_take_attendance():
     st.header("Take AI Attendence")

def teacher_tab_take_manage_subject():
     st.header("Manage subject")
def teacher_tab_take_attendance_records():
     st.header("Records")