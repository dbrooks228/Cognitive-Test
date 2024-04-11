import time
import random
import pyttsx3
from colorama import init, Fore

init(autoreset=True)
engine = pyttsx3.init()
results = {}

def run_pasat(test_length=15, interval=3):
    print("\nStarting PASAT Test:")
    previous_number = 0
    correct_answers = 0
    response_times = []

    for i in range(test_length):
        current_number = random.randint(1, 20)
        print(f"Number {i+1}/{test_length}: {current_number}")
        start_time = time.time()
        user_input = int(input("Enter the sum: "))
        end_time = time.time()

        correct_sum = current_number + previous_number
        if user_input == correct_sum:
            print("Correct!")
            correct_answers += 1
        else:
            print(f"Incorrect. The correct sum was: {correct_sum}")
        
        response_time = end_time - start_time
        response_times.append(response_time)
        previous_number = current_number

        time.sleep(max(0, interval - response_time))  # Adjusting time to maintain interval consistency

    avg_response_time = sum(response_times) / len(response_times)
    results['PASAT'] = {'Correct Answers': correct_answers, 'Average Response Time': avg_response_time}
    print("PASAT Test Complete.\n")

def run_digit_span():
    level = 2  # Start with 2 numbers
    while level <= 9:  # Limiting to 9 for practical purposes
        digits = [random.randint(1, 9) for _ in range(level)]
        engine.say(' '.join(map(str, digits)))
        engine.runAndWait()

        forward_input = list(map(int, input("Enter the digits in order you heard: ").split()))
        if forward_input != digits:
            break

        backward_input = list(map(int, input("Now enter them in reverse order: ").split()))
        if backward_input != digits[::-1]:
            break
        
        level += 1  # Increase the level by adding one more digit

    results['Digit Span'] = {'Max Forward Level': len(forward_input), 'Max Backward Level': len(backward_input)}
    print("Digit Span Test Complete.\n")

def run_stroop(test_length=10, delay=1):
    print("\nStarting Stroop Test:")
    colors = ['red', 'green', 'blue', 'yellow']
    color_codes = {'red': Fore.RED, 'green': Fore.GREEN, 'blue': Fore.BLUE, 'yellow': Fore.YELLOW}
    words = [random.choice(colors) for _ in range(test_length)]
    inks = [random.choice(colors) for _ in range(test_length)]
    correct_answers = 0
    response_times = []

    for word, ink in zip(words, inks):
        print(color_codes[ink] + word)
        start_time = time.time()
        response = input("Type the color of the ink, not the word: ").strip().lower()
        response_time = time.time() - start_time

        if response == ink:
            correct_answers += 1
        response_times.append(response_time)
        time.sleep(delay)

    results['Stroop Test'] = {
        'Correct Answers': correct_answers,
        'Response Times': response_times,
        'Average Response Time': sum(response_times) / len(response_times)
    }
    print("Stroop Test Complete.\n")

def save_results():
    with open('cognitive_test_results.json', 'w') as file:
        json.dump(results, file, indent=4)
    print("Results saved to 'cognitive_test_results.json'.")

# Running all tests
run_pasat()
run_digit_span()
run_stroop()
save_results()

# Printing results
for test_name, scores in results.items():
    print(f"{test_name} Results: {scores}\n")
