#!/usr/bin/env python3
"""
🔐 Password Strength Checker

A simple tool to analyze password strength and provide security recommendations.
Part of CEH Practice Tools for learning system hacking concepts.

Author: Rohith D
CEH Domain: System Hacking
"""

import re
import getpass
from colorama import Fore, Style, init

# Initialize colorama for cross-platform colored output
init(autoreset=True)

# Common weak passwords list
COMMON_PASSWORDS = [
    'password', '123456', '12345678', 'qwerty', 'abc123',
    'monkey', '1234567', 'letmein', 'trustno1', 'dragon',
    'baseball', 'iloveyou', 'master', 'sunshine', 'ashley',
    'bailey', 'passw0rd', 'shadow', '123123', '654321'
]

def check_length(password):
    """Check if password meets minimum length requirements."""
    length = len(password)
    if length < 8:
        return 0, f"{Fore.RED}✗ Too short (minimum 8 characters)"
    elif length < 12:
        return 1, f"{Fore.YELLOW}⚠ Acceptable length ({length} characters)"
    else:
        return 2, f"{Fore.GREEN}✓ Good length ({length} characters)"

def check_character_variety(password):
    """Check for variety of character types."""
    score = 0
    feedback = []
    
    if re.search(r'[a-z]', password):
        score += 1
        feedback.append(f"{Fore.GREEN}✓ Contains lowercase letters")
    else:
        feedback.append(f"{Fore.RED}✗ No lowercase letters")
    
    if re.search(r'[A-Z]', password):
        score += 1
        feedback.append(f"{Fore.GREEN}✓ Contains uppercase letters")
    else:
        feedback.append(f"{Fore.YELLOW}! Add uppercase letters")
    
    if re.search(r'\d', password):
        score += 1
        feedback.append(f"{Fore.GREEN}✓ Contains numbers")
    else:
        feedback.append(f"{Fore.YELLOW}! Add numbers")
    
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
        feedback.append(f"{Fore.GREEN}✓ Contains special characters")
    else:
        feedback.append(f"{Fore.YELLOW}! Add special characters")
    
    return score, feedback

def check_common_password(password):
    """Check if password is in common passwords list."""
    if password.lower() in COMMON_PASSWORDS:
        return 0, f"{Fore.RED}✗ This is a commonly used password!"
    return 1, f"{Fore.GREEN}✓ Not a common password"

def check_patterns(password):
    """Check for common patterns and sequences."""
    # Check for sequential numbers
    if re.search(r'(012|123|234|345|456|567|678|789)', password):
        return 0, f"{Fore.YELLOW}⚠ Contains sequential numbers"
    
    # Check for repeated characters
    if re.search(r'(.)\1{2,}', password):
        return 0, f"{Fore.YELLOW}⚠ Contains repeated characters"
    
    return 1, f"{Fore.GREEN}✓ No obvious patterns detected"

def calculate_strength(password):
    """Calculate overall password strength."""
    total_score = 0
    max_score = 10
    
    # Length check (max 2 points)
    length_score, length_msg = check_length(password)
    total_score += length_score
    
    # Character variety (max 4 points)
    variety_score, variety_msgs = check_character_variety(password)
    total_score += variety_score
    
    # Common password check (max 2 points)
    common_score, common_msg = check_common_password(password)
    total_score += common_score * 2
    
    # Pattern check (max 2 points)
    pattern_score, pattern_msg = check_patterns(password)
    total_score += pattern_score * 2
    
    return total_score, max_score, {
        'length': length_msg,
        'variety': variety_msgs,
        'common': common_msg,
        'pattern': pattern_msg
    }

def get_strength_label(score, max_score):
    """Get strength label based on score."""
    percentage = (score / max_score) * 100
    
    if percentage >= 80:
        return f"{Fore.GREEN}Strong ✓", Fore.GREEN
    elif percentage >= 60:
        return f"{Fore.YELLOW}Moderate ⚠", Fore.YELLOW
    elif percentage >= 40:
        return f"{Fore.YELLOW}Weak !", Fore.YELLOW
    else:
        return f"{Fore.RED}Very Weak ✗", Fore.RED

def print_banner():
    """Print tool banner."""
    print(f"\n{Fore.CYAN}{'='*50}")
    print(f"{Fore.CYAN}🔐  Password Strength Checker")
    print(f"{Fore.CYAN}{'='*50}")
    print(f"{Fore.WHITE}Part of CEH Practice Tools")
    print(f"{Fore.WHITE}Educational Tool - Learn Password Security\n")

def main():
    """Main function."""
    print_banner()
    
    # Get password input (hidden)
    password = getpass.getpass("Enter password to check: ")
    
    if not password:
        print(f"{Fore.RED}Error: Please enter a password!")
        return
    
    print(f"\n{Fore.CYAN}Analyzing password...\n")
    
    # Calculate strength
    score, max_score, feedback = calculate_strength(password)
    strength_label, color = get_strength_label(score, max_score)
    
    # Display results
    print(f"{Fore.CYAN}Results:")
    print(f"{Fore.CYAN}{'-'*50}")
    print(f"Strength: {strength_label}")
    print(f"Score: {color}{score}/{max_score}\n")
    
    print(f"{Fore.CYAN}Detailed Analysis:")
    print(f"{Fore.CYAN}{'-'*50}")
    print(feedback['length'])
    print(feedback['common'])
    print(feedback['pattern'])
    print(f"\n{Fore.CYAN}Character Variety:")
    for msg in feedback['variety']:
        print(f"  {msg}")
    
    # Provide recommendations
    if score < 8:
        print(f"\n{Fore.CYAN}Recommendations:")
        print(f"{Fore.CYAN}{'-'*50}")
        print(f"{Fore.YELLOW}• Use at least 12 characters")
        print(f"{Fore.YELLOW}• Mix uppercase and lowercase letters")
        print(f"{Fore.YELLOW}• Include numbers and special characters")
        print(f"{Fore.YELLOW}• Avoid common words and patterns")
        print(f"{Fore.YELLOW}• Don't use personal information")
    
    print(f"\n{Fore.GREEN}Remember: Use unique passwords for each account!")
    print(f"{Fore.GREEN}Consider using a password manager.\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}\nOperation cancelled by user.")
    except Exception as e:
        print(f"{Fore.RED}Error: {str(e)}")
