import google.generativeai as genai

genai.configure(api_key="AIzaSyBFioTK7-BkdaXo8Fz4EOdRiBXTzobTJ-w")
model = genai.GenerativeModel('gemini-2.0-flash')

response = model.generate_content("Create a simple html css code template")
print(response.text)