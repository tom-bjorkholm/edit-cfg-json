## Project status

**Alpha. No API stability and no backward compatibility is offered while
this package is in Alpha.** That applies to the core and to both
backends. Public names may change without a major version bump.

Semantic versioning starts when the Alpha period ends. Until then, pin an
exact version if your build needs to be reproducible.

### Stable exception: Descriptions

A library or a program that only does

```python
from edit_cfg_json import Descriptions
```

and then uses the `Descriptions` type definition can safely use the
latest version of `edit_cfg_json` in its declared dependencies with
`install_requires = [ 'edit_cfg_json >=`...
That type definition will be kept stable (or at least backward
compatible).
