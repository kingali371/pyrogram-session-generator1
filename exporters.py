# -*- coding: utf-8 -*-
"""
تصدير الجلسات بصيغ مختلفة (JSON, Python, Base64, Environmental Variables)
"""

import json
import base64
from typing import Dict, Optional

class مصدر_الجلسات:
    """تصدير الجلسات بصيغ متعددة"""
    
    @staticmethod
    def تصدير_JSON(الجلسة: Dict, المسار: str = None) -> str:
        """
        تصدير الجلسة بصيغة JSON
        
        Args:
            الجلسة: بيانات الجلسة
            المسار: مسار حفظ الملف (اختياري)
            
        Returns:
            نص JSON
        """
        بيانات_التصدير = {
            "اسم_الجلسة": الجلسة["الاسم"],
            "نص_الجلسة": الجلسة["نص_الجلسة"],
            "تاريخ_الانشاء": الجلسة["تاريخ_الانشاء"],
            "بيانات_اضافية": الجلسة.get("بيانات_اضافية", {})
        }
        
        نص_JSON = json.dumps(بيانات_التصدير, ensure_ascii=False, indent=2)
        
        if المسار:
            with open(المسار, 'w', encoding='utf-8') as ملف:
                ملف.write(نص_JSON)
        
        return نص_JSON
    
    @staticmethod
    def تصدير_Python(الجلسة: Dict, المسار: str = None) -> str:
        """
        تصدير الجلسة ككود Python جاهز للاستخدام
        
        Args:
            الجلسة: بيانات الجلسة
            المسار: مسار حفظ الملف (اختياري)
            
        Returns:
            كود Python
        """
        كود = f'''# -*- coding: utf-8 -*-
"""
جلسة Pyrogram للمستخدم: {الجلسة["الاسم"]}
تم الإنشاء: {الجلسة["تاريخ_الانشاء"]}
"""

from pyrogram import Client

# نص الجلسة
SESSION_STRING = "{الجلسة["نص_الجلسة"]}"

# مثال الاستخدام:
"""
app = Client(
    name="{الجلسة["الاسم"]}",
    session_string=SESSION_STRING,
    api_id=API_ID,  # ضع API ID الخاص بك
    api_hash=API_HASH  # ضع API HASH الخاص بك
)

@app.on_message()
async def hello(client, message):
    await message.reply("مرحباً! البوت يعمل")

app.run()
"""
'''
        
        if المسار:
            with open(المسار, 'w', encoding='utf-8') as ملف:
                ملف.write(كود)
        
        return كود
    
    @staticmethod
    def تصدير_Base64(الجلسة: Dict) -> str:
        """
        تصدير الجلسة كـ Base64 (مضغوط)
        
        Args:
            الجلسة: بيانات الجلسة
            
        Returns:
            نص Base64
        """
        بيانات = json.dumps({
            "session": الجلسة["نص_الجلسة"],
            "name": الجلسة["الاسم"]
        }).encode('utf-8')
        
        return base64.b64encode(بيانات).decode('utf-8')
    
    @staticmethod
    def تصدير_Env(الجلسة: Dict, المسار: str = None) -> str:
        """
        تصدير الجلسة كمتغيرات بيئية
        
        Args:
            الجلسة: بيانات الجلسة
            المسار: مسار حفظ الملف (اختياري)
            
        Returns:
            نص متغيرات البيئة
        """
        نص_env = f'''# ملف .env للجلسة: {الجلسة["الاسم"]}
SESSION_STRING="{الجلسة["نص_الجلسة"]}"
SESSION_NAME="{الجلسة["الاسم"]}"
SESSION_CREATED="{الجلسة["تاريخ_الانشاء"]}"
'''
        
        if المسار:
            with open(المسار, 'w', encoding='utf-8') as ملف:
                ملف.write(نص_env)
        
        return نص_env
    
    @staticmethod
    def تصدير_TXT(الجلسة: Dict, المسار: str = None) -> str:
        """
        تصدير الجلسة كنص عادي
        
        Args:
            الجلسة: بيانات الجلسة
            المسار: مسار حفظ الملف (اختياري)
            
        Returns:
            نص عادي
        """
        نص = f'''========================================
جلسة Pyrogram
========================================
الاسم: {الجلسة["الاسم"]}
تاريخ الإنشاء: {الجلسة["تاريخ_الانشاء"]}
عدد مرات الاستخدام: {الجلسة.get("مرات_الاستخدام", 0)}
========================================
نص الجلسة:
{الجلسة["نص_الجلسة"]}
========================================
'''
        
        if المسار:
            with open(المسار, 'w', encoding='utf-8') as ملف:
                ملف.write(نص)
        
        return نص
    
    @staticmethod
    def تصدير_HTML(الجلسة: Dict, المسار: str = None) -> str:
        """
        تصدير الجلسة كصفحة HTML
        
        Args:
            الجلسة: بيانات الجلسة
            المسار: مسار حفظ الملف (اختياري)
            
        Returns:
            كود HTML
        """
        html = f'''<!DOCTYPE html>
<html dir="rtl" lang="ar">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>جلسة {الجلسة["الاسم"]}</title>
    <style>
        body {{
            font-family: 'Tahoma', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            margin: 0;
            padding: 20px;
            direction: rtl;
        }}
        .container {{
            max-width: 800px;
            margin: auto;
            background: white;
            border-radius: 15px;
            padding: 30px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        }}
        h1 {{
            color: #667eea;
            text-align: center;
            border-bottom: 3px solid #667eea;
            padding-bottom: 10px;
        }}
        .info {{
            background: #f7f7f7;
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
        }}
        .session-string {{
            background: #2d3748;
            color: #68d391;
            padding: 20px;
            border-radius: 10px;
            font-family: monospace;
            word-break: break-all;
            direction: ltr;
            text-align: left;
        }}
        .warning {{
            background: #fed7d7;
            color: #c53030;
            padding: 15px;
            border-radius: 10px;
            border-right: 4px solid #c53030;
            margin-top: 20px;
        }}
        button {{
            background: #667eea;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
            margin: 5px;
        }}
        button:hover {{
            background: #5a67d8;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>🔐 جلسة Pyrogram</h1>
        
        <div class="info">
            <p><strong>📝 الاسم:</strong> {الجلسة["الاسم"]}</p>
            <p><strong>📅 تاريخ الإنشاء:</strong> {الجلسة["تاريخ_الانشاء"]}</p>
            <p><strong>🔄 عدد مرات الاستخدام:</strong> {الجلسة.get("مرات_الاستخدام", 0)}</p>
        </div>
        
        <h3>📋 نص الجلسة:</h3>
        <div class="session-string" id="sessionString">
            {الجلسة["نص_الجلسة"]}
        </div>
        
        <button onclick="copyToClipboard()">📋 نسخ النص</button>
        <button onclick="downloadSession()">💾 تحميل</button>
        
        <div class="warning">
            <strong>⚠️ تحذير أمني:</strong>
            <p>نص الجلسة يسمح بالوصول الكامل لحسابك. لا تشاركه مع أي شخص!</p>
        </div>
    </div>
    
    <script>
        function copyToClipboard() {{
            const text = document.getElementById('sessionString').innerText;
            navigator.clipboard.writeText(text);
            alert('✅ تم نسخ نص الجلسة!');
        }}
        
        function downloadSession() {{
            const text = document.getElementById('sessionString').innerText;
            const blob = new Blob([text], {{type: 'text/plain'}});
            const link = document.createElement('a');
            link.href = URL.createObjectURL(blob);
            link.download = 'session_{الجلسة["الاسم"]}.txt';
            link.click();
        }}
    </script>
</body>
</html>'''
        
        if المسار:
            with open(المسار, 'w', encoding='utf-8') as ملف:
                ملف.write(html)
        
        return html
