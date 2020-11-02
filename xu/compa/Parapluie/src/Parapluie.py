from typing import Final

# Widget
Object_Test: Final[str] = "Test"
Object_Raised: Final[str] = "Raised"
Object_Header: Final[str] = "Header"
Object_QSplitter: Final[str]= "QSplitter"
# Sticky Window
Object_StickyWindow: Final[str] = "StickyWindow"
Object_StickyWindow_FunctionButton: Final[str] = "FunctionButton"
Object_StickyWindow_ResizeBottom: Final[str] = "ResizeBottom"
Object_Alert_Error: Final[str] = "Alert_Error"
Object_Alert_Warning: Final[str] = "Alert_Warning"
Object_Alert_Information: Final[str] = "Alert_Information"
Object_Alert_Success: Final[str] = "Alert_Success"
# Button
Object_OptimizeButton: Final[str] = "OptimizeButton"
Object_NegativeButton: Final[str] = "NegativeButton"
Object_ColorButton: Final[str] = "ColorButton"
# Form
Object_FormLabel: Final[str] = "FormLabel"

# Edit
Object_OutlineBox: Final[str] = "OutlineBox"

# Item
Object_Item: Final[str] = "Item"
Object_Item_Category: Final[str] = "Category"
Object_Item_Tittle: Final[str] = "Tittle"
Object_Item_Description: Final[str] = "Description"
Object_ItemHeader: Final[str] = "ItemHeader"
Object_ItemHeader2: Final[str] = "ItemHeader2"

# Icon
Icon_Add_Svg: Final[str] = "add.svg"
Icon_Arrow_Drop_Down_Svg: Final[str] = "arrow_drop_down.svg"
Icon_Arrow_Drop_Up_Svg: Final[str] = "arrow_drop_up.svg"
Icon_Cancel_Svg: Final[str] = "cancel.svg"
Icon_Color_Wheel_Svg: Final[str] = "color_wheel.svg"
Icon_Document_Json_Svg: Final[str] = "document_json.svg"
Icon_Folder_Svg: Final[str] = "folder.svg"
Icon_Information_Svg: Final[str] = "information.svg"
Icon_Keyboard_Arrow_Down_Svg: Final[str] = "keyboard_arrow_down.svg"
Icon_Keyboard_Arrow_Up_Svg: Final[str] = "keyboard_arrow_up.svg"
Icon_Left_Arrow_Svg: Final[str] = "left-arrow.svg"
Icon_Levels_Svg: Final[str] = "levels.svg"
Icon_Link_Svg: Final[str] = "link.svg"
Icon_Open_Folder_Outline_Svg: Final[str] = "open-folder-outline.svg"
Icon_Plus_Svg: Final[str] = "plus.svg"
Icon_Resize_Bottom_Right_Svg: Final[str] = "resize-bottom-right.svg"
Icon_Refresh_Svg: Final[str] = "refresh.svg"
Icon_Clean_Code_Svg: Final[str] = "clean_code.svg"
Icon_Arrow_Right_Svg: Final[str] = "arrow_right.svg"
Icon_Double_Right_Chevron_Svg: Final[str] = "double_right_chevron.svg"
Icon_Save_Svg: Final[str] = "save.svg"
Icon_Play_Button_Svg: Final[str] = "play-button.svg"
Icon_Drag_Horizontal_Svg: Final[str] = "drag_horizontal.svg"
Icon_Drag_Vertical_Svg: Final[str] = "drag_vertical.svg"
Icon_Clear_All_Svg: Final[str] = "clear_all.svg"
Icon_Wrap_Text_Svg: Final[str] = "wrap_text.svg"
Icon_Web_Development_Svg: Final[str] = "web-development.svg"

# MessageDialog: code form 0 -> 7
Button_Neutral: Final[int] = 0
Button_Positive: Final[int] = 1
Button_Negative: Final[int] = 2


def MessageChecked(tpe: int) -> bool:
    return 0 <= tpe <= 2


# Alert: code from 16 -> 31
Right = 0b00010000  # bit12 = 0
Left = 0b00010001  # bit12 = 1
HCenter = 0b00010010  # bit12 = 2

Top = 0b00010000  # bit34 = 0
Bottom = 0b00010100  # bit34 = 1
VCenter = 0b00011000  # bit34 = 2


def PositionChecked(tpe: int) -> bool:
    return 16 <= tpe <= 31


def PositionHRead(tpe: int) -> int:
    if PositionChecked(tpe):
        data = bin(tpe).zfill(8)[6:]
        if data == "00":
            return Right
        elif data == "01":
            return Left
        elif data == "10":
            return HCenter
        else:
            raise Exception("Alert type invalid.")
    else:
        raise Exception("Not an alert type.")


def PositionVRead(tpe: int) -> int:
    if PositionChecked(tpe):
        data = bin(tpe).zfill(8)[4:6]
        if data == "00":
            return Top
        elif data == "01":
            return Bottom
        elif data == "10":
            return VCenter
        else:
            raise Exception("Alert type invalid.")
    else:
        raise Exception("Not an alert type.")


# AlertType
Alert_Error: Final[str] = "Error"
Alert_Warning: Final[str] = "Warning"
Alert_Information: Final[str] = "Information"
Alert_Success: Final[str] = "Success"
