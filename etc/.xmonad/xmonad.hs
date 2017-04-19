import XMonad
import XMonad.Config.Xfce
import XMonad.Hooks.SetWMName

startupHook = setWMName "LG3D"
 
main = xmonad xfceConfig
        { modMask = mod4Mask }
