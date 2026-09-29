#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete Video Enhancer - Works 100%
No external dependencies except opencv-python
"""

import cv2
import numpy as np
import os
import sys
from pathlib import Path


def enhance_video():
    """Main video enhancement function"""
    
    print("\n" + "="*70)
    print("VIDEO ENHANCER - PROFESSIONAL QUALITY")
    print("="*70 + "\n")
    
    # Step 1: Get input file
    print("[1/4] SELECT INPUT VIDEO")
    print("-" * 70)
    while True:
        input_path = input("Enter video file path: ").strip().strip('"').strip("'")
        input_file = Path(input_path)
        
        if not input_file.exists():
            print(f"❌ File not found: {input_path}")
            continue
        if not input_file.is_file():
            print(f"❌ Not a file: {input_path}")
            continue
        
        supported = ['.mp4', '.avi', '.mov', '.mkv', '.flv', '.webm', '.m4v', '.wmv']
        if input_file.suffix.lower() not in supported:
            print(f"❌ Unsupported format: {input_file.suffix}")
            print(f"   Supported: {', '.join(supported)}")
            continue
        
        print(f"✅ File loaded: {input_file.name}")
        break
    
    # Step 2: Get output file
    print("\n[2/4] CONFIGURE OUTPUT")
    print("-" * 70)
    output_name = input("Output filename [video_enhanced.mp4]: ").strip()
    if not output_name:
        output_name = "video_enhanced.mp4"
    if not output_name.endswith('.mp4'):
        output_name += '.mp4'
    print(f"✅ Output: {output_name}")
    
    # Step 3: Load video
    print("\n[3/4] ANALYZING VIDEO")
    print("-" * 70)
    
    cap = cv2.VideoCapture(str(input_file))
    if not cap.isOpened():
        print("❌ Failed to open video")
        return False
    
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if fps == 0:
        fps = 30
    if total_frames == 0:
        print("❌ Cannot read frame count")
        return False
    
    duration = total_frames / fps
    print(f"✅ Resolution: {width}x{height}")
    print(f"✅ FPS: {fps}")
    print(f"✅ Frames: {total_frames:,}")
    print(f"✅ Duration: {duration:.1f} seconds")
    
    # Step 4: Process video
    print("\n[4/4] PROCESSING VIDEO")
    print("-" * 70)
    
    # Output resolution (2x upscale)
    out_width = width * 2
    out_height = height * 2
    print(f"✅ Output Resolution: {out_width}x{out_height}")
    
    # Create video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_name, fourcc, fps, (out_width, out_height))
    
    if not out.isOpened():
        print("❌ Failed to create output video")
        cap.release()
        return False
    
    frame_idx = 0
    print("Processing frames:\n")
    
    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            
            # === ENHANCEMENT PROCESS ===
            
            # 1. Bilateral denoise (preserves edges)
            frame = cv2.bilateralFilter(frame, 9, 75, 75)
            
            # 2. Upscale using Lanczos
            frame = cv2.resize(frame, (out_width, out_height), interpolation=cv2.INTER_LANCZOS4)
            
            # 3. Sharpen
            kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]) / 1.5
            frame = cv2.filter2D(frame, -1, kernel)
            
            # 4. Enhance contrast with CLAHE
            lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
            l = lab[:, :, 0]
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
            l = clahe.apply(l)
            lab[:, :, 0] = l
            frame = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
            
            # 5. Boost colors and brightness
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV).astype(np.float32)
            hsv[:, :, 1] = np.clip(hsv[:, :, 1] * 1.25, 0, 255)  # Saturation
            hsv[:, :, 2] = np.clip(hsv[:, :, 2] * 1.10, 0, 255)  # Brightness
            frame = cv2.cvtColor(hsv.astype(np.uint8), cv2.COLOR_HSV2BGR)
            
            # === END ENHANCEMENT ===
            
            out.write(frame)
            frame_idx += 1
            
            # Progress
            progress = (frame_idx / total_frames) * 100
            bar_len = 40
            filled = int(bar_len * frame_idx / total_frames)
            bar = '█' * filled + '░' * (bar_len - filled)
            print(f"\r[{bar}] {progress:.1f}% ({frame_idx}/{total_frames})", end='', flush=True)
        
        cap.release()
        out.release()
        
        print("\n")
        print("="*70)
        print("✅ SUCCESS! Video enhanced and saved.")
        print("="*70)
        print(f"\n📊 Results:")
        print(f"   • Output file: {output_name}")
        print(f"   • Original size: {width}x{height}")
        print(f"   • Enhanced size: {out_width}x{out_height}")
        print(f"   • Frames processed: {frame_idx:,}")
        
        size_mb = os.path.getsize(output_name) / (1024**2)
        print(f"   • File size: {size_mb:.1f} MB")
        print("\n✨ Your video is ready!\n")
        
        return True
        
    except KeyboardInterrupt:
        print("\n\n⚠️ Stopped by user")
        cap.release()
        out.release()
        return False
    except Exception as e:
        print(f"\n\n❌ Error: {e}")
        cap.release()
        out.release()
        return False


if __name__ == "__main__":
    try:
        success = enhance_video()
        if not success:
            sys.exit(1)
    except Exception as e:
        print(f"❌ Fatal error: {e}")
        sys.exit(1)
    finally:
        input("\nPress Enter to exit...")
