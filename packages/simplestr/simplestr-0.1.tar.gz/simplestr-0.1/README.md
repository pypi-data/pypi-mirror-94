# simplestr
A python package with annotations to automatically generate `__str__(self)` and `__repr__(self)` methods in classes


# Description
This package provides only two annotations:
- `@gen_str` to generate `__str__(self)` method
- `@gen_repr` to generate `__repr__(self)` method

# Installation
 
## Normal installation

```bash
pip install simplestr
```

## Development installation

```bash
git clone https://github.com/jpleorx/simplestr.git
cd simplestr
pip install --editable .
```