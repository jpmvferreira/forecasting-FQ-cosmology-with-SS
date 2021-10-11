// user defined functions
// (declarations and definitions)
functions{
  real integrand(real x, real xc, real[] theta, real[] x_r, int[] x_i) {
    // real x: function argument (integration variable)
    // real xc: complement of the function argument to avoid precision loss (not used explicitly)
    // real[] theta: array of the model parameters (e.g.: theta = {mu, sigma})
    // real[] x_r: data values used to evaluate the integral (can be null)
    // real[] x_i: integer data values used to evaluate the integral (can be null)

    real h = theta[1];
    real Omega_m = theta[2];
    return ( Omega_m*(1+x)^3 + (1-Omega_m) )^(-0.5);
  }
}

// declare data required to the model
// read for external input
// (declarations)
data {
  int n;
  real redshift[n];
  real luminosity_distance[n];
  real error[n];
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
  real<lower=0> h;
  real<lower = 0, upper=1> Omega_m;
}

// allows variables to be defined in terms of data and/or parameters that may be used later and will be saved
// will be evaluated on each leapfrog step
// (declarations and statements)
transformed parameters {
  real dL[n];
  for (i in 1:n) {
    dL[i] = (1.0 + redshift[i]) * (2.9979/h) * integrate_1d(integrand, 0, redshift[i], {h, Omega_m}, x_r, x_i);
  }
}

// likelihood and priors
// (declarations and statements)
model {
  // priors
  h ~ normal(0.7, 0.1);
  Omega_m ~ normal(0.284, 0.1);

  // likelihood
  luminosity_distance ~ normal(dL, error);
}

// allows derived quantities based on parameters, data, and rng
// (declarations and statements)
generated quantities {
}
