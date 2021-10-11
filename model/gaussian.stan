// data provided to Stan
data {
  int N;      // number of observations
  real y[N];  // array of observations
}

// model parameters
parameters {
  real mu;
  real<lower=0> sigma;
}

// likelihood and priors considered
model {
  // likelihood
  for (i in 1:N)
    y[i] ~ normal(mu, sigma);

  // priors
  mu ~ normal(1, 5);
  sigma ~ normal(2, 1);
}
