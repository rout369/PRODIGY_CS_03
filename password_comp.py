import re
import math
from pyfiglet import Figlet
from termcolor import colored

def print_banner():
    f = Figlet(font='slant')
    banner = f.renderText('Password Checker')
    print(colored(banner, 'cyan'))
    print(colored("Task: 03 | Password_Complexity_Checker\n", "green"))

def estimate_entropy(password):
    charset_size = 0
    if any(c.islower() for c in password):
        charset_size += 26
    if any(c.isupper() for c in password):
        charset_size += 26
    if any(c.isdigit() for c in password):
        charset_size += 10
    if any(not c.isalnum() for c in password):
        charset_size += 32  # Approx. special characters

    if charset_size == 0:
        return 0

    entropy = len(password) * math.log2(charset_size)
    return round(entropy, 2)

def format_crack_time(seconds):
    if seconds < 1:
        return "< 1 second"
    units = [
        ("years", 60 * 60 * 24 * 365),
        ("days", 60 * 60 * 24),
        ("hours", 60 * 60),
        ("minutes", 60),
        ("seconds", 1),
    ]
    parts = []
    for name, count in units:
        value = int(seconds // count)
        if value:
            parts.append(f"{value} {name}")
            seconds %= count
    return ", ".join(parts)

def crack_time_estimation(entropy):
    guesses = 2 ** entropy
    speeds = {
        "Online Attack (~1k guesses/sec)": 1e3,
        "Offline Fast Attack (~100B guesses/sec)": 1e11
    }
    times = {}
    for method, speed in speeds.items():
        time_seconds = guesses / speed
        times[method] = format_crack_time(time_seconds)
    return times

def check_password_strength(password):
    length = len(password)
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    common_passwords = {'password', '123456', 'qwerty', 'abc123', 'letmein'}

    score = 0
    feedback = []

    if length >= 16:
        score += 3
        feedback.append("Excellent: Password length is 16 or more characters")
    elif length >= 12:
        score += 2
        feedback.append("Good: Password length is 12 or more characters")
    elif length >= 8:
        score += 1
        feedback.append("Moderate: Password length is at least 8 characters")
    else:
        feedback.append("Weak: Password is too short (less than 8 characters)")

    if has_upper:
        score += 1
        feedback.append("Good: Contains uppercase letters")
    else:
        feedback.append("Weak: No uppercase letters")

    if has_lower:
        score += 1
        feedback.append("Good: Contains lowercase letters")
    else:
        feedback.append("Weak: No lowercase letters")

    if has_digit:
        score += 1
        feedback.append("Good: Contains numbers")
    else:
        feedback.append("Weak: No numbers")

    if has_special:
        score += 1
        feedback.append("Good: Contains special characters")
    else:
        feedback.append("Weak: No special characters")

    if password.lower() in common_passwords:
        score = max(0, score - 2)
        feedback.append("Weak: Password is too common")

    if re.search(r'(.)\1{2,}', password):
        score = max(0, score - 1)
        feedback.append("Weak: Contains repeated characters (3 or more in a row)")

    keyboard_patterns = {'qwerty', 'asdf', 'zxcv', 'qazwsx'}
    for pattern in keyboard_patterns:
        if pattern in password.lower():
            score = max(0, score - 1)
            feedback.append("Weak: Contains keyboard pattern")
            break

    if score >= 7:
        strength = "Very Strong"
    elif score >= 5:
        strength = "Strong"
    elif score >= 3:
        strength = "Moderate"
    else:
        strength = "Weak"

    progress_bar = "[" + "#" * score + "-" * (8 - score) + "]"
    entropy = estimate_entropy(password)
    crack_times = crack_time_estimation(entropy)

    return {
        "strength": strength,
        "score": score,
        "feedback": feedback,
        "progress_bar": progress_bar,
        "entropy": entropy,
        "crack_times": crack_times
    }

def main():
    print_banner()
    password = input(colored("Enter a password to check: ", "yellow"))
    result = check_password_strength(password)

    print(colored(f"\nPassword Strength: {result['strength']}", "cyan"))
    print(colored(f"Score: {result['score']}/8", "cyan"))
    print(colored(f"Entropy: {result['entropy']} bits", "cyan"))
    print(colored(f"Strength Indicator: {result['progress_bar']}", "magenta"))

    print(colored("\nEstimated Crack Time:", "red"))
    for method, time in result["crack_times"].items():
        print(f"- {method}: {time}")

    print(colored("\nFeedback:", "green"))
    for item in result['feedback']:
        print(f"- {item}")

if __name__ == "__main__":
    main()
