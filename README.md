# Cornell_Auto_Enrollment
Python Selenium script that adds courses from shopping cart

## How to Use
### 1. Install requirements
>pip install -r requirements.txt
### 2. Select which semester you will choose
<img width="616" alt="Screen Shot 2021-05-12 at 6 50 36 PM" src="https://user-images.githubusercontent.com/55479314/117955384-f3912d00-b352-11eb-908a-c537a850b8ee.png">     
If you want to choose the last column for example, you will put len(buttons) - 1 like below.    
If you want to choose 2021 Summer in the above picture, you will put len(buttons) - 2       
   
<img width="548" alt="Screen Shot 2021-05-12 at 6 51 35 PM" src="https://user-images.githubusercontent.com/55479314/117955511-14f21900-b353-11eb-8a9b-eb23cb9a7907.png">

### 3. run python file
>python enroll_while.py "netid" "password"   
>use **enroll_while.py** when you want to add courses that are currently closed   
>use **enroll_before.py** when you are waiting for your enrollment period. It checks whether it is a valid enrollment time or not.
