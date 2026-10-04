#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TikTok Video Enhancer 120 FPS
Professional quality enhancement for TikTok, Free Fire, and mobile games
Output: 1080x1920 (9:16 aspect ratio) at 120 FPS
"""

import cv2
import numpy as np
import os
import sys
from pathlib import Path
import time


class TikTokEnhancer120FPS:
    """Professional TikTok video enhancer with 120 FPS output"""
    
    def __init__(self):
        self.input_path = None
        self.output_path = None
        self.cap = None
        self.fps = 0
        self.width = 0
        self.height = 0
        self.total_frames = 0

    def print_banner(self):
        """Display welcome banner"""
        banner = """
╔════════════════════════════════════════════════════════════════╗
║                                                                ║
║         🎮 TIKTOK VIDEO ENHANCER 120 FPS 🎮                  ║
║     Professional Quality for Free Fire & Mobile Games         ║
║                                                                ║
╚════════════════════════════════════════════════════════════════╝
        """
        print(banner)
        print("Output: 1080x1920 (TikTok 9:16) at 120 FPS")
        print("Enhancement: Sharp + Colors + Clean + Professional\n")

    def get_input_file(self):
        """Get input video file"""
        print("[STEP 1] SELECT VIDEO FILE")
        print("-" * 60)
        
        while True:
            path = input("\nEnter video file path (or drag & drop): ").strip().strip('"').strip("'")
            
            if not path:
                print("❌ Please enter a file path")
                continue
            
            file_path = Path(path)
            
            if not file_path.exists():
                print(f"❌ File not found")
                continue
            
            if not file_path.is_file():
                print(f"❌ Not a file")
                continue
            
            supported = ['.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.m4v', '.wmv', '.3gp']
            if file_path.suffix.lower() not in supported:
                print(f"❌ Format not supported. Use: {', '.join(supported)}")
                continue
            
            self.input_path = str(file_path.resolve())
            size_mb = file_path.stat().st_size / (1024**2)
            print(f"✅ File loaded: {file_path.name}")
            print(f"   Size: {size_mb:.1f} MB")
            return True

    def get_output_file(self):
        """Get output filename"""
        print("\n[STEP 2] OUTPUT FILE NAME")
        print("-" * 60)
        
        output = input("\nOutput filename [tiktok_enhanced_120fps.mp4]: ").strip()
        
        if not output:
            output = "tiktok_enhanced_120fps.mp4"
        
        if not output.endswith('.mp4'):
            output += '.mp4'
        
        self.output_path = output
        print(f"✅ Output: {output}")
        return True

    def load_video_info(self):
        """Load video information"""
        print("\n[STEP 3] ANALYZING VIDEO")
        print("-" * 60)
        
        try:
            self.cap = cv2.VideoCapture(self.input_path)
            
            if not self.cap.isOpened():
                print("❌ Failed to open video")
                return False
            
            self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
            self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            if self.fps == 0:
                self.fps = 30
            
            duration = self.total_frames / self.fps if self.fps > 0 else 0
            
            print(f"\n✅ Video Information:")
            print(f"   • Original Resolution: {self.width}x{self.height}")
            print(f"   • Original FPS: {self.fps}")
            print(f"   • Total Frames: {self.total_frames:,}")
            print(f"   • Duration: {duration:.1f} seconds")
            print(f"\n✅ Output Settings:")
            print(f"   • Output Resolution: 1080x1920 (TikTok 9:16)")
            print(f"   • Output FPS: 120")
            print(f"   • Estimated Output Frames: {int(duration * 120):,}")
            
            return True
        
        except Exception as e:
            print(f"❌ Error: {e}")
            return False

    def resize_to_tiktok(self, frame):
        """Resize frame to TikTok 9:16 aspect ratio (1080x1920)"""
        h, w = frame.shape[:2]
        
        # Calculate scaling to fit in 1080x1920
        scale_w = 1080 / w
        scale_h = 1920 / h
        scale = min(scale_w, scale_h)
        
        new_w = int(w * scale)
        new_h = int(h * scale)
        
        resized = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
        
        # Create black canvas
        canvas = np.zeros((1920, 1080, 3), dtype=np.uint8)
        
        # Center the frame on canvas
        y_offset = (1920 - new_h) // 2
        x_offset = (1080 - new_w) // 2
        
        canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
        
        return canvas

    def denoise(self, frame):
        """Remove noise using bilateral filter"""
        return cv2.bilateralFilter(frame, 9, 75, 75)

    def sharpen(self, frame):
        """Sharpen the frame"""
        kernel = np.array([
            [-1, -1, -1],
            [-1, 10, -1],
            [-1, -1, -1]
        ]) / 1.3
        
        sharpened = cv2.filter2D(frame, -1, kernel)
        return sharpened

    def enhance_contrast(self, frame):
        """Enhance contrast using CLAHE"""
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        l_channel = lab[:, :, 0]
        
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
        l_channel = clahe.apply(l_channel)
        
        lab[:, :, 0] = l_channel
        return cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)

    def boost_colors(self, frame):
        """Boost saturation and brightness for vibrant colors"""
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)
        
        # Increase saturation (more vivid colors)
        hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.35, 0, 255)
        
        # Increase brightness slightly
        hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.15, 0, 255)
        
        return cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)

    def enhance_frame(self, frame):
        """Apply all enhancements to frame"""
        # 1. Denoise
        frame = self.denoise(frame)
        
        # 2. Resize to TikTok 9:16
        frame = self.resize_to_tiktok(frame)
        
        # 3. Sharpen
        frame = self.sharpen(frame)
        
        # 4. Enhance contrast
        frame = self.enhance_contrast(frame)
        
        # 5. Boost colors
        frame = self.boost_colors(frame)
        
        return frame

    def get_progress_bar(self, current, total, length=50):
        """Create progress bar"""
        if total == 0:
            return "[" + "░" * length + "] 0%"
        
        percent = current / total
        filled = int(length * percent)
        bar = '█' * filled + '░' * (length - filled)
        return f"[{bar}] {percent*100:.1f}%"

    def process_video(self):
        """Process video with interpolation to 120 FPS"""
        print("\n[STEP 4] PROCESSING VIDEO")
        print("=" * 60)
        print("Creating enhanced 120 FPS video...\n")
        
        try:
            # Output settings
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out_fps = 120
            out_width = 1080
            out_height = 1920
            
            out = cv2.VideoWriter(
                self.output_path,
                fourcc,
                out_fps,
                (out_width, out_height)
            )
            
            if not out.isOpened():
                print("❌ Failed to create output video")
                return False
            
            frame_count = 0
            last_frame = None
            start_time = time.time()
            
            print("Processing frames:\n")
            
            while True:
                ret, frame = self.cap.read()
                
                if not ret:
                    break
                
                # Enhance current frame
                enhanced = self.enhance_frame(frame)
                out.write(enhanced)
                
                # If FPS is less than 120, interpolate frames
                if self.fps < 120:
                    frames_to_add = int((120 / self.fps) - 1)
                    
                    if last_frame is not None:
                        for i in range(1, frames_to_add + 1):
                            alpha = i / (frames_to_add + 1)
                            interpolated = cv2.addWeighted(
                                last_frame, 1 - alpha,
                                enhanced, alpha, 0
                            )
                            out.write(interpolated)
                
                last_frame = enhanced
                frame_count += 1
                
                # Progress update
                if frame_count % max(1, self.total_frames // 50) == 0:
                    elapsed = time.time() - start_time
                    progress = self.get_progress_bar(frame_count, self.total_frames)
                    speed = frame_count / elapsed if elapsed > 0 else 0
                    print(f"\r{progress} | Frame {frame_count:,}/{self.total_frames:,} | Speed: {speed:.1f} f/s", 
                          end='', flush=True)
            
            self.cap.release()
            out.release()
            
            total_time = time.time() - start_time
            output_size = os.path.getsize(self.output_path) / (1024**2)
            
            print("\n\n" + "="*60)
            print("✅ SUCCESS! Video Enhanced")
            print("="*60)
            print(f"\n📊 Final Results:")
            print(f"   ✓ Original: {self.width}x{self.height} @ {self.fps} FPS")
            print(f"   ✓ Enhanced: {out_width}x{out_height} @ {out_fps} FPS")
            print(f"   ✓ Frames: {int(self.total_frames * (120 / self.fps)):,}")
            print(f"   ✓ Output: {self.output_path}")
            print(f"   ✓ File Size: {output_size:.1f} MB")
            print(f"   ✓ Time: {total_time/60:.1f} minutes")
            print(f"\n✨ Your TikTok video is READY! Upload now for maximum impact!")
            print(f"🎮 Perfect for Free Fire and mobile gaming videos!\n")
            
            return True
        
        except KeyboardInterrupt:
            print("\n\n⚠️ Processing stopped by user")
            self.cap.release()
            return False
        except Exception as e:
            print(f"\n\n❌ Error: {e}")
            import traceback
            traceback.print_exc()
            self.cap.release()
            return False


def main():
    """Main program"""
    try:
        enhancer = TikTokEnhancer120FPS()
        enhancer.print_banner()
        
        if not enhancer.get_input_file():
            return 1
        
        if not enhancer.get_output_file():
            return 1
        
        if not enhancer.load_video_info():
            return 1
        
        if not enhancer.process_video():
            return 1
        
        return 0
    
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        input("\nPress Enter to exit...")


if __name__ == "__main__":
    sys.exit(main())
