# All the TSS stuff is from https://github.com/AoDev/ti-alloy-in-sublime-text-2
# thx a lot!

import sublime, sublime_plugin
import re


common = {  "boolean" : ["true", "false"],
            "buttonmode" : ["INPUT_BUTTONMODE_ALWAYS", "INPUT_BUTTONMODE_NEVER", "INPUT_BUTTONMODE_ONBLUR", "INPUT_BUTTONMODE_ONFOCUS"],
            "color": ["rgb($1)", "rgba($1)", "\"transparent\"", "\"aqua\"", "\"black\"", "\"blue\"", "\"brown\"", "\"cyan\"", "\"darkgray\"", "\"fuchsia\"", "\"gray\"", "\"green\"", "\"lightgray\"", "\"lime\"", "\"magenta\"", "\"maroon\"", "\"navy\"", "\"olive\"", "\"orange\"", "\"pink\"", "\"purple\"", "\"red\"", "\"silver\"", "\"teal\"", "\"white\"", "\"yellow\""],
            "colorIOS" : ["COLOR_SCROLLVIEW_BACKGROUND", "COLOR_VIEW_FLIPSIDE_BACKGROUND", "COLOR_GROUP_TABLEVIEW_BACKGROUND", "COLOR_UNDER_PAGE_BACKGROUND"],
            "dimension" : ["{ x: $1, y: , height: , width:  }"],
            "fill" : ["Ti.UI.FILL", "Ti.UI.SIZE"],
            "point" :["{x:$1 , y: }"],
            "gradient" : ["{ $1 }"]
            }

tss_data = """

"accessibilityHidden" = <boolean>
"accessibilityHint" = ""
"accessibilityLabel" = ""
"accessibilityValue" = ""
"active" = <boolean>
"activeTab" = ""
"activeTabBackgroundColor" = <color> | <colorIOS>
"activeTabBackgroundDisabledColor" = ""
"activeTabBackgroundDisabledImage" = ""
"activeTabBackgroundFocusedColor" = ""
"activeTabBackgroundFocusedImage" = ""
"activeTabBackgroundImage" = ""
"activeTabBackgroundSelectedColor" = ""
"activeTabBackgroundSelectedImage" = ""
"adSize" = AD_SIZE_PORTRAIT | AD_SIZE_LANDSCAPE
"allowsSelection" = <boolean>
"allowsSelectionDuringEditing" = <boolean>
"allowUserCustomization" = <boolean>
"anchorPoint" = <point>
"appearance" = KEYBOARD_APPEARANCE_ALERT | KEYBOARD_APPEARANCE_DEFAULT
"autocapitalization" = TEXT_AUTOCAPITALIZATION_NONE | TEXT_AUTOCAPITALIZATION_WORDS | TEXT_AUTOCAPITALIZATION_SENTENCES | TEXT_AUTOCAPITALIZATION_ALL
"autocorrect" = <boolean>
"autoLink" = AUTOLINK_ALL | AUTOLINK_EMAIL_ADDRESSES | AUTOLINK_MAP_ADDRESSES | AUTOLINK_NONE | AUTOLINK_PHONE_NUMBERS | AUTOLINK_URLS
"backButtonTitle" = ""
"backButtonTitleImage" = ""
"backgroundColor" = <color> | <colorIOS>
"backgroundDisabledColor" = <color> | <colorIOS>
"backgroundDisabledImage" = ""
"backgroundFocusedColor" = <color> | <colorIOS>
"backgroundFocusedImage" = ""
"backgroundGradient" = <gradient>
"backgroundImage" = ""
"backgroundLeftCap" = ""
"backgroundPaddingBottom" = ""
"backgroundPaddingLeft" = ""
"backgroundPaddingRight" = ""
"backgroundPaddingTop" = ""
"backgroundRepeat" = <boolean>
"backgroundSelectedColor" = ""
"backgroundSelectedImage" = ""
"backgroundTopCap" = ""
"badge" = ""
"barColor" = <color>
"barImage" = ""
"borderBottom" = <boolean>
"borderColor" = <color>
"borderRadius" = ""
"borderStyle" =  INPUT_BORDERSTYLE_BEZEL | INPUT_BORDERSTYLE_LINE | INPUT_BORDERSTYLE_NONE | INPUT_BORDERSTYLE_ROUNDED
"borderTop" = <boolean>
"borderWidth" = ""
"bottom" = ""
"cacheSize" = ""
"canCancelEvents" = <boolean>
"cancel" = ""
"cancelable" = <boolean>
"canDelete" = <boolean>
"canScale" = <boolean>
"center" = <point>
"className" = ""
"clearButtonMode" =  INPUT_BUTTONMODE_ALWAYS | INPUT_BUTTONMODE_NEVER | INPUT_BUTTONMODE_ONBLUR | INPUT_BUTTONMODE_ONFOCUS
"clearOnEdit" = <boolean>
"color" = <color>
"contentHeight" = ""
"contentOffset" = ""
"contentWidth" = ""
"countDownDuration" = ""
"currentPage" = ""
"decodeRetries" = ""
"defaultImage" = ""
"disableBounce" = <boolean>
"disabledLeftTrackImage" = ""
"disabledRightTrackImage" = ""
"disabledThumbImage" = ""
"duration" = ""
"editable" = <boolean>
"editButtonTitle" = ""
"editing" = <boolean>
"ellipsize" = <boolean>
"enabled" = <boolean>
"enableReturnKey" = <boolean>
"enableZoomControls" = <boolean>
"endPoint" = <point>
"filterAttribute" = ""
"filterCaseInsensitive" = <boolean>
"focusable" = <boolean>
"font" = ""
"fontSize" = ""
"footerTitle" = ""
"format24" = <boolean>
"fullscreen" = <boolean>
"hasCheck" = <boolean>
"hasChild" = <boolean>
"hasDetail" = <boolean>
"headerTitle" = ""
"height" = <fill>
"hideLoadIndicator" = <boolean>
"hideSearchOnSelection" = <boolean>
"highlightedColor" = <color>
"highlightedLeftTrackImage" = ""
"highlightedRightTrackImage" = ""
"highlightedThumbImage" = ""
"hintText" = ""
"hinttextid" = ""
"hires" = <boolean>
"hitRect" = <dimension>
"horizontalBounce" = <boolean>
"horizontalMargin" = ""
"horizontalWrap" = <boolean>
"html" = ""
"icon" = ""
"indentionLevel" = ""
"keepScreenOn" = <boolean>
"keyboardToolbarColor" = <color> | <colorIOS>
"keyboardToolbarHeight" = ""
"keyboardType" =  KEYBOARD_ASCII | KEYBOARD_DECIMAL_PAD | KEYBOARD_DEFAULT | KEYBOARD_EMAIL | KEYBOARD_NAMEPHONE_PAD | KEYBOARD_NUMBERS_PUNCTUATION | KEYBOARD_NUMBER_PAD | KEYBOARD_PHONE_PAD | KEYBOARD_URL
"layout" = \"composite\" | \"vertical\" | \"horizontal\"
"left" = ""
"leftButton" = ""
"leftButtonMode" = <buttonmode>
"leftButtonPadding" = ""
"leftImage" = ""
"leftTrackImage" = ""
"leftTrackLeftCap" = ""
"leftTrackTopCap" = ""
"loading" = <boolean>
"locale" = ""
"location" = ""
"mask" = ""
"max" = ""
"maxDate" = ""
"maxLength" = ""
"maxRange" = ""
"maxRowHeight" = ""
"maxZoomScale" = ""
"message" = ""
"messageBody" = ""
"messageid" = ""
"min" = ""
"minDate" = ""
"minimumFontSize" = ""
"minRange" = ""
"minRowHeight" = ""
"minuteInterval" = ""
"minZoomScale" = ""
"modal" = <boolean>
"mode" = BLEND_MODE_CLEAR | BLEND_MODE_COLOR | BLEND_MODE_COLOR_BURN | BLEND_MODE_COLOR_DODGE | BLEND_MODE_COPY | BLEND_MODE_DARKEN | BLEND_MODE_DESTINATION_ATOP | BLEND_MODE_DESTINATION_IN | BLEND_MODE_DESTINATION_OUT | BLEND_MODE_DESTINATION_OVER | BLEND_MODE_DIFFERENCE | BLEND_MODE_EXCLUSION | BLEND_MODE_HARD_LIGHT | BLEND_MODE_HUE | BLEND_MODE_LIGHTEN | BLEND_MODE_LUMINOSITY | BLEND_MODE_MULTIPLY | BLEND_MODE_NORMAL | BLEND_MODE_OVERLAY | BLEND_MODE_PLUS_DARKER | BLEND_MODE_PLUS_LIGHTER | BLEND_MODE_SATURATION | BLEND_MODE_SCREEN | BLEND_MODE_SOFT_LIGHT | BLEND_MODE_SOURCE_ATOP | BLEND_MODE_SOURCE_IN | BLEND_MODE_SOURCE_OUT | BLEND_MODE_XOR
"moveable" = <boolean>
"navBarHidden" = <boolean>
"opacity" = ""
"orientationModes" = ""
"overlayEnabled" = <boolean>
"paddingLeft" = ""
"paddingRight" = ""
"pagingControlAlpha" = ""
"pagingControlColor" = <color> | <colorIOS>
"pagingControlHeight" = ""
"pagingControlOnTop" = <boolean>
"passwordMask" = <boolean>
"persistent" = <boolean>
"pluginState" = Titanium.UI.Android.WEBVIEW_PLUGINS_OFF | Titanium.UI.Android.WEBVIEW_PLUGINS_ON | or Titanium.UI.Android.WEBVIEW_PLUGINS_ON_DEMAND
"preventDefaultImage" = <boolean>
"prompt" = ""
"promptid" = ""
"repeatCount" = ""
"returnKeyType" =  RETURNKEY_DEFAULT | RETURNKEY_DONE | RETURNKEY_EMERGENCY_CALL | RETURNKEY_GO | RETURNKEY_GOOGLE | RETURNKEY_JOIN | RETURNKEY_NEXT | RETURNKEY_ROUTE | RETURNKEY_SEARCH | RETURNKEY_SEND | RETURNKEY_YAHOO.
"reverse" = <boolean>
"right" = ""
"rightButtonMode" = <buttonmode>
"rightButtonPadding" = ""
"rightImage" = ""
"rightTrackImage" = ""
"rightTrackLeftCap" = ""
"rightTrackTopCap" = ""
"rowHeight" = ""
"scalesPageToFit" = <boolean>
"scrollable" = <boolean>
"scrollIndicatorStyle" = BLACK | DEFAULT | WHITE
"scrollingEnabled" = <boolean>
"scrollsToTop" = <boolean>
"searchHidden" = <boolean>
"selectedBackgroundColor" = <color> | <colorIOS>
"selectedBackgroundImage" = ""
"selectedColor" = <color> | <colorIOS>
"selectedImage" = ""
"selectedLeftTrackImage" = ""
"selectedRightTrackImage" = ""
"selectedThumbImage" = ""
"selectionIndicator" = ""
"selectionStyle" = BLUE | GRAY | NONE
"separatorColor" = <color> | <colorIOS>
"separatorStyle" = NONE | SINGLE_LINE
"shadowColor" = <color> | <colorIOS>
"shadowOffset" = <point>
"showBookmark" = <boolean>
"showCancel" = <boolean>
"showHorizontalScrollIndicator" = <boolean>
"showPagingControl" = <boolean>
"showScrollbars" = <boolean>
"showVerticalScrollIndicator" = <boolean>
"softKeyboardOnFocus" = Titanium.UI.Android.SOFT_KEYBOARD_DEFAULT_ON_FOCUS | Titanium.UI.Android.SOFT_KEYBOARD_HIDE_ON_FOCUS | Titanium.UI.Android.SOFT_KEYBOARD_SHOW_ON_FOCUS
"startPoint" = <point>
"style" = Titanium.UI.Android.SWITCH_STYLE_CHECKBOX | Titanium.UI.Android.SWITCH_STYLE_TOGGLEBUTTON | BAR | BORDERED | DONE | PLAIN | Titanium.UI.iPhone.ActivityIndicatorStyle.DARK | Titanium.UI.iPhone.ActivityIndicatorStyle.BIG | Titanium.UI.iPhone.ActivityIndicatorStyle.PLAIN | Titanium.UI.ActivityIndicatorStyle.DARK | Titanium.UI.ActivityIndicatorStyle.BIG | Titanium.UI.ActivityIndicatorStyle.BIG_DARK | Titanium.UI.ActivityIndicatorStyle.PLAIN.
"suppressReturn" = <boolean>
"systemButton" = ACTION | ACTIVITY | ADD | BOOKMARKS | CAMERA | CANCEL | COMPOSE | CONTACT_ADD | DISCLOSURE | DONE | EDIT | FAST_FORWARD | FIXED_SPACE | FLEXIBLE_SPACE | INFO_DARK | INFO_LIGHT | ORGANIZE | PAUSE | PLAY | REFRESH | REPLY | REWIND | SAVE | SPINNER | STOP | TRASH
"tabDividerColor" = <color> | <colorIOS>
"tabDividerWidth" = auto
"tabHeight" = ""
"tabsAtBottom" = <boolean>
"tabsBackgroundColor" = <color> | <colorIOS>
"tabsBackgroundDisabledColor" = <color> | <colorIOS>
"tabsBackgroundDisabledImage" = ""
"tabsBackgroundFocusedColor" = <color> | <colorIOS>
"tabsBackgroundFocusedImage" = ""
"tabsBackgroundImage" = ""
"tabsBackgroundSelectedColor" = <color> | <colorIOS>
"tabsBackgroundSelectedImage" = ""
"text" = ""
"textAlign" = TEXT_ALIGNMENT_LEFT | TEXT_ALIGNMENT_CENTER | TEXT_ALIGNMENT_RIGHT
"textid" = ""
"thumbImage" = ""
"tint" = <color> | <colorIOS>
"title" = ""
"titleid" = ""
"titleImage" = ""
"titleOff" = ""
"titleOn" = ""
"titlePrompt" = ""
"titlepromptid" = ""
"top" = ""
"touchEnabled" = <boolean>
"translucent" = <boolean>
"type" = 'linear' | 'radial'
"useSpinner" = <boolean>
"value" = ""
"verticalAlign" = TEXT_VERTICAL_ALIGNMENT_BOTTOM | TEXT_VERTICAL_ALIGNMENT_CENTER | TEXT_VERTICAL_ALIGNMENT_TOP
"verticalBounce" = <boolean>
"verticalMargin" = ""
"visible" = <boolean>
"visibleItems" = ""
"width" = <fill>
"willHandleTouches" = <boolean>
"windowPixelFormat" = PIXEL_FORMAT_A_8 | PIXEL_FORMAT_LA_88 | PIXEL_FORMAT_L_8 | PIXEL_FORMAT_OPAQUE | PIXEL_FORMAT_RGBA_4444 | PIXEL_FORMAT_RGBA_5551 | PIXEL_FORMAT_RGBA_8888 | PIXEL_FORMAT_RGBX_8888 | PIXEL_FORMAT_RGB_332 | PIXEL_FORMAT_RGB_565 | PIXEL_FORMAT_RGB_888 | PIXEL_FORMAT_TRANSLUCENT | PIXEL_FORMAT_TRANSPARENT | PIXEL_FORMAT_UNKNOWN
"wobble" = <boolean>
"wordWrap" = <boolean>
"xOffset" = ""
"yOffset" = ""
"zIndex" = ""
"zoomScale" = ""
"""

def parse_tss_data(data):
    props = {}
    for l in data.splitlines():
        if l == "":
            continue

        names, values = l.split('=')

        allowed_values = []
        for v in values.split('|'):
            v = v.strip()
            if v[0] == '<' and v[-1] == '>':
                key = v[1:-1]
                if key in common:
                    allowed_values += common[key]
            else:
                allowed_values.append(v)

        for e in names.split():
            if e[0] == '"':
                props[e[1:-1]] = sorted(allowed_values)
            else:
                break

    return props

class TSSCompletions(sublime_plugin.EventListener):
    props = None
    rex = None

    def on_query_completions(self, view, prefix, locations):
        if not view.match_selector(locations[0], "source.tss - meta.selector.tss"):
            return []

        if not self.props:
            self.props = parse_tss_data(tss_data)
            self.rex = re.compile("([a-zA-Z-]+):\s*$")

        l = []
        if (view.match_selector(locations[0], "meta.property-value.tss") or
            # This will catch scenarios like .foo {font-style: |}
            view.match_selector(locations[0] - 1, "meta.property-value.tss")):
            loc = locations[0] - len(prefix)
            line = view.substr(sublime.Region(view.line(loc).begin(), loc))

            m = re.search(self.rex, line)
            if m:
                prop_name = m.group(1)
                if prop_name in self.props:
                    values = self.props[prop_name]

                    add_semi_colon = view.substr(sublime.Region(locations[0], locations[0] + 1)) != ','

                    for v in values:
                        desc = v
                        snippet = v

                        if add_semi_colon:
                            snippet += ","

                        if snippet.find("$1") != -1:
                            desc = desc.replace("$1", "")

                        l.append((desc, snippet))

                    return (l, sublime.INHIBIT_WORD_COMPLETIONS)

            return None
        else:
            add_colon = not view.match_selector(locations[0], "meta.property-name.tss")

            for p in self.props:
                if add_colon:
                    l.append((p, p + ": "))
                else:
                    l.append((p, p))

            return (l, sublime.INHIBIT_WORD_COMPLETIONS)
