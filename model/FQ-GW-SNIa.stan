// user defined functions
functions{
  real E(real z, real Omega_m) {
    return ( Omega_m*(1.0+z)^3 + (1.0-Omega_m) )^(0.5);
  }

  real integrand(real x, real xc, real[] theta, real[] x_r, int[] x_i) {
    // real x: function argument (integration variable)
    // real xc: complement of the function argument to avoid precision loss (not used explicitly)
    // real[] theta: array of the model parameters (e.g.: theta = {mu, sigma})
    // real[] x_r: data values used to evaluate the integral (can be null)
    // real[] x_i: integer data values used to evaluate the integral (can be null)
    real Omega_m = theta[2];
    return 1/E(x, Omega_m);
  }
}

// declare variables that will hold the data required to the model
// must match the columns for each input .csv file, without conflicts!
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
  real M;
}

// allows new variables to be defined in terms of data and/or parameters that may be used later
// will be evaluated on each leapfrog step
transformed parameters {
  // GW
  real dL[N1];
  real correction;
  for (i in 1:N1) {
    correction = ( (2*6^0.5 + M) / (2*6^0.5 + M/E(redshift[i], Omega_m)) )^0.5;
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
    C += 1.0/dmb[i]^2;
  }
}

// likelihood and priors
model {
  // priors
  h ~ uniform(0.2, 1.2);
  Omega_m ~ uniform(0, 1);
  M ~ uniform(-4.5, 10);

  // likelihood for the GW
  luminosity_distance ~ normal(dL, error);
  //target += -(N1/2.0)*log(2.0*pi()); // yah secalhar eh inutil pq estamos a somar uma constante...

  // likelihood for the SNIa
  target += -A + B^2/C;
}

// allows derived quantities based on parameters, data, and rng
generated quantities {
}
