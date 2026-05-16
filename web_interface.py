# -*- coding: utf-8 -*-
"""
واجهة ويب بسيطة للجلسات (لرفع على Render)
"""

import os
from flask import Flask, render_template, request, jsonify, session
from session_manager import مدير_الجلسات
from exporters import مصدر_الجلسات

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', os.urandom(24))

# تهيئة مدير الجلسات
كلمة_المرور = os.environ.get('ENCRYPTION_KEY', 'default_key_change_me')
مدير = مدير_الجلسات(كلمة_المرور=كلمة_المرور)
مدير.تحميل_الجلسات()
مصدر = مصدر_الجلسات()

@app.route('/')
def الرئيسية():
    """الصفحة الرئيسية"""
    return render_template('index.html')

@app.route('/api/sessions', methods=['GET'])
def الحصول_على_الجلسات():
    """API: الحصول على قائمة الجلسات"""
    قائمة = مدير.قائمة_الجلسات()
    return jsonify(قائمة)

@app.route('/api/sessions/<name>', methods=['GET'])
def الحصول_على_جلسة(name):
    """API: الحصول على تفاصيل جلسة محددة"""
    جلسة = مدير.الحصول_على_جلسة(name)
    if جلسة:
        # لا نرسل نص الجلسة كاملاً للأمان
        return jsonify({
            "name": جلسة["الاسم"],
            "created": جلسة["تاريخ_الانشاء"],
            "last_used": جلسة.get("آخر_استخدام"),
            "usage_count": جلسة.get("مرات_الاستخدام", 0)
        })
    return jsonify({"error": "Session not found"}), 404

@app.route('/api/export/<name>/<format>', methods=['GET'])
def تصدير_جلسة(name, format):
    """API: تصدير جلسة بصيغة محددة"""
    جلسة = مدير.الحصول_على_جلسة(name)
    if not جلسة:
        return jsonify({"error": "Session not found"}), 404
    
    if format == 'json':
        return مصدر.تصدير_JSON(جلسة)
    elif format == 'python':
        return مصدر.تصدير_Python(جلسة)
    elif format == 'base64':
        return مصدر.تصدير_Base64(جلسة)
    elif format == 'env':
        return مصدر.تصدير_Env(جلسة)
    elif format == 'txt':
        return مصدر.تصدير_TXT(جلسة)
    elif format == 'html':
        return مصدر.تصدير_HTML(جلسة)
    else:
        return jsonify({"error": "Invalid format"}), 400

@app.route('/api/generate', methods=['POST'])
def توليد_جلسة():
    """API: توليد جلسة جديدة"""
    بيانات = request.json
    
    try:
        from pyrogram import Client
        
        with Client(
            name=بيانات.get('name', 'temp'),
            api_id=int(بيانات['api_id']),
            api_hash=بيانات['api_hash'],
            in_memory=True
        ) as العميل:
            نص_الجلسة = العميل.export_session_string()
            
            مدير.اضافة_جلسة(
                بيانات['name'],
                نص_الجلسة,
                {"api_id": بيانات['api_id'], "notes": بيانات.get('notes', '')}
            )
            
            return jsonify({
                "success": True,
                "session_string": نص_الجلسة,
                "message": "تم إنشاء الجلسة بنجاح"
            })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
