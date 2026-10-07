# Word Scramble Repair Lab

This project is an interactive anagram deduction word puzzle game using **Pygame**. It introduces students to string permutation, randomized list shuffling, uppercase letter sanitization, and text-box widget integration within an object-oriented codebase.
---

## What's Provided

A working Word Scramble game with:

- A built-in dictionary pool of words chosen at random each round
- A scrambling algorithm that randomizes letter order while ensuring the scrambled version differs from the original word
- A custom `TextBox` input component handling alphabetic keystrokes, automatic uppercase conversion, and backspace
- Interactive guess submission via the `Return` / `Enter` key or clicking the `SUBMIT` button
- Real-time score tracking, spaced letter displays, and color-coded status messaging

It has **one deliberate bug** and **three optional features** left as tasks to implement. You are expected to **analyze**, **interact with an AI assistant**, and **complete/fix** the game to make it fully functional and more interesting.

### **Use an LLM (e.g. ChatGPT or Claude) as your debugging and pair-programming partner for this lab.**
---

## Getting Started

### Setup

1. Make sure you have Python 3.10+ installed.
2. Install dependencies:

```bash
pip install pygame
```

3. Run the game:

```bash
python main.py
```

**Controls:** Type letters into the text box and press Return (or click SUBMIT) to submit your unscrambled word


## Tasks to Complete

Each task must be completed using an iterative process involving LLM suggestions and your critical code review.

### Task 1: Fix the guess comparison validation bug

Typing the correct unscrambled word is rejected as incorrect, while re-entering the scrambled letter string registers as a valid answer. Correct the guess verification logic so submitted words are validated against the actual secret target word rather than the scrambled display text.

### Task 2: Implement a progressive hint system

Challenging words can leave players stuck with no path forward. Add an interactive hint feature that reveals individual letters of the secret word in their correct positions upon request, applying a proportional score penalty for each hint used.
 
### Task 3: Implement a active round countdown timer

Players currently have unlimited time to ponder anagrams. Add a visible countdown timer bar to the round that ticks down during active play, automatically revealing the word and advancing to the next round if time runs out before a correct answer is submitted.

### Task 4: Implement Interactive Letter Tile Sorting

Scrambled letters are currently presented as a static text string. Replace the static label with interactive, graphical letter tiles that players can click or rearrange to physically experiment with different letter sequences before submitting a guess.

---

## Expected Behavior

- At the start of each round, a word is chosen and displayed with its letters jumbled.
- Typing the correctly unscrambled word into the input box awards 1 point, displays a success message, and advances to a new word.
- Typing an incorrect word displays a warning message and clears the input box for retry without advancing the round.
- Empty submissions trigger a prompt without penalty.
---

## Folder Structure

```
word_scramble/
├── game/
│   ├── game_engine.py
│   └── text_box.py
├── main.py
└── README.md
```

## Submission Checklist

Submission is only the following three things:

- [] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [] The Chat/LLM used page link, with the complete chat history
