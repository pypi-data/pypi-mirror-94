#### Introduction

The package py\_fractreg is a collection of functions to estimate various regression models for fractional outcomes
in the range of (0, 1). In the context of credit risk, LGD (loss given default) measures the proportion of losses 
not recovered from a default borrower. Therefore, the fractional outcome models can be useful to estimate LGD. 

```
Fractional Outcome Regressions
  |
  |-- Beta Regression
  |     |
  |     |-- beta0_reg() : Fixed Dispersion
  |     |
  |     `-- beta_reg()  : Varying Dispersion
  |
  `-- Simplex Regression
        |
        |-- simplex0_reg() : Fixed Dispersion
        |
        `-- simplex_reg()  : Varying Dispersion
```

#### Reference

WenSui Liu and Jason Xin (2014), Modeling Fractional Outcomes with SAS, Proceedings SAS Global Forum 2014, paper 1304-2014.
