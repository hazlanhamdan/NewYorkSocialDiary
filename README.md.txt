
    Author: Shatrunjai Singh

    Title: The New york social circle

    Date: 04/05/2015

    Purpose: To probe the new york social diary (website) to find which people appear more in pictures
    and which people tend to occur together

    Description: [New York Social Diary](http://www.newyorksocialdiary.com/) provides a fascinating lens onto New York's socially well-to-do.
    The data forms a natural social graph for New York's social elite.  Take a look at this page of a recent run-of-the-mill holiday party:
    http://www.newyorksocialdiary.com/party-pictures/2014/holiday-dinners-and-doers`
    Besides the brand-name celebrities, we notice the photos have carefully annotated captions labeling those that appear in the photos.  We can think of this as implicitly implying a social graph: there is a connection between two individuals if they appear in a picture together.
    The first step is to fetch the data.  This comes in two phases.The first step is to crawl the data.  We want photos from parties before December 1st, 2014.  From
    http://www.newyorksocialdiary.com/party-pictures to see a list of (party) pages.  For each party's page, we grab all the captions.
    After we have a list of all captions, we save the data on disk so that you can quickly retrieve it.  Now comes the parsing part.
    
    For the analysis, we think of the problem in terms of a [network](http://en.wikipedia.org/wiki/Computer_network) or a [graph](http://en.wikipedia.org/wiki/Graph_%28mathematics%29).  Any time a pair of people appear in a photo together, that is considered a link.  What we have described is more appropriately called an (undirected) [multigraph](http://en.wikipedia.org/wiki/Multigraph) with no self-loops but this has an obvious analog in terms of an undirected [weighted graph](http://en.wikipedia.org/wiki/Graph_%28mathematics%29Weighted_graph).  In this problem, we will analyze the social graph of the new york social elite.
    For this problem, we use python's `networkx` library.

    Questions asked:    1.) The simplest question we might want to ask is 'who is the most popular'?  The easiest way to answer this question is to look at how many connections everyone has.

                        2.) A similar way to determine popularity is to look at their [pagerank](http://en.wikipedia.org/wiki/PageRank).
                            Pagerank is used for web ranking and was originally
                            [patented](http://patft.uspto.gov/netacgi/nph-Parser?patentnumber=6285999) by Google and is essentially the
                            [stationary distribution](http://en.wikipedia.org/wiki/Markov_chainStationary_distribution_relation_to_eigenvectors_and_simplices)
                            of a [markov chain](http://en.wikipedia.org/wiki/Markov_chain) implied by the social graph.
                            Use 0.85 as the damping parameter so that there is a 15% chance of jumping to another vertex.

                        3.) Another interesting question is who tends to co-occur with each other.
