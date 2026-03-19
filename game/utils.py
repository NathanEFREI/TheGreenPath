import pygame


# Ta fonction pour le texte libre (très bien pour les titres !)
def draw_centered_text(text, y, color, font, screen):
    rendered_text = font.render(text, True, color)
    text_rect = rendered_text.get_rect(center=(screen.get_width() // 2, y))
    screen.blit(rendered_text, text_rect)
    return text_rect

# Ta nouvelle fonction de bouton tout-en-un
# Remarque : j'ai ajouté 'font' et un 'text_color' qui est noir par défaut
def draw_button(x, y, width, height, color, text, font, screen, text_color="black"):
    border_radius = 20

    button_rect = pygame.Rect(x, y, width, height)

    pygame.draw.rect(screen, color, button_rect, border_radius=border_radius)

    rendered_text = font.render(text, True, text_color)

    text_rect = rendered_text.get_rect(center=button_rect.center)
    screen.blit(rendered_text, text_rect)
    return button_rect

def draw_hover_button(x, y, width, height, color, text, font, screen,over_color, text_color="black"):
    border_radius = 20
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)

    pygame.draw.rect(screen, color, button_rect, border_radius=border_radius)

    rendered_text = font.render(text, True, text_color)

    text_rect = rendered_text.get_rect(center=button_rect.center)
    if button_rect.collidepoint(mouse_x,mouse_y):
        pygame.draw.rect(screen,over_color,button_rect, border_radius=15)
    screen.blit(rendered_text, text_rect)
    return button_rect