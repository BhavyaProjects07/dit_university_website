import google.generativeai as genai

genai.configure(api_key="AIzaSyBFioTK7-BkdaXo8Fz4EOdRiBXTzobTJ-w")
model = genai.GenerativeModel('gemini-2.0-flash')

response = model.generate_content("Create a simple html css code template")
print(response.text)


# git command to push every change 

#  --->   git add . ; git commit -m "Databse change" ; git push origin main