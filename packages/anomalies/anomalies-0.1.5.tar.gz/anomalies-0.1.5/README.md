# Anomalies
Implement the anomaly free solution of  [arXiv:1905.13729](https://arxiv.org/abs/1905.13729) [PRL]:

Obtain a numpy array `z` of `N` integers which satisfy the Diophantine equations
```python
>>> z.sum()
0
>>> (z**3).sum()
0
```
The input is two lists `l` and `k` with any `(N-3)/2` and `(N-1)/2` integers for `N` odd, or `N/2-1` and `N/2-1` for `N` even (`N>4`).
The function is implemented below under the name: `free(l,k)`

## Install
```bash
$ pip install anomalies
```
## USAGE
```python
>>> from anomalies import anomaly
>>> anomaly.free([-1,1],[4,-2])
array([  3,   3,   3, -12, -12,  15])
>>> anomaly.free.gcd
3
>>> anomaly.free.simplified
array([ 1,  1,  1, -4, -4,  5])
```
