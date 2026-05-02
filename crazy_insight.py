NUM_ITERATIONS = 10000

acc = 0.96


# generate a random sample of 1000 numbers, where 960 of them are 1 and 40 of them are 0
import random
def generate_sample():
    sample = [1] * 960 + [0] * 40
    random.shuffle(sample)
    return sample

labels = generate_sample()

history = []

for i in range(NUM_ITERATIONS):
    # randomly shuffle the labels
    random.shuffle(labels)
    
    # calculate the accuracy of the model (which predicts 1 with 96% chance and 0 with 4% chance)
    correct_predictions = 0
    for label in labels:
        if label == 1:
            if random.random() < acc:
                correct_predictions += 1
        else:
            if random.random() < (1 - acc):
                correct_predictions += 1

    accuracy = correct_predictions / len(labels)
    history.append(accuracy)
    print(f"Iteration {i+1}: Accuracy = {accuracy:.4f}")

print(f"Average Accuracy: {sum(history)/len(history):.4f}")