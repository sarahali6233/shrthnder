from .layouts import KeyboardLayouts

class LayoutManager:
    def __init__(self, layout_name='qwertz'):
        """Initialize the layout manager with a specific layout."""
        self.current_layout = KeyboardLayouts.get_layout(layout_name)
        if not self.current_layout:
            raise ValueError(f"Layout '{layout_name}' not found")
        
    def transform_text(self, text):
        """Transform text from QWERTY to the current layout."""
        if not self.current_layout:
            return text
            
        result = ""
        for char in text:
            # Find the QWERTY key that maps to this character in the current layout
            qwerty_key = None
            for k, v in self.current_layout.items():
                if k != 'score' and v == char.lower():
                    qwerty_key = k
                    break
            
            # If we found a mapping, use it; otherwise keep the original character
            if qwerty_key:
                # Preserve case
                if char.isupper():
                    result += self.current_layout[qwerty_key].upper()
                else:
                    result += self.current_layout[qwerty_key]
            else:
                result += char
                
        return result
    
    def get_layout_score(self):
        """Get the efficiency score of the current layout."""
        return self.current_layout.get('score', 0)
    
    @staticmethod
    def available_layouts():
        """Get a list of all available layout names."""
        return [
            'qwertz',
            'adnw',
            'cmos',
            'hamlak',
            'programmer_dvorak',
            'colemak_mod_dh',
            'workman'
        ]
    
    def switch_layout(self, layout_name):
        """Switch to a different keyboard layout."""
        new_layout = KeyboardLayouts.get_layout(layout_name)
        if new_layout:
            self.current_layout = new_layout
        else:
            raise ValueError(f"Layout '{layout_name}' not found") 