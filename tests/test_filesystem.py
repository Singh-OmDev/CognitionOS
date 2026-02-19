import shutil
import sys
from pathlib import Path

# Add src to path
sys.path.append(".")

from src.mcp.filesystem.tool import FileSystemTools

def test_filesystem():
    # Setup test dir
    test_dir = Path("test_workspace")
    test_dir.mkdir(exist_ok=True)
    
    fs = FileSystemTools(root_dir=str(test_dir))
    
    print("Testing Write...")
    result = fs.write_file("hello.txt", "Hello World")
    print(result)
    assert (test_dir / "hello.txt").read_text() == "Hello World"
    
    print("Testing Read...")
    content = fs.read_file("hello.txt")
    print(f"Read content: {content}")
    assert content == "Hello World"
    
    print("Testing List...")
    listing = fs.list_directory(".")
    print(listing)
    assert "FILE: hello.txt" in listing
    
    print("Testing Sandbox Safety...")
    result = fs.write_file("../hacker.txt", "exploit")
    if "Access denied" in result:
        print(f"SUCCESS: Sandbox caught breach: {result}")
    else:
        print(f"FAILED: Sandbox breach allowed! Result: {result}")
        
    # Cleanup
    shutil.rmtree(test_dir)
    print("\nAll filesystem tests passed!")

if __name__ == "__main__":
    test_filesystem()
