def save_markdown_to_file(markdown_string, filename):
    """
    Save a given markdown string to a file on local disk.

    :param markdown_string: String containing markdown content.
    :param filename: The path (with extension) where the markdown content will be saved.
    """
    try:
        # Open the file in write mode ('w')
        with open(filename, 'w', encoding='utf-8') as file:
            # Write the markdown content to the file
            file.write(markdown_string)
        print(f"Markdown content saved to {filename}")
    except IOError as e:
        print(f"An error occurred while writing to file: {e}")

# Example usage:
markdown_content = "# Hello, World!\nThis is a test markdown file."
save_markdown_to_file(markdown_content, "example.md")
