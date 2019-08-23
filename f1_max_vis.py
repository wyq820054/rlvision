import numpy as np
import torch
import matplotlib.pyplot as plt
from visualization import *
from dataloader import *
import os
from PlaneDetection import PlaneDetection

pr = np.load('precision_and_recall.npz')
p = pr['precision']
r = pr['recall']

f1score = 2*(p*r)/(p+r)
f1score[np.isnan(f1score)] = 0

plt.plot(f1score)
plt.xlabel("epoch")
plt.ylabel("F1 Score")
plt.title("F1 Score Per Epoch")
plt.savefig(os.path.join("plots", "f1score.png"), bbox_inches="tight")
plt.clf()

best_model_idx = np.argmax(f1score)
best_model = \
torch.load("plane_models/target_net_{}.pt".format(best_model_idx)).to(device)

VOCtest = PlaneDetection('val')
test_loader = torch.utils.data.DataLoader(VOCtest, batch_size=1, collate_fn=default_collate)

n_items = len(VOCtest)
n_success = 0
n_actions = []

for i, [s] in enumerate(test_loader):
	vis, action_sequence = localize2(s, 100, best_model)
	n_action = len(action_sequence)
	if n_action == 100:
		print("Could not localize item {}.".format(i))
	else:
		vis.save("visualization/{}.png".format(i))
		print("Localized item {0} in {1} actions.".format(i, n_action))
		n_actions.append(n_action)
		n_success += 1

mean_actions = np.mean(n_actions)

print("Successfully localized {0} of {1} items \
with {2:.2f} average number of actions taken.".format(n_success, n_items, mean_actions))
