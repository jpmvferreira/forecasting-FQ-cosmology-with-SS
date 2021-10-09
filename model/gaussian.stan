// data provided to Stan
data {
  int n;      // number of observations
  real y[n];  // array of observations
}

// model parameters
parameters {
  real mu;
  real<lower=0> sigma;
}

// model and priors considered
model {
  // model
  for (i in 1:n)
    y[i] ~ normal(mu, sigma);

  // priors
  mu ~ normal(1, 5);
  sigma ~ normal(2, 1);
}
