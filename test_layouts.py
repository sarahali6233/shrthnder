from keyboard_layouts import LayoutManager

def test_layout(layout_name, test_words):
    """Test a specific keyboard layout with given test words."""
    print(f"\nTesting {layout_name.upper()} layout:")
    print("-" * 50)
    
    try:
        layout = LayoutManager(layout_name)
        print(f"Layout score: {layout.get_layout_score()}")
        print("\nTransformations:")
        for word in test_words:
            transformed = layout.transform_text(word)
            print(f"{word:15} -> {transformed}")
    except Exception as e:
        print(f"Error testing {layout_name}: {e}")

def main():
    # Test words that include special characters and common programming terms
    test_words = [
        "hello",
        "python",
        "function",
        "class",
        "return",
        "import",
        "def",
        "print",
        "for",
        "while",
        "if else",
        "try except",
        "üäö",  # German special characters
        "ß",    # German sharp s
    ]

    # Test each layout
    layouts = LayoutManager.available_layouts()
    
    print("Available layouts:", ", ".join(layouts))
    print("\nStarting layout tests...")
    
    for layout in layouts:
        test_layout(layout, test_words)

if __name__ == "__main__":
    main() 