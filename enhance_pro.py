#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🎬 أداة تحسين الفيديو المتقدمة إلى جودة 8K
Advanced Video Enhancement Tool v2.0
"""

import cv2
import numpy as np
import os
import sys
import time
from pathlib import Path

class AdvancedVideoEnhancer:
    """أداة متقدمة لتحسين جودة الفيديوهات"""
    
    def __init__(self, input_video, output_video=None, quality_level=3):
        """
        تهيئة الأداة
        
        Args:
            input_video: مسار ملف الفيديو المدخل
            output_video: مسار ملف الفيديو المخرج (اختياري)
            quality_level: مستوى الجودة (1=منخفض، 2=متوسط، 3=عالي، 4=فائق)
        """
        self.input_video = input_video
        self.output_video = output_video or "output_8k_enhanced.mp4"
        self.quality_level = quality_level
        self.cap = None
        self.fps = 0
        self.width = 0
        self.height = 0
        self.total_frames = 0
        self.start_time = 0
        
    def print_banner(self):
        """عرض البنر الرئيسي"""
        banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║         🎬 أداة تحسين الفيديو المتقدمة إلى 8K 🎬          ║
║                   Advanced Video Enhancer v2.0              ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
        """
        print(banner)
    
    def check_file_exists(self):
        """التحقق من وجود الملف"""
        if not os.path.exists(self.input_video):
            print(f"❌ الملف غير موجود: {self.input_video}")
            return False
        
        file_size = os.path.getsize(self.input_video) / (1024**2)  # بالميجابايت
        print(f"✅ تم العثور على الملف: {self.input_video}")
        print(f"   📊 حجم الملف: {file_size:.2f} MB")
        return True
    
    def load_video_info(self):
        """تحميل معلومات الفيديو"""
        self.cap = cv2.VideoCapture(self.input_video)
        
        if not self.cap.isOpened():
            print("❌ فشل فتح الفيديو")
            return False
        
        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        duration = self.total_frames / self.fps
        
        print(f"\n📊 معلومات الفيديو:")
        print(f"   • الدقة: {self.width}x{self.height}")
        print(f"   • عدد الإطارات: {self.fps} FPS")
        print(f"   • إجمالي الإطارات: {self.total_frames}")
        print(f"   • المدة: {duration:.1f} ثانية ({duration/60:.1f} دقيقة)")
        
        # اختيار مستوى الجودة
        print(f"\n⚙️ مستوى الجودة المختار: ", end="")
        if self.quality_level == 1:
            print("منخفض (سريع)")
        elif self.quality_level == 2:
            print("متوسط (متوازن)")
        elif self.quality_level == 3:
            print("عالي (بطيء)")
        elif self.quality_level == 4:
            print("فائق (بطيء جداً)")
        
        return True
    
    def upscale_frame(self, frame):
        """رفع دقة الإطار"""
        if self.quality_level == 1:
            scale = 1.5
            method = cv2.INTER_LINEAR
        elif self.quality_level == 2:
            scale = 2.0
            method = cv2.INTER_CUBIC
        elif self.quality_level == 3:
            scale = 2.0
            method = cv2.INTER_LANCZOS4
        else:  # quality_level == 4
            scale = 2.5
            method = cv2.INTER_LANCZOS4
        
        new_width = int(self.width * scale)
        new_height = int(self.height * scale)
        
        upscaled = cv2.resize(frame, (new_width, new_height), 
                             interpolation=method)
        return upscaled
    
    def sharpen_frame(self, frame):
        """تحسين حدة الإطار"""
        if self.quality_level == 1:
            kernel = np.array([[-1, -1, -1],
                              [-1,  9, -1],
                              [-1, -1, -1]]) / 1.0
            iterations = 1
        elif self.quality_level == 2:
            kernel = np.array([[-1, -1, -1],
                              [-1,  9, -1],
                              [-1, -1, -1]]) / 1.2
            iterations = 1
        elif self.quality_level == 3:
            kernel = np.array([[-1, -1, -1],
                              [-1, 12, -1],
                              [-1, -1, -1]]) / 1.5
            iterations = 2
        else:  # quality_level == 4
            kernel = np.array([[-1, -1, -1],
                              [-1, 13, -1],
                              [-1, -1, -1]]) / 2.0
            iterations = 2
        
        sharpened = frame
        for _ in range(iterations):
            sharpened = cv2.filter2D(sharpened, -1, kernel)
        
        return sharpened
    
    def denoise_frame(self, frame):
        """تقليل التشويش من الإطار"""
        if self.quality_level == 1:
            return cv2.fastNlMeansDenoisingColored(
                frame, None, h=8, hForColorComponents=8,
                templateWindowSize=7, searchWindowSize=21
            )
        elif self.quality_level == 2:
            return cv2.fastNlMeansDenoisingColored(
                frame, None, h=10, hForColorComponents=10,
                templateWindowSize=7, searchWindowSize=21
            )
        elif self.quality_level == 3:
            denoised = cv2.fastNlMeansDenoisingColored(
                frame, None, h=12, hForColorComponents=12,
                templateWindowSize=7, searchWindowSize=21
            )
            return cv2.fastNlMeansDenoisingColored(
                denoised, None, h=8, hForColorComponents=8,
                templateWindowSize=7, searchWindowSize=21
            )
        else:  # quality_level == 4
            denoised = cv2.fastNlMeansDenoisingColored(
                frame, None, h=15, hForColorComponents=15,
                templateWindowSize=7, searchWindowSize=21
            )
            denoised = cv2.fastNlMeansDenoisingColored(
                denoised, None, h=10, hForColorComponents=10,
                templateWindowSize=7, searchWindowSize=21
            )
            return denoised
    
    def enhance_colors(self, frame):
        """تحسين الألوان والسطوع والتباين"""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)
        
        if self.quality_level == 1:
            saturation_boost = 1.1
            brightness_boost = 1.05
        elif self.quality_level == 2:
            saturation_boost = 1.2
            brightness_boost = 1.10
        elif self.quality_level == 3:
            saturation_boost = 1.3
            brightness_boost = 1.15
        else:  # quality_level == 4
            saturation_boost = 1.4
            brightness_boost = 1.20
        
        # زيادة التشبع (Saturation)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * saturation_boost, 0, 255)
        
        # زيادة السطوع (Value)
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * brightness_boost, 0, 255)
        
        # تحويل العودة إلى BGR
        enhanced = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
        
        return enhanced
    
    def enhance_contrast(self, frame):
        """تحسين التباين باستخدام معادلة الهستوجرام"""
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l_channel = lab[:, :, 0]
        
        if self.quality_level <= 2:
            l_channel = cv2.equalizeHist(l_channel)
        else:
            # استخدام CLAHE للجودة العالية والفائقة
            if self.quality_level == 3:
                clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            else:  # quality_level == 4
                clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(4, 4))
            
            l_channel = clahe.apply(l_channel)
        
        lab[:, :, 0] = l_channel
        enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        return enhanced
    
    def apply_unsharp_mask(self, frame):
        """تطبيق Unsharp Mask لتحسين إضافي"""
        if self.quality_level <= 2:
            return frame
        
        # تمويه الصورة
        blurred = cv2.GaussianBlur(frame, (0, 0), 1.0)
        
        # حساب الفرق
        if self.quality_level == 3:
            mask = cv2.addWeighted(frame, 1.5, blurred, -0.5, 0)
        else:  # quality_level == 4
            mask = cv2.addWeighted(frame, 2.0, blurred, -1.0, 0)
        
        return np.clip(mask, 0, 255).astype(np.uint8)
    
    def enhance_frame(self, frame):
        """تحسين الإطار الواحد بجميع التقنيات"""
        # 1. رفع الدقة
        frame = self.upscale_frame(frame)
        
        # 2. تقليل التشويش
        frame = self.denoise_frame(frame)
        
        # 3. تحسين الحدة
        frame = self.sharpen_frame(frame)
        
        # 4. تطبيق Unsharp Mask
        frame = self.apply_unsharp_mask(frame)
        
        # 5. تحسين الألوان
        frame = self.enhance_colors(frame)
        
        # 6. تحسين التباين
        frame = self.enhance_contrast(frame)
        
        return frame
    
    def get_progress_bar(self, current, total, length=40):
        """إنشاء شريط تقدم"""
        percent = current / total
        filled = int(length * percent)
        bar = '█' * filled + '░' * (length - filled)
        return f"[{bar}] {percent*100:.1f}%"
    
    def calculate_eta(self, elapsed, current, total):
        """حساب الوقت المتبقي المتوقع"""
        if current == 0:
            return "حساب..."
        rate = elapsed / current
        remaining = (total - current) * rate
        mins, secs = divmod(remaining, 60)
        return f"{int(mins)}:{int(secs):02d}"
    
    def process_video(self):
        """معالجة الفيديو الكامل"""
        print("\n" + "="*60)
        
        if not self.check_file_exists():
            return False
        
        if not self.load_video_info():
            return False
        
        print(f"\n🔄 جاري معالجة الفيديو...")
        print(f"📁 سيتم حفظ الفيديو في: {self.output_video}\n")
        
        # إعداد كاتب الفيديو
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        
        # حساب الدقة الجديدة بناءً على مستوى الجودة
        if self.quality_level == 1:
            scale = 1.5
        elif self.quality_level == 2:
            scale = 2.0
        elif self.quality_level == 3:
            scale = 2.0
        else:
            scale = 2.5
        
        new_width = int(self.width * scale)
        new_height = int(self.height * scale)
        
        out = cv2.VideoWriter(self.output_video, fourcc, self.fps, 
                             (new_width, new_height))
        
        if not out.isOpened():
            print("❌ فشل إنشاء ملف الفيديو المحسّن")
            return False
        
        frame_count = 0
        self.start_time = time.time()
        
        try:
            while True:
                ret, frame = self.cap.read()
                
                if not ret:
                    break
                
                # معالجة الإطار
                enhanced_frame = self.enhance_frame(frame)
                
                # كتابة الإطار
                out.write(enhanced_frame)
                
                frame_count += 1
                elapsed = time.time() - self.start_time
                eta = self.calculate_eta(elapsed, frame_count, self.total_frames)
                
                # عرض التقدم
                progress = self.get_progress_bar(frame_count, self.total_frames)
                print(f"\r{progress} | {frame_count}/{self.total_frames} | ⏱️ {eta}", end='', flush=True)
        
        except KeyboardInterrupt:
            print("\n\n⚠️ تم إيقاف المعالجة من قبل المستخدم")
            return False
        
        finally:
            self.cap.release()
            out.release()
        
        # عرض النتائج
        total_time = time.time() - self.start_time
        output_size = os.path.getsize(self.output_video) / (1024**2)
        
        print(f"\n\n{'='*60}")
        print(f"✅ تمت المعالجة بنجاح!")
        print(f"{'='*60}")
        print(f"\n📊 النتائج النهائية:")
        print(f"   • الدقة الأصلية: {self.width}x{self.height}")
        print(f"   • الدقة الجديدة: {new_width}x{new_height}")
        print(f"   • عدد الإطارات: {self.fps} FPS")
        print(f"   • الملف: {self.output_video}")
        print(f"   • حجم الملف: {output_size:.2f} MB")
        print(f"   • وقت المعالجة: {total_time/60:.1f} دقيقة")
        print(f"   • السرعة: {self.total_frames/total_time:.1f} إطار/ثانية")
        print(f"\n" + "="*60)
        
        return True

def main():
    """البرنامج الرئيسي"""
    enhancer = AdvancedVideoEnhancer.__new__(AdvancedVideoEnhancer)
    enhancer.print_banner()
    
    # طلب اسم الملف
    print("\n📝 إدخال البيانات:\n")
    input_file = input("📁 أدخل اسم ملف الفيديو (مثلاً: video.mp4): ").strip()
    
    if not input_file:
        print("❌ يجب إدخال اسم الملف")
        return
    
    # اختيار مستوى الجودة
    print("\n⚙️ مستويات الجودة المتاحة:")
    print("   1️⃣  منخفض (سريع - 1.5x الدقة)")
    print("   2️⃣  متوسط (متوازن - 2x الدقة)")
    print("   3️⃣  عالي (بطيء - 2x الدقة + تقنيات متقدمة)")
    print("   4️⃣  فائق (بطيء جداً - 2.5x الدقة + أفضل التقنيات)")
    
    while True:
        try:
            quality = int(input("\n📊 اختر مستوى الجودة (1-4): ").strip())
            if 1 <= quality <= 4:
                break
            print("❌ الرجاء اختيار رقم بين 1 و 4")
        except ValueError:
            print("❌ الرجاء إدخال رقم صحيح")
    
    output_file = input("\n💾 أدخل اسم الملف المحفوظ (اتركها فارغة للاسم الافتراضي): ").strip()
    if not output_file:
        output_file = "output_8k_enhanced.mp4"
    
    # إنشاء الأداة ومعالجة الفيديو
    enhancer.__init__(input_file, output_file, quality)
    enhancer.process_video()

if __name__ == "__main__":
    main()
