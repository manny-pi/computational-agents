from pygame.sprite import Sprite, Group
from pygame import Rect
from pygame import Surface


class GenericSprite(Sprite):
    """
    This class receives an instance of the Robot agent, and creates a Sprite for it 
    """

    def __init__(self,
                 ID: int,
                 name: str = None,
                 shape: "tuple[int, int]" = (20, 20),
                 coordinates: "tuple[int, int]" = (100, 100),
                 color: "tuple[int, int, int]" = (255, 0, 0)):
        """
        Args:
            ID (int): _description_
            name (str): _description_
            shape (tuple[int, int]): _description_
            coordinates (tuple[int, int]): _description_
            color (tuple[int, int, int], optional): _description_. Defaults to (255, 0, 0).
        """ 
        Sprite.__init__(self)
        self.__ID = ID
        self.__name = name if name else f"sprite{ID}"
        self.__width, self.__height = shape
        self.__x, self.__y = coordinates
        self.__color = color

        self.__surface = Surface(shape)
        self.__surface.fill(color)
        self.__rect = self.__surface.get_rect(center=(coordinates))

    def set_name(self, name: str):
        """Set the name of the GenericSprite."""
        self.__name = name

    def set_coordinates(self, coordinates: "tuple[int, int]"):
        """Set the coordinates of the sprite."""
        self.__width, self.__height = coordinates
        self.__rect.center = coordinates

    def set_x(self, x: int):
        """Set the x coordinate of the sprite."""
        self.__x = x

    def set_y(self, y: int):
        """Set the y coordinate of the sprite."""
        self.__y = y

    def set_color(self, color: "tuple[int, int, int]"):
        """Set the color of the sprite."""
        self.__color = color
        self.__surface.fill(color)

    def get_ID(self) -> int:
        """Get the ID of the sprite."""
        return self.__ID

    def get_name(self) -> str:
        """Get the name of the sprite."""
        return self.__name

    def get_coordinates(self) -> "tuple[int, int]":
        """Get the coordinates of the sprite."""
        return self.__x, self.__y

    def get_x(self) -> int:
        """Get the x coordinate of the sprite."""
        return self.__x

    def get_y(self) -> int:
        """Get the y coordinate of the sprite."""
        return self.__y

    def get_color(self) -> "tuple[int, int, int]":
        """Get the color of the sprite."""
        return self.__color

    def get_width(self) -> int:
        """Get the width of the sprite."""
        return self.__width

    def get_height(self) -> int:
        """Get the height of the sprite."""
        return self.__height

    def get_surface(self) -> Surface:
        """Get the surface(pygame.Surface) of the sprite."""
        return self.__surface

    def get_rect(self) -> Rect:
        """Get the rect(pygame.Rect) of the sprite."""
        return self.__rect

    def __str__(self):
        info = {
            "ID": self.__ID,
            "Name": self.__name,
        }

        return info


class GenericSpriteGroup(Group):
    def __init__(self, *sprites):
        super().__init__(sprites)
