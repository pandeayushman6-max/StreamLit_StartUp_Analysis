import time

import streamlit as st
import pandas as pd
import json

st.title('Start Dashboard')
st.header('I am learning StreamLit')
st.subheader('Salan Khan!')
st.write('This is a normal text')
st.markdown("""
## My favourite movies ##
 - Race 3
 - Humshakals
 - Housefull
""")

st.code("""
    def foo(input):
        return input*2
""")

st.latex('x^2 + y^2 +2 =0')

#Display elements
df = pd.DataFrame({
    'name':['Nitish','Ayushman','Rohit'],
    'marks':[15,16,17],
    'package':[10,12,20]
})

st.dataframe(df)

st.metric('Revenue','Rs 3L','-3%')

st.json(json.dumps({
    'name':['Nitish','Ayushman','Rohit'],
    'marks':[15,16,17],
    'package':[10,12,20]
}))

#Diplaying Media

#st.image()
#st.video()
#st.audio()

#Sidebar
st.sidebar.title('Sidebar')

col1,col2=st.columns(2)

with col1:
    st.image('https://static.vecteezy.com/system/resources/thumbnails/083/933/835/small/beautiful-and-inspiring-picture-detailing-a-bright-hot-air-balloon-over-river-pure-cozy-perfect-for-creatives-moods-stock-image-free-photo.jpeg')

with col2:
    st.video('https://www.youtube.com/watch?v=6p_yaNFSYao')

#Progress Bar
st.error('This is an error message')
st.success('This is a success message')
st.info('This is an info message')
st.warning('This is a warning message')

bar = st.progress(0)
for i in range(0,100):
    time.sleep(0.01)
    bar.progress(i+1)


#Taking user input
email = st.text_input('Enter your email')
number = st.number_input('Enter a number')
date = st.date_input('Enter a date')

email =st.text_input('Enter your email',type='email',placeholder='example@gmail.com')
password = st.text_input('Enter your password',type='password')

gender = st.selectbox('Select your gender',['Male','Female','Other'])


btn = st.button('Submit')

if btn:
    if(email == 'pandeayushman6@gmail.com' and password == '1234'):
        st.success('Login Successful')
        st.write(gender)
        st.balloons()
    else:
        st.error('Login Failed')





