# Changelog

## 2.0.0

### Licensing
- License changed to a source-available model.
- Free for non-commercial use with attribution.
- Commercial use and any SaaS / cloud / hosted use require a paid license.
- Added a limited compatibility warranty related to block-format updates.

### Technical changes
- Added support for XOR-key handling when parsing `blocksdir` `*.dat` files.
  - The parser now detects whether an XOR key applies to the block files.
  - If no XOR key is present, or if the key is effectively zero, block files
    are parsed directly without decryption.
  - Compatible with existing `blocksdir` layouts and newly initialized ones
    using `blocksxor` (default: enabled).

- Improved incremental parsing behavior.
  - The parser now detects already processed block files in the `./result/`
    directory and processes only new block files.
  - If an incomplete or partially written `.dat` file is detected (typically
    the last file in the blocks directory), the parser reports an error and
    terminates execution without processing that file to avoid corrupted output.
