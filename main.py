import streamlit as st
import re
import string
import math

# Set page configuration
st.set_page_config(
    page_title="Password Strength Meter",
    page_icon="🔒",
    layout="centered"
)

# Add custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1E88E5;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #424242;
        margin-bottom: 1rem;
    }
    .strength-meter {
        margin-top: 20px;
        margin-bottom: 20px;
    }
    .feedback-container {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        margin-top: 20px;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        color: #9e9e9e;
        font-size: 0.8rem;
    }
    .weak {
        color: #f44336;
        font-weight: bold;
    }
    .medium {
        color: #ff9800;
        font-weight: bold;
    }
    .strong {
        color: #4caf50;
        font-weight: bold;
    }
    .very-strong {
        color: #2e7d32;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Title and description
st.markdown("<h1 class='main-header'>Password Strength Meter</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Check how strong your password is</p>", unsafe_allow_html=True)

# Common passwords list (abbreviated for demonstration)
common_passwords = [
    "password", "123456", "12345678", "qwerty", "abc123", "monkey", "1234567", 
    "letmein", "trustno1", "dragon", "baseball", "111111", "iloveyou", "master", 
    "sunshine", "ashley", "bailey", "passw0rd", "shadow", "123123", "654321", 
    "superman", "qazwsx", "michael", "football", "welcome", "jesus", "ninja", 
    "mustang", "password1", "123456789", "adobe123", "admin", "1234567890"
]

# Function to calculate password entropy
def calculate_entropy(password):
    # Calculate the character set size
    char_set_size = 0
    if any(c.islower() for c in password):
        char_set_size += 26
    if any(c.isupper() for c in password):
        char_set_size += 26
    if any(c.isdigit() for c in password):
        char_set_size += 10
    if any(c in string.punctuation for c in password):
        char_set_size += len(string.punctuation)
    
    # If we couldn't determine the character set, default to 26 (lowercase letters)
    if char_set_size == 0:
        char_set_size = 26
    
    # Calculate entropy
    entropy = math.log2(char_set_size) * len(password)
    return entropy

# Function to evaluate password strength
def evaluate_password(password):
    # Initialize score and feedback
    score = 0
    feedback = []
    
    # Check if password is empty
    if not password:
        return 0, ["Please enter a password."]
    
    # Check if password is in common passwords list
    if password.lower() in common_passwords:
        return 0, ["This is a commonly used password and can be easily guessed."]
    
    # Check length
    if len(password) < 8:
        feedback.append("Password is too short. Use at least 8 characters.")
    elif len(password) >= 12:
        score += 2
    else:
        score += 1
    
    # Check for character variety
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("Add uppercase letters (A-Z).")
    
    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Add lowercase letters (a-z).")
    
    if re.search(r'[0-9]', password):
        score += 1
    else:
        feedback.append("Add numbers (0-9).")
    
    if re.search(r'[^A-Za-z0-9]', password):
        score += 1
    else:
        feedback.append("Add special characters (!@#$%^&*...).")
    
    # Check for sequential characters
    if re.search(r'(abc|bcd|cde|def|efg|fgh|ghi|hij|ijk|jkl|klm|lmn|mno|nop|opq|pqr|qrs|rst|stu|tuv|uvw|vwx|wxy|xyz|012|123|234|345|456|567|678|789|890)', password.lower()):
        score -= 1
        feedback.append("Avoid sequential characters (abc, 123, etc.).")
    
    # Check for repeated characters
    if re.search(r'(.)\1{2,}', password):
        score -= 1
        feedback.append("Avoid repeated characters (aaa, 111, etc.).")
    
    # Calculate entropy and adjust score
    entropy = calculate_entropy(password)
    if entropy > 80:
        score += 2
    elif entropy > 60:
        score += 1
    
    # Ensure score is within bounds
    score = max(0, min(score, 6))
    
    # If score is good but no feedback, add positive feedback
    if score >= 4 and not feedback:
        feedback.append("Great password! It's strong and secure.")
    elif score >= 2 and not feedback:
        feedback.append("Good password, but could be stronger with more variety.")
    
    return score, feedback

# Password input
password = st.text_input("Enter your password:", type="password")

# Evaluate password when entered
if password:
    score, feedback = evaluate_password(password)
    
    # Display strength meter
    st.markdown("<div class='strength-meter'>", unsafe_allow_html=True)
    
    # Determine strength category
    if score <= 1:
        strength = "Weak"
        color = "weak"
        progress_color = "red"
    elif score <= 3:
        strength = "Medium"
        color = "medium"
        progress_color = "orange"
    elif score <= 5:
        strength = "Strong"
        color = "strong"
        progress_color = "green"
    else:
        strength = "Very Strong"
        color = "very-strong"
        progress_color = "green"
    
    # Display strength label
    st.markdown(f"<h3>Password Strength: <span class='{color}'>{strength}</span></h3>", unsafe_allow_html=True)
    
    # Display progress bar
    normalized_score = score / 6  # Normalize to 0-1 range
    st.progress(normalized_score)
    
    # Display entropy
    entropy = calculate_entropy(password)
    st.markdown(f"<p>Entropy: {entropy:.2f} bits</p>", unsafe_allow_html=True)
    
    # Display strength explanation
    st.markdown("<p>Strength explanation:</p>", unsafe_allow_html=True)
    st.markdown("""
    - <span class='weak'>Weak</span>: Easy to guess. Vulnerable to brute force attacks.
    - <span class='medium'>Medium</span>: Somewhat difficult to guess. Could resist simple attacks.
    - <span class='strong'>Strong</span>: Difficult to guess. Can withstand most attacks.
    - <span class='very-strong'>Very Strong</span>: Extremely difficult to guess. Highly secure.
    """, unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Display feedback
    if feedback:
        st.markdown("<div class='feedback-container'>", unsafe_allow_html=True)
        st.markdown("<h3>Feedback:</h3>", unsafe_allow_html=True)
        for item in feedback:
            st.markdown(f"- {item}", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)

# Password tips
with st.expander("Tips for creating strong passwords"):
    st.markdown("""
    ### Password Best Practices
    
    1. **Use at least 12 characters**: Longer passwords are generally more secure.
    
    2. **Mix character types**: Include uppercase letters, lowercase letters, numbers, and special characters.
    
    3. **Avoid personal information**: Don't use names, birthdays, or other personal details.
    
    4. **Don't use common patterns**: Avoid keyboard patterns (qwerty), sequential numbers (123456), or repeated characters (aaa).
    
    5. **Use unique passwords**: Don't reuse passwords across different accounts.
    
    6. **Consider using a passphrase**: A series of random words can be both secure and memorable.
    
    7. **Use a password manager**: Tools like LastPass, 1Password, or Bitwarden can generate and store strong passwords.
    """)

# Add footer
st.markdown("<div class='footer'>Created with Streamlit</div>", unsafe_allow_html=True)