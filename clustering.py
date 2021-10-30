import torch


def get_cluster_centers(train_df, model):
    centers = dict()
    for key, subdf in train_df.groupby(by=["obj_name"]):
        embeddings = model(torch.stack(list(subdf["hist"])))
        center = embeddings.sum(dim=0)
        center /= center.norm()
        centers[key] = center
    return centers


def cosine_dist(output1, output2):
    return (1 - output1.dot(output2)) / 2