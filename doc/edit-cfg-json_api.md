# Table of Contents

* [edit\_cfg\_json.hello](#edit_cfg_json.hello)
  * [core\_greeting](#edit_cfg_json.hello.core_greeting)

<a id="edit_cfg_json.hello"></a>

# edit\_cfg\_json.hello

Placeholder greeting for the user interface agnostic core package.

<a id="edit_cfg_json.hello.core_greeting"></a>

#### core\_greeting

```python
def core_greeting() -> str
```

Return a greeting naming this package and the library it builds on.

This is a placeholder until the real editor exists. It imports and
names `config_as_json` so that a greeting that can be produced at all
is evidence that the declared dependency resolved in the environment
the greeting runs in.

