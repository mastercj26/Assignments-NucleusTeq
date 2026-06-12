import os

def write_name_to_file(filename: str, name: str) -> None:
    """Creates a file and writes a name into it."""
    print(f"Writing {name} to {filename}")
    with open(filename, 'w') as f:

        f.write(name)

def analyze_file(filename: str) -> None:
    """Reads a file and counts words, lines, and characters."""
    if not os.path.exists(filename):
        print("File does not exist.")
        return
        
    lines = 0
    words = 0
    characters = 0
    
    with open(filename, 'r') as f:
        for line in f:
            lines += 1
            characters += len(line)
            words += len(line.split())
            
    print(f"Lines: {lines}, Words: {words}, Characters: {characters}")

def append_to_file(filename: str, data: str) -> None:
    """Appends data to an existing file."""
    with open(filename, 'a') as f:
        f.write("\n" + data)

def copy_file(source: str, destination: str) -> None:
    """Copies content from one file to another."""
    with open(source, 'r') as src, open(destination, 'w') as dest:
        dest.write(src.read())

def search_word_in_file(filename: str, word: str) -> bool:
    """Searches for a word in a file."""
    if not os.path.exists(filename):
        return False
        
    with open(filename, 'r') as f:
        content = f.read()
        if word in content:
            return True
    return False

if __name__ == "__main__":
    test_file = "test.txt"
    write_name_to_file(test_file, "Chetan Jain")
    analyze_file(test_file)
    append_to_file(test_file, "Learning Python")
    analyze_file(test_file)
    copy_file(test_file, "copy_test.txt")
    print("Found 'Chetan'?", search_word_in_file(test_file, "Chetan"))
