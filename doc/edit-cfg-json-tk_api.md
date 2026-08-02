# Table of Contents

* [edit\_cfg\_json\_tk.hello](#edit_cfg_json_tk.hello)
  * [tk\_greeting](#edit_cfg_json_tk.hello.tk_greeting)

<a id="edit_cfg_json_tk.hello"></a>

# edit\_cfg\_json\_tk.hello

Placeholder greeting for the Tkinter backend package.

<a id="edit_cfg_json_tk.hello.tk_greeting"></a>

#### tk\_greeting

```python
def tk_greeting() -> str
```

Return a greeting naming this backend and the available Tk version.

This is a placeholder until the real editor exists. It reads the Tk
version without creating a window, so it also works on a machine
with no display.

