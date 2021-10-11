// user defined functions
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

// declare variables that will hold the data required to the model
// must match the columns in the input .csv file!
data {
  int N;  // number of observations must always be N
  real redshift[N];
  real luminosity_distance[N];
  real error[N];
}

// define constants and transform the data
// only evaluated once upon reading the data
transformed data {
  // create null data values used to integrate the integral
  real x_r[0];
  int x_i[0];
}

// declare the model parameters
// these will be sampled and optimized
parameters {
  real<lower=0> h;
  real<lower = 0, upper=1> Omega_m;
}

// allows new variables to be defined in terms of data and/or parameters that may be used later
// will be evaluated on each leapfrog step
transformed parameters {
  real dL[N];
  for (i in 1:N) {
    dL[i] = (1.0 + redshift[i]) * (2.9979/h) * integrate_1d(integrand, 0, redshift[i], {h, Omega_m}, x_r, x_i);
  }
}

// likelihood and priors
model {
  // priors
  h ~ normal(0.7, 0.1);
  Omega_m ~ normal(0.284, 0.1);

  // likelihood
  // expressed in vector form to allow for vectorization
  luminosity_distance ~ normal(dL, error);
}

// allows derived quantities based on parameters, data, and rng
generated quantities {
}
