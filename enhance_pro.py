#!/usr/bin/env python3
"""English one-file video enhancer. Requires FFmpeg in PATH.

Note: upscaling to 8K changes the output canvas to 7680x4320; it cannot recreate
missing detail from a low-resolution source.
"""
from pathlib import Path
import shutil
import subprocess
import sys

TARGET_W, TARGET_H = 7680, 4320


def main() -> int:
    print("=" * 60)
    print("Advanced Video Enhancer - 8K Output")
    print("=" * 60)
    print("This creates a 7680x4320 output; it cannot restore detail that was\n"
          "not present in the original video.\n")

    if shutil.which("ffmpeg") is None:
        print("ERROR: FFmpeg was not found in PATH.")
        print("Install it from https://ffmpeg.org/download.html and restart the terminal.")
        return 1

    source = Path(input("Input video path: ").strip().strip('"'))
    if not source.is_file():
        print(f"ERROR: File not found: {source}")
        return 1

    output_text = input("Output file [output_8k.mp4]: ").strip().strip('"')
    output = Path(output_text or "output_8k.mp4")
    if output.resolve() == source.resolve():
        print("ERROR: Output must be different from the input file.")
        return 1

    # Good general-purpose enhancement: light denoise, controlled sharpening,
    # high-quality Lanczos scaling, and a TikTok-friendly 8K canvas.
    vf = (
        f"hqdn3d=1.2:1.2:6:6,"
        f"unsharp=5:5:0.65:5:5:0,"
        f"scale={TARGET_W}:{TARGET_H}:force_original_aspect_ratio=decrease:flags=lanczos,"
        f"pad={TARGET_W}:{TARGET_H}:(ow-iw)/2:(oh-ih)/2:color=black,"
        "format=yuv420p"
    )
    command = [
        "ffmpeg", "-y", "-i", str(source),
        "-vf", vf,
        "-c:v", "libx264", "-preset", "slow", "-crf", "16",
        "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart",
        str(output),
    ]

    print(f"\nProcessing to {TARGET_W}x{TARGET_H}...\n")
    try:
        subprocess.run(command, check=True)
    except subprocess.CalledProcessError as exc:
        print(f"\nFFmpeg failed with exit code {exc.returncode}.")
        return exc.returncode or 1

    print(f"\nDone. Output: {output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
