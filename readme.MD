This script downloads a GitHub repository as a ZIP file, extracts its contents, and generates a detailed structure and content description output in Markdown format. The output includes a hierarchical folder structure and the content of each file in the repository.

Features

- Download and Extract: Automatically downloads and extracts the entire repository for offline inspection.
- Structure Description: Provides a detailed hierarchical view of the directory structure.
- Content Description: Extracts and outputs the content of each file, attempting to detect and display the programming language when applicable.

Usage

Clone this repository and navigate to the directory. Run the script using the following command:

python script.py [repo_url]

- Replace [repo_url] with the URL of the GitHub repository you want to analyze.
- If no URL is provided, the script defaults to analyzing the repository: https://github.com/karpathy/cryptos/.

Example

To analyze a specific repository, use:

python script.py https://github.com/someuser/somerepo

Output

- The script generates an output.txt file in the script's directory.
- This file contains a Markdown-formatted description of the directory structure and the contents of each file within the repository.

Notes

- The script uses the requests library to download the repository. If not already installed, you can add it using:

  pip install requests

- The script will overwrite the output.txt file each time it is run.

License

This project is open-source and available under the MIT License. See the LICENSE file for more details.
