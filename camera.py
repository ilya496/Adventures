import pygame


class Camera():
    def __init__(self, focus_rect, surface_x, surface_y):
        self.focus_rect = focus_rect
        self.x = surface_x
        self.y = surface_y

    def shift_rect(self, rect):
        if self.focus_rect is None:
            return rect
        copy_rect = rect.copy()
        copy_rect.x -= self.focus_rect.centerx - self.x / 2
        copy_rect.y -= self.focus_rect.centery - self.y / 2
        return copy_rect

    def change_focus_rect(self, new_focus_rect):
        self.focus_rect = new_focus_rect


class GroupWithCamera(Camera, pygame.sprite.LayeredUpdates):
    def __init__(self, focus_rect, surface_x, surface_y, *args, **kwargs):
        pygame.sprite.LayeredUpdates.__init__(self, *args, **kwargs)
        Camera.__init__(self, focus_rect, surface_x, surface_y)

    def draw(self, surface: pygame.Surface) -> None:
        for i in self.sprites():
            surface.blit(i.image, self.shift_rect(i.rect))
