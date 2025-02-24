import torch
import torch.distributed as dist
import os

def main():
    # Get environment variables for multi-node setup
    local_rank = int(os.environ["LOCAL_RANK"])
    rank = int(os.environ["RANK"])
    world_size = int(os.environ["WORLD_SIZE"])
    
    # Initialize process group
    dist.init_process_group("nccl")
    
    # Move to GPU
    device = torch.device(f"cuda:{local_rank}")
    
    print(f"Running on node rank {rank} (local_rank: {local_rank}) out of {world_size} processes")
    
    # Test broadcast
    if rank == 0:
        tensor = torch.randn(3, 3).to(device)
    else:
        tensor = torch.empty(3, 3).to(device)
    
    print(f"Before broadcast, rank {rank}:", tensor)
    dist.broadcast(tensor, src=0)
    print(f"After broadcast, rank {rank}:", tensor)
    
    # Test all_gather
    local_tensor = torch.ones(2, 2).to(device) * (rank + 1)
    gathered_list = [torch.empty_like(local_tensor).to(device) for _ in range(world_size)]
    dist.all_gather(gathered_list, local_tensor)
    print(f"Rank {rank} gathered tensors:", gathered_list)
    
    # Test reduce
    value = torch.tensor([rank + 1.0]).to(device)
    dist.reduce(value, dst=0, op=dist.ReduceOp.SUM)
    if rank == 0:
        print(f"Rank 0 got sum: {value.item()}")
    
    # Test all_reduce
    local_value = torch.tensor([rank + 1.0]).to(device)
    dist.all_reduce(local_value, op=dist.ReduceOp.SUM)
    print(f"Rank {rank} got all_reduced sum: {local_value.item()}")
    
    dist.destroy_process_group()

if __name__ == "__main__":
    main()
