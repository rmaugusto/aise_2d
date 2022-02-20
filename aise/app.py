from window import AiseWindow
from plugin_manager import PluginManager
from context import AiseContext
import arcade

def main():
    aise_context = AiseContext()
    AiseWindow(aise_context).setup()
    arcade.run()

if __name__ == "__main__":
    main()
