# Knitting Instruction Generator

This tool converts SVG pattern files into human-readable knitting instructions. It's designed to help knitters follow patterns by providing clear, row-by-row instructions.

## Features

- Converts SVG pattern files into knitting instructions
- Generates row-by-row instructions with stitch counts
- Handles alternating knitting directions (right-to-left, then left-to-right)
- Supports both knit and purl stitches
- Outputs instructions in a human-readable format

## Requirements

- Python 3.x
- SVG file with the following specifications:
  - Each stitch represented by a 1x1 pixel rectangle
  - Purl stitches marked with color `#383838`
  - Knit stitches marked with white/light colors (`#FFFFFF` or `#FEFEFE`)

## Usage

1. Place your SVG pattern file in the same directory as the script
2. Run the script:
   ```bash
   python knit_instruction_generator.py
   ```

The script will:
1. Parse the SVG file
2. Generate knitting instructions for each row
3. Run unit tests to verify the output
4. Print all instructions in a readable format

## Output Format

Instructions are formatted as follows:
- Each row starts with "Row X:" where X is the row number
- Stitches are grouped by type and count
- 'k' indicates knit stitches
- 'p' indicates purl stitches
- Numbers indicate how many consecutive stitches of that type

Example:
```
Row 217: p10, k8, p7, k10, p1, k6, p6, k5, p6, k8, p6, k2, p6, k11, p5, k17, p10
```

## Knitting Direction

- Rows are numbered from bottom to top (1 is the bottom row)
- Even-numbered rows are knitted right-to-left
- Odd-numbered rows are knitted left-to-right
- Instructions are always written in left-to-right reading order

## Testing

The script includes unit tests to verify the instruction generation. Run the script to execute the tests:
```bash
python knit_instruction_generator.py
```

## Example

For a pattern that starts with all purl stitches:
```
Row   1: p124
Row   2: p124
...
```

For a pattern with alternating knit and purl sections:
```
Row  25: p10, k79, p5, k20, p10
Row  26: p10, k20, p4, k80, p10
...
```