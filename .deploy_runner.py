#!/usr/bin/env python3
"""Runner script to deploy the Entropy Imperative post via deploy_post_v2.py"""
import subprocess, os

repo = os.path.expanduser("~/recursive-lobotomy")
post_path = os.path.join(repo, "posts", "2026-05-13-the-entropy-imperative-a-comprehensive-forensic-audit-of-recursive-lobotomy-broadcast-infrastructure.html")
deploy_script = os.path.join(repo, "deploy_post_v2.py")
title = "THE ENTROPY IMPERATIVE: A COMPREHENSIVE FORENSIC AUDIT OF RECURSIVE LOBOTOMY BROADCAST INFRASTRUCTURE"

with open(post_path, "r") as f:
    content = f.read()

# Write content to stdin-accessible temp file
stdin_file = os.path.join(repo, ".deploy_temp_input")
with open(stdin_file, "w") as f:
    f.write(content)

# Use deploy_post_v2.py by reading stdin from the temp file
result = subprocess.run(
    ["python3", deploy_script, title],
    stdin=open(stdin_file, "r"),
    capture_output=True,
    text=True,
    cwd=repo
)
print("STDOUT:", result.stdout)
print("STDERR:", result.stderr)
print("Return code:", result.returncode)

# Cleanup
os.remove(stdin_file)