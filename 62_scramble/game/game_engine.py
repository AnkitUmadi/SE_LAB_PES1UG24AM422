import random
import pygame
from game.text_box import TextBox


class LetterTile:
    def __init__(self, letter, x, y, size=48):
        self.letter = letter
        self.rect = pygame.Rect(x, y, size, size)
        self.selected = False

    def render(self, surface, font):
        bg_color = (230, 160, 40) if self.selected else (60, 115, 205)
        border_color = (255, 255, 255) if self.selected else (135, 175, 240)

        pygame.draw.rect(surface, bg_color, self.rect, border_radius=8)
        pygame.draw.rect(surface, border_color, self.rect, width=2, border_radius=8)

        text_surf = font.render(self.letter, True, (255, 255, 255))
        surface.blit(
            text_surf,
            (self.rect.centerx - text_surf.get_width() // 2,
             self.rect.centery - text_surf.get_height() // 2)
        )


class GameEngine:
    ROUND_TIME_MS = 25000  # 25-second round countdown

    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.words = ["PYTHON", "PYGAME", "PLANET", "ROCKET", "GALAXY", "STREAM", "PUZZLE", "ALGORITHM"]
        self.secret_word = ""
        self.scrambled_letters = []
        self.tiles = []
        self.selected_tile_idx = None

        self.score = 0
        self.hints_revealed = 0
        self.feedback_msg = "Unscramble or click two tiles to swap them!"
        self.feedback_color = (210, 215, 225)

        # UI interactive components
        self.input_box = TextBox(width // 2 - 180, 245, 160, 46)
        self.submit_btn = pygame.Rect(width // 2 - 5, 245, 95, 46)
        self.hint_btn = pygame.Rect(width // 2 + 100, 245, 80, 46)

        # Countdown timer tracker
        self.round_start_time = pygame.time.get_ticks()

        # Fonts
        self.font_title = pygame.font.SysFont(None, 40)
        self.font_tile = pygame.font.SysFont(None, 34)
        self.font_msg = pygame.font.SysFont(None, 24)
        self.font_btn = pygame.font.SysFont(None, 22)
        self.font_hint = pygame.font.SysFont(None, 26)

        self.next_round()

    def scramble_string(self, word):
        letters = list(word)
        while True:
            random.shuffle(letters)
            shuffled = "".join(letters)
            if shuffled != word or len(word) <= 1:
                return list(shuffled)

    def _setup_tiles(self):
        self.tiles = []
        tile_size = 46
        spacing = 8
        total_width = len(self.scrambled_letters) * (tile_size + spacing) - spacing
        start_x = (self.width - total_width) // 2
        y = 125

        for i, char in enumerate(self.scrambled_letters):
            tile = LetterTile(char, start_x + i * (tile_size + spacing), y, tile_size)
            self.tiles.append(tile)

    def next_round(self):
        self.secret_word = random.choice(self.words)
        self.scrambled_letters = self.scramble_string(self.secret_word)
        self.hints_revealed = 0
        self.selected_tile_idx = None
        self._setup_tiles()
        self.input_box.clear()
        self.round_start_time = pygame.time.get_ticks()

    def request_hint(self):
        max_hints = len(self.secret_word) - 1
        if self.hints_revealed < max_hints:
            self.hints_revealed += 1
            self.score = max(0, self.score - 1)  # Hint penalty
            self.feedback_msg = f"Hint used (-1 pt): Letter {self.hints_revealed} revealed!"
            self.feedback_color = (255, 215, 0)
        else:
            self.feedback_msg = "No more hints available for this word!"
            self.feedback_color = (240, 160, 60)

    def submit_guess(self):
        guess = self.input_box.text.strip().upper()
        if not guess:
            self.feedback_msg = "Type a word before submitting!"
            self.feedback_color = (240, 170, 50)
            return

        # Task 1: Validated against secret_word
        is_correct = (guess == self.secret_word)

        if is_correct:
            self.score += 2
            self.feedback_msg = f"CORRECT! '{self.secret_word}' is right."
            self.feedback_color = (80, 230, 110)
            self.next_round()
        else:
            self.feedback_msg = "WRONG GUESS! Try again."
            self.feedback_color = (240, 80, 80)
            self.input_box.clear()

    def handle_event(self, event):
        self.input_box.handle_event(event)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.submit_guess()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.submit_btn.collidepoint(event.pos):
                self.submit_guess()
            elif self.hint_btn.collidepoint(event.pos):
                self.request_hint()
            else:
                # Task 4: Interactive Tile swapping
                for idx, tile in enumerate(self.tiles):
                    if tile.rect.collidepoint(event.pos):
                        if self.selected_tile_idx is None:
                            self.selected_tile_idx = idx
                            tile.selected = True
                        elif self.selected_tile_idx == idx:
                            tile.selected = False
                            self.selected_tile_idx = None
                        else:
                            prev = self.selected_tile_idx
                            self.scrambled_letters[prev], self.scrambled_letters[idx] = (
                                self.scrambled_letters[idx],
                                self.scrambled_letters[prev]
                            )
                            self.selected_tile_idx = None
                            self._setup_tiles()
                        break

    def update(self):
        # Task 3: Timer depletion check
        elapsed = pygame.time.get_ticks() - self.round_start_time
        if elapsed >= self.ROUND_TIME_MS:
            self.feedback_msg = f"TIME UP! The word was '{self.secret_word}'."
            self.feedback_color = (240, 90, 90)
            self.next_round()

    def render(self, screen):
        screen.fill((26, 30, 38))

        # Title
        title_surf = self.font_title.render("Word Scramble Arena", True, (245, 245, 245))
        screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 18))

        # Score
        score_surf = self.font_msg.render(f"Score: {self.score}", True, (255, 220, 80))
        screen.blit(score_surf, (self.width // 2 - score_surf.get_width() // 2, 54))

        # Task 3: Countdown Timer Bar
        elapsed = pygame.time.get_ticks() - self.round_start_time
        remaining_ratio = max(0.0, 1.0 - (elapsed / self.ROUND_TIME_MS))
        bar_width = 340
        bar_height = 8
        bar_x = (self.width - bar_width) // 2
        bar_y = 88

        pygame.draw.rect(screen, (50, 55, 65), (bar_x, bar_y, bar_width, bar_height), border_radius=4)
        fill_color = (80, 220, 110) if remaining_ratio > 0.4 else (240, 160, 40) if remaining_ratio > 0.2 else (235, 75, 75)
        pygame.draw.rect(screen, fill_color, (bar_x, bar_y, int(bar_width * remaining_ratio), bar_height), border_radius=4)

        # Task 4: Interactive Letter Tiles
        for tile in self.tiles:
            tile.render(screen, self.font_tile)

        # Task 2: Progressive Hint Display
        if self.hints_revealed > 0:
            hint_display = " ".join([self.secret_word[i] if i < self.hints_revealed else "_" for i in range(len(self.secret_word))])
            hint_surf = self.font_hint.render(f"Hint: {hint_display}", True, (255, 215, 100))
            screen.blit(hint_surf, (self.width // 2 - hint_surf.get_width() // 2, 195))

        # Input Box
        self.input_box.render(screen)

        # Submit Button
        pygame.draw.rect(screen, (50, 150, 85), self.submit_btn, border_radius=6)
        pygame.draw.rect(screen, (220, 220, 220), self.submit_btn, width=2, border_radius=6)
        btn_text = self.font_btn.render("SUBMIT", True, (255, 255, 255))
        screen.blit(btn_text, (self.submit_btn.centerx - btn_text.get_width() // 2, self.submit_btn.centery - btn_text.get_height() // 2))

        # Hint Button
        pygame.draw.rect(screen, (200, 130, 40), self.hint_btn, border_radius=6)
        pygame.draw.rect(screen, (240, 220, 180), self.hint_btn, width=2, border_radius=6)
        hint_btn_text = self.font_btn.render("HINT", True, (255, 255, 255))
        screen.blit(hint_btn_text, (self.hint_btn.centerx - hint_btn_text.get_width() // 2, self.hint_btn.centery - hint_btn_text.get_height() // 2))

        # Status & Feedback Message
        feedback_surf = self.font_msg.render(self.feedback_msg, True, self.feedback_color)
        screen.blit(feedback_surf, (self.width // 2 - feedback_surf.get_width() // 2, 315))