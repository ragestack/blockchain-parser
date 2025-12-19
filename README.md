[![PyPI version](https://img.shields.io/pypi/v/blockchain-scalpel.svg)](https://pypi.org/project/blockchain-scalpel/)

# Blockchain Scalpel
(formerly: Blockchain parser / Russian scalpel)

## Русский скальпель

**Author:** Denis Leonov (ragestack)  
**Contact:** 466611@gmail.com

Blockchain Scalpel is a lightweight script for parsing raw **blkXXXXX.dat**
files of the Bitcoin blockchain database.

The tool provides direct access to blockchain data stored on disk and allows
exploring the main database as close as possible to its original binary
representation.

The parser is also compatible with many altcoins with minimal adjustments.

---

## Overview

Blockchain Scalpel is a low-level blockchain data parser designed for research,
analysis, and infrastructure-level processing.

The project focuses on:
- transparent and deterministic parsing
- minimal dependencies
- direct work with raw blockchain data
- long-term maintainability

No third-party modules or libraries are required.  
A standard Python installation is sufficient.

---

## Installation

### Install from PyPI

```bash
pip install blockchain-scalpel
```
This will install the **blockchain-scalpel** command-line tool.

### Manual usage
```bash
python blockchain-parser.py <blocks_dir> <result_dir>
```

---

## Usage

After installation from PyPI:
```bash
blockchain-scalpel <blocks_dir> <result_dir>
```

This is equivalent to:
```bash
python blockchain-parser.py <blocks_dir> <result_dir>
```

Where:

- <blocks_dir> is the directory containing blkXXXXX.dat files

- <result_dir> is the directory for parsed output

---

## Typical Usage

- academic and scientific research
- grant-funded university projects
- blockchain data analysis and forensics
- internal analytics and data processing pipelines

The script converts the raw blockchain database stored in **blkXXXXX.dat**
files into a simple, human-readable format.

Make sure to configure the paths for:
- input **blkXXXXX.dat** files
- output directory for parsing results

---

## Source Code

Repository:  
https://github.com/ragestack/blockchain-parser

PyPI package:
https://pypi.org/project/blockchain-scalpel/

---

## License

### Important: License by version

- Versions **up to and including `v1.0.0-gpl`** are licensed under **GPL-3.0**
- Versions **starting from `v2.0.0`** are distributed under the
  **Blockchain Scalpel License** (source-available)

### License summary (v2.0.0 and later)

- Free for **non-commercial use** with mandatory attribution
- Academic and grant-funded research is permitted
- **Commercial use requires a paid license**
- **SaaS / cloud / hosted use is not permitted without a commercial license**

See the full license text in the `LICENSE` file.

---

## Commercial Licensing

Commercial licenses, including licenses permitting use in commercial
organizations or SaaS / cloud / hosted environments, are available under
negotiated terms.

For commercial licensing inquiries, contact:

**Denis Leonov**  
466611@gmail.com

---

## Warranty

A limited compatibility warranty is provided for changes introduced by the
author related to new or updated blockchain block formats.

This warranty is limited in scope and does not constitute an SLA.

See `WARRANTY.md` for details.

---

## Notes

If this project is useful for your research or work, attribution to the author
is required.

Questions and licensing inquiries are welcome via email.

---

© Denis Leonov. All rights reserved.
