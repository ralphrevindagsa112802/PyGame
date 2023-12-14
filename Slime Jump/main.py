import pygame
import pygame.mixer
from singleton import Singleton
from camera import Camera
from player import Player
from level import Level
import settings as config



class Game(Singleton):

	# constructor called on new instance: Game()
	def __init__(self) -> None:
		
		# ============= Initialization =============
		self.__alive = True
		# Window / Render
		self.window = pygame.display.set_mode(config.DISPLAY,config.FLAGS)
		self.clock = pygame.time.Clock()

		# Instances
		self.camera = Camera()
		self.lvl = Level()
		self.player = Player(
			config.HALF_XWIN - config.PLAYER_SIZE[0]/2,# X POS
			config.HALF_YWIN + config.HALF_YWIN/2,#      Y POS
			*config.PLAYER_SIZE,# SIZE
			config.PLAYER_COLOR#  COLOR
		)

		# User Interface
		self.game_over_sound = pygame.mixer.Sound('data/sounds/game_over.wav')
		self.bg_music = pygame.mixer.Sound('data/sounds/bg_music.mp3')
		self.bg_music.set_volume(0.1)
		self.bg_music.play()

		self.score = 0
		self.score_txt = config.SMALL_FONT.render("0 points",1,config.GRAY)
		self.score_pos = pygame.math.Vector2(10,10)

		self.bg_image = pygame.image.load('data/image/bg_pygame.png')

		self.gameover_txt = config.LARGE_FONT.render("Game Over",1,config.WHITE)
		self.gameover_rect = self.gameover_txt.get_rect(
		center=(config.HALF_XWIN,config.HALF_YWIN))

		self.instructions_txt = config.SMALL_FONT.render("Press ENTER to restart", 1, config.WHITE)
		self.instructions_rect = self.instructions_txt.get_rect(
			center=(config.HALF_XWIN, config.HALF_YWIN + 50)
		)
		
	
	def close(self):
		self.__alive = False


	def reset(self):
		self.camera.reset()
		self.lvl.reset()
		self.player.reset()
		self.game_over_sound.stop()
		self.bg_music.set_volume(0.1)
		self.bg_music.play()
		self.score = 0


	def _event_loop(self):
		# ---------- User Events ----------
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.close()
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					self.close()
				if event.key == pygame.K_RETURN and self.player.dead:
					self.reset()
			self.player.handle_event(event)


	def _update_loop(self):
		# ----------- Update -----------
		self.player.update()
		self.lvl.update()

		if not self.player.dead:
			self.camera.update(self.player.rect)
			#calculate score and update UI txt
			self.score=-self.camera.state.y//50
			self.score_txt = config.SMALL_FONT.render(
				str(self.score)+" SCORE", 1, config.GRAY)
	

	def _render_loop(self):
		# ----------- Display ----------- 
		self.window.blit(self.bg_image, (0,0))
		self.lvl.draw(self.window)
		self.player.draw(self.window)

		if self.player.dead:
			self.bg_music.stop()
			self.game_over_sound.set_volume(0.1)
			self.game_over_sound.play()
			self.window.blit(self.gameover_txt, self.gameover_rect)
			self.window.blit(self.instructions_txt, self.instructions_rect)
		self.window.blit(self.score_txt, self.score_pos)

		pygame.display.update()
		self.clock.tick(config.FPS)


	def run(self):
		# ============= MAIN GAME LOOP =============
		while self.__alive:
			self._event_loop()
			self._update_loop()
			self._render_loop()
		pygame.quit()




if __name__ == "__main__":
	# ============= PROGRAM STARTS HERE =============
	game = Game()
	game.run()

