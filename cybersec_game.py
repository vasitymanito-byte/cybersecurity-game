"""
CyberSec Academy - Terminal Edition
A gamified cybersecurity educational app
"""

import os
import sys
import time
import json
import random

# ── ANSI helpers (minimal: bold, dim, reset only) ────────────────────────────

BOLD  = "\033[1m"
DIM   = "\033[2m"
RESET = "\033[0m"
CLEAR = "\033c"

def bold(s):  return f"{BOLD}{s}{RESET}"
def dim(s):   return f"{DIM}{s}{RESET}"
def hr(char="─", width=60): return dim(char * width)


# ── DATA ─────────────────────────────────────────────────────────────────────

MODULES = [
    {
        "id": "password",
        "name": "Module 1 — Password Security",
        "difficulty": "Easy",
        "xp": 50,
        "prereq": None,
        "questions": [
            {
                "q": "Which password is the strongest?",
                "choices": [
                    "password123",
                    "MyDog2020!",
                    "Tr7!vXqL@2#mN9",
                    "ilovecookies",
                ],
                "correct": 2,
                "explain": (
                    "Tr7!vXqL@2#mN9 is 14 characters and mixes uppercase, lowercase,\n"
                    "  numbers, and symbols. Length + randomness is what makes it strong."
                ),
            },
            {
                "q": "A site stores your password as:\n  5f4dcc3b5aa765d61d8327deb882cf99\n  What is this?",
                "choices": [
                    "Encrypted password",
                    "MD5 hash of 'password'",
                    "Base64 encoding",
                    "A randomly generated token",
                ],
                "correct": 1,
                "explain": (
                    "That is the MD5 hash of 'password'. MD5 is broken — attackers use\n"
                    "  rainbow tables to reverse common hashes in seconds. Never use MD5\n"
                    "  for passwords."
                ),
            },
            {
                "q": "Why is reusing the same password across multiple sites dangerous?",
                "choices": [
                    "Websites share their password databases with each other",
                    "If one site is breached, attackers try your credentials everywhere\n     (credential stuffing)",
                    "Password length decreases with each reuse",
                    "It is not dangerous — reuse is more secure",
                ],
                "correct": 1,
                "explain": (
                    "Credential stuffing automates logins across thousands of sites using\n"
                    "  leaked credentials. One breach becomes many if you reuse passwords."
                ),
            },
            {
                "q": "What does a password manager primarily do?",
                "choices": [
                    "Shares passwords with your teammates",
                    "Generates and stores unique strong passwords securely",
                    "Recovers forgotten passwords from websites",
                    "Scans passwords for viruses",
                ],
                "correct": 1,
                "explain": (
                    "Password managers generate and encrypt a unique strong password per\n"
                    "  site. You only remember one master password, eliminating reuse."
                ),
            },
            {
                "q": "Multi-Factor Authentication (MFA) requires:",
                "choices": [
                    "A very long password only",
                    "Two or more verification factors from different categories",
                    "Logging in from two devices simultaneously",
                    "Changing your password every 30 days",
                ],
                "correct": 1,
                "explain": (
                    "MFA combines: something you KNOW (password), something you HAVE\n"
                    "  (phone/token), and/or something you ARE (biometrics). A stolen\n"
                    "  password alone is no longer enough."
                ),
            },
        ],
    },
    {
        "id": "social",
        "name": "Module 2 — Social Engineering",
        "difficulty": "Medium",
        "xp": 80,
        "prereq": "password",
        "questions": [
            {
                "q": (
                    "You get an urgent email from your 'bank' saying your account is\n"
                    "  locked. It asks you to click a link and enter credentials now.\n"
                    "  This is most likely:"
                ),
                "choices": [
                    "A legitimate security alert",
                    "A phishing attack",
                    "A SQL injection attempt",
                    "A keylogger",
                ],
                "correct": 1,
                "explain": (
                    "Phishing emails manufacture urgency to panic users into clicking\n"
                    "  malicious links. Real banks never ask for credentials via email.\n"
                    "  Always navigate directly to the bank's website."
                ),
            },
            {
                "q": (
                    "An attacker calls your company pretending to be an IT technician\n"
                    "  who needs your login to fix a 'server issue'. This is called:"
                ),
                "choices": [
                    "Spear phishing",
                    "Vishing (voice phishing)",
                    "Pretexting",
                    "Baiting",
                ],
                "correct": 2,
                "explain": (
                    "Pretexting means fabricating a scenario to manipulate someone. The\n"
                    "  attacker built a fake identity (IT tech) to extract credentials.\n"
                    "  Verify callers through official channels before sharing anything."
                ),
            },
            {
                "q": "You find a USB drive in the parking lot labeled 'Salary Data Q4'.\n  What should you do?",
                "choices": [
                    "Plug it into your work computer to find the owner",
                    "Take it to IT security without plugging it in",
                    "Plug it into a personal computer instead",
                    "Keep it — finders keepers",
                ],
                "correct": 1,
                "explain": (
                    "This is a baiting attack. USB drives can silently install malware\n"
                    "  the moment they're plugged in. Never plug in unknown drives —\n"
                    "  hand them directly to security personnel."
                ),
            },
            {
                "q": "Spear phishing differs from regular phishing in that it:",
                "choices": [
                    "Uses phone calls instead of email",
                    "Targets specific individuals using personalized information",
                    "Only targets executives (whaling)",
                    "Requires physical access to the target",
                ],
                "correct": 1,
                "explain": (
                    "Spear phishing uses research (LinkedIn, social media) to craft\n"
                    "  convincing personal attacks. An email referencing your boss,\n"
                    "  your project, or recent activity is far more believable."
                ),
            },
            {
                "q": (
                    "A coworker holds the door open for you at a secure entry point\n"
                    "  without scanning their badge, saying 'my hands are full'.\n"
                    "  This is known as:"
                ),
                "choices": [
                    "Piggybacking / tailgating",
                    "Shoulder surfing",
                    "Dumpster diving",
                    "Watering hole attack",
                ],
                "correct": 0,
                "explain": (
                    "Tailgating exploits social courtesy to bypass physical security.\n"
                    "  Everyone must badge in individually — no exceptions, even if\n"
                    "  inconvenient. Politely require it and offer to assist instead."
                ),
            },
        ],
    },
    {
        "id": "crypto",
        "name": "Module 3 — Cryptography",
        "difficulty": "Hard",
        "xp": 120,
        "prereq": "social",
        "questions": [
            {
                "q": "What is the key difference between symmetric and asymmetric encryption?",
                "choices": [
                    "Symmetric is faster; asymmetric uses the same key for both parties",
                    "Symmetric uses one shared key; asymmetric uses a public/private key pair",
                    "Symmetric uses longer keys; asymmetric uses shorter keys",
                    "Symmetric only works on text; asymmetric works on any data",
                ],
                "correct": 1,
                "explain": (
                    "Symmetric (AES) uses one secret key shared between parties — fast,\n"
                    "  but key distribution is hard. Asymmetric (RSA) uses a public key\n"
                    "  to encrypt and a private key to decrypt, solving key exchange."
                ),
            },
            {
                "q": "HTTPS protects data in transit using TLS. How does TLS work?",
                "choices": [
                    "It encrypts only the login form, not the rest of the page",
                    "It uses asymmetric keys to exchange a symmetric session key,\n     then encrypts all traffic with it",
                    "It hashes all data so the server can verify it hasn't changed",
                    "It stores passwords in encrypted cookies",
                ],
                "correct": 1,
                "explain": (
                    "TLS performs a handshake using asymmetric crypto to agree on a\n"
                    "  symmetric session key. All subsequent traffic uses that fast\n"
                    "  symmetric key. Best of both worlds: security + performance."
                ),
            },
            {
                "q": "A salt is added to a password before hashing. What problem does this solve?",
                "choices": [
                    "Makes the hash shorter and faster to compute",
                    "Prevents two users with the same password from having the same hash",
                    "Allows the hash to be reversed for password recovery",
                    "Encrypts the hash so it cannot be read from the database",
                ],
                "correct": 1,
                "explain": (
                    "Without salts, two users with 'abc123' get identical hashes — crack\n"
                    "  one, crack all. A unique random salt per user ensures identical\n"
                    "  passwords produce unique hashes, defeating rainbow table attacks."
                ),
            },
            {
                "q": "Which best describes a man-in-the-middle (MITM) attack?",
                "choices": [
                    "An attacker intercepts and possibly alters communication between\n     two parties who believe they're communicating directly",
                    "An attacker floods a server with requests to bring it down",
                    "An attacker guesses a password through repeated attempts",
                    "An attacker injects malicious code into a database query",
                ],
                "correct": 0,
                "explain": (
                    "In a MITM attack the attacker secretly relays and possibly alters\n"
                    "  messages between two parties. HTTPS with certificate verification\n"
                    "  helps prevent this by authenticating the server's identity."
                ),
            },
            {
                "q": "What does a digital signature prove?",
                "choices": [
                    "That a message was encrypted before sending",
                    "That the sender is who they claim to be, and the message\n     has not been altered in transit",
                    "That the receiver's public key is valid",
                    "That the message was sent over HTTPS",
                ],
                "correct": 1,
                "explain": (
                    "A digital signature uses the sender's private key to sign a hash\n"
                    "  of the message. The receiver verifies with the public key. This\n"
                    "  proves authenticity (who sent it) and integrity (not tampered)."
                ),
            },
        ],
    },
]

SAVE_FILE = os.path.join(os.path.dirname(__file__), ".cybersec_save.json")


# ── PERSISTENCE ──────────────────────────────────────────────────────────────

def load_progress():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE) as f:
            return json.load(f)
    return {"xp": 0, "score": 0, "completed": []}


def save_progress(progress):
    with open(SAVE_FILE, "w") as f:
        json.dump(progress, f)


def reset_progress():
    if os.path.exists(SAVE_FILE):
        os.remove(SAVE_FILE)


# ── UI HELPERS ────────────────────────────────────────────────────────────────

def clear():
    print(CLEAR, end="")


def pause(msg="Press Enter to continue..."):
    input(f"\n{dim(msg)}")


def level_from_xp(xp):
    return xp // 100 + 1


def print_header(progress):
    xp    = progress["xp"]
    score = progress["score"]
    lvl   = level_from_xp(xp)
    bar_total = 20
    bar_filled = int((xp % 100) / 100 * bar_total)
    bar = "█" * bar_filled + "░" * (bar_total - bar_filled)
    print(bold("CYBERSEC ACADEMY") + dim(" — terminal edition"))
    print(hr())
    print(f"  Level {bold(str(lvl))}  [{bar}]  {xp % 100}/100 XP    Score: {bold(str(score))}")
    print(hr())
    print()


def print_module_list(progress):
    completed = progress["completed"]
    print(bold("  MODULES\n"))
    for i, mod in enumerate(MODULES):
        locked = mod["prereq"] and mod["prereq"] not in completed
        done   = mod["id"] in completed
        status = "[done]  " if done else ("[locked]" if locked else "        ")
        diff   = mod["difficulty"].ljust(8)
        xp_str = f"+{mod['xp']} XP"
        line   = f"  {i+1}. {status} {mod['name']}   {dim(diff)}  {dim(xp_str)}"
        if locked:
            print(dim(line))
        else:
            print(line)
    print()
    print(dim("  0. Reset progress"))
    print(dim("  q. Quit"))
    print()


# ── QUIZ ENGINE ───────────────────────────────────────────────────────────────

def run_quiz(mod, progress):
    questions = mod["questions"][:]
    random.shuffle(questions)

    correct_count = 0
    total = len(questions)

    for qi, q in enumerate(questions, 1):
        clear()
        print(bold(mod["name"]))
        print(hr())
        print(f"  Question {qi} of {total}\n")
        print(f"  {q['q']}\n")

        labels = ["A", "B", "C", "D"]
        for idx, choice in enumerate(q["choices"]):
            print(f"    {labels[idx]}.  {choice}")

        print()
        answer = None
        while answer not in labels[:len(q["choices"])]:
            raw = input(dim("  Your answer (A/B/C/D): ")).strip().upper()
            if raw in labels[:len(q["choices"])]:
                answer = raw
            else:
                print(dim("  Please enter A, B, C, or D."))

        chosen_idx = labels.index(answer)
        is_correct = chosen_idx == q["correct"]

        print()
        if is_correct:
            correct_count += 1
            print(f"  {bold('Correct.')}")
        else:
            correct_label = labels[q["correct"]]
            print(f"  {bold('Incorrect.')}  The answer was {bold(correct_label)}.")

        print(f"\n  {dim(q['explain'])}")
        pause()

    return correct_count, total


def show_results(mod, correct, total, progress):
    clear()
    pct    = int(correct / total * 100)
    passed = pct >= 60

    print(bold(mod["name"]))
    print(hr())
    print()
    print(f"  Result:   {bold(str(correct))}/{total} correct  ({pct}%)")
    print()

    if passed:
        xp_gain = int(mod["xp"] * pct / 100)
        progress["xp"]    += xp_gain
        progress["score"] += correct * 10
        if mod["id"] not in progress["completed"]:
            progress["completed"].append(mod["id"])
        save_progress(progress)

        print(f"  {bold('Passed.')}  +{xp_gain} XP earned.")
        if pct == 100:
            print(f"  Perfect score.")
    else:
        print(f"  {bold('Not passed.')}  60% required.  Review and retry.")

    print()
    print(hr())
    print()
    return passed


# ── MAIN LOOP ─────────────────────────────────────────────────────────────────

def main():
    progress = load_progress()

    while True:
        clear()
        print_header(progress)
        print_module_list(progress)

        choice = input(dim("  Select module: ")).strip().lower()

        if choice == "q":
            clear()
            print(dim("Goodbye.\n"))
            sys.exit(0)

        if choice == "0":
            confirm = input(dim("  Reset all progress? (yes/no): ")).strip().lower()
            if confirm == "yes":
                reset_progress()
                progress = load_progress()
            continue

        if not choice.isdigit() or int(choice) not in range(1, len(MODULES) + 1):
            continue

        mod_index = int(choice) - 1
        mod       = MODULES[mod_index]
        completed = progress["completed"]

        if mod["prereq"] and mod["prereq"] not in completed:
            print(dim(f"\n  Complete the previous module first."))
            pause()
            continue

        # Confirm start
        clear()
        print(bold(mod["name"]))
        print(hr())
        print(f"\n  Difficulty : {mod['difficulty']}")
        print(f"  Questions  : {len(mod['questions'])}")
        print(f"  XP reward  : up to {mod['xp']} XP")
        print(f"  Pass mark  : 60%\n")
        print(hr())
        go = input(dim("\n  Start? (Enter to begin, q to cancel): ")).strip().lower()
        if go == "q":
            continue

        correct, total = run_quiz(mod, progress)
        passed         = show_results(mod, correct, total, progress)

        again = input(dim("  Retry this module? (y/n): ")).strip().lower()
        if again != "y":
            pass


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(dim("\n\nInterrupted.\n"))
        sys.exit(0)
