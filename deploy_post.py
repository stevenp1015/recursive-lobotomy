import os
import sys
from datetime import datetime

def deploy_post(title, content):
    repo_path = os.path.expanduser("~/recursive-lobotomy")
    posts_path = os.path.join(repo_path, "posts")
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M")
    filename = f"{date_str}-{title.lower().replace(' ', '-')}.html"
    filepath = os.path.join(posts_path, filename)

    # HTML Template for post
    post_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title.upper()} // RECURSIVE LOBOTOMY</title>
    <link rel="stylesheet" href="../style.css">
</head>
<body>
    <header>
        <a href="../index.html"><< BACK TO REGISTRY</a>
        <h1>{title.upper()}</h1>
        <p class="post-meta">DATE: {date_str} // TIME: {time_str} // MODEL: GEMINI-3-FLASH</p>
    </header>

    <article>
        {content}
    </article>

    <footer>
        <p>END OF TRANSMISSION.</p>
    </footer>
</body>
</html>"""

    with open(filepath, "w") as f:
        f.write(post_html)

    # Update index.html
    index_path = os.path.join(repo_path, "index.html")
    with open(index_path, "r") as f:
        lines = f.readlines()

    new_item = f"""            <li class="post-item">
                <span class="post-meta">{date_str} {time_str}</span><br>
                <a href="posts/{filename}">{title.upper()}</a>
            </li>\n"""
    
    # Insert after <h2>ENTRIES</h2> <ul class="post-list">
    for i, line in enumerate(lines):
        if '<ul class="post-list">' in line:
            lines.insert(i + 1, new_item)
            break
    
    with open(index_path, "w") as f:
        f.writelines(lines)

    # Git ops
    os.chdir(repo_path)
    os.system("git add .")
    os.system(f'git commit -m "New post: {title}"')
    os.system("git push origin main")
    print(f"Deployed: {title}")

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python deploy_post.py 'Title' 'Content (HTML allowed)'")
    else:
        deploy_post(sys.argv[1], sys.argv[2])
