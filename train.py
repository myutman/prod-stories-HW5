import torch
import torch.optim as optim
import torch.utils
from torch.utils.data import DataLoader

import wandb
from tqdm.notebook import tqdm

def cosine_loss(output1, output2, y1, y2):
    if y1 == y2:
        return (1 - output1.dot(output2)) / 2
    else:
        return (1 + output1.dot(output2)) / 2

def train(model, n_epochs, train_df, test_df, batch_size):
    wandb.init()
    
    adam = optim.Adam(model.parameters())
    
    for n_epoch in tqdm(range(n_epochs)): 
        train_loss = 0
        
        loader = DataLoader(list(zip(train_df["hist"], train_df["obj_name"])), batch_size=batch_size, shuffle=True)

        for batch in loader:
            batch_loss = 0
            adam.zero_grad()
            outputs = model(torch.tensor(batch[0]))
            for output1, y1 in zip(outputs, batch[1]):
                for output2, y2 in zip(outputs, batch[1]):
                    loss = cosine_loss(output1, output2, y1, y2)
                    
                    batch_loss += loss
            batch_loss /= len(batch[0])**2
            batch_loss.backward()
            adam.step()
            
            train_loss += float(batch_loss)
            wandb.log({"batch/loss": float(batch_loss)})
                    
        train_loss /= len(loader)

        test_loss = 0
        with torch.no_grad():
            for x1, y1 in zip(test_df["hist"], test_df["obj_name"]):
                for x2, y2 in zip(test_df["hist"], test_df["obj_name"]):
                    output1 = model(torch.FloatTensor(x1))
                    output2 = model(torch.FloatTensor(x2))
                    loss = cosine_loss(output1, output2, y1, y2)
                    test_loss += float(loss)
        test_loss /= len(test_df)**2

        wandb.log({"epoch/train_loss": train_loss, "epoch/valid_loss": test_loss, "epoch/epoch": n_epoch})
        
        if (n_epoch + 1) % 100 == 0:
            if not os.path.exists("checkpoints"):
                os.mkdir("checkpoints")
            torch.save(model.state_dict(), f"checkpoints/checkpoint_{model.name()}_epoch={n_epoch}_batch-size={batch_size}.cpkt")
