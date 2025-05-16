import xml.etree.ElementTree as ET
from typing import List, Tuple
import unittest

class KnitInstructionGenerator:
    def __init__(self, svg_path: str):
        self.svg_path = svg_path
        self.width = 0
        self.height = 0
        self.stitches = []
        self._parse_svg()

    def _parse_svg(self):
        """Parse the SVG file and extract stitch information."""
        tree = ET.parse(self.svg_path)
        root = tree.getroot()
        
        # Get SVG dimensions from the root element
        self.width = int(root.get('width', '0'))
        self.height = int(root.get('height', '0'))
        
        # Initialize stitches grid
        self.stitches = [[False for _ in range(self.width)] for _ in range(self.height)]
        
        # Parse rect elements to determine stitch types
        for rect in root.findall('.//{http://www.w3.org/2000/svg}rect'):
            x = int(float(rect.get('x', '0')))
            y = int(float(rect.get('y', '0')))
            fill = rect.get('fill', '')
            
            # If the rect is dark gray/black (#383838), it's a purl stitch
            is_purl = fill.lower() == '#383838'
            
            if 0 <= y < self.height and 0 <= x < self.width:
                self.stitches[y][x] = is_purl

    def get_row_instructions(self, row: int) -> str:
        """Generate knitting instructions for a specific row.
        Rows are numbered from bottom to top (1 is bottom row).
        Even-numbered rows are read right-to-left, odd-numbered rows are read left-to-right."""
        if not 1 <= row <= self.height:
            raise ValueError(f"Row {row} is out of bounds (1-{self.height})")
        
        # Convert row number to actual row index (from bottom)
        actual_row = self.height - row
        
        # Determine if we're reading right-to-left (even rows) or left-to-right (odd rows)
        is_right_to_left = row % 2 == 0
        
        instructions = []
        if is_right_to_left:
            # Start from the right side
            current_type = self.stitches[actual_row][-1]
            count = 1
            for col in range(self.width - 2, -1, -1):
                if self.stitches[actual_row][col] == current_type:
                    count += 1
                else:
                    stitch_type = 'p' if current_type else 'k'
                    instructions.append(f"{stitch_type}{count}")
                    current_type = self.stitches[actual_row][col]
                    count = 1
            # Add the last group
            stitch_type = 'p' if current_type else 'k'
            instructions.append(f"{stitch_type}{count}")
            # Reverse the instructions for even rows to output in left-to-right order
            instructions.reverse()
        else:
            # For odd rows, we knit right-to-left and output in the same order
            current_type = self.stitches[actual_row][-1]
            count = 1
            for col in range(self.width - 2, -1, -1):
                if self.stitches[actual_row][col] == current_type:
                    count += 1
                else:
                    stitch_type = 'p' if current_type else 'k'
                    instructions.append(f"{stitch_type}{count}")
                    current_type = self.stitches[actual_row][col]
                    count = 1
            # Add the last group
            stitch_type = 'p' if current_type else 'k'
            instructions.append(f"{stitch_type}{count}")
        return ', '.join(instructions)

    def get_all_instructions(self) -> List[str]:
        """Generate knitting instructions for all rows, starting from the bottom."""
        return [self.get_row_instructions(row) for row in range(1, self.height + 1)]


class TestKnitInstructionGenerator(unittest.TestCase):
    def setUp(self):
        self.generator = KnitInstructionGenerator('input.svg')

    def test_rows(self):
        instructions = self.generator.get_row_instructions(1)
        self.assertEqual(instructions, "p124")
        instructions = self.generator.get_row_instructions(25)
        self.assertEqual(instructions, "p10, k79, p5, k20, p10")
        instructions = self.generator.get_row_instructions(26)
        self.assertEqual(instructions, "p10, k20, p4, k80, p10")
        instructions = self.generator.get_row_instructions(217)
        self.assertEqual(instructions, "p10, k8, p7, k10, p1, k6, p6, k5, p6, k8, p6, k2, p6, k11, p5, k17, p10")
        instructions = self.generator.get_row_instructions(102)
        self.assertEqual(instructions, "p10, k6, p4, k47, p13, k8, p18, k8, p10")


if __name__ == '__main__':
    # Run the tests
    unittest.main(exit=False)
    
    # Print all instructions in a readable format
    print("\nComplete Knitting Instructions:")
    print("===============================")
    generator = KnitInstructionGenerator('input.svg')
    instructions = generator.get_all_instructions()
    
    # Print instructions with correct row numbers (1 to height)
    for i, instruction in enumerate(instructions, 1):
        print(f"Row {i:3d}: {instruction}") 
    