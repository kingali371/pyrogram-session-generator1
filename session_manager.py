# -*- coding: utf-8 -*-
"""
إدارة الجلسات المتعددة مع التشفير
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List, Optional
from pyrogram import Client
from crypto_utils import مشفر_الجلسات

class مدير_الجلسات:
    """إدارة متعددة للجلسات مع حفظ مشفر"""
    
    def __init__(self, مجلد_الحفظ: str = "sessions", كلمة_المرور: str = None):
        """
        تهيئة مدير الجلسات
        
        Args:
            مجلد_الحفظ: المجلد لحفظ ملفات الجلسات
            كلمة_المرور: كلمة المرور للتشفير (اختياري)
        """
        self.مجلد_الحفظ = مجلد_الحفظ
        self.كلمة_المرور = كلمة_المرور
        self.الجلسات = {}
        self.المشفر = مشفر_الجلسات(كلمة_المرور) if كلمة_المرور else None
        
        # إنشاء المجلد إذا لم يكن موجوداً
        if not os.path.exists(مجلد_الحفظ):
            os.makedirs(مجلد_الحفظ)
    
    def اضافة_جلسة(self, الاسم: str, نص_الجلسة: str, بيانات_اضافية: Dict = None):
        """
        إضافة جلسة جديدة
        
        Args:
            الاسم: اسم الجلسة (للتعريف)
            نص_الجلسة: نص الجلسة من Pyrogram
            بيانات_اضافية: بيانات إضافية مثل التاريخ والوصف
        """
        بيانات_الجلسة = {
            "الاسم": الاسم,
            "نص_الجلسة": نص_الجلسة,
            "تاريخ_الانشاء": datetime.now().isoformat(),
            "آخر_استخدام": None,
            "مرات_الاستخدام": 0,
            "بيانات_اضافية": بيانات_اضافية or {}
        }
        
        # حفظ الجلسة
        if self.المشفر:
            # حفظ مشفر
            مسار_الملف = os.path.join(self.مجلد_الحفظ, f"{الاسم}.enc")
            بيانات_مشفر = self.المشفر.تشفير(json.dumps(بيانات_الجلسة, ensure_ascii=False))
            with open(مسار_الملف, 'w', encoding='utf-8') as ملف:
                ملف.write(بيانات_مشفر)
        else:
            # حفظ عادي
            مسار_الملف = os.path.join(self.مجلد_الحفظ, f"{الاسم}.json")
            with open(مسار_الملف, 'w', encoding='utf-8') as ملف:
                json.dump(بيانات_الجلسة, ملف, ensure_ascii=False, indent=2)
        
        self.الجلسات[الاسم] = بيانات_الجلسة
        return True
    
    def تحميل_الجلسات(self):
        """تحميل جميع الجلسات المحفوظة"""
        self.الجلسات = {}
        
        for اسم_ملف in os.listdir(self.مجلد_الحفظ):
            if اسم_ملف.endswith('.enc') and self.المشفر:
                # فك تشفير
                مسار_الملف = os.path.join(self.مجلد_الحفظ, اسم_ملف)
                with open(مسار_الملف, 'r', encoding='utf-8') as ملف:
                    بيانات_مشفر = ملف.read()
                    بيانات_جيسون = self.المشفر.فك_تشفير(بيانات_مشفر)
                    الجلسة = json.loads(بيانات_جيسون)
                    self.الجلسات[الجلسة["الاسم"]] = الجلسة
                    
            elif اسم_ملف.endswith('.json'):
                # قراءة عادية
                مسار_الملف = os.path.join(self.مجلد_الحفظ, اسم_ملف)
                with open(مسار_الملف, 'r', encoding='utf-8') as ملف:
                    الجلسة = json.load(ملف)
                    self.الجلسات[الجلسة["الاسم"]] = الجلسة
        
        return self.الجلسات
    
    def الحصول_على_جلسة(self, الاسم: str) -> Optional[Dict]:
        """الحصول على جلسة محددة"""
        return self.الجلسات.get(الاسم)
    
    def تحديث_آخر_استخدام(self, الاسم: str):
        """تحديث تاريخ آخر استخدام للجلسة"""
        if الاسم in self.الجلسات:
            self.الجلسات[الاسم]["آخر_استخدام"] = datetime.now().isoformat()
            self.الجلسات[الاسم]["مرات_الاستخدام"] += 1
            self.حفظ_جلسة_محددة(الاسم)
    
    def حفظ_جلسة_محددة(self, الاسم: str):
        """حفظ جلسة محدثة"""
        if الاسم not in self.الجلسات:
            return False
        
        بيانات_الجلسة = self.الجلسات[الاسم]
        
        if self.المشفر:
            مسار_الملف = os.path.join(self.مجلد_الحفظ, f"{الاسم}.enc")
            بيانات_مشفر = self.المشفر.تشفير(json.dumps(بيانات_الجلسة, ensure_ascii=False))
            with open(مسار_الملف, 'w', encoding='utf-8') as ملف:
                ملف.write(بيانات_مشفر)
        else:
            مسار_الملف = os.path.join(self.مجلد_الحفظ, f"{الاسم}.json")
            with open(مسار_الملف, 'w', encoding='utf-8') as ملف:
                json.dump(بيانات_الجلسة, ملف, ensure_ascii=False, indent=2)
        
        return True
    
    def حذف_جلسة(self, الاسم: str) -> bool:
        """حذف جلسة"""
        if الاسم in self.الجلسات:
            # حذف الملف
            for صيغة in ['.enc', '.json']:
                مسار_الملف = os.path.join(self.مجلد_الحفظ, f"{الاسم}{صيغة}")
                if os.path.exists(مسار_الملف):
                    os.remove(مسار_الملف)
            
            # حذف من الذاكرة
            del self.الجلسات[الاسم]
            return True
        return False
    
    def قائمة_الجلسات(self) -> List[Dict]:
        """الحصول على قائمة الجلسات للمعاينة"""
        قائمة = []
        for اسم, بيانات in self.الجلسات.items():
            قائمة.append({
                "الاسم": اسم,
                "تاريخ_الانشاء": بيانات["تاريخ_الانشاء"],
                "آخر_استخدام": بيانات["آخر_استخدام"],
                "مرات_الاستخدام": بيانات["مرات_الاستخدام"]
            })
        return قائمة
    
    def تصدير_جلسة_كنص(self, الاسم: str) -> Optional[str]:
        """تصدير جلسة كنص عادي"""
        جلسة = self.الحصول_على_جلسة(الاسم)
        if جلسة:
            return جلسة["نص_الجلسة"]
        return None
