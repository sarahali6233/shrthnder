from keyboard_layouts import LayoutManager

def main():
    # Get available layouts
    layouts = LayoutManager.available_layouts()
    
    # Show available layouts
    print("\nAvailable layouts:")
    for i, layout in enumerate(layouts, 1):
        print(f"{i}. {layout}")
    
    # Let user choose a layout
    while True:
        try:
            choice = int(input("\nChoose a layout number (or 0 to exit): "))
            if choice == 0:
                break
            if 1 <= choice <= len(layouts):
                layout_name = layouts[choice - 1]
                layout = LayoutManager(layout_name)
                print(f"\nUsing {layout_name.upper()} layout (score: {layout.get_layout_score()})")
                print("Type some text (or 'quit' to choose another layout):")
                
                while True:
                    text = input("> ")
                    if text.lower() == 'quit':
                        break
                    transformed = layout.transform_text(text)
                    print(f"Transformed: {transformed}")
            else:
                print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

if __name__ == "__main__":
    main() 