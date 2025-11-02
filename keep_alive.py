from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    # שים לב, שיניתי את ההודעה חזרה למה שהיה לך
    # כדי שהכרון-ג'וב שלך ימשיך לראות את התגובה שהוא מצפה לה
    return "I'm alive!" 

# 🔽 --- הוסף את הקטע הבא --- 🔽
@app.route('/wakeup')
def wakeup_from_yemot():
    """
    נתיב זה מיועד לקריאה ממערכת ימות המשיח.
    הוא מחזיר פקודת טקסט פשוטה שימות המשיח מבין.
    """
    # פקודה זו גורמת לימות להשמיע "השרת התעורר בהצלחה"
    # (או להשמיע "שגיאה" אם הקידוד לא תואם, כפי שדיברנו)
    response_text = "id_list_message=t-השרת התעורר בהצלחה"
    
    # מחזירים את הטקסט הפשוט, שימות המשיח יקרא
    return response_text
# 🔼 --- סוף הקטע להוספה --- 🔼

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
