//// FQ_GW_SNIa.stan
// stan model file for GW events and SNIa data, for a single parameter F(Q) modified gravity model that mimics a ΛCDM background

// user defined functions
functions{
  real Einverse(real z, real Omega_m) {
    return ( Omega_m*(1.0+z)^3 + (1.0-Omega_m) )^(-0.5);
  }

  real integrand(real x, real xc, real[] theta, real[] x_r, int[] x_i) {
    // real x: function argument (integration variable)
    // real xc: complement of the function argument to avoid precision loss (not used explicitly)
    // real[] theta: array of the model parameters (e.g.: theta = {mu, sigma})
    // real[] x_r: data values used to evaluate the integral (can be null)
    // real[] x_i: integer data values used to evaluate the integral (can be null)
    real Omega_m = theta[2];
    return Einverse(x, Omega_m);
  }
}

// declare variables that will hold the data required to the model
// must match the columns for each input .csv file!
// if two file have the same columns then they will stack as one big array.
// the order of the files in the CLI must be the same as the order on which we define each data variable here
// unless we're stacking several measurements with the same column names, those can show up anywhere
data {
  // observations for gravitational waves
  int N1;
  real redshift[N1];
  real luminosity_distance[N1];
  real error[N1];

  // observations for SNIa
  int N2;
  real zcmb[N2];
  real mb[N2];
  real dmb[N2];
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
  real<lower=-2*6^0.5> M;
}

// allows new variables to be defined in terms of data and/or parameters that may be used later
// will be evaluated on each leapfrog step
transformed parameters {
  // GW
  real dL[N1];
  real correction;
  for (i in 1:N1) {
    correction = ( (2*6^0.5 + M) / (2*6^0.5 + M*Einverse(redshift[i], Omega_m)) )^0.5;
    dL[i] = correction * (1.0 + redshift[i]) * (2.9979/h) * integrate_1d(integrand, 0, redshift[i], {h, Omega_m, M}, x_r, x_i);
  }

  // SNIa
  real Delta[N2];
  real A = 0;
  real B = 0;
  real C = 0;
  for (i in 1:N2) {
    Delta[i] = mb[i] - 5.0*log10((1.0+zcmb[i]) * integrate_1d(integrand, 0, zcmb[i], {h, Omega_m, M}, x_r, x_i));
    A += (Delta[i]/dmb[i])^2;
    B += Delta[i]/dmb[i]^2;
    C += dmb[i]^(-2);
  }
}

// likelihood and priors
// will be evaluated on each leapfrog step
model {
  // priors
  h ~ normal(0.7, 10);
  Omega_m ~ normal(0.284, 10);
  M ~ normal(0, 5);

  // likelihood for the GW
  luminosity_distance ~ normal(dL, error);

  // likelihood for the SNIa
  target += -A + B^2/C;
}

// allows derived quantities based on parameters, data, and rng
// is executed once per iteration
generated quantities {
}
