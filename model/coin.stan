data {
  int<lower=0> n;  // number of tosses
  int<lower=0> y;  // number of heads
}

transformed data {
}

parameters {
  real<lower=0, upper=1> p;
}

transformed parameters {
}

model {
  p ~ beta(2, 2);
  y ~ binomial(n, p);
}

generated quantities {
}
