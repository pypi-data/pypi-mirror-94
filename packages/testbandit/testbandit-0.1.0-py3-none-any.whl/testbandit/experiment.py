from scipy.stats import beta
import numpy as np
import matplotlib.pyplot as plt

SAMPLE_COUNT = 200000

def plot_beta( a, b ):
    x = np.arange (0.0, 1, 0.001)
    y = beta.pdf(x, a=a, b=b)
    plt.plot(x,y)
    plt.show()

class Variation:
    def __init__( self, name, prior_a, prior_b, value_at_risk ):
        self._name = name
        self._prior_a = prior_a
        self._prior_b = prior_b
        self._value_at_risk_threshold = value_at_risk
        self._posterior_a = 0
        self._posterior_b = 0
        self._trials = 0
        self._successes = 0
        self._value_at_risk = None

    def add_trials( self, successes, trials ):
        if successes > trials:
            raise ValueError( 'trials must be equal or greater than successes' )

        self._trials = self._trials + trials
        self._successes = self._successes + successes

        self._posterior_a = self.prior_a() + self._successes
        self._posterior_b = self.prior_b() + self._trials - self._successes

        # calculate value at risk
        samples=beta.rvs(
            size=SAMPLE_COUNT,
            a=self._posterior_a,
            b=self._posterior_b,
            loc=0,
            scale=1
        )
        self._value_at_risk = np.mean( samples < self._value_at_risk_threshold )

    def value_at_risk( self ):
        return self._value_at_risk

    def name( self ):
        return self._name

    def prior_a( self ):
        return self._prior_a

    def prior_b( self ):
        return self._prior_b

    def posterior_a( self ):
        return self._posterior_a

    def posterior_b( self ):
        return self._posterior_b

    def maximum_likelihood_estimate( self ):
        if ( self._trials == 0 ):
            return None

        return self._successes / self._trials

    def posterior_mean( self ):
        if ( self._posterior_a == 0 and self._posterior_b == 0 ):
            return None

        return self._posterior_a / ( self._posterior_a + self._posterior_b )

    def credible_interval( self ):
        if ( self._posterior_a == 0 and self._posterior_b == 0 ):
            return None

        lower = beta.ppf( q=0.025, a=self.posterior_a(), b=self.posterior_b(), loc=0, scale=1 )
        upper = beta.ppf( q=0.975, a=self.posterior_a(), b=self.posterior_b(), loc=0, scale=1 )
        return ( lower, upper )

    def print_summary( self ):
        print( "----", self.name(), "----")
        print( "Prior alpha:", self.prior_a() )
        print( "Prior beta:", self.prior_b() )
        print( "Posterior alpha:", self.posterior_a() )
        print( "Posterior beta:", self.posterior_b() )
        print( "Posterior Mean: %2.3f" % self.posterior_mean() )
        print( "Maximum Likelihood Estimate: %2.3f" % self.maximum_likelihood_estimate() )
        print( "Probability that conversion rate is less than %2.3f" % self._value_at_risk_threshold, "-", self._value_at_risk )

        ( lower, upper ) = self.credible_interval()

        print()
        print( "Equal tail 95% credible interval" )
        print( "Lower bound: %2.3f" % lower )
        print( "Upper bound: %2.3f" % upper )

        plot_beta( self.posterior_a(), self.posterior_b() )

    def sample_from_posterior( self, count = SAMPLE_COUNT ):
        if ( self._posterior_a == 0 and self._posterior_b == 0 ):
            return None

        return beta.rvs(
            size=count,
            a=self.posterior_a(),
            b=self.posterior_b(),
            loc=0,
            scale=1
        )

class Sampler:
    def __init__( self, count, variations ):
        self._variations = variations
        self._sample_count = count
        samples = []
        for variation in variations:
            samples.append( variation.sample_from_posterior( count ) )

        max = np.argmax( samples, 0 )
        ( unique, counts ) = np.unique(max, return_counts=True)
        self._frequencies = np.asarray( ( unique, counts ) ).T

    def get_winning_variation( self ):
        counts = [ 0 ] * len( self._variations )
        for f in self._frequencies:
            counts[ f[ 0 ] ] = f[ 1 ]

        return self._variations[ np.argmax( counts ) ]

    def get_winning_percentages( self ):
        percentages = [ 0 ] * len( self._variations )
        for f in self._frequencies:
            percentages[ f[ 0 ] ] = f[ 1 ] / self._sample_count
        return percentages

class Experiment:
    def __init__( self ):
        self._variations = []
        self._winning_frequencies = []

    def add_variation( self, variation ):
        self._variations.append( variation )

    def get_variations( self ):
        return self._variations

    def get_winning_percentages( self ):
        return self._experiment_sampler.get_winning_percentages()

    def get_winning_variation( self ):
        return self._experiment_sampler.get_winning_variation()

    def calculate_winning_variation( self ):
        self._experiment_sampler = Sampler( SAMPLE_COUNT, self.get_variations() )

    # Draw n samples from each variation and return the variation with the highest value
    def thompson_sample( self, count = 1 ):
        sampler = Sampler( count, self.get_variations() )
        return sampler.get_winning_variation()
