// user defined functions
// (declarations and definitions)
functions{
  real integrand(real x, real xc, real[] theta, real[] x_r, int[] x_i) {
    // real x: function argument (integration variable)
    // real xc: complement of the function argument to avoid precision loss (not used explicitly)
    // real[] theta: array of the model parameters (e.g.: theta = {mu, sigma})
    // real[] x_r: data values used to evaluate the integral (can be null)
    // real[] x_i: integer data values used to evaluate the integral (can be null)

    real mu = theta[1];
    real sigma = theta[2];
    return mu;
  }
}

// declare data required to the model
// read for external input
// (declarations)
data {
  int n;
  real y[n];
}

// define constants and transform the data
// only evaluated once upon reading the data
// (declarations and statements)
transformed data {
  // create null data values used to integrate the integral
  real x_r[0];
  int x_i[0];
}

// declare the model parameters (what's going to be sampled and optimized)
// (declarations)
parameters {
  real mu;
  real<lower = 0> sigma;
}

// allows variables to be defined in terms of data and/or parameters that may be used later and will be saved
// will be evaluated on each leapfrog step
// (declarations and statements)
transformed parameters {
  real mu2;
  mu2 = integrate_1d(integrand, 0, 2, {mu, sigma}, x_r, x_i);
}

// likelihood and priors
// (declarations and statements)
model {
  // priors
  mu ~ normal(1, 5);
  sigma ~ normal(2, 1);

  // likelihood
  for (i in 1:n)
    y[i] ~ normal(mu2, sigma);
}

// allows derived quantities based on parameters, data, and rng
// (declarations and statements)
generated quantities {
}
