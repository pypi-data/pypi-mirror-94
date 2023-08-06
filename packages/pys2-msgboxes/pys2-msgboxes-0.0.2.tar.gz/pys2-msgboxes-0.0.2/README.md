# pys2-msgboxes

pys2-msgboxes is a module of pre-built messageboxes using the QMessageBox class from PySide2 library.

## Installation
Use the package manager pip to install pys2-msgboxes.
```pip install pys2-msgboxes```

## For now List of pre-built Messageboxes

* successful_msgbox()  
* input_error_msgbox() 
* information_msgbox()
* warning_msgbox() - Question Yes or No, return answer
* database_error_msgbox
* error_msgbox()

## Usage
Each of the pre-built messageboxes take two arguments: title and text.
```
from pys2_msgboxes import msgboxes

# Execute Successful Messagebox
msgboxes.successful_msgbox('Successful', 'Operation Finished Successfully')
```
All the messageboxes Execute like above except warning_msgbox that return a answer of the user.

### Question Messagebox (warning_msgbox)

```
from pys2_msgboxes import msgboxes

# importing the class MsgBox
from pys2_msgboxes.msgboxes import MsgBox

# This messagebox return the answer (Yes or No) of the user and saved in a variable
resp = msgboxes.warning_msgbox('Warning', 'Are your sure to perform this operation?')

# check which button (Yes or No) was pressed

if resp == MsgBox.Yes:
    # Operation when Yes is pressed
    print('"Yes" Button was pressed')
else:
    # Otherwise
    print('The "close" or "No" button was pressed')
```
Is not necessary to put the else stament if you are not going to do any action if the close or no Button is pressed.

## License
[MIT](https://opensource.org/licenses/MIT)