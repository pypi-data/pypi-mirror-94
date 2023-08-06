# high_dimensional_density
HighDim is a numerical package for computing the marginal density distribution. The algorithm is inspired by the paper: [High-Dimensional Probability Estimation with Deep Density Models](https://arxiv.org/abs/1302.5125). This originally applied to verify the distribution of output of machine learning. The authors proposed the algorithm which mapped the complex high dimensional data into Dirichlet distribution. This approach preserve the number of dimension and gives us known and identical marginal density function. 

The proof for the approach is in here: [High-dimensional probability estimation for empirical data](https://github.com/liyo6397/high_dimensional_density/blob/master/docs/introduction.pdf)



## Installation
```
pip install HighDim
```
## Usage
```python
 #The domain of high dimensional data
 data = np.random.rand(100, 10)

 # The marginal density distribution of x
 x = 0.3

 # The marginal density distribution of x for each dimension
 density = marginal_density(data, x)

 print(density)
 # [1.24974725e-119 2.12110416e-067 1.61715010e-097 5.76937215e-109
 # 1.63627432e-091 1.72724426e-126 1.49437302e-091 6.77392214e-064
 # 1.45718278e-120 3.84252945e-082]
```
