## Main entry points

Everything a user of this package needs is re-exported from the top-level
`{{import_name}}` package, so it can be imported directly:

````python
from {{import_name}} import tk_greeting
````

The package is still a skeleton. `tk_greeting` is a placeholder that
returns the core greeting extended with the Tk version it found. It
exists so that the build, the generated API documentation and the test
summary can be verified end to end before the real editor is written.
