#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FFmpeg-based video enhancer
Fast, reliable, and much better for long videos.
Works on Windows, macOS, Linux.
"""

import os
import shutil
import subprocess
import sys


def ensure_ffmpeg():
    if shutil.which("ffmpeg") is None:
        print("ERROR: FFmpeg not found in PATH.")
        print("Install it from: https://www.ffmpeg.org/download.html")
        return False
    return True


def ask_path(prompt):
    value = input(prompt).strip().strip('"').strip("'")
    return value


def main():
    print("=" * 60)
    print("FFmpeg Video Enhancer - Better Quality / Fast")
    print("=" * 60)

    if not ensure_ffmpeg():
        input("Press Enter to exit...")
        return 1

    src = ask_path("Input video path: ")
    if not src or not os.path.exists(src):
        print("ERROR: File not found.")
        input("Press Enter to exit...")
        return 1

    out = ask_path("Output file name [output_enhanced.mp4]: ")
    if not out:
        out = "output_enhanced.mp4"
    if not out.lower().endswith(".mp4"):
        out += ".mp4"

    # Use a strong but stable enhancement profile.
    # This works well for TikTok and general quality boosts.
    filter_complex = (
        "hqdn3d=1.0:1.0:6:6,"
        "unsharp=5:5:0.8:5:5:0.0,"
        "scale=3840:2160:force_original_aspect_ratio=decrease:flags=lanczos,"
        "pad=3840:2160:(ow-iw)/2:(oh-ih)/2:color=black,"
        "format=yuv420p"
    )

    cmd = [
        "ffmpeg",
        "-y",
        "-i", src,
        "-vf", filter_complex,
        "-c:v", "libx264",
        "-preset", "slow",
        "-crf", "18",
        "-c:a", "aac",
        "-b:a", "192k",
        "-movflags", "+faststart",
        out,
    ]

    print("\nEnhancing video...")
    print("Command:")
    print(" ".join(cmd))
    print()

    try:
        subprocess.run(cmd, check=True)
        print("\nSUCCESS: Video enhanced and saved as:", out)
    except subprocess.CalledProcessError as e:
        print("\nERROR: FFmpeg failed with exit code", e.returncode)
        print("Try a shorter clip first or use a different source file.")
        input("Press Enter to exit...")
        return e.returncode

    input("Press Enter to exit...")
    return 0


if __name__ == "__main__":
    sys.exit(main())
