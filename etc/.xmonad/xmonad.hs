import XMonad
import XMonad.Config.Xfce
import XMonad.Hooks.SetWMName

startupHook = do
        setWMName "LG3D"
        spawn "~/.xmonad/xmonadrc"
 
main = xmonad xfceConfig
        { modMask = mod4Mask }
