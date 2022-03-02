from window import AiseWindow
from plugin_manager import PluginManager
from context import AiseContext
import arcade

def main():
    arcade.enable_timings()
    aise_context = AiseContext()
    aise_win = AiseWindow(aise_context)
    aise_win.setup()
    arcade.run()

if __name__ == "__main__":
    main()
