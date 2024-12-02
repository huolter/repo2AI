import requests
import zipfile
import os
import io
import shutil
import argparse

# edit this URL for the default repo to the fetched
default_repo_url = 'https://github.com/karpathy/cryptos/'

def get_default_branch(repo_url: str) -> str:
    api_url = f"https://api.github.com/repos/{'/'.join(repo_url.rstrip('/').split('/')[-2:])}"
    try:
        response = requests.get(api_url)
        response.raise_for_status()
        repo_data = response.json()
        return repo_data.get("default_branch", "main")
    except requests.RequestException as e:
        print(f"Error fetching default branch: {e}")
        raise

def download_github_repo_as_zip(repo_url: str, destination: str = None):
    if not repo_url.startswith("https://github.com/"):
        raise ValueError("The provided URL must be a GitHub repository URL.")
    
    if destination is None:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        destination = os.path.join(script_dir, "repo")

    if os.path.exists(destination):
        shutil.rmtree(destination)

    os.makedirs(destination, exist_ok=True)

    default_branch = get_default_branch(repo_url)
    repo_parts = repo_url.rstrip("/").split("/")
    zip_url = f"https://github.com/{repo_parts[-2]}/{repo_parts[-1]}/archive/refs/heads/{default_branch}.zip"

    try:
        print(f"Downloading repository as ZIP from: {zip_url}")
        response = requests.get(zip_url, stream=True)
        response.raise_for_status()
        
        with zipfile.ZipFile(io.BytesIO(response.content)) as zf:
            extract_path = os.path.join(destination, repo_parts[-1])
            zf.extractall(extract_path)
            print(f"Repository extracted to: {extract_path}")
            return extract_path
    except requests.RequestException as e:
        print(f"Error downloading repository: {e}")
        raise
    except zipfile.BadZipFile as e:
        print(f"Error extracting ZIP file: {e}")
        raise

def describe_repo_contents(repo_folder: str = None):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if repo_folder is None:
        repo_folder = os.path.join(script_dir, "repo")

    def build_description(path, level=0):
        description = ""
        for item in sorted(os.listdir(path)):
            item_path = os.path.join(path, item)
            if os.path.isdir(item_path):
                description += "  " * level + f"- {item}\n"
                description += build_description(item_path, level + 1)
            else:
                description += "  " * level + f"- {item}\n"
        return description

    output_path = os.path.join(script_dir, "output.txt")

    try:
        if os.path.exists(output_path):
            os.remove(output_path)

        if not os.path.isdir(repo_folder):
            raise ValueError(f"The provided path '{repo_folder}' is not a valid directory.")

        header = "# This is the structure of the repository and its contents:\n\n"
        description = f"root\n{build_description(repo_folder)}"
        full_description = header + description + "\n\n# The following are the contents of the repository:\n"

        with open(output_path, "w") as file:
            file.write(full_description)
        
        print(f"Repository structure saved to: {output_path}")
        return output_path
    except Exception as e:
        print(f"Error generating description: {e}")
        raise

def append_file_contents_to_description(repo_folder: str = None):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if repo_folder is None:
        repo_folder = os.path.join(script_dir, "repo")
    output_path = os.path.join(script_dir, "output.txt")
    
    # Dictionary mapping file extensions to language names
    extension_to_language = {
        '.py': 'python',
        '.js': 'javascript',
        '.java': 'java',
        '.cpp': 'cpp',
        '.c': 'c',
        '.cs': 'csharp',
        '.html': 'html',
        '.css': 'css',
        '.rb': 'ruby',
        '.php': 'php',
        '.go': 'go',
        '.rs': 'rust',
        '.swift': 'swift',
        '.kt': 'kotlin',
        '.ts': 'typescript',
        '.sh': 'bash',
        '.md': 'markdown',
        # Add more extensions and languages as needed
    }

    try:
        def process_files(base_path):
            for root, dirs, files in os.walk(base_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    _, ext = os.path.splitext(file)
                    lang_hint = extension_to_language.get(ext, '')

                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()

                    with open(output_path, "a", encoding='utf-8') as output_file:
                        output_file.write(f"\n\n## Content of {file}\n\n")
                        output_file.write(f"```{lang_hint}\n{content}\n```\n")

        process_files(repo_folder)
        print(f"File contents appended to: {output_path}")
    except Exception as e:
        print(f"Error processing files: {e}")
        raise

def main():
    parser = argparse.ArgumentParser(description='Download and describe a GitHub repository.')
    parser.add_argument('repo_url', nargs='?', default=default_repo_url, help='URL of the GitHub repository')
    
    args = parser.parse_args()
    repo_url = args.repo_url

    download_github_repo_as_zip(repo_url)
    describe_repo_contents()
    append_file_contents_to_description()

if __name__ == "__main__":
    main()
