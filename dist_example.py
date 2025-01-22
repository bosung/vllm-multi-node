import torch
import torch.distributed as dist
import torch.multiprocessing as mp
import os

def run(rank, world_size):
    dist.init_process_group(backend="nccl", rank=rank, world_size=world_size)
  
    tensor = torch.tensor(rank + 1.0)
    print(f"Rank {rank} starts with: {tensor.item()}")
    dist.all_reduce(tensor, op=dist.ReduceOp.SUM)
    print(f"Rank {rank} after all_reduce: {tensor.item()}")
  
    dist.destroy_process_group()

if __name__ == "__main__":
    world_size = 16
    mp.spawn(lambda rank: run(rank, world_size), nprocs=world_size)
