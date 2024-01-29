# Coiled memo

## Setup

```bash
coiled setup gcp --region europe-west1
```
Note that the default Coiled instance type (e2-standard-4) has 4 vCPUs, so a 10 worker cluster (plus scheduler) would require 44 vCPUs, 440 GB Persistent Disk SSD, and 11 IP addresses. │

## Usage

### Create a cluster

```python
import coiled
from dask.distributed import Client
```

#### CPU cluster

Smallest cluster possible:
```python
cluster = coiled.Cluster(n_workers=1, 
                         name='test-simple', 
                         scheduler_vm_types=['n1-standard-1'],                       
                         worker_vm_types=['n1-standard-1'],
                         scheduler_options={"idle_timeout": "1 hours"},
                         shutdown_on_close=False,
                         use_best_zone=True, 
                         spot_policy="spot_with_fallback",
                        )
```

Same scheduler but more workers:
```python 
cluster = coiled.Cluster(n_workers=4, 
                         name='test-larger', 
                         scheduler_vm_types=['n1-standard-1'],   
                         worker_vm_types=['n1-standard-1'], 
                         scheduler_options={"idle_timeout": "1 hours"},
                         shutdown_on_close=False,
                         use_best_zone=True, 
                         spot_policy="spot_with_fallback",
                        )
```

Cluster optimised to use all possible ressources within the free GCP quotas:
```python 
cluster = coiled.Cluster(n_workers=5, 
                         name='free-large', 
                         scheduler_vm_types=['n1-standard-2'],   
                         worker_vm_types=['e2-standard-4'],
                         scheduler_options={"idle_timeout": "1 hours"},
                         shutdown_on_close=False,
                         use_best_zone=True, 
                         spot_policy="spot_with_fallback",
                         #software='ds2-coiled',
                        )
```

With GCP free trial, quotas allows for 24 VM instances, 8 T2D vCPUs, 500Gb of SSD, 5 networks, 32 vCPUs (all regions)...

All Compute Engine API quota details [here](https://console.cloud.google.com/apis/api/compute.googleapis.com/quotas?project=ds2-2024).


### Cluster (re)use for Dask
If you want to (re)use an existing cluster from anywhere, call it by its name:

```python
cluster = coiled.Cluster(name="test-simple")
```

And to use with Dask, you need the client:
```python
client = cluster.get_client()
```

### VM Types
How to know keywords to use for VM types ?


```python
def sizeof_fmt(num, suffix="B"):
    for unit in ("Mi", "Gi", "Ti", "Pi", "Ei", "Zi"):
        if abs(num) < 1024.0:
            return f"{num:3.1f}{unit}{suffix}"
        num /= 1024.0
    return f"{num:.1f}Yi{suffix}"
    
l = coiled.list_instance_types(backend="gcp", cores=[8])
for i in l:
    print("%20s: vCPU=%i, MEM=%8s, GPU=%i, " % (i, l[i]['cores'], sizeof_fmt(l[i]['memory']), l[i]['gpus']))
```

More details from GCP: https://cloud.google.com/compute/docs/general-purpose-machines

### Software Environment

```python
coiled.create_software_environment(
    name="ds2-coiled",
    conda="/Users/gmaze/git/github/obidam/ds2-2024/practice/environment/coiled/environment-coiled.yml",
)
```


### Jupyter notebook

```bash
coiled notebook start --sync --idle-timeout '1 hour' --vm-type n1-standard-1 --name notebook --software ds2-coiled
```

### Using DS2 GCP project:

The quota is of 72 CPUs in us-east1 region. So, if we use 2 CPUs for the scheduler, we're left with 70 CPUs to be distributed among the workers. That's gibing us the choice of using few VMs with a lot of CPUs, or a lot of VMs with a few CPUs.

A lot of workers with only 2 CPUs/core:
```python 
cluster = coiled.Cluster(n_workers=35, 
                         name='ds2-cluster', 
                         scheduler_vm_types=['n1-standard-2'],   
                         worker_vm_types=['n1-standard-2'],
                         scheduler_options={"idle_timeout": "1 hours"},
                         shutdown_on_close=False,
                         use_best_zone=True, 
                         spot_policy="spot_with_fallback",
                        )

cluster = coiled.Cluster(n_workers=10, 
                         name='ds2-cluster', 
                         scheduler_vm_types=['n1-standard-2'],   
                         worker_vm_types=['n1-standard-2'],
                         scheduler_options={"idle_timeout": "1 hours"},
                         shutdown_on_close=False,
                         use_best_zone=True, 
                         spot_policy="spot_with_fallback",
                        )
```

Or a few workers with a lot of CPUs:
```python 
cluster = coiled.Cluster(n_workers=2, 
                         name='ds2-cluster', 
                         scheduler_vm_types=['n1-standard-2'],   
                         worker_vm_types=['n1-standard-32'],
                         scheduler_options={"idle_timeout": "1 hours"},
                         shutdown_on_close=False,
                         use_best_zone=True, 
                         spot_policy="spot_with_fallback",
                        )
```

Performances should depend on the kind of tasks submitted to these clusters.


A Cluster of 8 GPUs-VM workers, providing 8*8=64 CPUs:
```python 
cluster = coiled.Cluster(n_workers=8, 
                         name='ds2-cluster-gpu', 
                         scheduler_vm_types=['n1-standard-2'],   
                         worker_vm_types=['g2-standard-8'],
                         scheduler_options={"idle_timeout": "1 hours"},
                         shutdown_on_close=False,
                         use_best_zone=True, 
                         spot_policy="spot_with_fallback",
                        )
```


# Computation examples
```python
def inc(x):
    return x + 1
future = client.submit(inc, 10)
future.result() # returns 11
```

```python
import dask.array as da
x = da.random.normal(10, 0.1, size=(20000,20000), chunks= (1000,1000))
y = x.mean(axis=0)[::100]
y.compute();
```

