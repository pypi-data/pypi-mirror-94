# igwp - Improved Global Warming Potential (IGWP)
> A Global Warming Potential model with improved support for short-lived climate pollutions (SLCPs).


## Why an improved version

The Global Warming Potential (GWP) is a commonly used, simple model
to "normalize" the warming impact of different climate pollutants to 
$CO_2$ equivalents. This approach works well for long-lived climate 
pollutants (LLCPs) but fails for short-lived climate pollutants (SLCPs).
The improved version IGWP accounts much better for impacts of SLCPs.

## Scientific background

This project:

* is based on the findings in this paper: 
  Cain, M., Lynch, J., Allen, M.R., Fuglestedt, D.J. & Macey, A.H. (2019).
  Improved calculation of warming- equivalent emissions for short-lived 
  climate pollutants. npj Climate and Atmospheric Science. 2(29). 
  Retrieved from https://www.nature.com/articles/s41612-019-0086-4

* inspired by: 
  https://gitlab.ouce.ox.ac.uk/OMP_climate_pollutants/co2-warming-equivalence/

* and uses the simple emissions-based impulse response and carbon cycle 
  model FaIR: https://github.com/OMS-NetZero/FAIR
  
### The maths

{% raw %}
$$IGWP = GWP_H * (r * \frac{\Delta E_{SLCP}}{\Delta t} * H + s * E_{SLCP})$$
{% endraw %}

with:

* $IGWP$ - Improved Global Warming Potential
* $GWP_H$ - Global Warming Potential for period $H$ (e.g. $GWP_{100}$ for 100 years)
* $H$ time-horizon (commonly 100 years)
* $r$ - flow term faction, found to be 0.75 with linear regression
* $s$ - stock term fraction, found to be 0.25 with linear regression, condition: $r + s = 1$ 
* $\Delta E_{SLCP}$ - change of rate of short-lived climate pollutant
* ${\Delta t}$ - time difference for $\Delta E_{SLCP}$, typical value: 20 years
* $E_{SLCP}$ emission short-lived climate pollutant for investigated year

## Install

With `pip`:

    pip install igwp
    
With `conda`:

    conda instal -c hydrocomputing igwp

## Plot all results

This plots shows the differences between GWP, GWP*, and IGWP.

```python
from igwp.core import get_emission_data_paths, make_gwps_improved
from igwp.plotting import plot_all

rcp_scenarios = get_emission_data_paths()

plot_all(rcp_scenarios, make_df=make_gwps_improved)
```


![png](docs/images/output_4_0.png)


This plot reproduces the Fig.1 in the paper descriobung IGWP (although with this name, https://www.nature.com/articles/s41612-019-0086-4).

## Show some values

The results for the emissions based on GWP, GWP*, and IGWP for scenario RCP 2.6 for the years 2000 through 2020:

```python
from igwp.core import make_gwps_improved

paths = get_emission_data_paths()

df26 = make_gwps_improved(file_name=paths['RCP 2.6'])
df26.loc[2000:2020]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>$CH_4$ GWP</th>
      <th>$CH_4$ GWP*</th>
      <th>$CH_4$ IGWP</th>
    </tr>
    <tr>
      <th>Years</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2000</th>
      <td>8.405793</td>
      <td>-0.896435</td>
      <td>1.429122</td>
    </tr>
    <tr>
      <th>2001</th>
      <td>8.495458</td>
      <td>-0.924463</td>
      <td>1.430517</td>
    </tr>
    <tr>
      <th>2002</th>
      <td>8.584206</td>
      <td>-0.957068</td>
      <td>1.428251</td>
    </tr>
    <tr>
      <th>2003</th>
      <td>8.672059</td>
      <td>-0.994154</td>
      <td>1.422399</td>
    </tr>
    <tr>
      <th>2004</th>
      <td>8.759072</td>
      <td>-1.035440</td>
      <td>1.413188</td>
    </tr>
    <tr>
      <th>2005</th>
      <td>8.845276</td>
      <td>-1.080772</td>
      <td>1.400740</td>
    </tr>
    <tr>
      <th>2006</th>
      <td>8.961719</td>
      <td>-0.974904</td>
      <td>1.509252</td>
    </tr>
    <tr>
      <th>2007</th>
      <td>9.077956</td>
      <td>-0.870071</td>
      <td>1.616936</td>
    </tr>
    <tr>
      <th>2008</th>
      <td>9.193784</td>
      <td>-0.767278</td>
      <td>1.722987</td>
    </tr>
    <tr>
      <th>2009</th>
      <td>9.309613</td>
      <td>-0.664485</td>
      <td>1.829040</td>
    </tr>
    <tr>
      <th>2010</th>
      <td>9.425441</td>
      <td>-0.561693</td>
      <td>1.935091</td>
    </tr>
    <tr>
      <th>2011</th>
      <td>9.201847</td>
      <td>-1.113669</td>
      <td>1.465210</td>
    </tr>
    <tr>
      <th>2012</th>
      <td>8.978253</td>
      <td>-1.665646</td>
      <td>0.995329</td>
    </tr>
    <tr>
      <th>2013</th>
      <td>8.754659</td>
      <td>-2.217622</td>
      <td>0.525448</td>
    </tr>
    <tr>
      <th>2014</th>
      <td>8.531065</td>
      <td>-2.769599</td>
      <td>0.055567</td>
    </tr>
    <tr>
      <th>2015</th>
      <td>8.307471</td>
      <td>-3.321576</td>
      <td>-0.414314</td>
    </tr>
    <tr>
      <th>2016</th>
      <td>8.083877</td>
      <td>-3.873554</td>
      <td>-0.884196</td>
    </tr>
    <tr>
      <th>2017</th>
      <td>7.860283</td>
      <td>-4.425530</td>
      <td>-1.354077</td>
    </tr>
    <tr>
      <th>2018</th>
      <td>7.636689</td>
      <td>-4.977507</td>
      <td>-1.823958</td>
    </tr>
    <tr>
      <th>2019</th>
      <td>7.413095</td>
      <td>-5.529483</td>
      <td>-2.293839</td>
    </tr>
    <tr>
      <th>2020</th>
      <td>7.189501</td>
      <td>-6.081460</td>
      <td>-2.763720</td>
    </tr>
  </tbody>
</table>
</div>



## Add emissions for some years and see effects

Let's assume very strong increases of $CH_4$ emissions for the years 2005 through 2007 and see what impact ths has on the three different models. (Units of additional emssions are Gt $CH_4$ / yr).

```python
import pandas as pd 

additional_emssions = pd.Series([0.1, 0.5, 0.2], index=[2005, 2006, 2007])
additional_emssions.name = 'CH_4 [Gt/yr]'
additional_emssions.index.name = 'Year'
additional_emssions
```




    Year
    2005    0.1
    2006    0.5
    2007    0.2
    Name: CH_4 [Gt/yr], dtype: float64



```python
df26 = make_gwps_improved(file_name=paths['RCP 2.6'], additional_emssions=additional_emssions)
df26.loc[2000:2010]
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>$CH_4$ GWP</th>
      <th>$CH_4$ GWP*</th>
      <th>$CH_4$ IGWP</th>
    </tr>
    <tr>
      <th>Years</th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2000</th>
      <td>8.405793</td>
      <td>-0.896435</td>
      <td>1.429122</td>
    </tr>
    <tr>
      <th>2001</th>
      <td>8.495458</td>
      <td>-0.924463</td>
      <td>1.430517</td>
    </tr>
    <tr>
      <th>2002</th>
      <td>8.584206</td>
      <td>-0.957068</td>
      <td>1.428251</td>
    </tr>
    <tr>
      <th>2003</th>
      <td>8.672059</td>
      <td>-0.994154</td>
      <td>1.422399</td>
    </tr>
    <tr>
      <th>2004</th>
      <td>8.759072</td>
      <td>-1.035440</td>
      <td>1.413188</td>
    </tr>
    <tr>
      <th>2005</th>
      <td>11.645276</td>
      <td>12.919228</td>
      <td>12.600740</td>
    </tr>
    <tr>
      <th>2006</th>
      <td>22.961719</td>
      <td>69.025096</td>
      <td>57.509252</td>
    </tr>
    <tr>
      <th>2007</th>
      <td>14.677956</td>
      <td>27.129929</td>
      <td>24.016936</td>
    </tr>
    <tr>
      <th>2008</th>
      <td>9.193784</td>
      <td>-0.767278</td>
      <td>1.722987</td>
    </tr>
    <tr>
      <th>2009</th>
      <td>9.309613</td>
      <td>-0.664485</td>
      <td>1.829040</td>
    </tr>
    <tr>
      <th>2010</th>
      <td>9.425441</td>
      <td>-0.561693</td>
      <td>1.935091</td>
    </tr>
  </tbody>
</table>
</div>



Notice the different impacts of this $CH_4$ "flush" on these GWP models.
