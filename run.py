from timetable import app
import os  
port = int(os.environ.get('PORT', 33507)) 
app.run(host='0.0.0.0', port=port) #debug=True