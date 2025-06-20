# MIT License
# 
# Copyright (c) 2025 S3Ducky

"""
S3Ducky package main entry point.
Allows running the package as: python -m s3ducky
"""

from .app import S3DuckyApp


def main():
    """Main entry point when package is run as module."""
    app = S3DuckyApp()
    app.run()


if __name__ == "__main__":
    main()
