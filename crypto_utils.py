# -*- coding: utf-8 -*-
"""
أدوات التشفير وفك التشفير للجلسات
"""

import os
import json
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

class مشفر_الجلسات:
    """فئة لتشفير وفك تشفير الجلسات باستخدام AES-256"""
    
    def __init__(self, كلمة_المرور: str):
        """
        تهيئة المشفر بكلمة مرور المستخدم
        
        Args:
            كلمة_المرور: كلمة المرور لتشفير الجلسات
        """
        self.كلمة_المرور = كلمة_المرور
        self.الملح = None
        self.مفتاح_التشفير = self._توليد_مفتاح()
    
    def _توليد_مفتاح(self):
        """توليد مفتاح تشفير من كلمة المرور"""
        # توليد ملح عشوائي إذا لم يكن موجوداً
        if not self.الملح:
            self.الملح = os.urandom(16)
        
        # استخدام PBKDF2 لتوليد مفتاح قوي
        kdf = PBKDF2(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.الملح,
            iterations=100000,
            backend=default_backend()
        )
        return kdf.derive(self.كلمة_المرور.encode())
    
    def تشفير(self, البيانات: str) -> str:
        """
        تشفير البيانات النصية
        
        Args:
            البيانات: النص المراد تشفيره
            
        Returns:
            النص المشفر بصيغة Base64
        """
        # توليد IV عشوائي
        iv = os.urandom(16)
        
        # إنشاء cipher
        cipher = Cipher(
            algorithms.AES(self.مفتاح_التشفير),
            modes.CFB(iv),
            backend=default_backend()
        )
        
        # تشفير البيانات
        encryptor = cipher.encryptor()
        بيانات_مشفرة = encryptor.update(البيانات.encode()) + encryptor.finalize()
        
        # دمج الملح و IV والبيانات المشفرة
        البيانات_الكاملة = self.الملح + iv + بيانات_مشفرة
        
        # تحويل إلى Base64
        return base64.b64encode(البيانات_الكاملة).decode('utf-8')
    
    def فك_تشفير(self, البيانات_المشفر: str) -> str:
        """
        فك تشفير البيانات المشفرة
        
        Args:
            البيانات_المشفر: النص المشفر بصيغة Base64
            
        Returns:
            النص الأصلي بعد فك التشفير
        """
        # فك Base64
        البيانات_الكاملة = base64.b64decode(البيانات_المشفر)
        
        # استخراج الملح (أول 16 بايت)
        self.الملح = البيانات_الكاملة[:16]
        
        # استخراج IV (16 بايت التالية)
        iv = البيانات_الكاملة[16:32]
        
        # استخراج البيانات المشفرة
        بيانات_مشفرة = البيانات_الكاملة[32:]
        
        # إعادة توليد المفتاح بالملح الجديد
        self.مفتاح_التشفير = self._توليد_مفتاح()
        
        # فك التشفير
        cipher = Cipher(
            algorithms.AES(self.مفتاح_التشفير),
            modes.CFB(iv),
            backend=default_backend()
        )
        
        decryptor = cipher.decryptor()
        البيانات_النصية = decryptor.update(بيانات_مشفرة) + decryptor.finalize()
        
        return البيانات_النصية.decode('utf-8')


class مدير_المفاتيح:
    """إدارة مفاتيح التشفير وتخزينها بشكل آمن"""
    
    @staticmethod
    def توليد_مفتاح_عشوائي(الطول: int = 32) -> str:
        """توليد مفتاح عشوائي قوي"""
        return base64.b64encode(os.urandom(الطول)).decode('utf-8')
    
    @staticmethod
    def حفظ_المفتاح(المفتاح: str, المسار: str):
        """حفظ المفتاح في ملف مع صلاحيات مقيدة"""
        with open(المسار, 'w') as ملف:
            ملف.write(المفتاح)
        # تقييد صلاحيات الملف (Unix only)
        os.chmod(المسار, 0o600)
    
    @staticmethod
    def تحميل_المفتاح(المسار: str) -> str:
        """تحميل المفتاح من الملف"""
        with open(المسار, 'r') as ملف:
            return ملف.read().strip()
