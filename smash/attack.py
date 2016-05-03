from pygame.locals import *
from pygame import font
from labels import *
from projectile import *
from character import *

class Attack():
	def __init__(self, character):
		if character.isFacingLeft:
			self.hitbox = pygame.Rect(character.rect.x - 20, character.rect.y - 20, character.rect.width + 20, character.rect.height + 20)
		else:
			self.hitbox = pygame.Rect(character.rect.x, character.rect.y - 20, character.rect.width + 20, character.rect.height + 20)

		self.character = character

	def show(self):
		pygame.draw.rect(self.character.game.screen, (255,0,0), self.hitbox)
