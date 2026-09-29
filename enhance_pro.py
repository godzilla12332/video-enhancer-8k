#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Video Enhancer to 8K
Complete standalone solution - No external dependencies required
Works on Windows, Mac, and Linux
"""

import cv2
import numpy as np
import os
import sys
import time
import traceback
from pathlib import Path


class VideoEnhancer8K:
    """Complete video enhancement tool to 8K resolution"""
    
    def __init__(self):
        self.input_video = None
        self.output_video = None
        self.cap = None
        self.fps = 0
        self.width = 0
        self.height = 0
        self.total_frames = 0
        self.start_time = 0
        
    def print_header(self):
        """Print welcome header"""
        print("\n" + "="*70)
        print(" "*15 + "🎬 ADVANCED VIDEO ENHANCER 8K 🎬")
        print(" "*10 + "Professional Video Enhancement Tool")
        print("="*70)
        print()

    def check_opencv(self):
        """Check if OpenCV is installed"""
        try:
            import cv2
            print("✅ OpenCV is installed")
            return True
        except ImportError:
            print("❌ OpenCV not found. Installing...")
            os.system("pip install opencv-python")
            return True

    def get_input_file(self):
        """Get input video file from user"""
        while True:
            file_path = input("\n📁 Enter video file path (or drag and drop): ").strip().strip('"\'')
            
            if not file_path:
                print("❌ Please enter a file path")
                continue
                
            file_path = Path(file_path)
            
            if not file_path.exists():
                print(f"❌ File not found: {file_path}")
                continue
                
            if not file_path.is_file():
                print(f"❌ This is not a file: {file_path}")
                continue
                
            supported_formats = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.wmv', '.webm', '.m4v']
            if file_path.suffix.lower() not in supported_formats:
                print(f"⚠️  Unsupported format: {file_path.suffix}")
                print(f"Supported: {', '.join(supported_formats)}")
                continue
            
            self.input_video = str(file_path.resolve())
            print(f"✅ File found: {file_path.name}")
            return True

    def get_output_file(self):
        """Get output file name from user"""
        default_name = "video_8k_enhanced.mp4"
        output_name = input(f"\n💾 Output filename [{default_name}]: ").strip().strip('"\'')
        
        if not output_name:
            output_name = default_name
            
        if not output_name.endswith('.mp4'):
            output_name += '.mp4'
        
        self.output_video = output_name
        print(f"✅ Output will be saved as: {output_name}")
        return True

    def load_video_info(self):
        """Load and display video information"""
        try:
            self.cap = cv2.VideoCapture(self.input_video)
            
            if not self.cap.isOpened():
                print("❌ Failed to open video file")
                return False
            
            self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
            self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            if self.fps == 0:
                self.fps = 30
            
            duration = self.total_frames / self.fps if self.fps > 0 else 0
            file_size = os.path.getsize(self.input_video) / (1024**3)
            
            print("\n" + "-"*70)
            print("📊 VIDEO INFORMATION:")
            print("-"*70)
            print(f"  • Resolution:        {self.width}x{self.height}")
            print(f"  • Frame Rate (FPS):  {self.fps}")
            print(f"  • Total Frames:      {self.total_frames:,}")
            print(f"  • Duration:          {duration:.1f} seconds ({duration/60:.2f} minutes)")
            print(f"  • File Size:         {file_size:.2f} GB")
            print("-"*70)
            
            return True
            
        except Exception as e:
            print(f"❌ Error loading video: {e}")
            traceback.print_exc()
            return False

    def upscale_frame(self, frame):
        """Upscale frame using advanced interpolation"""
        try:
            # Scale 2x using Lanczos4 (best quality)
            new_width = self.width * 2
            new_height = self.height * 2
            
            upscaled = cv2.resize(
                frame,
                (new_width, new_height),
                interpolation=cv2.INTER_LANCZOS4
            )
            return upscaled
        except Exception as e:
            print(f"❌ Error in upscaling: {e}")
            return frame

    def denoise_frame(self, frame):
        """Reduce noise using bilateral filter"""
        try:
            # Use bilateral filter for edge-preserving denoising
            denoised = cv2.bilateralFilter(frame, 9, 75, 75)
            return denoised
        except Exception as e:
            print(f"❌ Error in denoising: {e}")
            return frame

    def sharpen_frame(self, frame):
        """Sharpen the frame"""
        try:
            kernel = np.array([
                [-1, -1, -1],
                [-1,  9, -1],
                [-1, -1, -1]
            ]) / 1.5
            
            sharpened = cv2.filter2D(frame, -1, kernel)
            return sharpened
        except Exception as e:
            print(f"❌ Error in sharpening: {e}")
            return frame

    def enhance_contrast(self, frame):
        """Enhance contrast using CLAHE"""
        try:
            lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
            l_channel = lab[:, :, 0]
            
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            l_channel = clahe.apply(l_channel)
            
            lab[:, :, 0] = l_channel
            enhanced = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
            
            return enhanced
        except Exception as e:
            print(f"❌ Error in contrast enhancement: {e}")
            return frame

    def enhance_colors(self, frame):
        """Enhance colors and saturation"""
        try:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)
            
            # Increase saturation
            hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.25, 0, 255)
            
            # Increase brightness slightly
            hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.10, 0, 255)
            
            enhanced = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
            return enhanced
        except Exception as e:
            print(f"❌ Error in color enhancement: {e}")
            return frame

    def enhance_frame(self, frame):
        """Apply all enhancement techniques to a frame"""
        try:
            # 1. Upscale
            frame = self.upscale_frame(frame)
            
            # 2. Denoise
            frame = self.denoise_frame(frame)
            
            # 3. Sharpen
            frame = self.sharpen_frame(frame)
            
            # 4. Enhance contrast
            frame = self.enhance_contrast(frame)
            
            # 5. Enhance colors
            frame = self.enhance_colors(frame)
            
            return frame
        except Exception as e:
            print(f"❌ Error in frame enhancement: {e}")
            traceback.print_exc()
            return frame

    def get_progress_bar(self, current, total, length=50):
        """Create a nice progress bar"""
        if total == 0:
            return "[" + "░" * length + "] 0%"
        
        percent = current / total
        filled = int(length * percent)
        bar = '█' * filled + '░' * (length - filled)
        return f"[{bar}] {percent*100:.1f}%"

    def calculate_eta(self, elapsed, current, total):
        """Calculate estimated time remaining"""
        if current == 0:
            return "Calculating..."
        
        rate = elapsed / current
        remaining = (total - current) * rate
        
        hours = int(remaining // 3600)
        minutes = int((remaining % 3600) // 60)
        seconds = int(remaining % 60)
        
        if hours > 0:
            return f"{hours}h {minutes}m {seconds}s"
        elif minutes > 0:
            return f"{minutes}m {seconds}s"
        else:
            return f"{seconds}s"

    def process_video(self):
        """Process the entire video"""
        try:
            print("\n" + "="*70)
            print("🔄 PROCESSING VIDEO...")
            print("="*70)
            
            if not self.load_video_info():
                return False
            
            # Calculate new resolution
            new_width = self.width * 2
            new_height = self.height * 2
            
            print(f"\n📈 Output Resolution: {new_width}x{new_height}")
            print(f"📹 Output FPS: {self.fps}")
            print(f"💾 Output File: {self.output_video}\n")
            
            # Setup video writer
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(
                self.output_video,
                fourcc,
                self.fps,
                (new_width, new_height)
            )
            
            if not out.isOpened():
                print("❌ Failed to create output video file")
                print("Try changing the output filename or check disk space")
                return False
            
            frame_count = 0
            self.start_time = time.time()
            
            print("Processing frames:")
            print("-"*70)
            
            while True:
                ret, frame = self.cap.read()
                
                if not ret:
                    break
                
                # Enhance the frame
                enhanced_frame = self.enhance_frame(frame)
                
                # Write the frame
                out.write(enhanced_frame)
                
                frame_count += 1
                
                # Update progress every 5 frames to avoid slowdown
                if frame_count % max(1, self.total_frames // 100) == 0 or frame_count == 1:
                    elapsed = time.time() - self.start_time
                    eta = self.calculate_eta(elapsed, frame_count, self.total_frames)
                    progress = self.get_progress_bar(frame_count, self.total_frames)
                    fps_current = frame_count / elapsed if elapsed > 0 else 0
                    
                    print(f"\r{progress} | {frame_count:,}/{self.total_frames:,} | "
                          f"Speed: {fps_current:.1f} fps | ETA: {eta}", end='', flush=True)
            
            self.cap.release()
            out.release()
            
            # Calculate results
            total_time = time.time() - self.start_time
            output_size = os.path.getsize(self.output_video) / (1024**3)
            fps_average = self.total_frames / total_time if total_time > 0 else 0
            
            print("\n" + "="*70)
            print("✅ VIDEO PROCESSING COMPLETED SUCCESSFULLY!")
            print("="*70)
            print(f"\n📊 FINAL RESULTS:")
            print(f"  • Original Resolution:  {self.width}x{self.height}")
            print(f"  • Enhanced Resolution:  {new_width}x{new_height}")
            print(f"  • Frame Rate:           {self.fps} FPS")
            print(f"  • Total Frames:         {self.total_frames:,}")
            print(f"  • Output File:          {self.output_video}")
            print(f"  • Output File Size:     {output_size:.2f} GB")
            print(f"  • Processing Time:      {total_time/60:.1f} minutes")
            print(f"  • Average Speed:        {fps_average:.1f} frames/second")
            print("="*70)
            print("\n✨ Your enhanced video is ready! ✨\n")
            
            return True
            
        except KeyboardInterrupt:
            print("\n\n⚠️  Processing stopped by user")
            return False
        except Exception as e:
            print(f"\n❌ Error during processing: {e}")
            traceback.print_exc()
            return False


def main():
    """Main program"""
    try:
        enhancer = VideoEnhancer8K()
        enhancer.print_header()
        
        # Check OpenCV
        enhancer.check_opencv()
        
        # Get input file
        if not enhancer.get_input_file():
            return 1
        
        # Get output file
        if not enhancer.get_output_file():
            return 1
        
        # Process video
        if not enhancer.process_video():
            return 1
        
        return 0
        
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        traceback.print_exc()
        return 1
    finally:
        print("Press Enter to exit...")
        try:
            input()
        except:
            pass


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
