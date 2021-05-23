# Transcistor-2.0

Download and run the Python file on Command-Line.
Currently, there are four parameters required for input:
- Location of GENCODE File
- Location of FANTOM Metadata file
- Location of FANTOM/Other folder containing experimental data files corresponding to each lncrna
- Location of output csv file

Run the following help command to see description and sequence of inputs (Please input location of Python file on your local system) -
```
 python3 /Users/sanatmishra27/Desktop/GOLDLAB.py -h
```

## Filters
Only those genes which satisfy the folowing criteria are considered for evaluating the test-statistic:
- Genes on same chr. as the lncrna


## Test-statistic
<img src=
"https://render.githubusercontent.com/render/math?math=%5Clarge+%5Cdisplaystyle+%5Cbegin%7Balign%2A%7D%0ATest+Stat+%26%3D+%5Cfrac%7B1%7D%7Bn%7D+%5Csum_%7Bi%3D1%7D%5E%7Bn%7D+%5Cfrac%7B1%7D%7Bd_i%5Ea%7D+%5C%5C%0A%5Cend%7Balign%2A%7D%0A" 
alt="\begin{align*}
Test Stat &= \frac{1}{n} \sum_{i=1}^{n} \frac{1}{d_i^a} \\
\end{align*}
"> \
where 
- n = Number of genes that pass the filters 
- d = Distance of gene from UMLILO 
- a = Exponent (Set as 1)

