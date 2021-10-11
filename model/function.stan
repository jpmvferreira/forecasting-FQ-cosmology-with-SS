// user defined functions
functions{
  real normal_density(real x, real xc, real[] theta, real[] x_r, int[] x_i) {
    // real x: function argument (integration variable)
    // real xc: complement of the function argument to avoid precision loss (not used explicitly)
    // real[] theta: array of the model parameters (e.g.: theta = {mu, sigma})
    // real[] x_r: ?
    // real[] x_i: ?

    real mu = theta[1];
    real sigma = theta[2];
    return 1 / (sqrt(2 * pi()) * sigma) * exp(-0.5 * ((x - mu) / sigma)^2);
  }
}

// data provided to stan
data {
  int n;
  real y[n];
}

// ?
transformed data {
  real x_r[0];
  int x_i[0];
}

// model parameters
parameters {
  real mu;
  real<lower = 0> sigma;
}

// likelihood and priors
model {
  // priors
  mu ~ normal(1, 5);
  sigma ~ normal(2, 1);

  // likelihood
  target += normal_lpdf(y | mu, sigma);
  target += log(integrate_1d(normal_density, -10, 10, {mu, sigma}, x_r, x_i));
}
