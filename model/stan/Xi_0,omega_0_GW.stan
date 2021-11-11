//// Xi_0,omega_0_GW.stan
// stan model file for GW events for a Ξ₀, ω₀ parametrization, using GW data

// user defined functions
functions{
  real integrand(real x, real xc, real[] theta, real[] x_r, int[] x_i) {
    // real x: function argument (integration variable)
    // real xc: complement of the function argument to avoid precision loss (not used explicitly)
    // real[] theta: array of the model parameters (e.g.: theta = {mu, sigma})
    // real[] x_r: data values used to evaluate the integral (can be null)
    // real[] x_i: integer data values used to evaluate the integral (can be null)
    real Omega_m = theta[2];
    real omega_0 = theta[3];
    return ( Omega_m*(1.0+x)^3 + (1.0-Omega_m)*((1.0+x)^(3.0*(1.0+omega_0))) )^(-0.5);
  }
}

// declare variables that will hold the data required to the model
// must match the columns for each input .csv file!
// if two file have the same columns then they will stack as one big array.
// the order of the files in the CLI must be the same as the order on which we define each data variable here
// unless we're stacking several measurements with the same column names, those can show up anywhere
data {
  int N1;
  real redshift[N1];
  real luminosity_distance[N1];
  real error[N1];
}

// define constants and transform the data
// only evaluated in the beginning of each chain
transformed data {
  // create null data values to give to integrate_1d because it's required
  real x_r[0];
  int x_i[0];
}

// declare the model parameters
// these will be sampled and optimized
parameters {
  real<lower=0> h;
  real<lower=0, upper=1> Omega_m;
  real omega_0;
  real<lower=0> Xi_0;
}

// allows new variables to be defined in terms of data and/or parameters that may be used later
// will be evaluated on each leapfrog step
transformed parameters {
  real dL[N1];
  real correction;
  real dLem;
  for (i in 1:N1) {
    correction = Xi_0 + (1.0-Xi_0) / ((1.0+redshift[i]))^(5.0/2.0);
    dLem = (1.0+redshift[i]) * (2.9979/h) * integrate_1d(integrand, 0, redshift[i], {h, Omega_m, omega_0, Xi_0}, x_r, x_i);
    dL[i] = correction * dLem;
  }
}

// likelihood and priors
// will be evaluated on each leapfrog step
model {
  // priors
  h ~ normal(0.7, 10);
  Omega_m ~ normal(0.284, 10);
  omega_0 ~ normal(-1, 10);
  Xi_0 ~ normal(1, 10);

  // likelihood for the GW
  luminosity_distance ~ normal(dL, error);
}

// allows derived quantities based on parameters, data, and rng
// is executed once per iteration
generated quantities {
}
