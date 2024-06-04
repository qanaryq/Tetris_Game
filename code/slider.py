import pygame

class Slider:
    def __init__(self, x, y, w, h, min_val, max_val, start_val):
        self.rect = pygame.Rect(x, y, w, h)
        self.min_val = min_val
        self.max_val = max_val
        self.value = start_val
        self.grabbed = False

    def draw(self, screen):
        # Draw background bar
        pygame.draw.rect(screen, (200, 200, 200), self.rect)

        # Calculate position of the handle
        handle_x = self.rect.x + (self.value - self.min_val) / (self.max_val - self.min_val) * self.rect.width

        # Draw handle
        handle_rect = pygame.Rect(handle_x - 5, self.rect.y - 5, 10, self.rect.height + 10)
        pygame.draw.rect(screen, (255, 255, 255), handle_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.grabbed = True
        elif event.type == pygame.MOUSEBUTTONUP:
            self.grabbed = False
        elif event.type == pygame.MOUSEMOTION:
            if self.grabbed:
                relative_x = event.pos[0] - self.rect.x
                self.value = self.min_val + (relative_x / self.rect.width) * (self.max_val - self.min_val)
                self.value = max(self.min_val, min(self.max_val, self.value))

    def set_value(self, value):
        # Sets the value of the slider
        self.value = max(self.min_val, min(self.max_val, value))

    def get_value(self):
        # Returns the current value of the slider
        return self.value
