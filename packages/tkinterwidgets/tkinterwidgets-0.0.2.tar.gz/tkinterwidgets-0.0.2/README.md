
# Tkinter Custom Widgets

This package contains custom `tkinter` widgets that might be useful.

## Installation

```shell
pip install tkinterwidgets
``` 

## Widgets

* [Label](#label)

***

* ### Label

  #### Features
  * Transparent background
  * Control opacity

  #### Usage 
  ```
  tkinterwidgets.Label(parent,OPTIONS)
  ```

  Options
  * All the options of native `tkinter` `Label` except `bg`/`background` since the background is transparent.
  * `opacity` - Used to specify the opacity of the contents on a scale of `0` to `1` (where `0` implies transparent and `1` implies opaque). The default is set to `1`.
  * `transcolor` - Used to specify the color to be used to create the transparency effect (you can imagine this as a green screen but of the specified color, make sure that the visible contents of the label do not have this color). The default is set to `SystemButtonFace` .

  Methods
  * `pack` - Same usage as that of the `pack` geometry manager in `tkinter`.
  *  `config`/`configure` - Set values of one or more options.

  #### Current Limitations / Issues
  * Only `pack` geometry manager can be used.
  * Can not be treated as a `window` in `Canvas.create_window()` or `Text.window_create()` or any similar usage.
  * In some cases, the label remains outside the window when the size of the window is reduced.

  #### Sample Code
  ```python
  from tkinter import *
  import tkinterwidgets as tkw 

  root=Tk()
  root.config(bg='yellow')

  label=Label(root,text='Default Label')
  label.pack()

  trans_label=tkw.Label(root,text='tkinterwidgets Label',opacity=0.7)
  trans_label.pack(pady=10)

  root.mainloop()
  ```

